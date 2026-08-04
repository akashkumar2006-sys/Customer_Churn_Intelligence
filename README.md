# Customer_Churn_Intelligence
# Customer Churn Intelligence & Prediction Platform

An end-to-end Machine Learning web application that predicts customer churn, estimates churn probability, categorizes customers by risk level, and provides business-oriented churn analytics.

The platform is built with Python, Flask, Pandas, Scikit-learn, HTML, CSS, and JavaScript.

---

## 🚀 Overview

Customer churn is an important business problem for subscription-based companies.

This project uses Machine Learning to analyze customer information and estimate whether a customer is likely to churn.

The application provides both individual and batch prediction capabilities along with an analytics dashboard and model performance information.

---

## ✨ Features

### 👤 Single Customer Prediction

Enter individual customer information and receive:

- Churn prediction
- Churn probability
- Risk level
- Customer information summary
- Risk assessment explanation

Risk categories:

- 🟢 Low Risk
- 🟠 Medium Risk
- 🔴 High Risk

---

### 📊 Batch Customer Prediction

Upload a CSV file containing multiple customers.

The application:

1. Reads the uploaded CSV
2. Validates customer data
3. Applies the trained ML model
4. Predicts churn for each customer
5. Calculates churn probability
6. Assigns a risk category
7. Generates a downloadable results CSV

---

### 📈 Analytics Dashboard

The dashboard provides an overview of the customer dataset, including:

- Total customers
- Customers who churned
- Customers retained
- Overall churn rate
- Churn by contract type
- Churn by internet service
- Churn by payment method

---

### 🤖 Model Performance

The application provides information about the trained Machine Learning model, including:

- Model name
- Training samples
- Number of features
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Feature importance

---

### 📥 Sample Dataset

A sample CSV can be downloaded directly from the application to understand the required input format for batch prediction.

---

## 🧠 Machine Learning Workflow

The project follows a typical Machine Learning workflow:


Customer Dataset
       ↓
Data Preparation
       ↓
Feature Processing
       ↓
Model Training
       ↓
Model Evaluation
       ↓
Model Serialization
       ↓
Flask Application
       ↓
Customer Input / CSV Upload
       ↓
Churn Prediction
       ↓
Risk Assessment
---
🛠️ Technologies Used
Backend
Python
Flask
Pandas
NumPy
Scikit-learn
Joblib
Frontend
HTML5
CSS3
JavaScript
Machine Learning
Classification
Feature preprocessing
Model evaluation
Probability-based prediction
Feature importance analysis
---
📁 Project Structure
Customer-Churn-Platform/
│
├── app.py
├── README.md
├── .gitignore
│
├── data/
│   └── dataset.csv
│
├── models/
│   ├── churn_model.pkl
│   └── model_info.pkl
│
├── static/
│   ├── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│   ├── batch.html
│   ├── batch_result.html
│   └── model_info.html
│
├── uploads/
│
└── outputs/
---
📋 Dataset Features
The application uses customer attributes such as:
Gender
Senior Citizen
Partner
Dependents
Tenure
Phone Service
Multiple Lines
Internet Service
Online Security
Online Backup
Device Protection
Tech Support
Streaming TV
Streaming Movies
Contract
Paperless Billing
Payment Method
Monthly Charges
Total Charges

An optional customerID can be included when performing batch predictions.
---

⚙️ Installation

1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
2. Move into the project directory
cd Customer-Churn-Platform
3. Install dependencies
pip install flask pandas numpy scikit-learn joblib
4. Run the application
python app.py
5. Open the application
Open the local Flask URL shown in the terminal.
Usually:
http://127.0.0.1:5000

---

🔮 How to Use
Single Prediction
Open the application.
Enter customer information.
Click Predict Customer Churn.
View the prediction.
Review churn probability.
Check the customer's risk level.
Batch Prediction
Open Batch Prediction.
Download the sample CSV if required.
Prepare your customer dataset.
Upload the CSV.
Click Analyze Customers.
Review the prediction summary.
Download the complete results CSV.
Dashboard
Open Analytics Dashboard to explore customer churn patterns across different categories.
Model Performance
Open Model Performance to review the model's evaluation metrics and feature importance.

---

📊 Prediction Output

For individual predictions, the system provides:
Prediction
Churn Probability
Risk Level
Customer Information
Risk Assessment
For batch predictions, the system provides:
Total Customers
Predicted Churn
Predicted Stay
High Risk Customers
Medium Risk Customers
Low Risk Customers
Detailed Prediction Table
Downloadable CSV

---

🎯 Risk Classification

The platform categorizes customers based on predicted churn probability.
Probability
Risk Level
< 40%
Low Risk
40% – 69%
Medium Risk
≥ 70%
High Risk
These thresholds are used to make model output easier to interpret from a business perspective.

---

🔐 Data Handling

Uploaded CSV files are processed by the Flask application to generate predictions.
Generated prediction files are stored separately from the original dataset.
For production deployment, additional security and data privacy measures should be implemented before handling real customer information.

---

📚 Learning Objectives

This project demonstrates practical understanding of:
Machine Learning classification
Data preprocessing
Model evaluation
Pandas data analysis
Feature importance
Probability-based predictions
Flask web development
HTML/CSS/JavaScript integration
File upload handling
CSV processing
Model serialization using Joblib
Basic ML deployment concepts

---

🚧 Future Improvements

Possible future improvements include:
Interactive charts using Plotly or Chart.js
Customer segmentation
Explainable AI for individual predictions
Automated retention recommendations
Additional Machine Learning models
Model comparison
Cross-validation
Hyperparameter tuning
REST API endpoints
Authentication
Cloud deployment
Database integration
Advanced monitoring and logging

---

👨‍💻 Author
Akash Kumar Jha
B.Tech — Artificial Intelligence & Machine Learning

---


⭐ Project Goal
The goal of this project is to demonstrate how Machine Learning can be integrated into a practical web application to transform customer data into actionable churn insights.

If you find this project useful, consider giving the repository a ⭐.
