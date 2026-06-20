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
            },
            {
                "title": "Product Manager",
                "department": "Product",
                "location": "Seattle, WA",
                "remote_type": "hybrid",
                "salary_min": 120000,
                "salary_max": 160000,
                "experience_level": "mid",
                "employment_type": "full-time",
                "skills_required": ["Product Strategy", "Analytics", "SQL", "Excel", "Jira"],
                "skills_preferred": ["Mixpanel", "Amplitude", "Tableau", "A/B Testing"],
                "application_url": "https://innovatesolutions.com/jobs/product-manager",
                "posting_date": datetime.now() - timedelta(days=random.randint(1, 12)),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 6)),
                "ats_source": "lever",
                "job_description": "Drive product vision and execution for our enterprise software solutions. Work with engineering, design, and customers to deliver valuable features.",
                "is_active": True
            },
            {
                "title": "Data Scientist",
                "department": "Data Analytics",
                "location": "Boston, MA",
                "remote_type": "remote",
                "salary_min": 130000,
                "salary_max": 170000,
                "experience_level": "senior",
                "employment_type": "full-time",
                "skills_required": ["Python", "Statistics", "Machine Learning", "SQL", "Python"],
                "skills_preferred": ["Spark", "AWS SageMaker", "Tableau", "Git"],
                "application_url": "https://datadriven.com/careers/data-scientist",
                "posting_date": datetime.now() - timedelta(days=random.randint(1, 8)),
                "last_updated": datetime.now() - timedelta(days=random.randint(0, 4)),
                "ats_source": "workday",
                "job_description": "Analyze complex datasets to uncover business insights and build predictive models. Partner with stakeholders to drive data-informed decision making.",
                "is_active": True
            }
        ]

        # Create jobs - assign each job to a company matching its ats_source
        for job_data in sample_jobs:
            ats_source = job_data["ats_source"]

            # Find company with matching ats_source
            company = None
            for c in company_objects:
                if c.ats_type == ats_source:
                    company = c
                    break

            # Fallback: assign to first company if no match found
            if company is None:
                company = company_objects[0]

            job_data["company_id"] = company.id
            # Keep ats_source in job_data for Job model
            job = Job(**job_data)
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
