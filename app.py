import os, sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-demo-key-change-before-deployment")
DB = Path(os.environ.get("DATABASE_PATH", Path(__file__).parent / "instance" / "portal.db"))
JOBS = [
 {"id":1,"title":"Graduate Software Engineer","company":"BrightByte Technologies","location":"Chennai / Hybrid","type":"Full-time","package":"₹6–8 LPA","category":"Engineering","deadline":"2026-12-15","skills":"Python, Java, SQL, Git","description":"Build, test, and maintain web applications with a product engineering team. Ideal for graduates with programming fundamentals."},
 {"id":2,"title":"Data Analyst Trainee","company":"InsightWorks","location":"Bengaluru","type":"Full-time","package":"₹4–6 LPA","category":"Data","deadline":"2026-11-30","skills":"Python, SQL, Excel","description":"Clean data, prepare dashboards, and communicate insights to business teams."},
 {"id":3,"title":"DevOps Intern","company":"CloudHarbor Systems","location":"Remote","type":"Internship","package":"₹20,000/month","category":"Cloud & DevOps","deadline":"2026-11-20","skills":"Git, Docker, Linux basics","description":"Learn containerized development, CI pipelines, cloud deployment, and application monitoring."},
 {"id":4,"title":"Frontend Developer","company":"PixelCraft Labs","location":"Coimbatore","type":"Full-time","package":"₹5–7 LPA","category":"Engineering","deadline":"2026-12-05","skills":"HTML, CSS, JavaScript","description":"Create responsive interfaces and work with backend developers to deliver reliable experiences."},
 {"id":5,"title":"Quality Assurance Associate","company":"Northstar Digital","location":"Chennai","type":"Full-time","package":"₹4–5 LPA","category":"Testing","deadline":"2026-11-28","skills":"Testing, SQL, attention to detail","description":"Design test cases, report defects, verify fixes, and improve web application quality."},
 {"id":6,"title":"Business Analyst Intern","company":"Elevate Consulting","location":"Hybrid","type":"Internship","package":"₹18,000/month","category":"Business","deadline":"2026-12-10","skills":"Excel, communication, analysis","description":"Assist with requirements, process documentation, data analysis, and presentations."}
]
def db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS applications(id INTEGER PRIMARY KEY, job_id INTEGER, full_name TEXT NOT NULL, email TEXT NOT NULL, department TEXT NOT NULL, graduation_year INTEGER NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(job_id,email))""")
    return c

@app.route("/")
def home():
    q=request.args.get("q","").strip().lower(); category=request.args.get("category","")
    jobs=[j for j in JOBS if (not q or q in " ".join(map(str,j.values())).lower()) and (not category or j["category"]==category)]
    with db() as c: count=c.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    return render_template("index.html",jobs=jobs,categories=sorted({j["category"] for j in JOBS}),q=q,category=category,count=count)

@app.route("/jobs/<int:job_id>")
def job_detail(job_id):
    job=next((j for j in JOBS if j["id"]==job_id),None)
    if not job: abort(404)
    return render_template("job.html",job=job)

@app.route("/apply/<int:job_id>",methods=["GET","POST"])
def apply(job_id):
    job=next((j for j in JOBS if j["id"]==job_id),None)
    if not job: abort(404)
    if request.method=="POST":
        name=request.form.get("full_name","").strip(); email=request.form.get("email","").strip().lower()
        dept=request.form.get("department","").strip(); year=request.form.get("graduation_year","").strip()
        try: year=int(year)
        except ValueError: year=0
        if len(name)<2 or "@" not in email or not dept or not 2020<=year<=2035:
            flash("Please check all fields and enter valid details.","error")
            return render_template("apply.html",job=job),400
        try:
            with db() as c: c.execute("INSERT INTO applications(job_id,full_name,email,department,graduation_year) VALUES(?,?,?,?,?)",(job_id,name,email,dept,year))
        except sqlite3.IntegrityError:
            flash("An application for this role already exists for that email.","error")
            return render_template("apply.html",job=job),409
        return redirect(url_for("success",job_id=job_id))
    return render_template("apply.html",job=job)

@app.route("/success/<int:job_id>")
def success(job_id):
    job=next((j for j in JOBS if j["id"]==job_id),None)
    if not job: abort(404)
    return render_template("success.html",job=job)

@app.route("/admin/applications")
def applications():
    with db() as c:
        rows=c.execute("""SELECT applications.*, jobs.title, jobs.company FROM applications JOIN (SELECT 1 id,'Graduate Software Engineer' title,'BrightByte Technologies' company UNION SELECT 2,'Data Analyst Trainee','InsightWorks' UNION SELECT 3,'DevOps Intern','CloudHarbor Systems' UNION SELECT 4,'Frontend Developer','PixelCraft Labs' UNION SELECT 5,'Quality Assurance Associate','Northstar Digital' UNION SELECT 6,'Business Analyst Intern','Elevate Consulting') jobs ON jobs.id=applications.job_id ORDER BY applications.created_at DESC""").fetchall()
    return render_template("applications.html",rows=rows)

@app.route("/health")
def health():
    try:
        with db() as c: c.execute("SELECT 1")
        return {"status":"healthy","database":"connected"},200
    except sqlite3.Error:
        app.logger.exception("Health check failed")
        return {"status":"unhealthy"},503

@app.route("/ready")
def ready(): return {"status":"ready"},200

@app.errorhandler(404)
def missing(_): return render_template("error.html",code=404,message="The page could not be found."),404

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","8080")),debug=os.environ.get("FLASK_DEBUG")=="1")
