"""
VERA Comply - SB 1288 AI Policy Compliance Platform
Verification Engine for Results & Accountability

SB 1288 requires California LEAs to adopt AI policies covering:
A - Academic integrity and plagiarism
B - Acceptable and unacceptable uses of AI
C - Data privacy and security
D - Parent/guardian access to pupil information
E - Procurement of AI software
F - Human oversight and effective use
"""

import streamlit as st
from datetime import datetime, date
import json

# ============================================================
# CONFIGURATION
# ============================================================
APP_PASSWORD = "vera2026"
PRIMARY_COLOR = "#1B4D89"  # California blue
ACCENT_COLOR = "#C4A000"   # Gold accent

# ============================================================
# SB 1288 MODEL POLICY LANGUAGE
# ============================================================
SB_1288_SECTIONS = {
    "A": {
        "title": "Academic Integrity & Plagiarism",
        "description": "Policies governing academic integrity in the context of AI tools",
        "model_language": """
The District recognizes that artificial intelligence tools present both opportunities and challenges
for academic integrity. Students shall be expected to:

1. Disclose the use of AI tools in completing assignments when required by the instructor
2. Not submit AI-generated content as their own original work unless expressly permitted
3. Understand that using AI to complete assessments without authorization constitutes academic dishonesty
4. Learn to use AI tools as learning aids rather than substitutes for critical thinking

Educators shall clearly communicate expectations regarding AI use for each assignment and
establish consistent consequences for violations of academic integrity standards.
""",
        "questions": [
            "Does your district currently have an academic integrity policy?",
            "Does your existing policy address AI-generated content?",
            "Have you established clear disclosure requirements for AI use?"
        ]
    },
    "B": {
        "title": "Acceptable & Unacceptable Uses",
        "description": "Guidelines for appropriate AI use by pupils and educators",
        "model_language": """
ACCEPTABLE USES of AI tools include:
- Research assistance and information gathering
- Writing feedback and grammar checking
- Differentiated instruction and personalized learning
- Administrative efficiency (scheduling, communications)
- Accessibility accommodations for students with disabilities

UNACCEPTABLE USES of AI tools include:
- Submitting AI-generated work as original without disclosure
- Using AI to complete standardized assessments
- Inputting personally identifiable student information into non-approved AI systems
- Using AI to make disciplinary or placement decisions without human review
- Circumventing content filters or safety controls
""",
        "questions": [
            "Have you identified specific AI tools approved for classroom use?",
            "Do educators have guidance on integrating AI into instruction?",
            "Are there clear boundaries for student AI use across grade levels?"
        ]
    },
    "C": {
        "title": "Data Privacy & Security",
        "description": "Protection of pupil and educator data in AI systems",
        "model_language": """
The District shall ensure that all AI tools used in educational settings comply with:
- Family Educational Rights and Privacy Act (FERPA)
- California Consumer Privacy Act (CCPA)
- Student Online Personal Information Protection Act (SOPIPA)
- Children's Online Privacy Protection Act (COPPA) where applicable

Prior to deploying any AI tool that processes student data, the District shall:
1. Conduct a privacy impact assessment
2. Execute a Data Privacy Agreement with the vendor
3. Verify the tool's compliance with applicable state and federal law
4. Ensure student data is not used to train AI models without consent
5. Establish data retention and deletion protocols
""",
        "questions": [
            "Do you have a Data Privacy Agreement template for AI vendors?",
            "Have you conducted privacy assessments for current AI tools?",
            "Is there a process for reviewing new AI tool requests?"
        ]
    },
    "D": {
        "title": "Parent & Guardian Access",
        "description": "Transparency and access rights for parents regarding AI use",
        "model_language": """
Parents and guardians shall have the right to:
1. Be informed of AI tools used in their child's education
2. Access information their child has entered into AI systems
3. Request that their child opt out of non-essential AI tool use
4. Receive plain-language explanations of how AI tools affect their child's learning
5. Review any AI-generated assessments or recommendations about their child

The District shall provide annual notification to parents regarding AI tools in use,
including the purpose of each tool and the data collected.
""",
        "questions": [
            "Do you have a parent notification process for AI tool adoption?",
            "Can parents access their child's AI interaction history?",
            "Is there an opt-out process for non-essential AI tools?"
        ]
    },
    "E": {
        "title": "Procurement & Vendor Management",
        "description": "Standards for purchasing AI software safely",
        "model_language": """
Prior to procuring any AI-enabled software, the District shall:
1. Verify vendor compliance with California student data privacy laws
2. Review the vendor's AI ethics and bias mitigation practices
3. Ensure the contract includes data ownership and deletion provisions
4. Confirm the tool has been evaluated for age-appropriateness
5. Document the educational purpose and expected outcomes
6. Establish a review cycle for continued use (minimum annual)

The District shall maintain a registry of all approved AI tools including vendor name,
purpose, data accessed, privacy certifications, and renewal dates.
""",
        "questions": [
            "Do you have a formal AI tool vetting process?",
            "Is there a centralized registry of approved AI tools?",
            "Are contracts reviewed for data privacy provisions?"
        ]
    },
    "F": {
        "title": "Human Oversight & Effective Use",
        "description": "Ensuring human review of AI outputs affecting students",
        "model_language": """
The District shall ensure that:
1. No AI-generated recommendation affecting student placement, discipline, or
   services shall be implemented without review by a qualified educator or administrator
2. Educators receive professional development on effective AI integration
3. AI tools are used to support, not replace, professional judgment
4. Regular evaluation occurs to assess AI tool effectiveness and equity impact
5. Clear escalation procedures exist for AI-related concerns

Human oversight is mandatory before any AI output influences:
- Special education eligibility or services
- Student discipline decisions
- Grade-level placement or advancement
- Intervention or support service assignments
""",
        "questions": [
            "Is human review required before AI affects student decisions?",
            "Do educators receive AI professional development?",
            "Is there a process to evaluate AI tool effectiveness?"
        ]
    }
}

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_section' not in st.session_state:
        st.session_state.current_section = None
    if 'district_info' not in st.session_state:
        st.session_state.district_info = {}
    if 'section_responses' not in st.session_state:
        st.session_state.section_responses = {key: {} for key in SB_1288_SECTIONS.keys()}
    if 'section_complete' not in st.session_state:
        st.session_state.section_complete = {key: False for key in SB_1288_SECTIONS.keys()}
    if 'custom_language' not in st.session_state:
        st.session_state.custom_language = {key: "" for key in SB_1288_SECTIONS.keys()}

