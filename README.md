# CareerHunter AI

An AI-powered job discovery platform that helps users find their dream jobs by leveraging AI for resume analysis, job matching, and automated applications.

## Features

- **Job Discovery**: Crawl jobs from multiple ATS systems (Workday, Greenhouse, Lever)
- **AI-Powered Matching**: Advanced job-to-resume matching using Anthropic Claude
- **Resume Optimization**: AI-driven resume analysis and improvement suggestions
- **Application Tracking**: Track your job applications from submission to offer
- **Watchlists**: Follow companies and get notified when they post new jobs
- **Notifications**: Email, SMS, and push notifications for application updates
- **Multi-tenancy**: Secure user authentication and data isolation

## Architecture

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis
- **Authentication**: JWT-based auth
- **AI Integration**: Anthropic Claude API for resume analysis and job matching
- **Deployment**: Dockerized with Docker Compose

### Frontend
- **Framework**: Next.js 12 (React)
- **Styling**: CSS (can be extended with Tailwind)
- **State Management**: Zustand
- **Data Fetching**: SWR for React Query-like functionality
- **Deployment**: Dockerized

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git
- Anthropic API key (for AI features)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd careerhunter-ai
   ```

2. Copy the environment example file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Anthropic API key:
   ```env
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
   ```

4. Start the application:
   ```bash
   docker-compose up --build
   ```

5. The application will be available at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development

#### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

The application uses SQLAlchemy. For production deployments, consider using Alembic for migrations.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing-feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI and Next.js
- Powered by Anthropic Claude AI
- Inspired by modern job search platforms
