from flask import Flask, render_template, request
import os
import pdfplumber

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    text = ""

    if file.filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

        except Exception as e:
            return f"Unable to read PDF: {e}"

    print("========== RESUME TEXT ==========")
    print(text)
    print("================================")

    resume_text = text.lower()

    skills = [
        "python",
        "java",
        "html",
        "css",
        "javascript",
        "sql",
        "bootstrap",
        "react",
        "react.js",
        "spring boot",
        "mysql",
        "rest api",
        "git",
        "github",
        "hibernate",
        "thymeleaf",
        "power bi",
        "pandas",
        "matplotlib",
        "excel"
    ]

    found_skills = []
    score = 50

    for skill in skills:
        if skill in resume_text:
            found_skills.append(skill.title())
            score += 5

    if score > 100:
        score = 100

        # ATS Score
    ats_score = score

    # Job Role Analysis
    frontend = ["html", "css", "javascript", "bootstrap", "react"]

    java = ["java", "spring boot", "mysql", "hibernate"]

    data = [
        "python",
        "sql",
        "power bi",
        "pandas",
        "matplotlib",
        "excel"
    ]

    fullstack = [
        "java",
        "spring boot",
        "react",
        "mysql",
        "html",
        "css",
        "javascript"
    ]

    frontend_score = sum(1 for s in frontend if s in resume_text)
    java_score = sum(1 for s in java if s in resume_text)
    data_score = sum(1 for s in data if s in resume_text)
    fullstack_score = sum(1 for s in fullstack if s in resume_text)

    scores = {
        "Frontend Developer": frontend_score,
        "Java Developer": java_score,
        "Data Analyst": data_score,
        "Full Stack Developer": fullstack_score
    }

    job_role = max(scores, key=scores.get)

    # AI Suggestions
    suggestions = []

    if "github" not in resume_text:
        suggestions.append("Add GitHub profile.")

    if "linkedin" not in resume_text:
        suggestions.append("Add LinkedIn profile.")

    if score < 80:
        suggestions.append("Add more technical skills.")

    if len(found_skills) < 5:
        suggestions.append("Include more relevant skills.")

    return render_template(
        "result.html",
        score=score,
        ats_score=ats_score,
        job_role=job_role,
        found_skills=found_skills,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)