# ============================================================
# AUTHENTICATION
# ============================================================
def show_login():
    st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <h1 style="color: {PRIMARY_COLOR};">VERA Comply</h1>
            <h3 style="color: #666;">SB 1288 AI Policy Compliance Platform</h3>
            <p style="color: #888;">Verification Engine for Results & Accountability</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter access code:", type="password", key="login_password")
        if st.button("Access Platform", use_container_width=True):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code")

# ============================================================
# DISTRICT INFORMATION
# ============================================================
def show_district_info():
    st.markdown(f"""
        <h2 style="color: {PRIMARY_COLOR};">District Information</h2>
        <p>Please provide your district information to begin the SB 1288 compliance process.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        district_name = st.text_input(
            "District Name",
            value=st.session_state.district_info.get('name', ''),
            key="district_name"
        )
        county = st.selectbox(
            "County",
            options=[""] + [
                "Alameda", "Alpine", "Amador", "Butte", "Calaveras", "Colusa",
                "Contra Costa", "Del Norte", "El Dorado", "Fresno", "Glenn",
                "Humboldt", "Imperial", "Inyo", "Kern", "Kings", "Lake", "Lassen",
                "Los Angeles", "Madera", "Marin", "Mariposa", "Mendocino", "Merced",
                "Modoc", "Mono", "Monterey", "Napa", "Nevada", "Orange", "Placer",
                "Plumas", "Riverside", "Sacramento", "San Benito", "San Bernardino",
                "San Diego", "San Francisco", "San Joaquin", "San Luis Obispo",
                "San Mateo", "Santa Barbara", "Santa Clara", "Santa Cruz", "Shasta",
                "Sierra", "Siskiyou", "Solano", "Sonoma", "Stanislaus", "Sutter",
                "Tehama", "Trinity", "Tulare", "Tuolumne", "Ventura", "Yolo", "Yuba"
            ],
            index=0 if not st.session_state.district_info.get('county') else None,
            key="county"
        )

    with col2:
        enrollment = st.number_input(
            "Student Enrollment",
            min_value=0,
            value=st.session_state.district_info.get('enrollment', 0),
            key="enrollment"
        )
        contact_name = st.text_input(
            "Primary Contact Name",
            value=st.session_state.district_info.get('contact_name', ''),
            key="contact_name"
        )

    contact_email = st.text_input(
        "Contact Email",
        value=st.session_state.district_info.get('contact_email', ''),
        key="contact_email"
    )

    if st.button("Save District Information", type="primary"):
        st.session_state.district_info = {
            'name': district_name,
            'county': county,
            'enrollment': enrollment,
            'contact_name': contact_name,
            'contact_email': contact_email
        }
        st.success("District information saved")
        st.rerun()

# ============================================================
# SECTION WORKFLOW
# ============================================================
def show_section(section_key):
    section = SB_1288_SECTIONS[section_key]

    st.markdown(f"""
        <h2 style="color: {PRIMARY_COLOR};">Section {section_key}: {section['title']}</h2>
        <p style="color: #666;">{section['description']}</p>
    """, unsafe_allow_html=True)

    # Model language
    st.markdown("### Model Policy Language (CSBA)")
    st.info(section['model_language'])

    # Assessment questions
    st.markdown("### Current Status Assessment")
    responses = st.session_state.section_responses[section_key]

    for i, question in enumerate(section['questions']):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(question)
        with col2:
            response = st.selectbox(
                f"Response {i+1}",
                options=["Not addressed", "Partially addressed", "Fully addressed"],
                index=["Not addressed", "Partially addressed", "Fully addressed"].index(
                    responses.get(f"q{i}", "Not addressed")
                ),
                key=f"section_{section_key}_q{i}",
                label_visibility="collapsed"
            )
            responses[f"q{i}"] = response

    st.session_state.section_responses[section_key] = responses

    # Custom language
    st.markdown("### District-Specific Language")
    st.write("Customize the model language for your district (optional):")
    custom = st.text_area(
        "Custom policy language",
        value=st.session_state.custom_language.get(section_key, ""),
        height=150,
        key=f"custom_{section_key}",
        label_visibility="collapsed"
    )
    st.session_state.custom_language[section_key] = custom

    # Navigation
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if section_key != "A":
            prev_key = chr(ord(section_key) - 1)
            if st.button(f"< Section {prev_key}"):
                st.session_state.current_section = prev_key
                st.rerun()

    with col2:
        if st.button("Mark Complete", type="primary"):
            st.session_state.section_complete[section_key] = True
            st.success(f"Section {section_key} marked complete")
            # Auto-advance to next section
            if section_key != "F":
                next_key = chr(ord(section_key) + 1)
                st.session_state.current_section = next_key
                st.rerun()

    with col3:
        if section_key != "F":
            next_key = chr(ord(section_key) + 1)
            if st.button(f"Section {next_key} >"):
                st.session_state.current_section = next_key
                st.rerun()

# ============================================================
# DASHBOARD
# ============================================================
def show_dashboard():
    st.markdown(f"""
        <h2 style="color: {PRIMARY_COLOR};">SB 1288 Compliance Dashboard</h2>
    """, unsafe_allow_html=True)

    # District info summary
    if st.session_state.district_info.get('name'):
        st.markdown(f"""
            **District:** {st.session_state.district_info.get('name', 'Not set')}
            **County:** {st.session_state.district_info.get('county', 'Not set')}
            **Enrollment:** {st.session_state.district_info.get('enrollment', 0):,}
        """)

    st.divider()

    # Progress overview
    completed = sum(1 for v in st.session_state.section_complete.values() if v)
    total = len(SB_1288_SECTIONS)

    st.markdown(f"### Compliance Progress: {completed}/{total} Sections Complete")
    st.progress(completed / total)

    # Section cards
    st.markdown("### Policy Sections")

    cols = st.columns(3)
    for i, (key, section) in enumerate(SB_1288_SECTIONS.items()):
        with cols[i % 3]:
            status = "Complete" if st.session_state.section_complete[key] else "Incomplete"
            status_color = "#28a745" if status == "Complete" else "#dc3545"

            st.markdown(f"""
                <div style="border: 2px solid {PRIMARY_COLOR}; border-radius: 8px; padding: 15px; margin: 10px 0; min-height: 150px;">
                    <h4 style="color: {PRIMARY_COLOR}; margin: 0;">Section {key}</h4>
                    <p style="font-weight: bold; margin: 5px 0;">{section['title']}</p>
                    <p style="color: {status_color}; font-size: 0.9em;">{status}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"Edit Section {key}", key=f"edit_{key}"):
                st.session_state.current_section = key
                st.rerun()

    # Generate policy document
    if completed == total:
        st.divider()
        st.markdown("### Generate Board-Ready Policy Document")
        st.success("All sections complete. You may now generate your AI policy document.")

        if st.button("Generate AI Policy Document", type="primary"):
            generate_policy_document()

