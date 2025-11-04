# IntelliScanAI - ATS Resume Expert 🚀

<div align="center">

![IntelliScanAI Banner](https://img.shields.io/badge/IntelliScanAI-ATS%20Resume%20Expert-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-red?style=for-the-badge&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Gemini-AI%20Powered-orange?style=for-the-badge&logo=google)

**Your AI-Powered Career Companion for Resume Optimization & Job Application Success**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Tech Stack](#tech-stack) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tab Descriptions](#tab-descriptions)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

**IntelliScanAI** is an advanced, AI-powered resume analysis and optimization platform designed to help job seekers navigate the complexities of Applicant Tracking Systems (ATS). Built with Google's Gemini AI and Streamlit, this comprehensive tool provides professional insights, personalized recommendations, and actionable strategies to maximize your chances of landing your dream job.

### Why IntelliScanAI?

- 📊 **ATS Optimization**: Understand how ATS systems evaluate your resume
- 🎯 **Match Analysis**: Get precise compatibility scores with job descriptions
- 🔍 **Keyword Intelligence**: Extract and optimize critical keywords
- 💬 **AI Career Coaching**: Receive personalized guidance from an AI expert
- 📝 **Resume Builder**: Create and edit ATS-friendly resumes with AI assistance
- 💡 **Project Ideas**: Generate tailored project recommendations to strengthen applications

---

## ✨ Key Features

### 🤖 AI-Powered Analysis
Leverages Google's Gemini 1.5 Flash model for intelligent resume evaluation and recommendations.

### 📄 PDF Processing
Advanced PDF-to-image conversion using PyMuPDF for accurate text extraction and analysis.

### 🎨 Modern UI/UX
Beautiful, responsive interface with custom CSS styling and intuitive navigation.

### 💾 Resume Management
Build, edit, import, and export resumes in markdown format with AI-generated suggestions.

### 🔒 Secure & Private
Local processing with secure API key management through environment variables.

### ⚡ Real-time Chat
Interactive AI chatbot for instant career advice and resume optimization tips.

---

## 📑 Tab Descriptions

### 🔍 **Resume Review**
Get comprehensive professional feedback on your resume from an AI Technical HR Manager.

**What it does:**
- Evaluates your resume against the job description
- Identifies strengths and competitive advantages
- Highlights areas for improvement
- Provides actionable recommendations
- Offers professional HR perspective on candidate fit

**Best for:** Understanding how hiring managers view your application

---

### 📊 **Match Analysis**
Receive a detailed ATS compatibility score with missing keywords and optimization strategies.

**What it does:**
- Calculates percentage match between resume and job description
- Identifies missing critical keywords
- Analyzes skill gaps
- Provides prioritized improvement recommendations
- Simulates ATS scanning algorithms

**Best for:** Quantifying your application strength and identifying quick wins

---

### 🔑 **Keyword Extraction**
Discover and optimize the most important keywords from your resume and target job.

**What it does:**
- **AI-Powered Analysis**: Categorizes keywords into technical skills, soft skills, certifications, and technologies
- **Frequency Analysis**: Ranks keywords by importance and frequency
- **Visual Representation**: Interactive charts and tag clouds
- **Comparison Matrix**: Maps your keywords against job requirements
- **Industry Insights**: Identifies industry-specific terminology

**Best for:** Ensuring your resume contains all critical keywords for ATS systems

---

### 💬 **Career Coach**
Chat with an AI career expert for personalized guidance and instant answers.

**What it does:**
- Answers specific questions about your resume
- Provides tailored career advice
- Explains job description requirements
- Suggests interview preparation strategies
- Offers industry-specific insights
- Maintains conversation context for follow-up questions

**Best for:** Getting personalized, contextual advice on your specific situation

---

### 📝 **Resume Builder**
Create, edit, and optimize your resume with AI-powered suggestions and templates.

**What it does:**
- **Contact Information**: Manage professional details
- **Professional Summary**: AI-generated summaries tailored to job descriptions
- **Experience Section**: Add, edit, and optimize work history with achievement-focused bullet points
- **Education**: Document academic credentials and certifications
- **Skills Management**: Tag-based skill organization with AI suggestions
- **Projects Showcase**: Highlight portfolio projects with technologies and links
- **Import/Export**: Support for text import and markdown export
- **Live Preview**: Real-time resume preview before download

**Best for:** Building ATS-optimized resumes from scratch or improving existing ones

---

### 💡 **Project Ideas**
Generate personalized project recommendations that bridge skill gaps and strengthen applications.

**What it does:**
- Analyzes your current skill set from resume
- Identifies gaps based on job requirements
- Generates comprehensive project proposals including:
  - **Project Overview**: Clear objectives and purpose
  - **Technical Stack**: Relevant technologies from job description
  - **Core Features**: 4-5 impressive functionalities
  - **Implementation Steps**: Phased development plan
  - **Skills Demonstrated**: Explicit mapping to job requirements
  - **Expected Outcomes**: Learning objectives and achievements
  - **Showcase Tips**: How to present in resume and interviews
- Downloadable project plan in markdown format

**Best for:** Creating portfolio projects that directly address job requirements and demonstrate expertise

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Step-by-Step Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/intelliscanai.git
cd intelliscanai
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

5. **Run the Application**
```bash
streamlit run app.py
```

6. **Access the Application**
Open your browser and navigate to: `http://localhost:8501`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file
4. Never commit `.env` to version control

### Security Best Practices

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.pdf" >> .gitignore
echo "__pycache__/" >> .gitignore
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Upload Resume**: Click "Browse files" and select your PDF resume
2. **Paste Job Description**: Copy and paste the target job description
3. **Explore Tabs**: Navigate through different analysis features
4. **Review Insights**: Read AI-generated recommendations
5. **Take Action**: Implement suggestions to optimize your resume
6. **Generate Projects**: Create portfolio projects to strengthen application

### Advanced Features

#### Resume Builder Workflow
1. Navigate to **Resume Builder** tab
2. Choose "Start New Resume" or "Import Resume"
3. Fill in each section (Contact, Summary, Experience, etc.)
4. Click "Get AI Suggestions" for intelligent recommendations
5. Preview and download in markdown format

#### Project Generation Workflow
1. Upload resume and provide job description
2. Navigate to **Project Ideas** tab
3. Click "Generate Ideal Project"
4. Review comprehensive project plan
5. Download and start building!

---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Streamlit** | 1.44.0 | Web framework and UI |
| **Google Gemini AI** | 0.8.4 | AI/ML model for analysis |
| **PyMuPDF** | 1.24.0 | PDF processing and conversion |
| **Pillow** | 11.1.0 | Image processing |
| **python-dotenv** | 1.1.0 | Environment variable management |

### Architecture

```
┌─────────────────────────────────────────────┐
│           Streamlit Frontend                │
│  (UI Components, Custom CSS, State Mgmt)    │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│         Application Layer                   │
│  (Business Logic, Data Processing)          │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│           AI Services                       │
│    Google Gemini API Integration            │
└────────────────┬────────────────────────────┘
                 │
┌────────────────┴────────────────────────────┐
│         Utility Services                    │
│  PDF Processing | Keyword Analysis          │
└─────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
intelliscanai/
│
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
├── assets/                    # Static assets (if any)
│   └── screenshots/           # Application screenshots
│
└── docs/                      # Additional documentation
    ├── SETUP.md              # Detailed setup guide
    ├── TROUBLESHOOTING.md    # Common issues and solutions
    └── API_GUIDE.md          # API integration guide
```

---

## 📸 Screenshots

### Main Dashboard
*Upload resume and job description to get started*

### Resume Review
*Comprehensive HR perspective on your application*

### Match Analysis
*Detailed ATS compatibility scoring*

### Keyword Extraction
*Visual keyword analysis with frequency charts*

### Career Coach Chatbot
*Interactive AI guidance*

### Resume Builder
*Build and edit ATS-optimized resumes*

### Project Generator
*Personalized project recommendations*

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Not Found Error
```
Error: 404 models/gemini-1.5-flash is not found
```
**Solution**: The app uses `gemini-1.5-flash-latest`. Ensure you have the latest version of `google-generativeai` package.

#### 2. API Key Issues
```
Error: Invalid API key
```
**Solution**: 
- Verify `.env` file exists
- Check API key is correctly formatted
- Regenerate key from Google AI Studio

#### 3. PDF Processing Errors
```
Error: Failed to process PDF
```
**Solution**:
- Ensure PDF is not corrupted
- Try a different PDF viewer/export
- Check file size (< 10MB recommended)

#### 4. Module Import Errors
```
ModuleNotFoundError: No module named 'xyz'
```
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where applicable
- Write descriptive commit messages

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🌟 Acknowledgments

- **Google Gemini AI**: For providing powerful AI capabilities
- **Streamlit**: For the amazing web framework
- **PyMuPDF**: For robust PDF processing
- **Open Source Community**: For continuous inspiration

---
---

## 🎯 Roadmap

### Version 1.0 (Current)
- ✅ Resume analysis and review
- ✅ ATS match scoring
- ✅ Keyword extraction
- ✅ AI career coach chatbot
- ✅ Resume builder
- ✅ Project idea generator

### Version 2.0 (Planned)
- [ ] Multi-language support
- [ ] Cover letter generator
- [ ] LinkedIn profile optimizer
- [ ] Interview question preparation
- [ ] Salary negotiation advisor
- [ ] Job search tracker

### Version 3.0 (Future)
- [ ] Resume templates library
- [ ] Video resume analysis
- [ ] Mock interview simulator
- [ ] Career path recommendations
- [ ] Job matching algorithm
- [ ] Company culture fit analysis

---

## 💖 Support the Project

If you find IntelliScanAI helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 📢 Sharing with others
- 💡 Suggesting features
- 🤝 Contributing code

---
[⬆ Back to Top](#intelliscanai---ats-resume-expert-)

</div>