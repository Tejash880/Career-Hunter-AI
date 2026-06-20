"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine, db_session
from app.models import Base, Company, Job
from app.services.job_service import JobService
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta


def seed_database():
    """Seed the database with sample data if it's empty."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Get a database session
    db: Session = db_session()
    
    try:
        # Check if we already have companies
        company_count = db.query(Company).count()
        if company_count > 0:
            # Database already seeded, skip
            return
        
        print("Seeding database with sample data...")
        
        # Sample companies with different ATS types
        sample_companies = [
            {
                "name": "TechCorp Inc.",
                "careers_url": "https://techcorp.com/careers",
                "ats_type": "greenhouse",
                "description": "Leading technology company specializing in AI and cloud solutions",
                "logo_url": "https://logo.clearbit.com/techcorp.com",
                "website_url": "https://techcorp.com",
                "hiring_frequency": "weekly",
                "tech_stack": ["Python", "React", "AWS", "Kubernetes", "Node.js"]
            },
            {
                "name": "InnovateSolutions Ltd.",
                "careers_url": "https://innovatesolutions.com/jobs",
                "ats_type": "lever",
                "description": "Innovative software development company focused on enterprise solutions",
                "logo_url": "https://logo.clearbit.com/innovatesolutions.com",
                "website_url": "https://innovatesolutions.com",
                "hiring_frequency": "bi-weekly",
                "tech_stack": ["Java", "Spring Boot", "Azure", "Docker", "Microservices"]
            },
            {
                "name": "DataDriven Analytics",
                "careers_url": "https://datadriven.com/careers",
                "ats_type": "workday",
                "description": "Data analytics and business intelligence company",
                "logo_url": "https://logo.clearbit.com/datadriven.com",
                "website_url": "https://datadriven.com",
                "hiring_frequency": "weekly",
                "tech_stack": ["Python", "Spark", "Tableau", "AWS", "SQL"]
            }
        ]
        
        # Create companies
        company_objects = []
        for company_data in sample_companies:
            company = Company(**company_data)
            db.add(company)
            company_objects.append(company)
        
        # Commit to get company IDs
        db.commit()
        
        # Refresh to get IDs
        for company in company_objects:
            db.refresh(company)
        
        # Sample jobs for each company
        sample_jobs = [
            {
                "title": "Senior AI Engineer",
                "department": "Artificial Intelligence",
                "location": "San Francisco, CA",
                "remote_type": "hybrid",
                "salary_min": 150000,
                "salary_max": 200000,
                "experience_level": "senior",
                "employment_type": "full-time",
                "skills_required": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning"],
                "skills_preferred": ["AWS SageMaker", "Kubernetes", "Docker", "MLOps"],
                "application_url": "https://techcorp.com/careers/senior-ai-engineer",
                "posting_date": datetime.now() - timedelta(days=random.randint(1, 10)),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 5)),
                "ats_source": "greenhouse",
                "job_description": "Lead the development of cutting-edge AI models for our products. Work with cross-functional teams to implement machine learning solutions that scale.",
                "is_active": True
            },
            {
                "title": "Full Stack Developer",
                "department": "Engineering",
                "location": "New York, NY",
                "remote_type": "remote",
                "salary_min": 110000,
                "salary_max": 140000,
                "experience_level": "mid",
                "employment_type": "full-time",
                "skills_required": ["JavaScript", "React", "Node.js", "Python", "REST APIs"],
                "skills_preferred": ["GraphQL", "TypeScript", "AWS", "Docker"],
                "application_url": "https://techcorp.com/careers/full-stack-developer",
                "posting_date": datetime.now() - timedelta(days=random.randint(1, 15)),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 7)),
                "ats_source": "greenhouse",
                "job_description": "Build scalable web applications using modern JavaScript frameworks. Collaborate with product and design teams to create exceptional user experiences.",
                "is_active": True
            }
        ]
        
        # Create jobs
        for job_data in sample_jobs:
            # Find the company for this job
            company_name = None
            ats_source = job_data["ats_source"]
            
            # Map ats_source to company name for simplicity
            company_mapping = {
                "greenhouse": "TechCorp Inc.",
                "lever": "InnovateSolutions Ltd.",
                "workday": "DataDriven Analytics"
            }
            
            # For variety, let's assign jobs to different companies based on index
            company_index = hash(job_data["title"]) % len(company_objects)
            company = company_objects[company_index]
            
            job_data["company_id"] = company.id
            # Remove ats_source from job_data as it's handled separately
            del job_data["ats_source"]
            
            job = Job(**job_data, ats_source=job_data.get("ats_source", company.ats_type))
            db.add(job)
        
        # Commit all jobs
        db.commit()
        
        print(f"Successfully seeded database with {len(sample_companies)} companies and {len(sample_jobs)} jobs")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Create FastAPI app
app = FastAPI(
    title="CareerHunter AI API",
    description="Job discovery platform API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    seed_database()


@app.get("/")
async def root():
    return {"message": "Welcome to CareerHunter AI API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
