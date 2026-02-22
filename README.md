# 🏦 Lend_Logic

## 📌 Overview
A full-stack banking-based web application built using Flask and MySQL.
The system allows users to calculate EMI, check loan eligibility,
generate repayment schedules, and enables admin to monitor loan analytics.

## 🚀 Features
- Secure user authentication (bcrypt hashing)
- EMI calculation engine
- Full repayment schedule generation
- Loan eligibility check (based on income)
- Admin dashboard with loan statistics
- MySQL relational database integration

## 🛠 Tech Stack
- Backend: Flask
- Database: MySQL
- Frontend: HTML, Bootstrap
- Security: Flask-Bcrypt

## 📊 Business Logic
EMI calculated using standard reducing balance formula.
Eligibility condition:
EMI must be less than 40% of monthly income.

## ▶ How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Setup MySQL database using database.sql

3. Run:
   python app.py

4. Open:
   http://127.0.0.1:5000/

## 🎯 Author
Aditi Chaudhari

## 💼 Project Type

Full-stack Financial Application (FinTech Simulation)
