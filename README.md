# KYC Document Automation System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Tesseract](https://img.shields.io/badge/Tesseract-3DDC84?style=for-the-badge&logo=tesseract&logoColor=white)

Automated KYC document processing system that extracts and analyzes identity documents (KBIS) using OCR and AI.

## Features

- **Document Processing**:
  - 📄 Extract text from KBIS documents
  - 🔍 Structured data extraction (SIREN, company name, dates)
- **Risk Analysis**:
  - ⚠️ Company age detection
  - 💰 Capital social verification
  - 🚨 DeepSeek AI-powered risk assessment
- **Output**:
  - 📊 Structured data tables
  - 🔗 API integration capabilities

## Tech Stack

- **Core**: Python 3.10
- **OCR**: Tesseract 5
- **Web Interface**: Streamlit
- **AI Analysis**: DeepSeek API
- **Containerization**: Docker

## Installation

### Prerequisites
- Docker 20.10+
- Docker Compose 2.20+

### Quick Start
```bash
git clone https://github.com/BenkhaddaMd/kyc-automation.git
cd kyc-automation

# Build and run
docker-compose up --build

# Access the app at:
http://localhost:8501

```

## Project Structure
```bash
KYC_PROJECT/
├── .github/
│   ├── workflows/python_ci.yml 
├── app/
│   ├── main.py            # Streamlit application
│   ├── ocr.py             # Tesseract OCR processing
│   └── utils.py           # Helper functions
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Service orchestration
└── requirements.txt       # Python dependencies
```

## Usage
- Upload document images (PNG/JPG) or PDFs
- View extracted data in structured tables
- Get automatic risk assessment

## Troubleshooting
- OCR Language Errors:
```bash
# Verify Tesseract data files
docker-compose exec kyc-app ls -la /usr/share/tesseract-ocr/tessdata/

# Reinstall language files manually
docker-compose exec kyc-app \
  wget -P /usr/share/tesseract-ocr/tessdata/ \
  https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata
```
- OR check the version and change it in docker-compose.yml (TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata)