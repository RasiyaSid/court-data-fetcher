
from flask import Flask, render_template, request, redirect, url_for, session
from scraper import scrape_court_data, get_captcha_image
import os

app = Flask(__name__)
app.secret_key = "ba6d27784d8e318285d7483ee890e213"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["case_type"] = request.form["case_type"]
        session["case_number"] = request.form["case_number"]
        session["case_year"] = request.form["case_year"]
        return redirect(url_for("captcha_page"))
    return render_template("index.html")

@app.route("/captcha")
def captcha_page():
    case_type = session.get("case_type")
    case_number = session.get("case_number")
    case_year = session.get("case_year")

    captcha_path = get_captcha_image(case_type, case_number, case_year)

    return render_template("captcha.html",
                           case_type=case_type,
                           case_number=case_number,
                           case_year=case_year,
                           captcha_path=captcha_path)

@app.route("/submit_captcha", methods=["POST"])
def submit_captcha():
    captcha_text = request.form["captcha"]
    case_type = session.get("case_type")
    case_number = session.get("case_number")
    case_year = session.get("case_year")

    result = scrape_court_data(case_type, case_number, case_year, captcha_text)

    # Check for captcha failure or "No Record Found"
    if result.get("error") and "captcha" in result.get("error", "").lower():
        # Redirect back to home page if captcha is wrong
        return redirect(url_for("index"))

    return render_template("result.html", result=result)
if __name__ == "__main__":
    app.run(debug=True)



