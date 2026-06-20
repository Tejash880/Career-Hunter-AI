"""
Job service layer.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobSearchParams


class JobService:
    @staticmethod
    def get_job(db: Session, job_id: int) -> Optional[Job]:
        return db.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def get_jobs(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search_params: JobSearchParams = None
    ) -> List[Job]:
        query = db.query(Job).filter(Job.is_active == True)
        
        if search_params:
            if search_params.query:
                search_term = f"%{search_params.query}%"
                query = query.filter(
                    or_(
                        Job.title.ilike(search_term),
                        Job.description.ilike(search_term),
                        Job.company.has(Job.company.name.ilike(search_term))
                    )
                )
            
            if search_params.location:
                query = query.filter(Job.location.ilike(f"%{search_params.location}%"))
            
            if search_params.remote_type:
                query = query.filter(Job.remote_type == search_params.remote_type)
            
            if search_params.experience_level:
                query = query.filter(Job.experience_level == search_params.experience_level)
            
            if search_params.employment_type:
                query = query.filter(Job.employment_type == search_params.employment_type)
            
            if search_params.salary_min is not None:
                query = query.filter(Job.salary_min >= search_params.salary_min)
            
            if search_params.salary_max is not None:
                query = query.filter(Job.salary_max <= search_params.salary_max)
            
            if search_params.company_ids:
                query = query.filter(Job.company_id.in_(search_params.company_ids))
            
            if search_params.skills:
                # Filter jobs that require any of the specified skills
                # This is a simplified approach - in production, you'd want better JSON filtering
                for skill in search_params.skills:
                    query = query.filter(Job.skills_required.contains([skill]))
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_job(db: Session, job_in: JobCreate) -> Job:
        job_data = job_in.dict()
        job = Job(**job_data)
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def update_job(
        db: Session, 
        job_id: int, 
        job_in: JobUpdate
    ) -> Optional[Job]:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return None
        
        update_data = job_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def delete_job(db: Session, job_id: int) -> bool:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return False
        
        job.is_active = False
        db.add(job)
        db.commit()
        return True

    @staticmethod
    def calculate_match_score(
        db: Session, 
        job: Job, 
        user_skills: List[str],
        user_experience: str = None
    ) -> int:
        """
        Calculate match score between job and user.
        Simple implementation - can be enhanced with ML/AI later.
        """
        score = 0
        
        # Skills match (40 points)
        if job.skills_required and user_skills:
            required_skills = set(job.skills_required)
            user_skills_set = set(user_skills)
            if required_skills:
                skill_match = len(required_skills.intersection(user_skills_set)) / len(required_skills)
                score += int(skill_match * 40)
        
        # Experience level match (20 points)
        if user_experience and job.experience_level:
            experience_levels = ["intern", "entry", "junior", "mid", "senior", "lead", "manager", "director", "executive"]
            try:
                job_level_idx = experience_levels.index(job.experience_level.value)
                user_level_idx = experience_levels.index(user_experience)
                # Closer levels get higher score
                exp_diff = abs(job_level_idx - user_level_idx)
                exp_score = max(0, 20 - (exp_diff * 4))  # Decrease by 4 points per level difference
                score += exp_score
            except ValueError:
                pass  # If experience level not found, skip this component
        
        # Salary relevance (20 points) - simplified
        # In reality, you'd want to know user's salary expectations
        score += 20  # Placeholder
        
        # Location/remote preference (20 points) - simplified
        score += 20  # Placeholder
        
        return min(score, 100)  # Cap at 100
