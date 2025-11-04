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
st.set_page_config(page_title="AI CarrerMate", page_icon="📄", layout="wide")


# Custom CSS for better UI
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

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            color: var(--text-primary);
            background-color: #fafbfc;
        }

        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            color: var(--primary-dark);
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            line-height: 1.3;
        }

        h1 { font-size: 2rem; }
        h2 { font-size: 1.5rem; }
        h3 { font-size: 1.2rem; }

        /* Main header with improved styling */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 2.5rem;
            margin-top: 1rem;
            box-shadow: 0 6px 20px rgba(75, 121, 161, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .main-header:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(75, 121, 161, 0.2);
        }

        .main-header h1 {
            color: white;
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }

        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            font-weight: 300;
            margin: 0;
        }

        /* Section headers */
        .section-header {
            background: linear-gradient(135deg, var(--bg-light) 0%, white 100%);
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            border-left: 5px solid var(--primary-color);
            margin-top: 1.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border-bottom: 1px solid var(--border-color);
        }

        .section-header h3 {
            margin: 0;
            font-size: 1.1rem;
            color: var(--primary-dark);
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            border-bottom: 2px solid var(--border-color);
            background-color: var(--bg-light);
            border-radius: 8px 8px 0 0;
            padding: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 45px;
            background-color: transparent;
            border-radius: 6px 6px 0 0;
            font-weight: 500;
            color: var(--text-secondary);
            border: none;
            padding: 0.8rem 1.2rem;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(75, 121, 161, 0.1);
            color: var(--primary-color);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-color) 0%, rgba(75, 121, 161, 0.8) 100%) !important;
            color: white !important;
            box-shadow: 0 2px 8px rgba(75, 121, 161, 0.2);
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.65rem 1.5rem;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(75, 121, 161, 0.15);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(75, 121, 161, 0.25);
            background: linear-gradient(135deg, var(--primary-dark) 0%, #1a2332 100%);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Download button styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--success-color) 0%, #1b5e20 100%);
            box-shadow: 0 2px 8px rgba(46, 125, 50, 0.15);
        }

        .stDownloadButton > button:hover {
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
        }

        /* Text area and input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border-radius: 6px !important;
            border: 1.5px solid var(--border-color) !important;
            padding: 0.75rem 1rem !important;
            background-color: white !important;
            color: var(--text-primary) !important;
            font-family: 'Roboto', sans-serif !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 3px rgba(75, 121, 161, 0.1) !important;
        }

        .stTextInput > div > div > input::placeholder,
        .stTextArea > div > div > textarea::placeholder {
            color: #999999 !important;
        }

        /* File uploader */
        .stFileUploader > div > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.7rem 1.5rem;
            box-shadow: 0 2px 8px rgba(75, 121, 161, 0.15);
            transition: all 0.3s ease;
        }

        .stFileUploader > div > button:hover {
            box-shadow: 0 4px 12px rgba(75, 121, 161, 0.25);
        }

        /* Chat message styling */
        .stChatMessage {
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid transparent;
        }

        .stChatMessage.user {
            background-color: var(--primary-light);
            border-left-color: var(--primary-color);
            margin-left: 1rem;
        }

        .stChatMessage.assistant {
            background-color: #f0f7f4;
            border-left-color: var(--success-color);
            margin-right: 0.5rem;
        }

        /* Analysis cards */
        .analysis-card {
            background-color: white;
            padding: 1.8rem;
            border-radius: 10px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            border-top: 3px solid var(--primary-color);
            transition: all 0.3s ease;
        }

        .analysis-card:hover {
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }

        .analysis-card p {
            margin: 0.8rem 0;
            line-height: 1.6;
            color: var(--text-secondary);
        }

        /* Success indicator */
        .success-indicator {
            color: var(--success-color);
            font-weight: 600;
            background: linear-gradient(135deg, var(--success-light) 0%, rgba(232, 245, 233, 0.6) 100%);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--success-color);
            box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1);
        }

        /* Info messages */
        .stInfo, [data-baseweb="notification"] {
            padding: 1rem 1.5rem !important;
            border-radius: 8px !important;
            border-left: 4px solid var(--info-color) !important;
            background-color: var(--info-light) !important;
            color: var(--info-color) !important;
            margin-bottom: 1rem !important;
        }

        /* Warning messages */
        .stWarning {
            padding: 1rem 1.5rem !important;
            border-radius: 8px !important;
            border-left: 4px solid var(--warning-color) !important;
            background-color: var(--warning-light) !important;
        }

        /* Error messages */
        .stError {
            padding: 1rem 1.5rem !important;
            border-radius: 8px !important;
            border-left: 4px solid #d32f2f !important;
            background-color: #ffebee !important;
        }

        /* Keyword tags */
        .keyword-tag {
            background: linear-gradient(135deg, var(--primary-light) 0%, rgba(227, 242, 253, 0.6) 100%);
            color: var(--primary-color);
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            margin: 0.3rem;
            display: inline-block;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid rgba(75, 121, 161, 0.2);
            transition: all 0.2s ease;
        }

        .keyword-tag:hover {
            background: linear-gradient(135deg, var(--primary-color) 0%, rgba(75, 121, 161, 0.8) 100%);
            color: white;
            transform: scale(1.05);
            border-color: var(--primary-color);
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: var(--bg-light) !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            border: 1px solid var(--border-color) !important;
            transition: all 0.2s ease !important;
        }

        .streamlit-expanderHeader:hover {
            background-color: rgba(75, 121, 161, 0.05) !important;
            border-color: var(--primary-color) !important;
        }

        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            border-radius: 8px !important;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        [data-testid="stDataFrame"] table {
            font-size: 0.95rem;
        }

        [data-testid="stDataFrame"] th {
            background-color: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.8rem !important;
        }

        [data-testid="stDataFrame"] td {
            padding: 0.7rem 0.8rem !important;
            border-bottom: 1px solid var(--border-color) !important;
        }

        [data-testid="stDataFrame"] tbody tr:hover {
            background-color: var(--primary-light) !important;
        }

        /* Chart styling */
        [data-testid="stMetricValue"] {
            color: var(--primary-color);
            font-weight: 600;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-light);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            border-radius: 5px;
            transition: all 0.2s ease;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, var(--primary-dark) 0%, #1a2332 100%);
        }

        /* Column layout improvements */
        .stColumn {
            padding: 0 0.5rem;
        }

        /* Spinner animation improvement */
        .stSpinner > div {
            color: var(--primary-color) !important;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 2rem;
            border-top: 2px solid var(--border-color);
            color: var(--text-secondary);
            background: linear-gradient(180deg, transparent 0%, var(--bg-light) 100%);
        }

        .footer p {
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }

        /* Responsive improvements */
        @media (max-width: 768px) {
            .main-header {
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }

            .main-header h1 {
                font-size: 1.7rem;
            }

            .analysis-card {
                padding: 1.2rem;
            }

            .section-header {
                padding: 1rem;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 0.6rem 0.8rem;
                font-size: 0.9rem;
            }
        }

        /* Print styling */
        @media print {
            .main-header, .stTabs, .stButton {
                display: none;
            }

            .analysis-card {
                box-shadow: none;
                border: 1px solid var(--border-color);
            }
        }
    </style>
    """, unsafe_allow_html=True)


def get_gemini_response(input, pdf_content, prompt):
    """Generate response using Gemini model"""
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    """Convert PDF to base64 encoded image using PyMuPDF"""
    if uploaded_file is not None:
        try:
            # Read PDF bytes
            pdf_bytes = uploaded_file.read()

            # Open PDF with PyMuPDF
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            # Get first page
            first_page = pdf_document[0]

            # Render page to image (higher resolution for better quality)
            pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]

            pdf_document.close()
            return pdf_parts

        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            st.error("Please make sure the PDF file is valid and not corrupted.")
            raise
    else:
        raise FileNotFoundError("No file uploaded")


# Chatbot context prompts
CHATBOT_SYSTEM_PROMPT = """
You are an AI career coach and ATS expert assistant specializing in resume analysis. 
You have access to a resume and a job description. Your goal is to:
1. Provide insightful, constructive career advice
2. Help the user understand how well their resume matches the job description
3. Offer specific, actionable recommendations for improvement
4. Maintain a professional, supportive tone

