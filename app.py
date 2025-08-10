'''
from flask import Flask, render_template, request
from scraper import fetch_case_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    case_data = None

    if request.method == "POST":
        try:
            case_type = request.form["case_type"]
            case_number = request.form["case_number"]
            case_year = request.form["case_year"]

            result = fetch_case_data(case_type, case_number, case_year)
            case_data = {"raw": result}

        except Exception as e:
            case_data = {"error": str(e)}

    return render_template("index.html", case_data=case_data)

if __name__ == "__main__":
    app.run(debug=True)
'''

from flask import Flask, render_template, request
import scraper  # This is your scraper.py file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # HTML form page

@app.route('/submit', methods=['POST'])
def submit():
    # Get form inputs
    case_type1 = request.form['case_type0']
    case_number = request.form['case_number']
    case_year = request.form['case_year']

    # Call scraper logic with collected data
    result=scraper.scrape_court_data(case_type1, case_number, case_year)
    

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
