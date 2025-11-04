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
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

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
        <h1 class="header-title">🎯 ATS Resume Expert</h1>
        <p class="header-subtitle">Optimize Your Resume with AI-Powered Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add performance note
    st.info("⏱️ **Note:** AI analysis typically takes 20-30 seconds. Please be patient while we analyze your resume thoroughly!")

# OPTIMIZED: Cache PDF processing
@st.cache_data(ttl=3600, show_spinner=False)
def input_pdf_setup(uploaded_file_bytes):
    """Convert PDF to image and encode to base64 - CACHED VERSION"""
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=uploaded_file_bytes, filetype="pdf")
        first_page = pdf_document[0]
        
        # OPTIMIZED: Reduced from 2x to 1.5x resolution
        pix = first_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # OPTIMIZED: Reduced JPEG quality from 95 to 85
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85)
        img_byte_arr = img_byte_arr.getvalue()
        
        # Encode to base64
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
        # Retrieve PDF content from session state
        pdf_content = st.session_state.get('current_pdf_content')
        if not pdf_content:
            return "Error: PDF content not found"
        
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
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                  'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
                  'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
                  'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
                  'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
                  'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
                  'other', 'some', 'such', 'than', 'too', 'very', 'from', 'as', 'by'}
    
    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out stop words and short words
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count frequency
    word_freq = Counter(filtered_words)
    
    # Get top 20 keywords
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
    md_content = f"""# {resume_data['contact_info']['name']}

**Email:** {resume_data['contact_info']['email']} | **Phone:** {resume_data['contact_info']['phone']}
**LinkedIn:** {resume_data['contact_info']['linkedin']} | **Location:** {resume_data['contact_info']['location']}

---

## Professional Summary

{resume_data['summary']}

---

## Experience

"""
    
    for exp in resume_data['experience']:
        md_content += f"""### {exp['title']} at {exp['company']}
*{exp['duration']}*

{exp['description']}

"""
    
    md_content += "---\n\n## Education\n\n"
    
    for edu in resume_data['education']:
        md_content += f"""### {edu['degree']} - {edu['institution']}
*{edu['year']}*

"""
    
    md_content += "---\n\n## Skills\n\n"
    md_content += ", ".join(resume_data['skills'])
    
    md_content += "\n\n---\n\n## Projects\n\n"
    
    for proj in resume_data['projects']:
        md_content += f"""### {proj['name']}
{proj['description']}

**Technologies:** {proj['tech']}
**Link:** {proj['link']}

"""
    
    return md_content