Always base your responses on the uploaded resume and job description.
"""


def initialize_chat_history():
    """Initialize or retrieve chat history from session state"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def display_chat_history():
    """Display previous chat messages"""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_message_to_history(role, content):
    """Add a message to chat history"""
    st.session_state.chat_history.append({"role": role, "content": content})


def chatbot_response(user_query, pdf_content, job_description):
    """Generate chatbot response using Gemini"""
    full_prompt = f"""{CHATBOT_SYSTEM_PROMPT}

Job Description:
{job_description}

User's Query: {user_query}

Please provide a detailed, helpful response that addresses the user's specific question while referencing the resume and job description."""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([full_prompt, pdf_content[0]])
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"


def extract_keywords_with_gemini(pdf_content, job_description):
    """Extract keywords using Gemini AI"""
    keyword_extraction_prompt = """
    As an expert in resume analysis and keyword extraction, your task is to:
    1. Extract the most significant and relevant keywords from the resume
    2. Categorize these keywords into different professional domains
    3. Provide insights into the candidate's key skills and expertise
    4. Compare the extracted keywords with the job description

    Please provide:
    - Technical Skills
    - Soft Skills
    - Professional Certifications
    - Key Technologies
    - Industry-specific Keywords
    - Match with Job Description Keywords

    Format the output as a structured, easy-to-read analysis.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            [keyword_extraction_prompt, pdf_content[0], f"Job Description: {job_description}"])
        return response.text
    except Exception as e:
        return f"An error occurred during keyword extraction: {str(e)}"


def manual_keyword_extraction(pdf_content):
    """Perform manual keyword extraction as a fallback"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        manual_prompt = """
        Extract raw text from this resume image. 
        Return only the plain text content, removing any formatting.
        Focus on extracting words that could be skills, technologies, job titles, and qualifications.
        """

        text_response = model.generate_content([manual_prompt, pdf_content[0]])
        text_content = text_response.text

        # Preprocessing and basic keyword extraction
        words = re.findall(r'\b\w+\b', text_content.lower())

        # Remove common stop words
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]

        # Count word frequencies
        word_freq = Counter(filtered_words)

        # Get top keywords
        top_keywords = word_freq.most_common(20)

        return top_keywords
    except Exception as e:
        return f"Manual keyword extraction error: {str(e)}"


def format_keywords_as_tags(keywords):
    """Format keywords as styled tags"""
    if not isinstance(keywords, list):
        return ""

    tags_html = ""
    for kw, freq in keywords:
        tags_html += f'<span class="keyword-tag">{kw} ({freq})</span> '

    return tags_html


def generate_resume_template():
    """Generate a default resume template structure"""
    return {
        "contact": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": ""
        },
        "summary": "",
        "experience": [
            {
                "id": str(uuid.uuid4()),
                "title": "",
                "company": "",
                "location": "",
                "start_date": "",
                "end_date": "",
                "description": ""
            }
        ],
        "education": [
            {
                "id": str(uuid.uuid4()),
                "degree": "",
                "institution": "",
                "location": "",
                "graduation_date": "",
                "description": ""
            }
        ],
        "skills": [],
        "projects": [
            {
                "id": str(uuid.uuid4()),
                "title": "",
                "description": "",
                "technologies": "",
                "url": ""
            }
        ]
    }


def initialize_resume_data():
    """Initialize or retrieve resume data from session state"""
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = generate_resume_template()
    return st.session_state.resume_data


def update_resume_data(section, index, field, value):
    """Update a specific field in the resume data"""
    if section in ["experience", "education", "projects"]:
        st.session_state.resume_data[section][index][field] = value
    elif section == "skills":
        if value and value not in st.session_state.resume_data["skills"]:
            st.session_state.resume_data["skills"].append(value)
    elif section == "contact":
        st.session_state.resume_data["contact"][field] = value
    else:
        st.session_state.resume_data[section] = value


def add_new_item(section):
    """Add a new item to a list section"""
    if section == "experience":
        st.session_state.resume_data["experience"].append({
            "id": str(uuid.uuid4()),
            "title": "",
            "company": "",
            "location": "",
            "start_date": "",
            "end_date": "",
            "description": ""
        })
    elif section == "education":
        st.session_state.resume_data["education"].append({
            "id": str(uuid.uuid4()),
            "degree": "",
            "institution": "",
            "location": "",
            "graduation_date": "",
            "description": ""
        })
    elif section == "projects":
        st.session_state.resume_data["projects"].append({
            "id": str(uuid.uuid4()),
            "title": "",
            "description": "",
            "technologies": "",
            "url": ""
        })


def remove_item(section, index):
    """Remove an item from a list section"""
    if 0 <= index < len(st.session_state.resume_data[section]):
        st.session_state.resume_data[section].pop(index)


def generate_resume_suggestions(job_description, section):
    """Generate AI suggestions for resume content"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        section_prompts = {
            "summary": f"""As a professional resume writer, create a compelling professional summary for a resume targeting this job description:

            {job_description}

            Write a concise, impactful 3-4 sentence professional summary that highlights the most relevant qualifications for this role.
            Focus on key skills, experience level, and career achievements that align with the job requirements.
            """,

            "skills": f"""As a resume expert, extract a list of 10-12 key hard and soft skills that would be most relevant for this job description:

            {job_description}

            Format your response as a simple comma-separated list with no explanations or additional text.
            Include both technical/hard skills and soft skills relevant to the position.
            """,

            "experience_bullets": f"""As a professional resume writer, create 3-4 powerful bullet points for a resume work experience section targeting this job description:

            {job_description}

            Write concise, achievement-focused bullet points that demonstrate relevant skills and accomplishments.
            Use strong action verbs and include measurable results where possible.
            Each bullet should be 1-2 lines long and highlight transferable skills relevant to the job.
            Format as simple bullet points with no additional explanations.
            """
        }

        if section in section_prompts:
            response = model.generate_content(section_prompts[section])
            return response.text
        else:
            return "No suggestions available for this section."
    except Exception as e:
        return f"Could not generate suggestions: {str(e)}"


