# CSV Cleaner Project
 
Transforming data with intelligent automation and intuitive design.  
Developed at **NTT DATA**, this project simplifies and accelerates the process of cleaning large-scale CSV files with both local and cloud-based automation workflows.
 
---
 
## 📌 Overview
 
The **CSV Cleaner Project** offers a Python-based solution for efficient and scalable CSV file cleaning. It provides:
 
- A **Tkinter-based local GUI** for quick, interactive edits.
- A **cloud backend powered by AWS** for asynchronous batch cleaning operations.
 
This hybrid approach ensures flexibility across use cases — from individual data prep to enterprise-scale automation.
 
---
 
## 💻 Local GUI (Tkinter)
 
A lightweight desktop application for immediate CSV cleaning.
 
### Key Features
 
- Upload CSV files locally
- Select cleaning operations via checkboxes:
  - ✅ Convert to lowercase
  - ✅ Remove HTML tags
  - ✅ Remove URLs & special characters
  - ✅ Remove punctuation
  - ✅ Remove stopwords and frequent words
- Output saved locally for quick use
 
---
 
## ☁️ AWS Cloud Automation
 
Uses serverless AWS components to automate CSV cleaning at scale.
 
### Workflow
 
1. **Input S3 Bucket**  
   User uploads a raw CSV file. The filename suffix indicates the cleaning functions (e.g., `_LP`, `_H`, `_URP`).
 
2. **SQS Queue**  
   Detects new uploads and sends event messages to Lambda.
 
3. **Lambda Function**  
   Executes cleaning logic based on regex suffix codes and stores the cleaned file.
 
4. **Output S3 Bucket**  
   Cleaned CSV is saved and ready for downstream consumption.
 
### Cleaning Functions (via filename suffix):
 
| Suffix | Function                              |
|--------|---------------------------------------|
| `_L`   | Make lowercase                        |
| `_H`   | Clear HTML tags                       |
| `_U`   | Remove URLs & special characters      |
| `_P`   | Remove punctuation                    |
| `_R`   | Remove stopwords and frequent words   |
 
---
 
## 🛠️ Tech Stack
 
- **Language**: Python 3.12, JSON
- **GUI Framework**: Tkinter
- **Cloud Platform**: Amazon Web Services (AWS)
- **AWS Services**: S3, Lambda, SQS, CloudFormation
- **Data Logic**: Regex-based parsing inside Lambda
 
---
 
## 🚀 Deployment with CloudFormation
 
### Benefits
 
1. **Automated Setup**  
   Instantly deploys all infrastructure (S3, Lambda, IAM) with one command.
 
2. **Version Control**  
   Infrastructure as Code ensures consistent environments.
 
3. **Cross-Region Availability**  
   Easily replicable across AWS regions.
 
---
 
## 📦 Getting Started
 
### Local GUI
 
```bash
python csv_cleaner_gui.py

 
