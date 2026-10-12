# College Placement Portal — DevOps Mini-Project

A responsive Flask web application for exploring placement opportunities and submitting student applications. Includes SQLite demo storage, health endpoints, automated tests, Docker, and GitHub Actions CI.

## Website or app?
This is a responsive **website/web application** that runs in your browser. An Android APK wrapper can be added later as an optional extra.

## Run locally (Windows PowerShell)
Install Python 3.10+ (Python 3.12 recommended). Open a terminal in this folder and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python app.py
```

If Python 3.12 is not installed, replace `py -3.12` with an installed supported version, for example `py -3.13`.

Open:
- Website: http://127.0.0.1:8080
- Health check: http://127.0.0.1:8080/health
- Readiness: http://127.0.0.1:8080/ready
- Submitted applications: http://127.0.0.1:8080/admin/applications

Stop the server with Ctrl+C.

## Test
With the virtual environment activated:
```powershell
python -m unittest discover -s tests -v
```

## Docker (later phase)
After installing and starting Docker Desktop:
```powershell
docker build -t college-placement-portal:local .
docker run --rm -p 8080:8080 college-placement-portal:local
```
Then open http://127.0.0.1:8080.

## GitHub (later phase)
Create an empty GitHub repository, then run:
```powershell
git init
git add .
git commit -m "Initial College Placement Portal"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
The `.github/workflows/ci.yml` workflow runs tests and builds the Docker image on pushes and pull requests.

## Structure
- `app.py` — Flask routes and application logic
- `templates/` — page templates
- `static/` — CSS and JavaScript
- `tests/` — automated tests
- `Dockerfile` — container build
- `.github/workflows/ci.yml` — continuous integration

## Important before public deployment
- `/admin/applications` is an unprotected demo page. Add authentication before handling real student data.
- The sample companies and vacancies are illustrative, not verified jobs.
- SQLite in a Cloud Run container is not durable production storage. Configure a managed database before relying on saved records after redeployments or instance changes.
- Set a strong `SECRET_KEY` in the deployment environment and never commit secrets.
