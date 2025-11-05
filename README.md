# AI CareerMate - Smart ATS Resume Optimizer 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-10b981?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-ec4899?style=for-the-badge&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Gemini%202.5-AI%20Powered-a855f7?style=for-the-badge&logo=google)

**AI-Powered Resume Analysis & Optimization Platform**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Try%20Now-9333ea?style=for-the-badge)](https://ai-careermate.streamlit.app)

</div>

---

## 🎯 Overview

**AI CareerMate** helps job seekers optimize resumes for Applicant Tracking Systems (ATS) using Google's Gemini 2.5 Flash AI. Get professional insights, match scores, keyword analysis, and personalized recommendations to land your dream job.

> **🚀 Coming Soon:** We're building AI CareerMate into a full-featured **SaaS platform** with subscriptions, team collaboration, and enterprise features!

---

## ✨ Key Features

- 📊 **Resume Review**: Comprehensive HR feedback with strengths and improvement areas
- 🎯 **ATS Match Analysis**: Industry-standard compatibility scores (80%+ is excellent)
- 🔑 **Keyword Extraction**: AI + manual analysis with horizontal display
- 💬 **Career Coach Chatbot**: Scope-restricted AI that only answers resume/career questions
- 📝 **Resume Builder**: Create ATS-friendly resumes (PDF & Markdown export)
- 💡 **Project Generator**: Get tailored project ideas to bridge skill gaps
- ⚡ **Lightning Fast**: 10-50x faster with advanced caching (1-hour TTL)

---

## 🚀 Quick Start


### Requirements

streamlit==1.44.0
google-generativeai==0.8.4
python-dotenv==1.1.0
PyMuPDF==1.24.0
Pillow==11.1.0
reportlab==4.0.7
pandas

**Get API Key:** [Google AI Studio](https://makersuite.google.com/app/apikey)

---

## 📖 Usage

1. **Upload PDF Resume** → Click "Browse files"
2. **Paste Job Description** → Enter target role details
3. **Analyze** → Press "🚀 Analyze Resume" (20-30s first time, instant after!)
4. **Explore 6 Tabs:**
   - Resume Review (qualitative feedback)
   - Match Analysis (80%+ score reference)
   - Keyword Extraction (comma-separated lists)
   - Career Coach (scope-restricted chatbot)
   - Resume Builder (PDF/Markdown export)
   - Project Ideas (skill gap projects)

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core language |
| Streamlit | 1.44.0 | Web framework |
| Gemini 2.5 Flash | Latest | AI analysis |
| PyMuPDF | 1.24.0 | PDF processing |
| ReportLab | 4.0.7 | PDF generation |

---

## ⚡ Performance

**Caching Magic:**

| Operation | First Time | Cached | Speedup |
|-----------|-----------|---------|---------|
| Resume Review | 25s | < 0.1s | **250x** |
| Match Analysis | 22s | < 0.1s | **220x** |
| Keywords | 28s | < 0.1s | **280x** |

**Optimizations:**
- Smart caching with hash-based keys
- PDF Matrix 1.5x scaling (33% faster)
- JPEG quality=85 (60% smaller files)
- Session state management

---

## 🆕 What's New (v2.0)

✅ Advanced caching system (10-50x faster)  
✅ Purple-pink gradient UI theme  
✅ Scope-restricted chatbot (refuses off-topic questions)  
✅ PDF resume export with ReportLab  
✅ Enhanced resume builder (Certifications, Achievements)  
✅ Horizontal keyword display (comma-separated)  
✅ Industry-standard ATS scoring (80%+ context)  
✅ No keyword overlap between tabs  

---

## 🔧 Troubleshooting

**API Key Error:**
Check .env file exists
cat .env

Restart Streamlit
streamlit run app.py

text

**Module Not Found:**
pip install -r requirements.txt --upgrade

text

**Deployment Issues:**
git push origin main # Push changes

Reboot app from Streamlit Cloud dashboard
Hard refresh browser: Ctrl+Shift+R
text

---

## 🚀 Future: SaaS Platform

We're transforming AI CareerMate into a complete SaaS product!

### Planned Features

**💼 Subscription Tiers**
- Free: 5 resumes/month
- Pro: Unlimited + advanced features
- Enterprise: Teams + API access

**👥 Collaboration**
- Team workspaces
- Shared resume libraries
- Admin dashboards

**📊 Analytics**
- Success tracking
- Industry benchmarks
- A/B testing

**🔗 Integrations**
- LinkedIn import
- Job board connections
- Calendar sync

**Timeline:** Beta launch Q1 2026

---

## 🤝 Contributing

Contributions welcome!

Fork repo → Create branch
git checkout -b feature/AmazingFeature

Make changes → Commit
git commit -m 'Add AmazingFeature'

Push → Open PR
git push origin feature/AmazingFeature

text

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file

---

## 🎯 Roadmap

**✅ v2.0 (Current)** - Advanced caching, PDF export, enhanced UI  
**🔄 v2.5 (Q1 2026)** - Cover letters, LinkedIn optimizer  
**📅 v3.0 (Q2 2026)** - SaaS launch with subscriptions  
**🚀 v4.0 (Q3 2026)** - API access, enterprise features  

---

## 💖 Support

- ⭐ Star this repo
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code

---

## 📞 Contact

**Maintainer:** [Your Name]

- 💼 LinkedIn: [Your Profile]
- 📧 Email: your.email@example.com
- 🌐 Live Demo: [ai-careermate.streamlit.app](https://ai-careermate.streamlit.app)

---

<div align="center">

**Made with ❤️ | Powered by Gemini 2.5 AI**

</div>
