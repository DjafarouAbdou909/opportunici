# OpportuniCI 

> AI-powered career assistant for African youth (18–30), starting in Côte d'Ivoire.

## The Problem & Vision

Millions of young Africans struggle to find jobs, internships, and scholarships. Opportunities are scattered, applications are repetitive, and most candidates don't know which skills they lack to reach their goals.

OpportuniCI transforms a CV into a concrete career plan — automatically.

## Features

- CV Upload → Automatic profile generation (Claude API)
- Employability score with detailed analysis
- Explainable AI matching with opportunities
- Career Gap Analyzer with 30/60/90-day roadmap
- Public profile + shareable QR Code

## Why Django + HTMX instead of React?

- Faster development for a 13-day hackathon MVP
- No JavaScript complexity — HTMX handles dynamic interactions
- Better performance on variable internet connections (West Africa context)
- Single codebase, easier to maintain and deploy

## System Architecture


## Database Schema

- `User` — custom auth model (email-based)
- `Profile` — extracted from CV (skills, experience, education)
- `EmployabilityScore` — score + strengths/weaknesses
- `Opportunity` — jobs, internships, scholarships, hackathons
- `MatchScore` — compatibility % with explanation
- `CareerGoal` — user objective + gap analysis
- `Roadmap` — personalized 30/60/90-day plan

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x (Python) |
| Database | PostgreSQL |
| AI | Claude API (Anthropic) — structured JSON outputs |
| Frontend | HTMX + Tailwind CSS + Flowbite |
| Analytics | Novus AI |
| Deployment | PythonAnywhere |
| PDF Generation | ReportLab |

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/opportunici.git
cd opportunici

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py migrate

# Compile Tailwind CSS
cd frontend
./node_modules/.bin/tailwindcss -i ../static/css/input.css -o ../static/css/output.css
cd ..

# Start development server
python manage.py runserver
```

## Environment Variables

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=opportunici
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
CLAUDE_API_KEY=your-claude-api-key
```

## Running Tests

```bash
python manage.py test
```

## Project Structure

## Impact

- Target: Youth aged 18–30 in Côte d'Ivoire
- Vision: Pan-African expansion
- SDG 8: Decent Work and Economic Growth

## Author

**Djafarou Abdou** — Computer Engineering Student, ENSEA Abidjan
EOF