def export_resume_to_markdown():
    """Convert resume data to markdown format"""
    resume = st.session_state.resume_data

    md = f"# {resume['contact']['name']}\n\n"

    # Contact info
    contact_details = []
    if resume['contact']['email']:
        contact_details.append(f"📧 {resume['contact']['email']}")
    if resume['contact']['phone']:
        contact_details.append(f"📱 {resume['contact']['phone']}")
    if resume['contact']['location']:
        contact_details.append(f"📍 {resume['contact']['location']}")
    if resume['contact']['linkedin']:
        contact_details.append(f"💼 {resume['contact']['linkedin']}")

    md += " | ".join(contact_details) + "\n\n"

    # Summary
    if resume['summary']:
        md += "## Professional Summary\n\n"
        md += f"{resume['summary']}\n\n"

    # Experience
    if any(exp['company'] for exp in resume['experience']):
        md += "## Experience\n\n"
        for exp in resume['experience']:
            if exp['title'] or exp['company']:
                md += f"### {exp['title']} | {exp['company']}\n"
                if exp['location'] or exp['start_date'] or exp['end_date']:
                    date_range = f"{exp['start_date']} - {exp['end_date']}"
                    md += f"{exp['location']} | {date_range}\n\n"
                if exp['description']:
                    md += f"{exp['description']}\n\n"

    # Education
    if any(edu['institution'] for edu in resume['education']):
        md += "## Education\n\n"
        for edu in resume['education']:
            if edu['degree'] or edu['institution']:
                md += f"### {edu['degree']} | {edu['institution']}\n"
                if edu['location'] or edu['graduation_date']:
                    md += f"{edu['location']} | {edu['graduation_date']}\n\n"
                if edu['description']:
                    md += f"{edu['description']}\n\n"

    # Skills
    if resume['skills']:
        md += "## Skills\n\n"
        md += ", ".join(resume['skills']) + "\n\n"

    # Projects
    if any(proj['title'] for proj in resume['projects']):
        md += "## Projects\n\n"
        for proj in resume['projects']:
            if proj['title']:
                md += f"### {proj['title']}\n"
                if proj['technologies']:
                    md += f"**Technologies:** {proj['technologies']}\n\n"
                if proj['description']:
                    md += f"{proj['description']}\n\n"
                if proj['url']:
                    md += f"**Link:** {proj['url']}\n\n"

    return md


