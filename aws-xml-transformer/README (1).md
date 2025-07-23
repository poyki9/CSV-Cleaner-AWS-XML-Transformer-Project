# 🧠 Company XML Tools – AWS Automation & GPT-Based Editor

This repository contains two integrated tools developed for processing and editing XML product data within our company environment. Both tools are designed to work independently or in combination, enabling efficient XML transformation and AI-powered editing.

---

## 📁 1. AWS XML Transformer (`/aws-xml-transformer`)

This project provides an automated infrastructure for transforming `items.xml` into `products.xml` using AWS services and XSLT.

### 🔧 Features
- Event-driven architecture: **S3 → SQS → Lambda**
- Automatically processes uploaded XML files
- Uses **XSLT** to convert XML structure
- Fully deployable via **CloudFormation**

### 📂 Folder Contents
- `template.yaml`: Main CloudFormation template
- `lambda/`: Python-based Lambda function for XML processing

### 🚀 Deployment (CLI)
```bash
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name xml-transformer-stack \
  --capabilities CAPABILITY_NAMED_IAM
```

---

## 📁 2. GPT-based XML Editor (`/gpt-xml-editor`)

A user-friendly **Streamlit** app that allows users to modify XML files using plain English commands. Ideal for non-technical users.

### 🧠 Key Features
- Natural language editing of XML files (powered by **GPT**)
- Sample command: _"Change the price of all items in category A to 10"_
- XML updated automatically and previewed instantly
- Modular design – can be run locally or deployed to the web

### 📂 Folder Contents
- `app.py`: Main Streamlit application
- `requirements.txt`: Dependencies
- `prompts/`: Example prompt templates

### ▶️ Run Locally
```bash
cd gpt-xml-editor
pip install -r requirements.txt
streamlit run app.py
```

---

## ✅ Benefits

- Reduces manual XML editing workload
- Enables automation through AWS
- Empowers non-technical users via natural language
- Fully modular and customizable

---

## 🏢 For Internal Use

This project was developed as part of internal digitalization initiatives.  
To request access or suggest improvements, please contact the project owner.
