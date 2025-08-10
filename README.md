# court-data-fetcher
Mini dashboard to retrieve court case details from eCourts portal

##  Overview
This web application allows users to enter court case details through a simple HTML form.  
The backend uses **Selenium automation** to fill out the official Thrissur District Court search form and retrieve case information directly from the **eCourts portal**.


##  Features Implemented
- User-friendly HTML form to input:
  - **Case Type**
  - **Case Number**
  - **Case Year**
- **Flask** backend to handle form submissions
- **Selenium** automation to:
  - Navigate to the Thrissur District Court search page
  - Automatically fill in the search form
  - Submit the form and retrieve results
- Results displayed on a dedicated HTML results page

## Project Structure
court-data-fetcher/  
├── app.py # Flask application  
├── scraper.py # Selenium scraping logic  
├── templates/  
│ ├── index.html # Input form  
│ ├── result.html # Results display  
│ └── captcha.html # CAPTCHA entry page  
├── static/  
│ └── style.css #Styling for HTML templates  
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

 ##  Sample Input for Testing  
Use the following example to try the application:

- **Case Type:** EP  
- **Case Number:** 100087
- **Case Year:** 2025  

