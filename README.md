### Community Blood Bank Management System

This is a comprehensive web application for managing blood bank operations, built using Streamlit and backed by a MySQL database.

# 1. Overview

The Community Blood Bank Management System provides a centralized platform for hospital staff to manage donors, recipients, donations, and blood requests. It features a secure login system and an analytics dashboard to visualize key metrics.

# 2. Features

Secure User Authentication: Register new hospital users and log in with hashed password verification.

Dashboard: At-a-glance view of key metrics like total donors, pending requests, and blood group distribution.

Donor Management: Add, view, and search for blood donors.

Recipient Management: Add and view recipients in need of blood.

Donation Tracking: Record new blood donations from registered donors.

Request Management: Create new blood requests for recipients and update their status (Pending, Fulfilled, Cancelled).

Hospital Management: View all registered hospitals.

Analytics Page: Advanced analytics on blood stock levels (donated vs. fulfilled), hospital activity, and age distributions.

# 3. Technical Stack

Frontend: Streamlit

Backend: Python

Database: MySQL

Core Libraries:

streamlit - For the web application interface.

mysql-connector-python - For database connectivity.

pandas - For data manipulation.

plotly - For data visualization and charts.

passlib - For password hashing and verification.

# 4. Setup and Installation

To run this application locally, follow these steps:

A. Database Setup

Install MySQL: Ensure you have a MySQL server running.

Create Database: Create a database (e.g., blood_bank).

Define Schema: Execute the required SQL scripts to create the tables (Donor, Recipient, Hospital, User_Login, Donation, Request, etc.) and procedures (Calculate_Age, GetDonorsByBloodGroup) used in the application.

Update Connection: Open app.py and update the get_connection function with your MySQL host, database, user, and password.

## Inside app.py
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='blood_bank',
            user='root',
            password='YOUR_MYSQL_PASSWORD',  # <--- UPDATE THIS
            autocommit=True,
            charset='utf8mb4'
        )
# ...


## B. Application Setup

#Clone the Repository:

git clone <repository-url>
cd <repository-directory>


Create a Virtual Environment (Recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
(Create a requirements.txt file with the libraries listed in section 3, or install them manually)

pip install streamlit mysql-connector-python pandas plotly passlib


Run the Application:

streamlit run app.py


The application will be accessible at http://localhost:8501.
