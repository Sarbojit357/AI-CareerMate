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
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #e0e7ff;
        --accent-color: #f59e0b;
        --accent-dark: #d97706;
        --success-color: #10b981;
        --success-light: #d1fae5;
        --warning-color: #f59e0b;
        --warning-light: #fef3c7;
        --info-color: #3b82f6;
        --info-light: #dbeafe;
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
    
    /* DARK MODE FIX - Force readable text colors */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, 
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    .element-container, p, li, span, div {
        color: var(--text-primary) !important;
    }
    
    [data-theme="dark"] .stMarkdown,
    [data-theme="dark"] .stMarkdown p,
    [data-theme="dark"] .stMarkdown li,
    [data-theme="dark"] .stMarkdown span,
    [data-theme="dark"] .stMarkdown h1,
    [data-theme="dark"] .stMarkdown h2,
    [data-theme="dark"] .stMarkdown h3,
    [data-theme="dark"] .element-container,
    [data-theme="dark"] p,
    [data-theme="dark"] li,
    [data-theme="dark"] span,
    [data-theme="dark"] div {
        color: #FFFFFF !important;
    }
    
    .stMarkdown strong, .stMarkdown b {
        font-weight: 700 !important;
        color: inherit !important;
    }
    
    [data-theme="dark"] .stMarkdown strong,
    [data-theme="dark"] .stMarkdown b {
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    
    /* Header styling - STUNNING INDIGO-BLUE GRADIENT */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 3rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 25px 70px rgba(102, 126, 234, 0.5);
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shine 4s infinite;
    }
    
    .header-container::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 24px;
        padding: 2px;
        background: linear-gradient(135deg, rgba(255,255,255,0.3), transparent);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .header-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.75rem;
        text-shadow: 0 6px 30px rgba(0,0,0,0.4), 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
        background: linear-gradient(to right, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.98) !important;
        font-size: 1.3rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
        text-shadow: 0 3px 15px rgba(0,0,0,0.3);
        letter-spacing: 0.3px;
    }
    
    /* Input styling */
    .stTextArea textarea {
        border-radius: 14px;
        border: 2px solid var(--border-color);
        padding: 1rem;
        font-family: 'Roboto', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px var(--primary-light), 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    /* Button styling - VIBRANT AMBER/ORANGE WITH EFFECTS */
    .stButton button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.9rem 2.8rem;
        font-size: 1.08rem;
        font-weight: 700;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 25px rgba(245, 158, 11, 0.45);
        position: relative;
        overflow: hidden;
        letter-spacing: 0.3px;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 10px 35px rgba(245, 158, 11, 0.6);
    }
    
    .stButton button:active {
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
    }
    
    /* Tab styling - INDIGO THEME */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: var(--bg-light);
        border-radius: 14px;
        padding: 0.6rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 0.85rem 1.8rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--primary-light);
        color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
    }
    
    /* Success/Info/Warning styling */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 14px;
        padding: 1.2rem;
    }
    
    /* Keyword tag styling - INDIGO THEME */
    .keyword-tag {
        display: inline-block;
        background: linear-gradient(135deg, #e0e7ff 0%, #ddd6fe 100%);
        color: #4f46e5 !important;
        padding: 0.6rem 1.2rem;
        border-radius: 24px;
        margin: 0.4rem;
        font-size: 0.95rem;
        font-weight: 600;
        border: 1px solid #c7d2fe;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
    }
    
    .keyword-tag:hover {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white !important;
        transform: translateY(-3px) scale(1.08);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        
        .header-subtitle {
            font-size: 1.05rem;
        }
        
        .main {
            padding: 1rem;
        }
        
        .header-container {
            padding: 2rem 1.5rem;
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
            'skills': [],
            'projects': []
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

# OPTIMIZED: Cache keyword extraction
@st.cache_data(ttl=3600, show_spinner=False)
def extract_keywords_with_gemini(input_text, pdf_content_hash):
    """Extract keywords using Gemini - CACHED VERSION"""
    pdf_content = st.session_state.get('current_pdf_content')
    if not pdf_content:
        return "Error: PDF content not found"
    
    prompt = """
    Analyze this resume and job description, then extract and categorize important keywords.
    
    Provide the output in this format:
    
    **Technical Skills:**
    - List all technical skills, programming languages, frameworks
    
    **Soft Skills:**
    - List all soft skills and interpersonal qualities
    
    **Certifications & Education:**
    - List all certifications, degrees, qualifications
    
    **Technologies & Tools:**
    - List all tools, platforms, software mentioned
    
    Be comprehensive and specific.
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

# OPTIMIZED: Cache chatbot responses
@st.cache_data(ttl=1800, show_spinner=False)
def chatbot_response(user_query, job_description, pdf_content_hash):
    """Get chatbot response - CACHED VERSION (30 min TTL)"""
    pdf_content = st.session_state.get('current_pdf_content')
    if not pdf_content:
        return "Error: PDF content not found"
    
    chatbot_prompt = f"""
    You are an expert career coach and resume consultant. A job seeker has the following question:
    
    User Question: {user_query}
    
    Context:
    - Job Description: {job_description}
    - The user has uploaded their resume for analysis
    
    Provide helpful, actionable advice that:
    1. Directly answers their question
    2. Relates to their specific resume and the target job
    3. Offers practical next steps
    4. Is encouraging and professional
    
    Keep the response concise but comprehensive.
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
    """Export resume to markdown format"""
    contact = resume_data.get('contact_info', {})
    
    md_content = f"""# {contact.get('name', 'Your Name')}

**Email:** {contact.get('email', '')} | **Phone:** {contact.get('phone', '')}
**LinkedIn:** {contact.get('linkedin', '')} | **Location:** {contact.get('location', '')}

---

## Professional Summary

{resume_data.get('summary', 'Add your professional summary here')}

---

## Experience

"""
    
    for exp in resume_data.get('experience', []):
        md_content += f"""### {exp.get('title', 'Job Title')} at {exp.get('company', 'Company')}
*{exp.get('duration', 'Duration')}*

{exp.get('description', 'Description')}

"""
    
    md_content += "---\n\n## Education\n\n"
    
    for edu in resume_data.get('education', []):
        md_content += f"""### {edu.get('degree', 'Degree')} - {edu.get('institution', 'Institution')}
*{edu.get('year', 'Year')}*

"""
    
    md_content += "---\n\n## Skills\n\n"
    skills = resume_data.get('skills', [])
    md_content += ", ".join(skills) if skills else "Add your skills here"
    
    md_content += "\n\n---\n\n## Projects\n\n"
    
    for proj in resume_data.get('projects', []):
        md_content += f"""### {proj.get('name', 'Project Name')}
{proj.get('description', 'Description')}

**Technologies:** {proj.get('tech', '')}
**Link:** {proj.get('link', '')}

"""
    
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
                    You are an experienced Technical HR Manager. Review this resume against the job description.
                    
                    Provide a detailed evaluation covering:
                    1. Overall candidate fit and alignment
                    2. Key strengths and competitive advantages
                    3. Areas for improvement
                    4. Missing qualifications or experience
                    5. Specific recommendations for enhancement
                    
                    Be professional, constructive, and specific in your feedback.
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
                    You are an ATS (Applicant Tracking System) scanner. Analyze this resume against the job description.
                    
                    Provide:
                    1. **Match Percentage:** X%
                    2. **Matched Keywords:** List the keywords that align
                    3. **Missing Keywords:** List critical keywords that are absent
                    4. **Profile Summary:** Brief assessment of candidate suitability
                    5. **Recommendations:** Specific actions to improve the match
                    
                    Format your response clearly with headers and bullet points.
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
