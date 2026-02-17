# 🎯AI CareerMate🚀👨🏻‍💻

<div align="center">

# Optimize Your Resume with AI-Powered Analysis

![AI CareerMate Banner](https://img.shields.io/badge/AI%20CareerMate-Smart%20ATS%20Optimizer-9333ea?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-10b981?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-ec4899?style=for-the-badge&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Gemini%202.5-AI%20Powered-a855f7?style=for-the-badge&logo=google)


[Live Demo](https://ai-careermate.streamlit.app/) • [Documentation](#-documentation) • [Setup Guide](#step-by-step-setup) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Live Demo](#-live-demo)
- [Quick Start](#-quick-start)
- [Step-by-Step Setup](#step-by-step-setup)
- [Configuration](#-configuration)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Support](#-support)

---

## 🎯 About

AI CareerMate is an intelligent resume optimization tool powered by Google's Gemini AI. It provides comprehensive resume analysis, ATS compatibility scoring, keyword optimization, and personalized career coaching to help you land your dream job.

Whether you're a recent graduate, career changer, or seasoned professional, AI CareerMate helps you:
- ✅ Pass ATS screening systems
- ✅ Identify skill gaps and opportunities
- ✅ Optimize resume content for specific jobs
- ✅ Get AI-powered career guidance
- ✅ Build and export professional resumes

---

## ✨ Features

### 📋 **Resume Review**
Comprehensive professional evaluation of your resume including:
- Key strengths and areas for improvement
- Specific, actionable recommendations
- Missing qualifications and skills identification
- Interview preparation tips
- Constructive feedback from HR perspective

### 🎯 **ATS Compatibility Score**
Get detailed ATS (Applicant Tracking System) analysis:
- Match percentage against job description
- Score breakdown by category (experience, skills, education, qualifications, job level)
- Visual scoring table with status indicators
- Clear path to improve from current score to 80%+ (excellent rating)
- ATS red flags and formatting issues identification
- Realistic recommendations with impact estimates

### 🔑 **Keyword Extraction & Analysis**
Two powerful keyword analysis methods:
- **AI-Powered**: Uses Gemini to extract industry-specific keywords with ATS optimization
- **Frequency Analysis**: Analyzes keyword frequency across job description
- Priority-based keyword recommendations
- Visual keyword cloud and frequency charts
- Implementation guide with specific placement suggestions

### 💬 **AI Career Coach**
Interactive chatbot specifically designed for your application:
- Answers resume and job-specific questions
- Personalized career advice
- Interview preparation guidance
- Maintains conversation context
- Scope-restricted to job/resume/career topics

### 📝 **Resume Builder**
Complete resume management system with:
- Contact Information
- Professional Summary
- Professional Experience (multiple entries)
- Education (multiple entries)
- Certifications (with credential tracking)
- Technical Skills
- Projects (with links and tech stacks)
- Achievements & Awards
- AI-powered suggestions for each section
- Export to clean Markdown format

### 💡 **Project Ideas Generator**
Intelligent project recommendations:
- Personalized project suggestions based on skill gaps
- Complete project structure with objectives and features
- Technical stack and implementation phases
- Skills showcasing guidance
- Interview talking points preparation

---

## 🌐 Live Demo

**Try AI CareerMate now!** [https://ai-careermate.streamlit.app/](https://ai-careermate.streamlit.app/)

> **Note**: You'll need a Google Gemini API key to use the application. Get one free from [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free)
- 100MB disk space

### Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/Sarbojit357/AI-CareerMate.git
cd AI-CareerMate

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser!

---

## 📋 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sarbojit357/AI-CareerMate.git
cd AI-CareerMate
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Getting your API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Paste it into your `.env` file
5. Never commit `.env` to version control (it's in `.gitignore`)

### 5. Run the Application

```bash
streamlit run app.py
```

### 6. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes | `AIza...` |

### Advanced Configuration

#### Model Selection
To use a different Gemini model, edit `app.py`:

```python
model = genai.GenerativeModel('gemini-pro')  
```

#### Caching Configuration
Adjust cache TTL (Time To Live) in seconds:

```python
@st.cache_data(ttl=1800, show_spinner=False)  # 30 minutes
```

#### PDF Processing
Modify PDF conversion quality:

```python
pix = first_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # Adjust multiplier
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface                        │
│         (Streamlit Frontend Components)                 │
│    ┌─────────────┬──────────────┬──────────────┐        │
│    │  Resume     │   Job        │  AI Analysis │        │
│    │  Upload     │  Description │  Tabs        │        │
│    └─────────────┴──────────────┴──────────────┘        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│             Application Logic Layer                     │
│  ┌──────────────┬──────────────┬──────────────┐         │
│  │   Resume     │   Analysis   │   Resume     │         │
│  │   Processing │   Engine     │   Builder    │         │
│  └──────────────┴──────────────┴──────────────┘         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│              AI & Utility Services                      │
│  ┌────────────────┬──────────────┬─────────────┐        │
│  │  Gemini API    │  PDF Parser  │  Keyword    │        │
│  │  Integration   │  (PyMuPDF)   │  Analyzer   │        │
│  └────────────────┴──────────────┴─────────────┘        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│            External Services & Data                     │
│  ┌────────────────────┬──────────────────┐              │
│  │  Google Gemini AI  │  Session Storage │              │
│  │  (Cloud)           │  (In-Memory)     │              │
│  └────────────────────┴──────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI-CareerMate/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── README.md                   # This file

---

## 💡 Usage Guide

### Basic Workflow

1. **Upload Your Resume** (PDF format)
2. **Paste Job Description** from job posting
3. **Click "Analyze Resume"** and wait 20-30 seconds
4. **Explore all 6 analysis tabs**:
   - 📋 Resume Review
   - 🎯 ATS Compatibility Score
   - 🔑 Keyword Extraction
   - 💬 Career Coach Chat
   - 📝 Resume Builder
   - 💡 Project Ideas

### Resume Review Tab
- Get comprehensive feedback from HR perspective
- Identify specific strengths and weaknesses
- Receive actionable improvement recommendations
- Prepare for potential interview questions

### ATS Compatibility Tab
- View your match percentage prominently
- Understand scoring across 5 key categories
- See specific gaps and how to fix them
- Get timeline and action plan

### Keyword Extraction Tab
- Use AI-powered analysis for comprehensive keyword extraction
- View frequency-based keyword analysis
- Get category-organized keyword suggestions
- Copy-paste optimized keywords directly

### Career Coach Tab
- Ask specific questions about your resume and job
- Get personalized advice for your situation
- Maintain conversation history
- Get interview preparation tips

### Resume Builder Tab
- Build complete professional resume
- Use AI suggestions to enhance content
- Add certifications and achievements
- Export to Markdown format
- Download ready-to-use resume

### Project Ideas Tab
- Generate project recommendations
- See complete project structure
- Get technical stack suggestions
- Learn how to showcase in interviews

### Tips for Best Results

#### Resume Upload
- ✅ Use well-formatted, text-based PDF
- ✅ Ensure all text is selectable
- ✅ Keep file size under 10MB
- ❌ Don't use scanned/image-based PDFs

#### Job Description
- ✅ Paste complete job posting
- ✅ Include all requirements and qualifications
- ✅ More detail = better analysis
- ❌ Don't use shortened versions

#### Implementation
- 📌 Focus on HIGH PRIORITY recommendations first
- 📌 Implement keyword suggestions strategically
- 📌 Use AI Coach for clarifications
- 📌 Review multiple times before applying

---

## 📚 API Documentation

### Core Functions

#### `input_pdf_setup(uploaded_file_bytes)`
Converts PDF to processable image format with OCR support.

**Parameters:**
- `uploaded_file_bytes` (bytes): PDF file content

**Returns:**
- `list`: Base64-encoded image parts for Gemini API

**Example:**
```python
pdf_parts = input_pdf_setup(pdf_bytes)
```

#### `get_gemini_response(input_text, pdf_content_hash, prompt)`
Calls Gemini API with prompt and PDF content.

**Parameters:**
- `input_text` (str): Job description
- `pdf_content_hash` (str): MD5 hash of PDF for caching
- `prompt` (str): Analysis prompt

**Returns:**
- `str`: AI-generated response

#### `extract_keywords_with_gemini(input_text, pdf_content_hash)`
Extracts ATS-optimized keywords using Gemini.

**Parameters:**
- `input_text` (str): Job description
- `pdf_content_hash` (str): PDF hash for caching

**Returns:**
- `str`: Formatted keyword analysis with recommendations

#### `chatbot_response(user_query, job_description, pdf_content_hash)`
Generates contextual career coach responses.

**Parameters:**
- `user_query` (str): User question
- `job_description` (str): Job posting
- `pdf_content_hash` (str): PDF hash

**Returns:**
- `str`: Personalized response

#### `generate_resume_suggestions(job_description, section_type)`
Generates AI suggestions for resume sections.

**Parameters:**
- `job_description` (str): Job posting
- `section_type` (str): 'summary', 'skills', or 'experience'

**Returns:**
- `str`: AI-generated suggestion

---

## ⚡ Performance

### Optimization Techniques
- **Smart Caching**: All AI responses cached with configurable TTL
- **Lazy Loading**: Features loaded on-demand
- **PDF Compression**: High-quality preview at reduced size
- **Session State**: Efficient data management across reruns
- **API Optimization**: Batch requests where possible

### Performance Metrics
| Operation | Time | Cached? |
|-----------|------|---------|
| Resume Upload & Processing | 5-10s | ✅ Yes (1hr) |
| Resume Review | 20-30s | ✅ Yes (1hr) |
| ATS Score Calculation | 20-30s | ✅ Yes (1hr) |
| Keyword Extraction | 25-35s | ✅ Yes (1hr) |
| Career Coach Response | 10-15s | ✅ Yes (30min) |
| Project Generation | 30-40s | ✅ Yes (1hr) |

### Caching Configuration
```python
@st.cache_data(ttl=3600, show_spinner=False)  # 1 hour
def get_gemini_response(input_text, pdf_content_hash, prompt):
    # Cached for 1 hour
    pass

@st.cache_data(ttl=1800, show_spinner=False)  # 30 minutes
def chatbot_response(user_query, job_description, pdf_content_hash):
    # Cached for 30 minutes
    pass
```

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "Error processing PDF"
**Cause**: Scanned or image-based PDF
**Solution**: 
- Convert PDF to text-based using online OCR tool
- Try a different PDF reader
- Ensure PDF is not password-protected

#### ❌ "API key not recognized"
**Cause**: Invalid or missing API key
**Solution**:
- Verify key format in `.env` file
- Check key is active in Google AI Studio
- Restart Streamlit after updating `.env`
- No spaces or quotes around key value

#### ❌ "Analysis takes too long"
**Cause**: Normal behavior for first analysis or network issues
**Solution**:
- First run takes 20-30s, subsequent runs use cache
- Check internet connection
- Try again in a few moments
- Results are cached for similar queries

#### ❌ "Keywords section shows no results"
**Cause**: Missing resume or job description
**Solution**:
- Ensure PDF is uploaded
- Paste complete job description
- Click Analyze Resume first
- Try refreshing the page

#### ❌ "Resume export fails"
**Cause**: Missing resume data
**Solution**:
- Fill in at least Contact Information and Summary
- Ensure all sections have valid content
- Check browser console for errors
- Try exporting again

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If issues persist:
1. Check [GitHub Issues](https://github.com/Sarbojit357/AI-CareerMate/issues)
2. Create a new issue with:
   - Error message
   - Steps to reproduce
   - System details (OS, Python version)
   - Screenshots

---

## 🔒 Privacy & Security

### Data Handling
- ✅ Your resume is processed through Google's Gemini API
- ✅ Data cached locally in Streamlit session only
- ✅ No permanent storage on our servers
- ✅ Each session is isolated
- ✅ Cache cleared on app restart

### Best Practices
- 🔐 Never hardcode API keys (use `.env`)
- 🔐 Don't commit `.env` to version control
- 🔐 Use `.env.example` as template
- 🔐 Rotate API keys regularly
- 🔐 Monitor API usage in Google Cloud Console

### Data Privacy Policy
By using AI CareerMate, you agree to:
- Your resume being processed by Google's Gemini API
- Temporary caching in session memory
- No personal data storage
- Compliance with Google's [Privacy Policy](https://policies.google.com/privacy)

---

## 🤝 Contributing

We love contributions! Here's how to help:

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Contribution Areas
- 🐛 Bug fixes and improvements
- ✨ New features (interview prep, salary negotiation, etc.)
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌍 Language support

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Test your changes locally
- Update documentation

### Pull Request Process
1. Update README.md with changes
2. Add/update comments in code
3. Test thoroughly locally
4. Provide clear PR description
5. Link related issues
6. Request review from maintainers

---


## 🆘 Support

### Getting Help

- 💬 **GitHub Issues**: [Report a bug](https://github.com/Sarbojit357/AI-CareerMate/issues)

### Quick Links

| Resource | Link |
|----------|------|
| 🌐 Live App | [ai-careermate.streamlit.app](https://ai-careermate.streamlit.app/) |
| 📦 Repository | [GitHub](https://github.com/Sarbojit357/AI-CareerMate) |
| 🔑 API Key | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| 📖 Documentation | [Full Guide](docs/USAGE.md) |
| 🐛 Report Bug | [GitHub Issues](https://github.com/Sarbojit357/AI-CareerMate/issues) |

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io) 🎨
- Powered by [Google Gemini AI](https://ai.google.dev) 🤖
- PDF processing with [PyMuPDF](https://pymupdf.readthedocs.io/) 📄
- Image processing with [Pillow](https://python-pillow.org/) 🖼️
- Inspired by modern ATS optimization practices

---


<div align="center">

### ⭐ If you find this helpful, please consider giving us a star!

</div>