# Main app
def main():
    load_css()
    display_header()
    initialize_chat_history()
    initialize_resume_data()
    
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
        
        # Process PDF with progress indication
        with st.spinner('📄 Processing your resume...'):
            # Read file bytes
            pdf_bytes = uploaded_file.read()
            
            # Generate hash for caching
            import hashlib
            pdf_hash = hashlib.md5(pdf_bytes).hexdigest()
            
            # Process PDF (cached)
            pdf_content = input_pdf_setup(pdf_bytes)
            
            if pdf_content:
                # Store in session state for use in cached functions
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
                    
                st.markdown(f'<div class="result-card">{response}</div>', unsafe_allow_html=True)
        
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
                    
                st.markdown(f'<div class="result-card">{response}</div>', unsafe_allow_html=True)
        
        # Tab 3: Keyword Extraction
        with tabs[2]:
            st.subheader("🔑 Keyword Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🤖 AI-Powered Keyword Extraction", key="ai_keywords"):
                    with st.spinner('🔍 Extracting keywords with AI... (this may take 20-30 seconds)'):
                        pdf_hash = st.session_state.get('pdf_hash', '')
                        response = extract_keywords_with_gemini(input_text, pdf_hash)
                        
                    st.markdown(f'<div class="result-card">{response}</div>', unsafe_allow_html=True)
            
            with col2:
                if st.button("📊 Manual Frequency Analysis", key="manual_keywords"):
                    combined_text = input_text + " " + uploaded_file.name
                    keywords = manual_keyword_extraction(combined_text)
                    
                    st.write("**Top 20 Keywords by Frequency:**")
                    for word, count in keywords:
                        st.markdown(f'<span class="keyword-tag">{word}: {count}</span>', unsafe_allow_html=True)
                    
                    # Bar chart
                    import pandas as pd
                    df = pd.DataFrame(keywords, columns=['Keyword', 'Frequency'])
                    st.bar_chart(df.set_index('Keyword'))
        
        # Tab 4: Career Coach Chatbot
        with tabs[3]:
            st.subheader("💬 AI Career Coach")
            
            # Display chat history
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            # Chat input
            user_query = st.chat_input("Ask me anything about your resume or career...")
            
            if user_query:
                # Add user message
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                
                with st.chat_message("user"):
                    st.write(user_query)
                
                # Get AI response (cached)
                with st.spinner('💭 Thinking...'):
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = chatbot_response(user_query, input_text, pdf_hash)
                
                # Add assistant message
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                with st.chat_message("assistant"):
                    st.write(response)
        
        # Tab 5: Resume Builder
        with tabs[4]:
            st.subheader("📝 Resume Builder")
            
            # Contact Information
            st.write("### Contact Information")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.resume_data['contact_info']['name'] = st.text_input(
                    "Full Name",
                    value=st.session_state.resume_data['contact_info']['name']
                )
                st.session_state.resume_data['contact_info']['email'] = st.text_input(
                    "Email",
                    value=st.session_state.resume_data['contact_info']['email']
                )
            with col2:
                st.session_state.resume_data['contact_info']['phone'] = st.text_input(
                    "Phone",
                    value=st.session_state.resume_data['contact_info']['phone']
                )
                st.session_state.resume_data['contact_info']['linkedin'] = st.text_input(
                    "LinkedIn",
                    value=st.session_state.resume_data['contact_info']['linkedin']
                )
            
            # Professional Summary
            st.write("### Professional Summary")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.session_state.resume_data['summary'] = st.text_area(
                    "Summary",
                    value=st.session_state.resume_data['summary'],
                    height=100
                )
            with col2:
                if st.button("✨ Generate Summary", key="gen_summary"):
                    with st.spinner('Generating...'):
                        suggestion = generate_resume_suggestions(input_text, 'summary')
                        st.session_state.resume_data['summary'] = suggestion
                        st.rerun()
            
            # Skills
            st.write("### Skills")
            col1, col2 = st.columns([3, 1])
            with col1:
                skills_input = st.text_area(
                    "Skills (comma-separated)",
                    value=", ".join(st.session_state.resume_data['skills']),
                    height=100
                )
                st.session_state.resume_data['skills'] = [s.strip() for s in skills_input.split(',') if s.strip()]
            with col2:
                if st.button("🎯 Suggest Skills", key="gen_skills"):
                    with st.spinner('Generating...'):
                        suggestion = generate_resume_suggestions(input_text, 'skills')
                        skills_list = [s.strip() for s in suggestion.split(',')]
                        st.session_state.resume_data['skills'] = skills_list
                        st.rerun()
            
            # Export
            st.write("---")
            if st.button("📥 Export Resume to Markdown", key="export"):
                markdown_content = export_resume_to_markdown(st.session_state.resume_data)
                st.download_button(
                    label="Download Resume",
                    data=markdown_content,
                    file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        
        # Tab 6: Project Ideas
        with tabs[5]:
            st.subheader("💡 Project Idea Generator")
            
            st.info("Generate a personalized project recommendation to strengthen your application!")
            
            if st.button("🚀 Generate Ideal Project", key="gen_project"):
                with st.spinner('🔍 Analyzing skills gap and generating project... (this may take 30-40 seconds)'):
                    pdf_hash = st.session_state.get('pdf_hash', '')
                    response = generate_ideal_project(input_text, pdf_hash)
                    
                st.markdown(f'<div class="result-card">{response}</div>', unsafe_allow_html=True)
                
                # Download option
                st.download_button(
                    label="📥 Download Project Plan",
                    data=response,
                    file_name=f"project_idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )

if __name__ == "__main__":
    main()
