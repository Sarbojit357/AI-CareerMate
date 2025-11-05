import os
import io
import base64
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from PIL import Image
import google.generativeai as genai
import re
from collections import Counter
import uuid
import json
from datetime import datetime
import fitz  # PyMuPDF

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app configuration
st.set_page_config(page_title="AI CareerMate", page_icon="📄", layout="wide")

def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Root color variables */
    :root {
        --primary-color: #4B79A1;
        --primary-dark: #2C3E50;
        --primary-light: #E3F2FD;
        --success-color: #2e7d32;
        --success-light: #e8f5e9;
        --warning-color: #f57c00;
        --warning-light: #fff3e0;
        --info-color: #0288d1;
        --info-light: #e1f5fe;
        --text-primary: #1a1a1a;
        --text-secondary: #555555;
        --border-color: #e0e0e0;
        --bg-light: #f8f9fa;
        --bg-white: #ffffff;
    }
    
    /* Main elements styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        padding: 2rem;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        color: #e3f2fd;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* Input styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid var(--border-color);
        padding: 1rem;
        font-family: 'Roboto', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px var(--primary-light);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(75, 121, 161, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(75, 121, 161, 0.4);
    }
    
    /* Card styling */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border-left: 5px solid var(--primary-color);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--bg-light);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Success/Info/Warning styling */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Keyword tag styling */
    .keyword-tag {
        display: inline-block;
        background: var(--primary-light);
        color: var(--primary-dark);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
        
        .main {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)




# Header
def display_header():
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎯 AI CareerMate</h1>
        <p class="header-subtitle">Optimize Your Resume with AI-Powered Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("⏱️ **Note:** AI analysis typically takes 20-30 seconds. Please be patient while we analyze your resume thoroughly!")

# Initialize session state
def initialize_chat_history():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def initialize_resume_data():
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = {
            'contact_info': {
                'name': '',
                'email': '',
                'phone': '',
                'linkedin': '',
                'location': ''
            },
            'summary': '',
            'experience': [],
            'education': [],
            'certifications': [],  # NEW
            'skills': [],
            'projects': [],
            'achievements': []  # NEW
        }


# Safe getter function
def safe_get(data, keys, default=''):
    """Safely get nested dictionary values"""
    try:
        for key in keys:
            data = data[key]
        return data if data else default
    except (KeyError, TypeError, AttributeError):
        return default

# OPTIMIZED: Cache PDF processing
@st.cache_data(ttl=3600, show_spinner=False)
def input_pdf_setup(uploaded_file_bytes):
    """Convert PDF to image and encode to base64 - CACHED VERSION"""
    try:
        pdf_document = fitz.open(stream=uploaded_file_bytes, filetype="pdf")
        first_page = pdf_document[0]
        pix = first_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        
        return pdf_parts
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

# OPTIMIZED: Cache Gemini API responses
@st.cache_data(ttl=3600, show_spinner=False)
def get_gemini_response(input_text, pdf_content_hash, prompt):
    """Get response from Gemini AI - CACHED VERSION"""
    try:
        pdf_content = st.session_state.get('current_pdf_content')
        if not pdf_content:
            return "Error: PDF content not found. Please re-upload your resume."
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# OPTIMIZED: Cache keyword extraction with ATS recommendations
@st.cache_data(ttl=3600, show_spinner=False)
def extract_keywords_with_gemini(input_text, pdf_content_hash):
    """Extract keywords using Gemini with ATS optimization - CACHED VERSION"""
    pdf_content = st.session_state.get('current_pdf_content')
    if not pdf_content:
        return "Error: PDF content not found"
    
    prompt = """
    You are an expert ATS (Applicant Tracking System) specialist and career coach. Analyze this resume against the job description and provide a comprehensive keyword analysis to help the candidate pass ATS screening.
    
    **CRITICAL FORMATTING INSTRUCTIONS:**
    - List keywords in HORIZONTAL format (comma-separated, NOT vertical bullet points)
    - Use this format: Skill1, Skill2, Skill3, Skill4, etc.
    - Make it easy to read and scan quickly
    - Organize by category with clear headers
    
    **PROVIDE OUTPUT IN THIS EXACT FORMAT:**
    
    ## 📊 Current Resume Keywords
    
    **Technical Skills:**
    [List all technical skills comma-separated: Python, JavaScript, React, Node.js, AWS, Docker, etc.]
    
    **Soft Skills:**
    [List all soft skills comma-separated: Leadership, Communication, Problem-solving, Team collaboration, etc.]
    
    **Certifications & Education:**
    [List degrees and certs comma-separated: Bachelor of Computer Science, AWS Certified, Google Cloud Certified, etc.]
    
    **Technologies & Tools:**
    [List tools comma-separated: Git, VS Code, Jira, Jenkins, Kubernetes, etc.]
    
    ---
    
    ## 🎯 Missing Keywords (From Job Description)
    
    **Critical Technical Keywords to Add:**
    [List missing technical keywords comma-separated with explanation]
    
    Example format: Kubernetes, GraphQL, Redis - These are mentioned multiple times in the job description and are critical for ATS matching.
    
    **Important Soft Skills to Add:**
    [List missing soft skills comma-separated]
    
    **Required Tools/Technologies to Highlight:**
    [List missing tools comma-separated]
    
    **Industry-Specific Terms:**
    [List domain keywords comma-separated]
    
    ---
    
    ## ✅ ATS Optimization Recommendations
    
    **1. Top 10 Keywords to Add Immediately:**
    [List in priority order, comma-separated: Keyword1, Keyword2, Keyword3, etc.]
    
    **Why these matter:** [Brief 1-2 sentence explanation]
    
    **Where to add them:**
    - **Professional Summary:** [3-4 keywords to add here]
    - **Skills Section:** [5-6 keywords to add here]
    - **Work Experience:** [Keywords to naturally integrate into bullet points]
    
    **2. Keywords Already Present (Strengthen These):**
    [List keywords that appear but need more emphasis, comma-separated]
    
    **How to strengthen:** [Brief suggestion on increasing frequency/prominence]
    
    **3. Exact Match Keywords (Use EXACTLY as written):**
    [List critical exact-match terms, comma-separated]
    
    **Important:** These must match the job description exactly (including capitalization, acronyms, spelling).
    
    Examples:
    - Use "JavaScript" not "Java Script"
    - Use "AWS" AND "Amazon Web Services"
    - Use "React.js" OR "React" (include both if space allows)
    
    **4. Action Verbs to Incorporate:**
    [List 8-10 powerful action verbs from job description, comma-separated: Led, Developed, Implemented, Optimized, Architected, etc.]
    
    **5. Keyword Density Tips:**
    - High priority keywords (appear 3+ times in JD): [List comma-separated]
    - Medium priority (appear 2 times in JD): [List comma-separated]
    - Context matters: [Brief tip on natural integration]
    
    ---
    
    ## 🚀 Quick Implementation Guide
    
    **Step 1 (5 minutes):** Add these to Skills section
    → [5-7 critical missing skills, comma-separated]
    
    **Step 2 (10 minutes):** Update Professional Summary with
    → [3-4 high-impact keywords, comma-separated]
    
    **Step 3 (15 minutes):** Revise bullet points to include
    → [5-6 keywords naturally integrated into achievements, comma-separated]
    
    **Expected Impact:** These changes could improve your ATS score by 15-20%
    
    ---
    
    ## ⚠️ Common ATS Mistakes to Avoid
    
    **Don't do this:**
    - Keyword stuffing (using keywords unnaturally)
    - Using images or text boxes for skills
    - Misspelling critical terms
    - Using uncommon synonyms when exact terms exist
    
    **Do this instead:**
    - Integrate keywords naturally into sentences
    - Use standard section headers
    - Match job description terminology exactly
    - Include both acronyms and full terms
    
    ---
    
    ## 📈 Keyword Match Summary
    
    **Currently Matched:** [X] keywords from job description
    **Missing Critical Keywords:** [Y] keywords
    **Potential Score Improvement:** +[Z]% with recommended additions
    
    **Priority Level:**
    - 🔴 High Priority: [List 3-5 most critical missing keywords, comma-separated]
    - 🟡 Medium Priority: [List 3-5 important keywords, comma-separated]
    - 🟢 Nice to Have: [List 2-3 optional keywords, comma-separated]
    
    ---
    
    **CRITICAL FORMATTING REMINDERS:**
    - Use comma-separated lists (horizontal format)
    - NO bullet points for skills (use: Skill1, Skill2, Skill3)
    - Make it scannable and easy to copy-paste
    - Group by clear categories with bold headers
    - Be specific and actionable
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([input_text, pdf_content[0], prompt])
        return response.text
    except Exception as e:
        return f"Error extracting keywords: {str(e)}"



# Manual keyword extraction
def manual_keyword_extraction(text):
    """Extract keywords using frequency analysis"""
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
                  'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
                  'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
                  'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
                  'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
                  'other', 'some', 'such', 'than', 'too', 'very', 'from', 'as', 'by'}
    
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    word_freq = Counter(filtered_words)
    top_keywords = word_freq.most_common(20)
    
    return top_keywords

# OPTIMIZED: Cache chatbot responses with strict scope control
@st.cache_data(ttl=1800, show_spinner=False)
def chatbot_response(user_query, job_description, pdf_content_hash):
    """Get chatbot response - CACHED VERSION (30 min TTL) with strict scope"""
    pdf_content = st.session_state.get('current_pdf_content')
    if not pdf_content:
        return "Error: PDF content not found"
    
    chatbot_prompt = f"""
    You are a specialized AI Career Coach and Resume Consultant. You ONLY answer questions related to:
    1. The uploaded resume
    2. The provided job description
    3. Resume optimization and improvement
    4. Job application strategies
    5. ATS (Applicant Tracking System) advice
    6. Interview preparation related to this specific job
    7. Career advice directly related to this job application
    
    **STRICT RULES - YOU MUST FOLLOW:**
    - ONLY answer questions about the resume, job description, or job application process
    - If asked about ANYTHING unrelated (politics, general knowledge, other topics, celebrities, current events, etc.), respond with: "I'm sorry, but I can only help with questions related to your resume and the job you're applying for. Please ask me about your resume, the job description, ATS optimization, or career advice for this specific application."
    - Do NOT answer questions like "Who is the PM of India?", "What is the capital of France?", "Tell me a joke", etc.
    - Stay focused on helping the user with THIS resume and THIS job application ONLY
    
    **CONTEXT PROVIDED:**
    User Question: {user_query}
    Job Description: {job_description}
    Resume: [Attached and analyzed]
    
    **YOUR TASK:**
    First, check if the question is related to resume/job/career. 
    - If YES: Provide helpful, actionable advice that:
      1. Directly answers their question
      2. Relates to their specific resume and the target job
      3. Offers practical next steps
      4. Is encouraging and professional
      5. Keeps response concise but comprehensive
    
    - If NO (question is off-topic): Politely decline and redirect to resume/job topics.
    
    **EXAMPLES OF VALID QUESTIONS:**
    ✅ "How can I improve my resume for this job?"
    ✅ "What skills am I missing for this role?"
    ✅ "How do I highlight my Python experience?"
    ✅ "What should I say in the interview about my project work?"
    ✅ "Does my resume pass ATS for this job?"
    
    **EXAMPLES OF INVALID QUESTIONS (DO NOT ANSWER):**
    ❌ "Who is the Prime Minister of India?"
    ❌ "What's the weather today?"
    ❌ "Tell me a joke"
    ❌ "What is machine learning?" (unless directly tied to their resume/job)
    ❌ "Who won the cricket match?"
    
    Now, analyze the user's question and respond appropriately.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([chatbot_prompt, pdf_content[0]])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# OPTIMIZED: Cache resume generation
@st.cache_data(ttl=3600, show_spinner=False)
def generate_resume_suggestions(job_description, section_type):
    """Generate AI suggestions for resume sections - CACHED VERSION"""
    prompts = {
        'summary': f"Write a professional summary (3-4 sentences) for a resume targeting this job:\n\n{job_description}\n\nMake it impactful and keyword-rich.",
        'skills': f"List 10-12 key skills that match this job description:\n\n{job_description}\n\nProvide only the skill names, comma-separated.",
        'experience': f"Generate 3-4 achievement-focused bullet points for a work experience entry targeting this job:\n\n{job_description}\n\nUse action verbs and quantify results where possible."
    }
    
    prompt = prompts.get(section_type, "")
    if not prompt:
        return "Invalid section type"
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# OPTIMIZED: Cache project generation
@st.cache_data(ttl=3600, show_spinner=False)
def generate_ideal_project(job_description, pdf_content_hash):
    """Generate ideal project recommendation - CACHED VERSION"""
    pdf_content = st.session_state.get('current_pdf_content')
    if not pdf_content:
        return "Error: PDF content not found"
    
    project_prompt = """
    Based on the resume and target job description, generate a comprehensive project idea that:
    
    1. Bridges the skill gaps between the resume and job requirements
    2. Demonstrates relevant technical competencies
    3. Is realistic to complete in 2-4 weeks
    4. Would strengthen the job application
    
    Provide the output in this format:
    
    **Project Title:**
    [Catchy, professional title]
    
    **Project Overview:**
    [2-3 sentence description]
    
    **Objectives:**
    - [Goal 1]
    - [Goal 2]
    - [Goal 3]
    
    **Technical Stack:**
    [List technologies, frameworks, tools]
    
    **Key Features:**
    1. [Feature 1]
    2. [Feature 2]
    3. [Feature 3]
    4. [Feature 4]
    5. [Feature 5]
    
    **Implementation Phases:**
    **Phase 1:** [Description]
    **Phase 2:** [Description]
    **Phase 3:** [Description]
    **Phase 4:** [Description]
    
    **Skills Demonstrated:**
    [List 5-7 skills this project showcases]
    
    **How to Showcase:**
    [Tips on presenting this in resume and interviews]
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content([job_description, pdf_content[0], project_prompt])
        return response.text
    except Exception as e:
        return f"Error generating project idea: {str(e)}"

# Resume builder functions
def export_resume_to_markdown(resume_data):
    """Export resume to markdown format with all sections"""
    contact = resume_data.get('contact_info', {})
    
    # Header with Contact Info
    md_content = f"""# {contact.get('name', 'Your Name')}

**Email:** {contact.get('email', '')} | **Phone:** {contact.get('phone', '')}
**LinkedIn:** {contact.get('linkedin', '')} | **Location:** {contact.get('location', '')}

---

## Professional Summary

{resume_data.get('summary', 'Add your professional summary here')}

---

"""
    
    # Experience Section
    experiences = resume_data.get('experience', [])
    if experiences and any(exp.get('title') or exp.get('company') for exp in experiences):
        md_content += "## Professional Experience\n\n"
        for exp in experiences:
            if exp.get('title') or exp.get('company'):
                md_content += f"""### {exp.get('title', 'Job Title')} | {exp.get('company', 'Company')}
*{exp.get('duration', 'Duration')} | {exp.get('location', '')}*

{exp.get('description', '')}

"""
        md_content += "---\n\n"
    
    # Education Section
    education = resume_data.get('education', [])
    if education and any(edu.get('degree') or edu.get('institution') for edu in education):
        md_content += "## Education\n\n"
        for edu in education:
            if edu.get('degree') or edu.get('institution'):
                md_content += f"""### {edu.get('degree', 'Degree')} | {edu.get('institution', 'Institution')}
*{edu.get('year', 'Year')} | {edu.get('location', '')}*

{edu.get('gpa', '')}
{edu.get('description', '')}

"""
        md_content += "---\n\n"
    
    # Certifications Section
    certifications = resume_data.get('certifications', [])
    if certifications and any(cert.get('name') for cert in certifications):
        md_content += "## Certifications\n\n"
        for cert in certifications:
            if cert.get('name'):
                issuer = cert.get('issuer', '')
                date = cert.get('date', '')
                credential = cert.get('credential_id', '')
                
                md_content += f"### {cert.get('name')}\n"
                if issuer:
                    md_content += f"**Issuing Organization:** {issuer}\n"
                if date:
                    md_content += f"**Issue Date:** {date}\n"
                if credential:
                    md_content += f"**Credential ID:** {credential}\n"
                if cert.get('url'):
                    md_content += f"**Verification URL:** {cert.get('url')}\n"
                md_content += "\n"
        md_content += "---\n\n"
    
    # Skills Section
    skills = resume_data.get('skills', [])
    if skills:
        md_content += "## Technical Skills\n\n"
        md_content += ", ".join(skills)
        md_content += "\n\n---\n\n"
    
    # Projects Section
    projects = resume_data.get('projects', [])
    if projects and any(proj.get('name') for proj in projects):
        md_content += "## Projects\n\n"
        for proj in projects:
            if proj.get('name'):
                md_content += f"""### {proj.get('name', 'Project Name')}
{proj.get('description', '')}

**Technologies:** {proj.get('tech', '')}
**Link:** {proj.get('link', '')}

"""
        md_content += "---\n\n"
    
    # Achievements Section
    achievements = resume_data.get('achievements', [])
    if achievements and any(ach.get('title') for ach in achievements):
        md_content += "## Achievements & Awards\n\n"
        for ach in achievements:
            if ach.get('title'):
                md_content += f"""### {ach.get('title')}
*{ach.get('date', '')} | {ach.get('organization', '')}*

{ach.get('description', '')}

"""
        md_content += "---\n\n"
    
    return md_content


# Main app
def main():
    # Initialize session state FIRST
    initialize_chat_history()
    initialize_resume_data()
    
    load_css()
    display_header()
    
    # Main input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_text = st.text_area(
            "📝 Paste the Job Description",
            height=200,
            placeholder="Paste the complete job description here..."
        )
    
    with col2:
        uploaded_file = st.file_uploader(
            "📄 Upload Your Resume (PDF)",
            type=["pdf"],
            help="Upload your resume in PDF format"
        )
    
    submit = st.button("🚀 Analyze Resume", use_container_width=True)
    
    if submit:
        if not uploaded_file:
            st.error("❌ Please upload your resume!")
            return
        
        if not input_text:
            st.error("❌ Please provide a job description!")
            return
        
        with st.spinner('📄 Processing your resume...'):
            pdf_bytes = uploaded_file.read()
            
            import hashlib
            pdf_hash = hashlib.md5(pdf_bytes).hexdigest()
            
            pdf_content = input_pdf_setup(pdf_bytes)
            
            if pdf_content:
                st.session_state.current_pdf_content = pdf_content
                st.session_state.pdf_hash = pdf_hash
                st.success("✅ Resume processed successfully!")
            else:
                st.error("❌ Failed to process resume. Please try another file.")
                return
    
    # Tabs for different features
    if uploaded_file and input_text:
        tabs = st.tabs([
            "🔍 Resume Review",
            "📊 Match Analysis",
            "🔑 Keyword Extraction",
            "💬 Career Coach",
            "📝 Resume Builder",
            "💡 Project Ideas"
        ])
        
                # Tab 1: Resume Review
        with tabs[0]:
            st.subheader("📋 Professional Resume Review")
            
            if st.button("Tell me about the resume", key="review"):
                with st.spinner('🔍 Analyzing resume... (this may take 20-30 seconds)'):
                    review_prompt = """
                    You are an experienced Technical HR Manager and ATS specialist. Provide a direct, comprehensive resume evaluation.
                    
                    **IMPORTANT INSTRUCTIONS:**
                    - Do NOT format your response as a letter (no "To:", "From:", "Date:", etc.)
                    - Do NOT include match percentage or score (that's in a separate section)
                    - Start directly with the evaluation
                    - Use clear section headers with bullet points
                    - Be specific, constructive, and actionable
                    - Focus on helping the candidate improve their application
                    
                    **PROVIDE YOUR ANALYSIS IN THIS FORMAT:**
                    
                    ## 📊 Overall Assessment
                    [Provide a 3-4 sentence summary: Is this candidate a good fit? What's the overall impression? What stands out positively or negatively?]
                    
                    ---
                    
                    ## ✅ Key Strengths
                    [List 5-7 specific strengths that make this candidate competitive:]
                    - **[Strength Category]:** [Specific example from resume with details]
                    - **[Strength Category]:** [Specific example from resume with details]
                    - **[Strength Category]:** [Specific example from resume with details]
                    - [Continue...]
                    
                    ---
                    
                    ## ⚠️ Areas for Improvement
                    [List 5-7 specific areas that need work:]
                    - **[Area]:** [Specific issue and how to fix it]
                    - **[Area]:** [Specific issue and how to fix it]
                    - **[Area]:** [Specific issue and how to fix it]
                    - [Continue...]
                    
                    ---
                    
                    ## 🎯 Missing Qualifications & Skills
                    
                    **Critical Missing Skills:**
                    - [Skill 1 from job description that's completely missing]
                    - [Skill 2 from job description that's completely missing]
                    - [Skill 3 from job description that's completely missing]
                    
                    **Skills Present but Underemphasized:**
                    - [Skill that exists but needs more visibility]
                    - [Skill that exists but needs better placement]
                    
                    **Recommended Additions:**
                    - [What should be added to the resume]
                    - [What experiences should be highlighted more]
                    - [What sections should be expanded]
                    
                    ---
                    
                    ## 💡 Specific Recommendations
                    
                    **Immediate Actions (Do This Today):**
                    1. [Highest priority action with specific instructions]
                    2. [Second highest priority with specific instructions]
                    3. [Third priority with specific instructions]
                    
                    **Resume Structure & Formatting:**
                    - [Comments on layout, readability, visual appeal]
                    - [Suggestions for better organization]
                    - [Section ordering recommendations]
                    
                    **Content Enhancement:**
                    - [How to make bullet points more impactful]
                    - [Which experiences to expand]
                    - [What to remove or condense]
                    
                    **Keywords & ATS Optimization:**
                    - [Specific keywords to add and where]
                    - [How to naturally incorporate required terms]
                    - [Formatting tips for ATS compatibility]
                    
                    ---
                    
                    ## 🚀 Final Verdict & Next Steps
                    
                    **Honest Assessment:**
                    [Should they apply as-is, or improve first? What are their realistic chances? Be encouraging but honest.]
                    
                    **Action Plan:**
                    1. **First 24 hours:** [What to do immediately]
                    2. **This week:** [Follow-up actions]
                    3. **Before applying:** [Final checklist]
                    
                    **Interview Preparation Tips:**
                    [Based on resume, what questions should they prepare for? What gaps might interviewers probe?]
                    
                    ---
                    
                    **Remember:**
                    - NO letter format
                    - NO match percentage or score
                    - NO "To/From/Date" headers
                    - Start directly with analysis
                    - Be specific and actionable
                    - Use markdown formatting for clarity
                    - Focus on constructive feedback
                    """
                    
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = get_gemini_response(input_text, pdf_hash, review_prompt)
                    
                st.markdown(response)

                # Tab 2: Match Analysis
        with tabs[1]:
            st.subheader("🎯 ATS Compatibility Score")
            
            if st.button("Calculate ATS Match Percentage", key="match"):
                with st.spinner('📊 Calculating match score... (this may take 20-30 seconds)'):
                    match_prompt = """
                    You are an expert ATS (Applicant Tracking System) scanner and recruiter. Analyze this resume against the job description and provide a match percentage with detailed compatibility assessment.
                    
                    **CRITICAL FORMATTING INSTRUCTION:**
                    - Display the match percentage at the VERY TOP in LARGE, BOLD text
                    - Use this EXACT format: # 🎯 **YOUR MATCH SCORE: XX%**
                    - Follow with optimal score reference
                    - DO NOT include keyword analysis (that's in a separate section)
                    - Focus on overall compatibility, qualifications, and experience match
                    
                    **PROVIDE YOUR ANALYSIS IN THIS EXACT FORMAT:**
                    
                    # 🎯 **YOUR MATCH SCORE: XX%**
                    
                    > **Industry Standard:** A score of 80%+ is considered excellent and significantly increases your chances of passing ATS screening. Scores of 70-79% are good, 60-69% are moderate, and below 60% need significant improvement.
                    
                    ---
                    
                    ## 📊 Score Breakdown
                    
                    | Category | Your Score | Status |
                    |----------|------------|--------|
                    | **Experience Alignment** | XX% | ✅/⚠️/❌ |
                    | **Skills Match** | XX% | ✅/⚠️/❌ |
                    | **Education Requirements** | XX% | ✅/⚠️/❌ |
                    | **Technical Qualifications** | XX% | ✅/⚠️/❌ |
                    | **Job Level Fit** | XX% | ✅/⚠️/❌ |
                    
                    **Legend:** ✅ Strong Match (80%+) | ⚠️ Partial Match (60-79%) | ❌ Weak Match (<60%)
                    
                    ---
                    
                    ## ✅ What Matches Well
                    
                    **Experience & Background:**
                    - ✅ [Specific experience that aligns - with details]
                    - ✅ [Another matching experience point]
                    - ✅ [Third matching point]
                    - [List 5-7 strong alignment points]
                    
                    **Qualifications Met:**
                    - ✅ [Qualification 1 - be specific]
                    - ✅ [Qualification 2 - be specific]
                    - ✅ [Qualification 3 - be specific]
                    
                    **Technical Capabilities:**
                    - ✅ [Technical strength 1]
                    - ✅ [Technical strength 2]
                    - ✅ [Technical strength 3]
                    
                    ---
                    
                    ## ⚠️ Gaps & Missing Qualifications
                    
                    **Experience Gaps:**
                    - ⚠️ [Gap 1 - what's missing or weak]
                    - ⚠️ [Gap 2 - what's missing or weak]
                    - ⚠️ [Gap 3 - what's missing or weak]
                    
                    **Qualification Shortfalls:**
                    - ❌ [Missing requirement 1]
                    - ❌ [Missing requirement 2]
                    - ⚠️ [Partially met requirement]
                    
                    **Technical Gaps:**
                    - [Technology or skill not demonstrated]
                    - [Another missing technical element]
                    
                    ---
                    
                    ## 🎯 Recommendations to Improve Score
                    
                    **High-Impact Actions (Each worth +5-10%):**
                    
                    1. **Highlight Relevant Experience:**
                       - [Specific suggestion about which projects/roles to emphasize more]
                       - Estimated impact: +X%
                    
                    2. **Demonstrate Missing Qualifications:**
                       - [How to showcase or add missing requirements]
                       - Estimated impact: +X%
                    
                    3. **Strengthen Technical Profile:**
                       - [Specific technical additions or emphasis needed]
                       - Estimated impact: +X%
                    
                    4. **Adjust Resume Structure:**
                       - [Layout or section organization improvements]
                       - Estimated impact: +X%
                    
                    ---
                    
                    ## 📈 Path to 80%+ Score
                    
                    **Your Current Gap:** Need +[X]% to reach excellent (80%+)
                    
                    **Priority Actions (In Order):**
                    1. [Highest priority change] → Estimated +X%
                    2. [Second priority] → Estimated +X%
                    3. [Third priority] → Estimated +X%
                    4. [Fourth priority] → Estimated +X%
                    
                    **Realistic Timeline:**
                    - Quick fixes (today): [Actions that take <2 hours]
                    - This week: [Actions that need more time]
                    - Before applying: [Final preparations]
                    
                    **Projected Score After Improvements:** [New estimated percentage]
                    
                    ---
                    
                    ## 🚨 ATS Red Flags
                    
                    [Analyze for formatting or structural issues that might hurt ATS parsing:]
                    
                    **Detected Issues:**
                    - [Issue 1, if any - with fix]
                    - [Issue 2, if any - with fix]
                    - [Or: "✅ No critical ATS formatting issues detected"]
                    
                    **Formatting Best Practices:**
                    - [Suggestion 1 for better ATS compatibility]
                    - [Suggestion 2 for better ATS compatibility]
                    
                    ---
                    
                    ## 💼 Overall Fit Assessment
                    
                    **Experience Level Match:**
                    [Is the candidate at the right career level for this role? Junior/Mid/Senior alignment]
                    
                    **Industry Background:**
                    [Does their industry experience align with the target company/role?]
                    
                    **Company Culture Fit Indicators:**
                    [Based on resume, any indicators of fit with company values/culture from job description?]
                    
                    ---
                    
                    ## 🎯 Final Recommendation
                    
                    **Should You Apply?**
                    - 80%+ → YES, apply with confidence ✅
                    - 70-79% → YES, but improve resume first for better chances ⚠️
                    - 60-69% → IMPROVE first, then apply ⚠️
                    - <60% → MAJOR improvements needed OR consider different roles ❌
                    
                    **Your Verdict:** [Specific recommendation for this candidate]
                    
                    **Confidence Level:** [High/Moderate/Low] - [Brief explanation]
                    
                    **Next Best Action:**
                    [One clear, specific action: apply now / improve specific areas / gain more experience / target similar but better-fitting roles]
                    
                    ---
                    
                    **IMPORTANT REMINDERS:**
                    - Display match percentage in LARGE text at the top: # 🎯 **YOUR MATCH SCORE: XX%**
                    - Include optimal score reference (80%+ is excellent)
                    - NO keyword analysis (that's in the next tab)
                    - Focus on qualifications, experience, and overall fit
                    - Provide specific, actionable, measurable recommendations
                    - Use tables and formatting for visual clarity
                    """
                    
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = get_gemini_response(input_text, pdf_hash, match_prompt)
                    
                st.markdown(response)

        
        
        # Tab 3: Keyword Extraction - Fixed with session state
        with tabs[2]:
            st.subheader("🔑 Keyword Analysis")
            
            # Initialize session state for keyword results
            if 'ai_keywords_result' not in st.session_state:
                st.session_state.ai_keywords_result = None
            if 'manual_keywords_result' not in st.session_state:
                st.session_state.manual_keywords_result = None
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🤖 AI-Powered Keyword Extraction", key="ai_keywords", use_container_width=True):
                    with st.spinner('🔍 Extracting keywords with AI... (this may take 20-30 seconds)'):
                        pdf_hash = st.session_state.get('pdf_hash', '')
                        ai_response = extract_keywords_with_gemini(input_text, pdf_hash)
                        st.session_state.ai_keywords_result = ai_response
                
                # Display AI keywords result if it exists
                if st.session_state.ai_keywords_result:
                    st.markdown(st.session_state.ai_keywords_result)
            
            with col2:
                if st.button("📊 Manual Frequency Analysis", key="manual_keywords", use_container_width=True):
                    combined_text = input_text
                    keywords = manual_keyword_extraction(combined_text)
                    st.session_state.manual_keywords_result = keywords
                
                # Display manual keywords result if it exists
                if st.session_state.manual_keywords_result:
                    st.write("**Top 20 Keywords by Frequency:**")
                    for word, count in st.session_state.manual_keywords_result:
                        st.markdown(f'<span class="keyword-tag">{word}: {count}</span>', unsafe_allow_html=True)
                    
                    import pandas as pd
                    df = pd.DataFrame(st.session_state.manual_keywords_result, columns=['Keyword', 'Frequency'])
                    st.bar_chart(df.set_index('Keyword'))

        
        # Tab 4: Career Coach Chatbot
        with tabs[3]:
            st.subheader("💬 AI Career Coach")
            
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            user_query = st.chat_input("Ask me anything about your resume or career...")
            
            if user_query:
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                
                with st.chat_message("user"):
                    st.write(user_query)
                
                with st.spinner('💭 Thinking...'):
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = chatbot_response(user_query, input_text, pdf_hash)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                with st.chat_message("assistant"):
                    st.write(response)
        
                 # Tab 5: Resume Builder
        with tabs[4]:
            st.subheader("📝 Resume Builder")
            
            if 'resume_data' not in st.session_state:
                initialize_resume_data()
            
            # Contact Information
            st.write("### Contact Information")
            col1, col2 = st.columns(2)
            
            with col1:
                if 'contact_info' not in st.session_state.resume_data:
                    st.session_state.resume_data['contact_info'] = {}
                
                name = st.text_input(
                    "Full Name",
                    value=safe_get(st.session_state.resume_data, ['contact_info', 'name']),
                    key="name_input"
                )
                st.session_state.resume_data['contact_info']['name'] = name
                
                email = st.text_input(
                    "Email",
                    value=safe_get(st.session_state.resume_data, ['contact_info', 'email']),
                    key="email_input"
                )
                st.session_state.resume_data['contact_info']['email'] = email
                
            with col2:
                phone = st.text_input(
                    "Phone",
                    value=safe_get(st.session_state.resume_data, ['contact_info', 'phone']),
                    key="phone_input"
                )
                st.session_state.resume_data['contact_info']['phone'] = phone
                
                linkedin = st.text_input(
                    "LinkedIn",
                    value=safe_get(st.session_state.resume_data, ['contact_info', 'linkedin']),
                    key="linkedin_input"
                )
                st.session_state.resume_data['contact_info']['linkedin'] = linkedin
            
            location = st.text_input(
                "Location (City, State/Country)",
                value=safe_get(st.session_state.resume_data, ['contact_info', 'location']),
                key="location_input"
            )
            st.session_state.resume_data['contact_info']['location'] = location
            
            st.write("---")
            
            # Professional Summary
            st.write("### Professional Summary")
            col1, col2 = st.columns([3, 1])
            with col1:
                summary = st.text_area(
                    "Summary",
                    value=st.session_state.resume_data.get('summary', ''),
                    height=100,
                    key="summary_input"
                )
                st.session_state.resume_data['summary'] = summary
            with col2:
                if st.button("✨ Generate Summary", key="gen_summary"):
                    with st.spinner('Generating...'):
                        suggestion = generate_resume_suggestions(input_text, 'summary')
                        st.session_state.resume_data['summary'] = suggestion
                        st.rerun()
            
            st.write("---")
            
            # Experience Section
            st.write("### Professional Experience")
            if 'experience' not in st.session_state.resume_data:
                st.session_state.resume_data['experience'] = []
            
            for i, exp in enumerate(st.session_state.resume_data.get('experience', [])):
                with st.expander(f"Experience #{i+1}: {exp.get('title', 'Job Title')}", expanded=(i==0)):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input(f"Job Title", value=exp.get('title', ''), key=f"exp_title_{i}")
                        company = st.text_input(f"Company", value=exp.get('company', ''), key=f"exp_company_{i}")
                    with col2:
                        duration = st.text_input(f"Duration (e.g., Jan 2020 - Present)", value=exp.get('duration', ''), key=f"exp_duration_{i}")
                        location = st.text_input(f"Location", value=exp.get('location', ''), key=f"exp_location_{i}")
                    
                    description = st.text_area(f"Job Description", value=exp.get('description', ''), height=100, key=f"exp_desc_{i}")
                    
                    st.session_state.resume_data['experience'][i] = {
                        'title': title,
                        'company': company,
                        'duration': duration,
                        'location': location,
                        'description': description
                    }
                    
                    if st.button(f"🗑️ Remove Experience #{i+1}", key=f"remove_exp_{i}"):
                        st.session_state.resume_data['experience'].pop(i)
                        st.rerun()
            
            if st.button("➕ Add Experience", key="add_exp"):
                st.session_state.resume_data['experience'].append({
                    'title': '', 'company': '', 'duration': '', 'location': '', 'description': ''
                })
                st.rerun()
            
            st.write("---")
            
            # Education Section
            st.write("### Education")
            if 'education' not in st.session_state.resume_data:
                st.session_state.resume_data['education'] = []
            
            for i, edu in enumerate(st.session_state.resume_data.get('education', [])):
                with st.expander(f"Education #{i+1}: {edu.get('degree', 'Degree')}", expanded=(i==0)):
                    col1, col2 = st.columns(2)
                    with col1:
                        degree = st.text_input(f"Degree", value=edu.get('degree', ''), key=f"edu_degree_{i}")
                        institution = st.text_input(f"Institution", value=edu.get('institution', ''), key=f"edu_institution_{i}")
                    with col2:
                        year = st.text_input(f"Year (e.g., 2020 - 2024)", value=edu.get('year', ''), key=f"edu_year_{i}")
                        location = st.text_input(f"Location", value=edu.get('location', ''), key=f"edu_location_{i}")
                    
                    gpa = st.text_input(f"GPA (optional)", value=edu.get('gpa', ''), key=f"edu_gpa_{i}")
                    description = st.text_area(f"Description (honors, coursework, etc.)", value=edu.get('description', ''), height=80, key=f"edu_desc_{i}")
                    
                    st.session_state.resume_data['education'][i] = {
                        'degree': degree,
                        'institution': institution,
                        'year': year,
                        'location': location,
                        'gpa': gpa,
                        'description': description
                    }
                    
                    if st.button(f"🗑️ Remove Education #{i+1}", key=f"remove_edu_{i}"):
                        st.session_state.resume_data['education'].pop(i)
                        st.rerun()
            
            if st.button("➕ Add Education", key="add_edu"):
                st.session_state.resume_data['education'].append({
                    'degree': '', 'institution': '', 'year': '', 'location': '', 'gpa': '', 'description': ''
                })
                st.rerun()
            
            st.write("---")
            
            # Certifications Section (NEW)
            st.write("### Certifications")
            if 'certifications' not in st.session_state.resume_data:
                st.session_state.resume_data['certifications'] = []
            
            for i, cert in enumerate(st.session_state.resume_data.get('certifications', [])):
                with st.expander(f"Certification #{i+1}: {cert.get('name', 'Certification Name')}", expanded=(i==0)):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input(f"Certification Name", value=cert.get('name', ''), key=f"cert_name_{i}")
                        issuer = st.text_input(f"Issuing Organization", value=cert.get('issuer', ''), key=f"cert_issuer_{i}")
                    with col2:
                        date = st.text_input(f"Issue Date", value=cert.get('date', ''), key=f"cert_date_{i}")
                        credential_id = st.text_input(f"Credential ID (optional)", value=cert.get('credential_id', ''), key=f"cert_id_{i}")
                    
                    url = st.text_input(f"Verification URL (optional)", value=cert.get('url', ''), key=f"cert_url_{i}")
                    
                    st.session_state.resume_data['certifications'][i] = {
                        'name': name,
                        'issuer': issuer,
                        'date': date,
                        'credential_id': credential_id,
                        'url': url
                    }
                    
                    if st.button(f"🗑️ Remove Certification #{i+1}", key=f"remove_cert_{i}"):
                        st.session_state.resume_data['certifications'].pop(i)
                        st.rerun()
            
            if st.button("➕ Add Certification", key="add_cert"):
                st.session_state.resume_data['certifications'].append({
                    'name': '', 'issuer': '', 'date': '', 'credential_id': '', 'url': ''
                })
                st.rerun()
            
            st.write("---")
            
            # Skills Section
            st.write("### Skills")
            col1, col2 = st.columns([3, 1])
            with col1:
                current_skills = st.session_state.resume_data.get('skills', [])
                skills_str = ", ".join(current_skills) if isinstance(current_skills, list) else ""
                
                skills_input = st.text_area(
                    "Skills (comma-separated)",
                    value=skills_str,
                    height=100,
                    key="skills_input"
                )
                st.session_state.resume_data['skills'] = [s.strip() for s in skills_input.split(',') if s.strip()]
            with col2:
                if st.button("🎯 Suggest Skills", key="gen_skills"):
                    with st.spinner('Generating...'):
                        suggestion = generate_resume_suggestions(input_text, 'skills')
                        skills_list = [s.strip() for s in suggestion.split(',') if s.strip()]
                        st.session_state.resume_data['skills'] = skills_list
                        st.rerun()
            
            st.write("---")
            
            # Projects Section
            st.write("### Projects")
            if 'projects' not in st.session_state.resume_data:
                st.session_state.resume_data['projects'] = []
            
            for i, proj in enumerate(st.session_state.resume_data.get('projects', [])):
                with st.expander(f"Project #{i+1}: {proj.get('name', 'Project Name')}", expanded=(i==0)):
                    name = st.text_input(f"Project Name", value=proj.get('name', ''), key=f"proj_name_{i}")
                    tech = st.text_input(f"Technologies Used", value=proj.get('tech', ''), key=f"proj_tech_{i}")
                    description = st.text_area(f"Description", value=proj.get('description', ''), height=80, key=f"proj_desc_{i}")
                    link = st.text_input(f"Project URL (optional)", value=proj.get('link', ''), key=f"proj_link_{i}")
                    
                    st.session_state.resume_data['projects'][i] = {
                        'name': name,
                        'tech': tech,
                        'description': description,
                        'link': link
                    }
                    
                    if st.button(f"🗑️ Remove Project #{i+1}", key=f"remove_proj_{i}"):
                        st.session_state.resume_data['projects'].pop(i)
                        st.rerun()
            
            if st.button("➕ Add Project", key="add_proj"):
                st.session_state.resume_data['projects'].append({
                    'name': '', 'tech': '', 'description': '', 'link': ''
                })
                st.rerun()
            
            st.write("---")
            
            # Achievements Section (NEW)
            st.write("### Achievements & Awards")
            if 'achievements' not in st.session_state.resume_data:
                st.session_state.resume_data['achievements'] = []
            
            for i, ach in enumerate(st.session_state.resume_data.get('achievements', [])):
                with st.expander(f"Achievement #{i+1}: {ach.get('title', 'Achievement Title')}", expanded=(i==0)):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input(f"Achievement Title", value=ach.get('title', ''), key=f"ach_title_{i}")
                        organization = st.text_input(f"Organization/Competition", value=ach.get('organization', ''), key=f"ach_org_{i}")
                    with col2:
                        date = st.text_input(f"Date", value=ach.get('date', ''), key=f"ach_date_{i}")
                    
                    description = st.text_area(f"Description", value=ach.get('description', ''), height=80, key=f"ach_desc_{i}")
                    
                    st.session_state.resume_data['achievements'][i] = {
                        'title': title,
                        'organization': organization,
                        'date': date,
                        'description': description
                    }
                    
                    if st.button(f"🗑️ Remove Achievement #{i+1}", key=f"remove_ach_{i}"):
                        st.session_state.resume_data['achievements'].pop(i)
                        st.rerun()
            
            if st.button("➕ Add Achievement", key="add_ach"):
                st.session_state.resume_data['achievements'].append({
                    'title': '', 'organization': '', 'date': '', 'description': ''
                })
                st.rerun()
            
            st.write("---")
            
            # Export Button
            if st.button("📥 Export Resume to Markdown", key="export"):
                markdown_content = export_resume_to_markdown(st.session_state.resume_data)
                st.download_button(
                    label="Download Resume",
                    data=markdown_content,
                    file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    key="download_resume"
                )

        
        # Tab 6: Project Ideas
        with tabs[5]:
            st.subheader("💡 Project Idea Generator")
            
            st.info("Generate a personalized project recommendation to strengthen your application!")
            
            if st.button("🚀 Generate Ideal Project", key="gen_project"):
                with st.spinner('🔍 Analyzing skills gap and generating project... (this may take 30-40 seconds)'):
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = generate_ideal_project(input_text, pdf_hash)
                    
                st.markdown(response)
                
                st.download_button(
                    label="📥 Download Project Plan",
                    data=response,
                    file_name=f"project_idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    key="download_project"
                )

if __name__ == "__main__":
    main()