def import_resume_from_text(text_content):
    """Extract resume information from plain text"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Extract structured information from this resume text into the following JSON format:

        {{
            "contact": {{
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": ""
            }},
            "summary": "",
            "experience": [
                {{
                    "title": "",
                    "company": "",
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "description": ""
                }}
            ],
            "education": [
                {{
                    "degree": "",
                    "institution": "",
                    "location": "",
                    "graduation_date": "",
                    "description": ""
                }}
            ],
            "skills": [],
            "projects": [
                {{
                    "title": "",
                    "description": "",
                    "technologies": "",
                    "url": ""
                }}
            ]
        }}

        Here is the resume text:
        {text_content}

        Respond with ONLY the JSON object, no explanations or other text.
        """

        response = model.generate_content(prompt)
        parsed_data = json.loads(response.text)

        # Add UUIDs to list items
        for section in ["experience", "education", "projects"]:
            for item in parsed_data.get(section, []):
                item["id"] = str(uuid.uuid4())

        return parsed_data
    except Exception as e:
        st.error(f"Error parsing resume: {str(e)}")
        return generate_resume_template()


def generate_ideal_project(pdf_content, job_description):
    """Generate an ideal project idea based on resume and job description"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        project_prompt = f"""
        As a senior technical mentor and career advisor, analyze the provided resume and job description to generate a comprehensive, 
        ideal project that would significantly strengthen the candidate's application.

        Job Description:
        {job_description}

        Based on the candidate's current skills and the job requirements, create a detailed project proposal that:
        1. Bridges skill gaps between the resume and job requirements
        2. Demonstrates proficiency in key technologies mentioned in the job description
        3. Shows real-world problem-solving abilities
        4. Is realistic and achievable within 2-4 weeks
        5. Would be impressive to hiring managers for this role

        Provide the following structure:

        ## Project Title
        [Creative, professional title]

        ## Project Overview
        [2-3 sentences describing what the project does and its purpose]

        ## Key Objectives
        - [Objective 1]
        - [Objective 2]
        - [Objective 3]

        ## Technical Stack
        [List all technologies, frameworks, and tools to be used]

        ## Core Features
        1. [Feature 1 with brief description]
        2. [Feature 2 with brief description]
        3. [Feature 3 with brief description]
        4. [Feature 4 with brief description]

        ## Implementation Steps
        ### Phase 1: [Phase Name]
        - [Step 1]
        - [Step 2]

        ### Phase 2: [Phase Name]
        - [Step 1]
        - [Step 2]

        ### Phase 3: [Phase Name]
        - [Step 1]
        - [Step 2]

        ## Skills Demonstrated
        - [Skill 1]: [How it's demonstrated]
        - [Skill 2]: [How it's demonstrated]
        - [Skill 3]: [How it's demonstrated]

        ## Expected Outcomes
        [What the candidate will learn and achieve]

        ## Bonus Enhancements (Optional)
        - [Enhancement 1]
        - [Enhancement 2]

        ## How to Showcase
        [Tips on presenting this project in resume, GitHub, and interviews]

        Make this comprehensive, actionable, and specifically tailored to help the candidate stand out for THIS specific job.
        """

        response = model.generate_content([project_prompt, pdf_content[0]])
        return response.text
    except Exception as e:
        return f"An error occurred while generating project idea: {str(e)}"


def main():
    # Load custom CSS
    load_css()

    # Main header with gradient background
    st.markdown(
        '<div class="main-header"><h1>✨ AI CarrerMate ✨</h1><p>Comprehensive Resume Analysis & Career Guidance</p></div>',
        unsafe_allow_html=True)

    # Two-column layout for inputs
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header"><h3>📝 Job Description</h3></div>', unsafe_allow_html=True)
        input_text = st.text_area("Enter the job description you're applying for:", key="job_description", height=200)

    with col2:
        st.markdown('<div class="section-header"><h3>📄 Your Resume</h3></div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF format):", type=["pdf"])

    # PDF processing
    pdf_content = None
    if uploaded_file is not None:
        st.markdown('<div class="success-indicator">✅ PDF Uploaded Successfully</div>', unsafe_allow_html=True)
        try:
            pdf_content = input_pdf_setup(uploaded_file)
        except Exception as e:
            st.error("Failed to process PDF. Please try again with a different file.")

    # Create stylized tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Resume Review",
        "📊 Match Analysis",
        "🔑 Keyword Extraction",
        "💬 Career Coach",
        "📝 Resume Builder",
        "💡 Project Ideas"
    ])

    with tab1:
        if pdf_content and input_text:
            st.markdown('<div class="section-header"><h3>📋 Detailed Resume Review</h3></div>', unsafe_allow_html=True)

            with st.spinner("Analyzing your resume against the job description..."):
                input_prompt1 = """
                You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
                Please share your professional evaluation on whether the candidate's profile aligns with the role.
                Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
                Format your response with clear sections for Strengths, Areas for Improvement, and Overall Assessment.
                """
                response = get_gemini_response(input_prompt1, pdf_content, input_text)

                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Please upload a resume and provide a job description to get a detailed review.")

    with tab2:
        if pdf_content and input_text:
            st.markdown('<div class="section-header"><h3>🎯 Resume-Job Match Analysis</h3></div>',
                        unsafe_allow_html=True)

            with st.spinner("Calculating match percentage..."):
                input_prompt3 = """
                You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality,
                your task is to evaluate the resume against the provided job description. 
                Give me the percentage of match if the resume matches the job description. 
                Format your response with:
                1. A clear percentage match at the beginning
                2. Missing keywords or skills section
                3. Final recommendations for improving the match

                Make your response visually structured with clear headings for each section.
                """
                response = get_gemini_response(input_prompt3, pdf_content, input_text)

                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.write(response)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Please upload a resume and provide a job description to see how well they match.")

    with tab3:
        if pdf_content and input_text:
            st.markdown('<div class="section-header"><h3>🔑 Keyword Analysis</h3></div>', unsafe_allow_html=True)

            with st.spinner("Extracting and analyzing keywords..."):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("### AI-Powered Keyword Analysis")
                    ai_keywords = extract_keywords_with_gemini(pdf_content, input_text)

                    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                    st.write(ai_keywords)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown("### Top Keywords by Frequency")
                    manual_keywords = manual_keyword_extraction(pdf_content)

                    if isinstance(manual_keywords, list):
                        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                        keyword_df = st.dataframe({
                            'Keyword': [kw[0] for kw in manual_keywords],
                            'Frequency': [kw[1] for kw in manual_keywords]
                        })

                        tags_html = format_keywords_as_tags(manual_keywords)
                        st.markdown(f"<div class='keyword-tags'>{tags_html}</div>", unsafe_allow_html=True)

                        chart_data = {
                            'keywords': [kw[0] for kw in manual_keywords[:10]],
                            'frequency': [kw[1] for kw in manual_keywords[:10]]
                        }
                        st.bar_chart(data=chart_data, x='keywords', y='frequency')
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Could not generate keyword chart")
        else:
            st.info("Please upload a resume and provide a job description to extract keywords.")

    with tab4:
        if pdf_content and input_text:
            st.markdown('<div class="section-header"><h3>💬 AI CarrerMate Chatbot</h3></div>',
                        unsafe_allow_html=True)
            st.markdown("Ask me anything about your resume, job application, or how to improve your chances!")

            initialize_chat_history()
            display_chat_history()

            user_query = st.chat_input("Type your question here...")

            if user_query:
                with st.chat_message("user"):
                    st.markdown(user_query)
                add_message_to_history("user", user_query)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = chatbot_response(user_query, pdf_content, input_text)
                        st.markdown(response)
                add_message_to_history("assistant", response)
        else:
            st.info("Please upload a resume and provide a job description to chat with the AI assistant.")

    with tab5:
        st.markdown('<div class="section-header"><h3>📝 Resume Builder & Editor</h3></div>', unsafe_allow_html=True)

        resume_data = initialize_resume_data()
        
        import_col1, import_col2, import_col3 = st.columns([1, 1, 1])

        with import_col1:
            if st.button("📄 Start New Resume"):
                st.session_state.resume_data = generate_resume_template()
                st.rerun()

        with import_col2:
            import_file = st.file_uploader("Import Resume (TXT)", type=["txt"], key="resume_import")
            if import_file is not None:
                text_content = import_file.read().decode("utf-8")
                st.session_state.resume_data = import_resume_from_text(text_content)
                st.success("Resume imported successfully!")
                st.rerun()

        with import_col3:
            if st.button("💾 Export Resume"):
                markdown_resume = export_resume_to_markdown()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = resume_data["contact"]["name"].replace(" ", "_") or "my_resume"
                filename = f"{name}_{timestamp}.md"

                st.download_button(
                    label="Download as Markdown",
                    data=markdown_resume,
                    file_name=filename,
                    mime="text/markdown"
                )

        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)

        builder_tab1, builder_tab2, builder_tab3, builder_tab4, builder_tab5 = st.tabs([
            "Contact", "Summary", "Experience", "Education", "Skills & Projects"
        ])

        with builder_tab1:
            st.subheader("Contact Information")
            contact_col1, contact_col2 = st.columns(2)

            with contact_col1:
                name = st.text_input("Full Name", resume_data["contact"]["name"])
                update_resume_data("contact", 0, "name", name)

                email = st.text_input("Email", resume_data["contact"]["email"])
                update_resume_data("contact", 0, "email", email)

                linkedin = st.text_input("LinkedIn URL", resume_data["contact"]["linkedin"])
                update_resume_data("contact", 0, "linkedin", linkedin)

            with contact_col2:
                phone = st.text_input("Phone Number", resume_data["contact"]["phone"])
                update_resume_data("contact", 0, "phone", phone)

                location = st.text_input("Location (City, State)", resume_data["contact"]["location"])
                update_resume_data("contact", 0, "location", location)

        with builder_tab2:
            st.subheader("Professional Summary")

            summary = st.text_area("Summary", resume_data["summary"], height=150)
            update_resume_data("summary", 0, "", summary)

            if input_text:
                if st.button("Get AI Suggestions for Summary"):
                    with st.spinner("Generating suggestions..."):
                        suggestions = generate_resume_suggestions(input_text, "summary")
                        st.markdown("### AI Suggestions")
                        st.write(suggestions)
                        if st.button("Use this suggestion"):
                            update_resume_data("summary", 0, "", suggestions)
                            st.rerun()

        with builder_tab3:
            st.subheader("Professional Experience")

            for i, exp in enumerate(resume_data["experience"]):
                with st.expander(f"Experience: {exp['title'] or exp['company'] or f'Position {i + 1}'}",
                                 expanded=i == 0):
                    exp_col1, exp_col2 = st.columns([3, 1])

                    with exp_col1:
                        title = st.text_input("Job Title", exp["title"], key=f"exp_title_{i}")
                        update_resume_data("experience", i, "title", title)

                        company = st.text_input("Company", exp["company"], key=f"exp_company_{i}")
                        update_resume_data("experience", i, "company", company)

                    with exp_col2:
                        location = st.text_input("Location", exp["location"], key=f"exp_location_{i}")
                        update_resume_data("experience", i, "location", location)

                    exp_date_col1, exp_date_col2 = st.columns(2)

                    with exp_date_col1:
                        start_date = st.text_input("Start Date", exp["start_date"], key=f"exp_start_{i}")
                        update_resume_data("experience", i, "start_date", start_date)

                    with exp_date_col2:
                        end_date = st.text_input("End Date", exp["end_date"], key=f"exp_end_{i}")
                        update_resume_data("experience", i, "end_date", end_date)

                    description = st.text_area("Description", exp["description"], height=150, key=f"exp_desc_{i}")
                    update_resume_data("experience", i, "description", description)

                    if input_text:
                        if st.button("Get AI Suggestions for Bullet Points", key=f"exp_suggest_{i}"):
                            with st.spinner("Generating suggestions..."):
                                suggestions = generate_resume_suggestions(input_text, "experience_bullets")
                                st.markdown("### AI Suggestions")
                                st.write(suggestions)
                                if st.button("Use these suggestions", key=f"exp_use_{i}"):
                                    update_resume_data("experience", i, "description", suggestions)
                                    st.rerun()

                    if len(resume_data["experience"]) > 1:
                        if st.button("Remove this position", key=f"remove_exp_{i}"):
                            remove_item("experience", i)
                            st.rerun()

            if st.button("+ Add Another Position"):
                add_new_item("experience")
                st.rerun()

        with builder_tab4:
            st.subheader("Education")

            for i, edu in enumerate(resume_data["education"]):
                with st.expander(f"Education: {edu['degree'] or edu['institution'] or f'Degree {i + 1}'}",
                                 expanded=i == 0):
                    edu_col1, edu_col2 = st.columns([3, 1])

                    with edu_col1:
                        degree = st.text_input("Degree/Certification", edu["degree"], key=f"edu_degree_{i}")
                        update_resume_data("education", i, "degree", degree)

                        institution = st.text_input("Institution", edu["institution"], key=f"edu_inst_{i}")
                        update_resume_data("education", i, "institution", institution)

                    with edu_col2:
                        location = st.text_input("Location", edu["location"], key=f"edu_location_{i}")
                        update_resume_data("education", i, "location", location)

                        grad_date = st.text_input("Graduation Date", edu["graduation_date"], key=f"edu_grad_{i}")
                        update_resume_data("education", i, "graduation_date", grad_date)

                    description = st.text_area("Description", edu["description"], height=100, key=f"edu_desc_{i}")
                    update_resume_data("education", i, "description", description)

                    if len(resume_data["education"]) > 1:
                        if st.button("Remove this education", key=f"remove_edu_{i}"):
                            remove_item("education", i)
                            st.rerun()

            if st.button("+ Add Another Education"):
                add_new_item("education")
                st.rerun()

        with builder_tab5:
            skills_col, projects_col = st.columns(2)

            with skills_col:
                st.subheader("Skills")

                skills_html = ""
                for i, skill in enumerate(resume_data["skills"]):
                    skills_html += f'<span class="keyword-tag" style="margin-right: 8px; margin-bottom: 8px;">{skill}</span>'

                st.markdown(f'<div style="margin-bottom: 15px;">{skills_html}</div>', unsafe_allow_html=True)

                new_skill = st.text_input("Add Skill", "")
                if new_skill:
                    if st.button("Add"):
                        update_resume_data("skills", 0, "", new_skill)
                        st.rerun()

                if input_text:
                    if st.button("Get AI Skill Suggestions"):
                        with st.spinner("Generating skill suggestions..."):
                            suggestions = generate_resume_suggestions(input_text, "skills")
                            st.markdown("### Suggested Skills")

                            suggested_skills = [s.strip() for s in suggestions.split(",")]
                            for skill in suggested_skills:
                                if skill and skill not in resume_data["skills"]:
                                    st.write(f"• {skill}")

                            if st.button("Add All Suggested Skills"):
                                for skill in suggested_skills:
                                    if skill and skill not in resume_data["skills"]:
                                        update_resume_data("skills", 0, "", skill)
                                st.rerun()

            with projects_col:
                st.subheader("Projects")

                for i, project in enumerate(resume_data["projects"]):
                    with st.expander(f"Project: {project['title'] or f'Project {i + 1}'}", expanded=i == 0):
                        title = st.text_input("Project Title", project["title"], key=f"proj_title_{i}")
                        update_resume_data("projects", i, "title", title)

                        tech = st.text_input("Technologies Used", project["technologies"], key=f"proj_tech_{i}")
                        update_resume_data("projects", i, "technologies", tech)

                        description = st.text_area("Description", project["description"], height=100,
                                                   key=f"proj_desc_{i}")
                        update_resume_data("projects", i, "description", description)

                        url = st.text_input("Project URL", project["url"], key=f"proj_url_{i}")
                        update_resume_data("projects", i, "url", url)

                        if len(resume_data["projects"]) > 1:
                            if st.button("Remove this project", key=f"remove_proj_{i}"):
                                remove_item("projects", i)
                                st.rerun()

                if st.button("+ Add Another Project"):
                    add_new_item("projects")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("📄 Resume Preview", expanded=False):
            markdown_resume = export_resume_to_markdown()
            st.markdown(markdown_resume)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = resume_data["contact"]["name"].replace(" ", "_") or "my_resume"
            filename = f"{name}_{timestamp}.md"

            st.download_button(
                label="Download Resume",
                data=markdown_resume,
                file_name=filename,
                mime="text/markdown"
            )

    with tab6:
        # Project Ideas Generator
        if pdf_content and input_text:
            st.markdown('<div class="section-header"><h3>💡 Ideal Project Generator</h3></div>', unsafe_allow_html=True)
            st.markdown("""
            Get a personalized project idea that will strengthen your application for this specific job. 
            This AI-generated project will help you:
            - Bridge skill gaps
            - Demonstrate relevant expertise
            - Stand out from other candidates
            """)

            if st.button("🚀 Generate Ideal Project", use_container_width=True):
                with st.spinner(
                        "Analyzing your resume and generating the perfect project idea... This may take a moment."):
                    project_idea = generate_ideal_project(pdf_content, input_text)

                    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                    st.markdown(project_idea)
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Add download button for the project
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    project_filename = f"project_idea_{timestamp}.md"

                    st.download_button(
                        label="📥 Download Project Plan",
                        data=project_idea,
                        file_name=project_filename,
                        mime="text/markdown",
                        use_container_width=True
                    )

                    st.success(
                        "✅ Project idea generated! Review the comprehensive plan above and start building to boost your chances!")
        else:
            st.info("Please upload a resume and provide a job description to generate a personalized project idea.")

    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:40px; padding:20px; border-top:1px solid #eee; color:#666;">
        <p>AI CarrerMate - Powered by Gemini AI</p>
        <p style="font-size:0.8rem;">Helping you optimize your resume for Applicant Tracking Systems</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()