# ============================================================
# POLICY DOCUMENT GENERATION
# ============================================================
def generate_policy_document():
    district = st.session_state.district_info

    doc_content = f"""
================================================================================
                         ARTIFICIAL INTELLIGENCE POLICY
                    SB 1288 Compliant - Board Ready Document
================================================================================

DISTRICT: {district.get('name', '[District Name]')}
COUNTY: {district.get('county', '[County]')}
DATE: {date.today().strftime('%B %d, %Y')}
PREPARED BY: VERA Comply - H-EDU.Solutions

================================================================================
SECTION A: ACADEMIC INTEGRITY AND PLAGIARISM
================================================================================
{st.session_state.custom_language.get('A') or SB_1288_SECTIONS['A']['model_language']}

================================================================================
SECTION B: ACCEPTABLE AND UNACCEPTABLE USES OF AI
================================================================================
{st.session_state.custom_language.get('B') or SB_1288_SECTIONS['B']['model_language']}

================================================================================
SECTION C: DATA PRIVACY AND SECURITY
================================================================================
{st.session_state.custom_language.get('C') or SB_1288_SECTIONS['C']['model_language']}

================================================================================
SECTION D: PARENT AND GUARDIAN ACCESS
================================================================================
{st.session_state.custom_language.get('D') or SB_1288_SECTIONS['D']['model_language']}

================================================================================
SECTION E: PROCUREMENT OF AI SOFTWARE
================================================================================
{st.session_state.custom_language.get('E') or SB_1288_SECTIONS['E']['model_language']}

================================================================================
SECTION F: HUMAN OVERSIGHT AND EFFECTIVE USE
================================================================================
{st.session_state.custom_language.get('F') or SB_1288_SECTIONS['F']['model_language']}

================================================================================
CERTIFICATION
================================================================================

This policy has been developed in compliance with California Senate Bill 1288
and the model policy guidance issued by the California Department of Education
AI in Education Working Group.

Prepared using VERA Comply by H-EDU.Solutions
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

================================================================================
"""

    st.markdown("### Generated Policy Document")
    st.text_area("Policy Document", value=doc_content, height=500)

    # Download button
    st.download_button(
        label="Download Policy Document",
        data=doc_content,
        file_name=f"AI_Policy_{district.get('name', 'District').replace(' ', '_')}_{date.today().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# ============================================================
# MAIN APP
# ============================================================
def main():
    st.set_page_config(
        page_title="VERA Comply - SB 1288 Compliance",
        page_icon="D",
        layout="wide"
    )

    # Custom CSS
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: #f8f9fa;
            }}
            .stButton > button {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
            .stButton > button:hover {{
                background-color: #153d6d;
                color: white;
            }}
        </style>
    """, unsafe_allow_html=True)

    init_session_state()

    if not st.session_state.authenticated:
        show_login()
        return

    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <h2 style="color: {PRIMARY_COLOR};">VERA Comply</h2>
                <p style="color: #666;">SB 1288 Compliance</p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        if st.button("Dashboard", use_container_width=True):
            st.session_state.current_section = None
            st.rerun()

        if st.button("District Info", use_container_width=True):
            st.session_state.current_section = "info"
            st.rerun()

        st.divider()
        st.markdown("**Policy Sections**")

        for key, section in SB_1288_SECTIONS.items():
            status = "+" if st.session_state.section_complete[key] else " "
            if st.button(f"[{status}] {key}: {section['title'][:20]}...", use_container_width=True, key=f"nav_{key}"):
                st.session_state.current_section = key
                st.rerun()

        st.divider()
        st.markdown(f"""
            <div style="text-align: center; font-size: 0.8em; color: #888;">
                VERA Comply v1.0<br>
                H-EDU.Solutions<br>
                {date.today().strftime('%Y')}
            </div>
        """, unsafe_allow_html=True)

    # Main content
    if st.session_state.current_section is None:
        show_dashboard()
    elif st.session_state.current_section == "info":
        show_district_info()
    elif st.session_state.current_section in SB_1288_SECTIONS:
        show_section(st.session_state.current_section)

if __name__ == "__main__":
    main()
