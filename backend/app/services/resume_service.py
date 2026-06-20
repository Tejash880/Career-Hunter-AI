"""
Resume service layer with AI integration.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate, ResumeAnalysisRequest, ResumeAnalysisResponse
from app.models.user import User
import json
import re
import google.generativeai as genai
from app.core.config import settings


class ResumeService:
    @staticmethod
    def get_resume(db: Session, resume_id: int) -> Optional[Resume]:
        return db.query(Resume).filter(Resume.id == resume_id).first()

    @staticmethod
    def get_resumes_by_user(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Resume]:
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_resume(db: Session, resume_in: ResumeCreate, user_id: int) -> Resume:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        resume_data = resume_in.dict()
        resume_data["user_id"] = user_id
        resume = Resume(**resume_data)
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def update_resume(
        db: Session, 
        resume_id: int, 
        resume_in: ResumeUpdate
    ) -> Optional[Resume]:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return None
        
        update_data = resume_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resume, field, value)
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def delete_resume(db: Session, resume_id: int) -> bool:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            return False
        
        resume.is_active = 0
        db.add(resume)
        db.commit()
        return True

    @staticmethod
    def analyze_resume(
        db: Session,
        analysis_request: ResumeAnalysisRequest
    ) -> ResumeAnalysisResponse:
        """
        Analyze resume against job description using Google Gemini API.
        """
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')

        # Create prompt for resume analysis
        prompt = f"""
        Analyze the following resume against the job description and provide:
        1. An ATS (Applicant Tracking System) compatibility score (0-100)
        2. Missing keywords/skills that should be added
        3. Specific suggestions for improvement
        4. An optimized version of the resume content

        Resume Content:
        {analysis_request.resume_content}

        Job Description:
        {analysis_request.job_description}

        Please format your response as a JSON object with the following structure:
        {{
            "ats_score": <integer between 0 and 100>,
            "missing_keywords": ["<keyword1>", "<keyword2>", ...],
            "suggestions": [
                {{
                    "type": "<suggestion_type>",
                    "suggestion": "<suggestion_text>",
                    "priority": "<high|medium|low>"
                }}
            ],
            "optimized_content": "<optimized_resume_content>"
        }}

        Focus on:
        - Technical skills match
        - Experience relevance
        - Keyword optimization for ATS systems
        - Clear, actionable suggestions for improvement
        """

        try:
            # Generate content using Gemini
            response = model.generate_content(prompt)
            response_text = response.text

            # Try to parse JSON from the response
            import json
            import re

            # Extract JSON from response (handle cases where there might be extra text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback if JSON parsing fails
                result = {
                    "ats_score": 75,
                    "missing_keywords": ["Unable to parse AI response"],
                    "suggestions": [{
                        "type": "parsing_error",
                        "suggestion": "AI response could not be parsed. Please check the API configuration.",
                        "priority": "high"
                    }],
                    "optimized_content": analysis_request.resume_content
                }

            # Ensure we have all required fields with proper types
            ats_score = max(0, min(100, int(result.get("ats_score", 75))))
            missing_keywords = result.get("missing_keywords", []) if isinstance(result.get("missing_keywords"), list) else []
            suggestions = result.get("suggestions", []) if isinstance(result.get("suggestions"), list) else []
            optimized_content = result.get("optimized_content", analysis_request.resume_content)

            # Ensure suggestions have proper structure
            formatted_suggestions = []
            for sugg in suggestions:
                if isinstance(sugg, dict):
                    formatted_suggestions.append({
                        "type": sugg.get("type", "general"),
                        "suggestion": sugg.get("suggestion", "Consider improving your resume"),
                        "priority": sugg.get("priority", "medium")
                    })

            return ResumeAnalysisResponse(
                ats_score=ats_score,
                missing_keywords=missing_keywords,
                suggestions=formatted_suggestions,
                optimized_content=optimized_content
            )

        except Exception as e:
            # Fallback to basic analysis if API call fails
            resume_content = analysis_request.resume_content.lower()
            job_description = analysis_request.job_description.lower()

            # Extract skills from job description (simplified)
            tech_skills_pattern = r'\b(python|java|javascript|typescript|react|node\.js|aws|docker|kubernetes|sql|nosql|machine learning|ai|data science|devops|ci/CD|agile|scrum)\b'
            job_skills = re.findall(tech_skills_pattern, job_description)
            job_skills = list(set(job_skills))

            # Extract skills from resume
            resume_skills = re.findall(tech_skills_pattern, resume_content)
            resume_skills = list(set(resume_skills))

            # Calculate missing keywords
            resume_skills_set = set(resume_skills)
            job_skills_set = set(job_skills)
            missing_keywords = list(job_skills_set - resume_skills_set)

            # Calculate ATS score (simplified)
            if job_skills_set:
                skills_match = len(resume_skills_set.intersection(job_skills_set)) / len(job_skills_set)
                ats_score = int(skills_match * 100)
            else:
                ats_score = 50

            # Generate suggestions
            suggestions = []
            if missing_keywords:
                suggestions.append({
                    "type": "skill_addition",
                    "suggestion": f"Consider adding these skills: {', '.join(missing_keywords[:5])}",
                    "priority": "high"
                })

            # Check for common resume issues
            if len(resume_content) < 100:
                suggestions.append({
                    "type": "content_length",
                    "suggestion": "Resume seems too brief. Consider adding more details about your experience.",
                    "priority": "medium"
                })

            # Generate optimized content
            optimized_content = analysis_request.resume_content
            if missing_keywords:
                optimized_content += f"\n\nAdditional Skills: {', '.join(missing_keywords)}"

            return ResumeAnalysisResponse(
                ats_score=ats_score,
                missing_keywords=missing_keywords,
                suggestions=suggestions,
                optimized_content=optimized_content
            )
