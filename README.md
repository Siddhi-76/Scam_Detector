# 🛡️ Scam Detector

> **An AI-Powered Phishing URL & Scam Message Detection System built using Python, Flask, and Machine Learning.**

Scam Detector is a cybersecurity-focused web application that helps identify potentially malicious URLs and scam messages using a combination of **feature engineering**, **rule-based analysis**, and **machine learning techniques**.

The objective of this project is to provide users with an intuitive platform where they can analyse suspicious links or messages, understand why they are considered risky, and receive an explainable prediction rather than a simple "safe" or "unsafe" label.

This project is being developed as part of my learning journey in **Artificial Intelligence, Machine Learning, Cybersecurity, and Full-Stack Development**, with a focus on building real-world AI applications.

---

# 📖 Table of Contents

* Overview
* Features
* Technology Stack
* Project Architecture
* Project Structure
* Installation
* Running the Application
* Detection Workflow
* Machine Learning Pipeline
* Future Enhancements
* Learning Outcomes
* Author

---

# 🎯 Project Overview

Phishing attacks and online scams have become one of the most common cybersecurity threats. Fraudulent websites often imitate trusted brands to steal user credentials, while scam messages attempt to manipulate users into revealing personal or financial information.

Instead of relying only on blacklists, this application analyses the behaviour and characteristics of URLs and messages to identify suspicious patterns.

The project combines:

* Feature Engineering
* Rule-Based Detection
* Machine Learning Classification
* Explainable Risk Analysis
* Flask Web Application

The long-term goal is to build an intelligent security assistant capable of detecting scams across multiple formats, including URLs, messages, emails, QR codes, and websites.

---

# ✨ Features

## URL Analysis

* HTTPS detection
* URL length analysis
* Subdomain counting
* IP address detection
* Suspicious Top-Level Domain (TLD) detection
* Hyphen analysis
* '@' symbol detection
* Shannon entropy calculation
* Brand impersonation detection

---

## Message Analysis

* Scam keyword detection
* Urgency phrase identification
* Suspicious link detection
* Email extraction
* Phone number extraction
* Message feature engineering

---

## Machine Learning

* Real-world dataset processing (UCI SMS Spam Collection & OpenPhish)
* Feature extraction (NLP tokenization & URL heuristics)
* Deep Learning Bidirectional LSTM for NLP context analysis
* Random Forest classification for URLs
* Exact scam probability scoring (e.g. 92% Scam Risk)
* Explainable AI output with dynamic PDF Reports

---

## Web Application

* Flask backend
* Interactive user interface
* Responsive design
* Real-time analysis

---

# 🛠️ Technology Stack

### Programming Language

* Python

### Backend

* Flask

### Machine Learning

* Scikit-learn
* TensorFlow & Keras
* Pandas
* NumPy
* Joblib

### Frontend

* HTML5
* CSS3
* JavaScript

### Development Tools

* Git
* GitHub
* Cursor IDE

---

# 🏗️ Project Architecture

```text
                  User
                    │
                    ▼
            Flask Web Application
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
 URL Feature Extraction   Message Feature Extraction
          │                   │
          └─────────┬─────────┘
                    ▼
          Machine Learning Model
                    │
                    ▼
      Prediction + Risk Assessment
                    │
                    ▼
           Result Displayed to User
```

---

# 📂 Project Structure

```text
Scam_Detector/

│── app.py
│── url_features.py
│── message_feature.py
│── ml_model.py
│── ml_message_dl.py
│── download_datasets.py
│── build_feature_matrix.py
│── report_generator.py
│── requirements.txt
│── README.md
│── Procfile
│── .gitignore

├── data/

├── static/
│   ├── style.css
│   └── script.js

├── templates/
│   └── index.html

├── tests/
│   └── test_features.py

└── venv/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Siddhi-76/Scam_Detector.git
```

Navigate into the project directory

```bash
cd Scam_Detector
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 🚀 Running the Project

### Option 1: Native Python Localhost Execution

Once the Flask server starts successfully, open your browser and visit:

```text
http://localhost:5000  or  http://127.0.0.1:5000
```

---

### Option 2: 🐳 Running with Docker Desktop

1. Make sure **Docker Desktop** is open and running on your system.
2. Open your terminal in the project directory and run:

```bash
docker compose up --build
```

Alternatively, you can build and run using standard Docker commands:

```bash
# Build the Docker image
docker build -t scam-detector .

# Run the container mapping port 5000
docker run -p 5000:5000 --name scam_detector_app scam-detector
```

3. Open your browser and navigate to:

```text
http://localhost:5000
```

To stop the Docker container:
```bash
docker compose down
```

---


# 🔍 Detection Workflow

```text
User Input
      │
      ▼
URL / Message Received
      │
      ▼
Feature Extraction
      │
      ▼
Rule-Based Analysis
      │
      ▼
Machine Learning Prediction
      │
      ▼
Risk Score Generation
      │
      ▼
Prediction + Explanation
```

---

# 🤖 Machine Learning Pipeline

```text
Dataset Collection
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
        │
        ▼
Prediction
        │
        ▼
Risk Assessment
```

---

# 📈 Future Enhancements

* Browser Extension
* QR Code Scam Detection
* Email Scam Detection
* SMS Scam Detection
* OCR-based Screenshot Analysis
* WHOIS Domain Lookup
* Domain Age Analysis
* VirusTotal API Integration
* Real-Time Threat Intelligence
* Explainable AI Dashboard

---

# 📚 Learning Outcomes

Through this project, I am strengthening my understanding of:

* Python Programming
* Flask Web Development
* Machine Learning
* Feature Engineering
* Cybersecurity Fundamentals
* URL Analysis
* Data Preprocessing
* Model Deployment
* Git & GitHub
* Full-Stack Development

---

# 👩‍💻 Author

## Siddhi Garg

**B.Tech in Artificial Intelligence & Machine Learning**
MIT Academy of Engineering (MITAOE), Pune

**GitHub:** https://github.com/Siddhi-76/Scam_Detector

**LinkedIn:** [www.linkedin.com/in/siddhigarg0](http://www.linkedin.com/in/siddhigarg0)

---

## ⭐ Support

If you found this project interesting, consider giving it a **Star ⭐** on GitHub. Feedback, suggestions, and contributions are always welcome.




