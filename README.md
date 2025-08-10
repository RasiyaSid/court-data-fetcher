# court-data-fetcher
Mini dashboard to retrieve court case details from eCourts portal

##  Overview
This project is a Flask + Selenium-based web application designed to fetch case details from the **Thrissur District Court Orders Search** portal.  
The user provides case details via an HTML form, and the system scrapes the court website to retrieve and display the information.

##  Features Implemented
- HTML form for user input (`case_type`, `case_number`, `case_year`)
- Flask backend to handle requests and responses
- Selenium-based automation to:
  - Open the Thrissur District Court search page
  - Fill in form details automatically
  - Retrieve case details from the results page
- Result display on a dedicated HTML page

##  Current Limitations
## ⚠ Current Limitations
- Extraction of data from the court page is not implemented in the current version.
- PDF extraction of court orders is also not implemented.
- The application currently focuses on opening the court search page and automating form submission.

## 📂 Project Structure
court-dashboard/  
├── app.py # Flask application  
├── scraper.py # Selenium scraping logic  
├── templates/  
│ └── index.html # Input form  
├── requirements.txt # Python dependencies  
├── README.md # Project documentation


##  Tech Stack
- **Python 3**
- **Flask** (Web framework)
- **Selenium** (Web automation & scraping)
- **HTML/CSS** (Frontend)

##  How to Run the Project
1. **Clone the repository:**
  - git clone https://github.com/RasiyaSid/court-data-fetcher.git
  - cd court-data-fetcher
2. **Install dependencies:**
  - pip install -r requirements.txt
3. **Run the Flask app:**
  - python app.py
4. **Open the app in your browser**
5. **Provide case details and click submit to view results.**
