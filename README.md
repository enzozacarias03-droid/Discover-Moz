# Enzo Blog

A full-stack blog application built with Python and Django, 
showcasing content about Mozambique — its cities, beaches, and culture.

Built as a learning project during my Bachelor of Business studies, 
this application demonstrates real-world web development practices 
including containerization, security, and content management.

## Features

- Browse posts organized by categories and tags
- Full-text search across all posts
- Rich text editor for content creation (Summernote + CodeMirror)
- Brute-force login protection (Django AXES — 3 attempt limit)
- Docker containerization for consistent deployment
- PostgreSQL database
- Responsive layout with image cards
- Custom admin panel with organized content management

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Framework | Django |
| Database | PostgreSQL |
| Containerization | Docker, Docker Compose |
| Editor | Summernote + CodeMirror (Dracula theme) |
| Security | Django AXES |
| Frontend | HTML, CSS |

## Project Structure
Project-Blog/
├── djangoapp/
│   ├── blog/          # Main blog app (posts, categories, tags)
│   ├── project/       # Django settings and configuration
│   ├── site_setup/    # Site-wide settings (menu, header)
│   └── utils/         # Shared utility functions
├── scripts/           # Docker helper scripts
├── dotenv_files/      # Environment variable templates
├── docker-compose.yml
└── Dockerfile

## Running Locally

### Prerequisites
- Docker Desktop installed and running
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/enzozacarias03-droid/Discover-Moz.git
cd Discover-Moz
```

2. Create your environment file:
```bash
cp dotenv_files/.env-example dotenv_files/.env
```
Then open `dotenv_files/.env` and fill in your own values.

3. Start the application:
```bash
docker-compose up --build
```

4. Visit `http://127.0.0.1:8000`

5. Access the admin panel at `http://127.0.0.1:8000/admin/`

## Environment Variables

Create a `dotenv_files/.env` file with these variables:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | 1 for development, 0 for production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `DB_ENGINE` | Database engine |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` | Database host |
| `POSTGRES_PORT` | Database port |

## Security Features

- **Django AXES** — locks account after 3 failed login attempts
- **1 hour cooldown** — automatic reset of failure count
- **Auto-unlock on success** — legitimate users unblocked immediately
- **Environment variables** — no credentials hardcoded anywhere
- **CSRF protection** — enabled on all forms

## Author

**Enzo Zacarias**  
Business student | Learning Python   
📍 Brussels, Belgium  

[LinkedIn](www.linkedin.com/in/enzo-zacarias-7112b914b) · 
[GitHub](https://github.com/enzozacarias03-droid)

---
*Open to internship and entry-level opportunities*