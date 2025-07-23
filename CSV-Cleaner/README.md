# 🧹 CSV Cleaner – Python GUI + AWS Automation

## 📌 Overview

CSV Cleaner is a two-phase project designed to simplify and automate the cleaning of CSV files. It provides both a **local GUI** for manual editing and a **cloud-based AWS solution** for fully automated processing, making it scalable and user-friendly for both developers and non-technical users.

---

## 🖥️ Phase 1: Python GUI (Tkinter)

A simple desktop application built using Python and Tkinter:

- ✅ Upload a CSV file
- ✅ Select cleaning functions using checkboxes:
  - Lowercase conversion
  - Remove punctuation
  - Remove URLs/special characters
  - Remove HTML tags
  - Remove repeated words
- ✅ Download the cleaned file locally

### 💡 How It Works

The user selects a CSV file and checks the transformations they want. Once submitted, the GUI processes the file and outputs a new cleaned version.

---

## ☁️ Phase 2: AWS Automation

An end-to-end serverless pipeline for automated CSV cleaning:

### 🔄 Workflow

1. **Upload**: User uploads a CSV file to the **Input S3 Bucket**
2. **Trigger**: S3 event triggers an **SQS Queue**, which activates a **Lambda function**
3. **Regex Parsing**: The Lambda reads the filename (e.g., `123_LHR.csv`) to identify which functions to apply:
   - `L` = lowercase
   - `H` = remove HTML
   - `U` = remove URLs/special characters
   - `P` = remove punctuation
   - `R` = remove repeated words
4. **Process**: The Lambda applies the transformations
5. **Save**: The cleaned file is uploaded to the **Output S3 Bucket**

### ⚙️ Infrastructure as Code

- Uses **AWS CloudFormation** to deploy:
  - S3 buckets (input/output)
  - SQS queue
  - Lambda function
- The setup is reusable and shareable across AWS accounts.

---

## 🚀 How to Use

