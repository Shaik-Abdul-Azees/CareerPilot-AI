

import streamlit as st

import fitz

from datetime import date

from urllib.parse import urlparse



from src.analysis.resume_analyzer import (
    analyze_resume,
    analyze_ats_compatibility,
)

from src.matching.job_matcher import match_job

from src.ai.recommendations import generate_recommendations

from src.database.job_tracker import (

    add_application,

    get_applications,

    update_application_status,

    delete_application,

)
# =========================================================# PAGE CONFIGURATION AND DARK THEME# =========================================================
st.set_page_config(

    page_title="CareerPilot AI",

    page_icon="🚀",

    layout="wide",

    initial_sidebar_state="expanded",

)



st.markdown(
    """
    <style>
    :root { color-scheme: dark; }

    .stApp {
        background: radial-gradient(ellipse at top left, rgba(99, 102, 241, 0.13), transparent 38%), #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stHeader"] { background: rgba(11, 16, 32, 0.92); }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111a30 0%, #0b1222 100%);
        border-right: 1px solid #253452;
    }

    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] h1 { color: #a5b4fc !important; }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 { color: #f8fafc !important; letter-spacing: -0.025em; }
    p, label, [data-testid="stMarkdownContainer"] { color: #cbd5e1; }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #17233c, #10182a);
        border: 1px solid #2b3c5c;
        padding: 20px 22px;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover { transform: translateY(-3px); border-color: #818cf8; }
    [data-testid="stMetricLabel"] { color: #a8b7d0; }
    [data-testid="stMetricValue"] { color: #f8fafc; }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #2a3853;
        border-radius: 15px;
    }

    div[data-testid="stExpander"] {
        background: #11192b;
        border: 1px solid #293751;
        border-radius: 12px;
    }

    .stTextInput input, .stTextArea textarea {
        background: #11192b;
        color: #f8fafc;
        border: 1px solid #34435f;
        border-radius: 9px;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: #11192b;
        border-color: #34435f;
        border-radius: 9px;
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 2.6rem;
        transition: all 0.15s ease;
    }

    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border: 1px solid #818cf8;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        border-color: #a5b4fc;
        color: white;
    }

    [data-testid="stFileUploader"] {
        background: #11192b;
        border: 1px dashed #53658b;
        border-radius: 12px;
        padding: 10px;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #22d3ee);
    }

    [data-testid="stAlert"] { border-radius: 10px; }
    hr { border-color: #26334c; }

    .hero-card {
        position: relative;
        overflow: hidden;
        padding: 30px;
        border-radius: 18px;
        background: linear-gradient(120deg, #172554, #312e81 65%, #164e63);
        border: 1px solid #454b91;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
    }

    .hero-title {
        position: relative;
        z-index: 1;
        color: #ffffff;
        font-size: 2rem;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        position: relative;
        z-index: 1;
        color: #dbeafe;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .eyebrow {
        color: #c7d2fe;
        text-transform: uppercase;
        font-size: 0.76rem;
        letter-spacing: 0.12em;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .section-note { color: #94a3b8; font-size: 0.9rem; }

    @media (max-width: 768px) {
        .block-container { padding: 1rem; }
        .hero-title { font-size: 1.55rem; }
        .hero-card { padding: 22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

STATUS_OPTIONS = [

    "Interested",

    "Applied",

    "Assessment",

    "Interview",

    "Offer",

    "Rejected",

    "Withdrawn",

]
# =========================================================# SESSION STATE# =========================================================
defaults = {

    "job_match": None,

    "job_description_saved": "",

    "resume_text_saved": "",

    "ai_recommendations": None,

    "uploaded_resume_id": None,

    "resume_analysis_results": None,

    "confirm_delete_id": None,

}



for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

if "main_navigation" not in st.session_state:
    st.session_state["main_navigation"] = "Dashboard"

if "pending_navigation" in st.session_state:
    st.session_state["main_navigation"] = (
        st.session_state.pop("pending_navigation")
    )

with st.sidebar:
    st.markdown("# 🚀 CareerPilot AI")
    st.caption("Your AI-powered career workspace")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Resume & AI",
            "Applications",
        ],
        key="main_navigation",
    )

    st.divider()
    st.markdown("### Your toolkit")
    st.caption("📄 Resume intelligence")
    st.caption("🎯 Job matching")
    st.caption("🧠 AI career recommendations")
    st.caption("📋 Application tracking")

    st.divider()
    st.caption("Powered by Streamlit · Python · Ollama")

    
# =========================================================# HEADER# =========================================================
st.markdown(
    """
    <div style="background: linear-gradient(120deg, #172554, #312e81, #164e63); border: 1px solid #454b91; border-radius: 18px; padding: 30px; margin-bottom: 24px; box-shadow: 0 12px 32px rgba(0,0,0,0.18);">
      <div style="color: #c7d2fe; font-size: 12px; letter-spacing: 2px; font-weight: 700; margin-bottom: 12px;">CAREER INTELLIGENCE PLATFORM</div>
      <h1 style="color: #ffffff !important; font-size: 34px; line-height: 1.2; margin: 0 0 12px 0;">Your next opportunity starts here.</h1>
      <p style="color: #dbeafe !important; font-size: 16px; line-height: 1.6; margin: 0;">Analyze your resume, discover skill gaps, get AI guidance, and manage every job application in one workspace.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================# LOAD APPLICATIONS# =========================================================
try:

    applications = get_applications() or []

except Exception as error:

    st.error(f"Could not load applications: {error}")

    applications = []
# =========================================================# DASHBOARD# =========================================================
if page == "Dashboard":

    st.title("📊 Dashboard")

    st.caption("An overview of your job search progress.")



    total = len(applications)



    applied = sum(

        1 for app in applications

        if app["status"] == "Applied"

    )



    interviews = sum(

        1 for app in applications

        if app["status"] == "Interview"

    )



    offers = sum(

        1 for app in applications

        if app["status"] == "Offer"

    )



    col1, col2, col3, col4 = st.columns(4)



    col1.metric("Total Applications", total)

    col2.metric("Applied", applied)

    col3.metric("Interviews", interviews)

    col4.metric("Offers", offers)



    st.divider()



    chart_col, recent_col = st.columns([1.15, 1])



    with chart_col:

        st.subheader("Application Status")



        status_counts = {}

        for app in applications:

            current = app["status"]

            status_counts[current] = status_counts.get(current, 0) + 1



        if status_counts:

            st.bar_chart(status_counts)

        else:

            st.info(

                "Your chart will appear after you add job applications."

            )



    with recent_col:

        st.subheader("Recent Applications")



        recent = sorted(

            applications,

            key=lambda app: (

                app.get("application_date") or ""

            ),

            reverse=True,

        )[:5]



        if recent:

            for app in recent:

                with st.container(border=True):

                    st.markdown(f"**{app['job_title']}**")

                    st.caption(app["company"])

                    st.caption(

                        f"{app['application_date']} · {app['status']}"

                    )

        else:

            st.info(

                "No applications yet. Open Applications to add your first one."

            )



    st.divider()

    st.subheader("Quick Actions")



    action1, action2 = st.columns(2)



    with action1:

        st.markdown("**📄 Resume & AI**")

        st.write("Upload a resume and discover how it matches a job.")

        if st.button("Open Resume & AI", use_container_width=True):
            st.session_state["pending_navigation"] = "Resume & AI"
            st.rerun()



    with action2:

        st.markdown("**📋 Applications**")

        st.write("Save jobs, search your tracker, and update statuses.")

        if st.button("Open Applications", use_container_width=True):
           st.session_state["pending_navigation"] = "Applications"
           st.rerun()
# =========================================================# RESUME ANALYSIS AND AI# =========================================================
elif page == "Resume & AI":

    st.title("📄 Resume Intelligence")

    st.caption(

        "Upload your resume, analyze your skills, and match a job description."

    )



    
MAX_RESUME_SIZE_MB = 5

uploaded_file = st.file_uploader(
    "Upload your resume (PDF, maximum 5 MB)",
    type=["pdf"],
    key="resume_uploader",
)

if uploaded_file is not None:
    if uploaded_file.size > MAX_RESUME_SIZE_MB * 1024 * 1024:
        st.error(
            "The uploaded file is too large. "
            "Please upload a PDF smaller than 5 MB."
        )
        uploaded_file = None




    if uploaded_file is None:

        st.info("Upload a text-based PDF to begin.")

    
    else:

        try:
            # Reject files larger than 5 MB before PDF processing.
            MAX_RESUME_SIZE_MB = 5
            pdf_bytes = uploaded_file.getvalue()

            if len(pdf_bytes) > MAX_RESUME_SIZE_MB * 1024 * 1024:
                st.error(
                    "The uploaded PDF is too large. "
                    "Please upload a file smaller than 5 MB."
                )
            else:
                resume_id = (
                    uploaded_file.name,
                    len(pdf_bytes),
                    hash(pdf_bytes),
                )

                if st.session_state["uploaded_resume_id"] != resume_id:
                    st.session_state["uploaded_resume_id"] = resume_id
                    st.session_state["job_match"] = None
                    st.session_state["job_description_saved"] = ""
                    st.session_state["resume_text_saved"] = ""
                    st.session_state["ai_recommendations"] = None
                    st.session_state["resume_analysis_results"] = None
                    st.session_state["ats_compatibility_results"] = None

                # Extract text from the uploaded PDF.
                with fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf",
                ) as document:
                    extracted_text = "\n\n".join(
                        page.get_text("text").strip()
                        for page in document
                        if page.get_text("text").strip()
                    )

                if not extracted_text.strip():
                    st.warning(
                        "No readable text found. "
                        "This may be a scanned PDF."
                    )
                else:
                    results = analyze_resume(extracted_text)
                    ats_result = analyze_ats_compatibility(extracted_text)

                    st.session_state["resume_analysis_results"] = results
                    st.session_state["ats_compatibility_results"] = ats_result

                    with st.expander("View extracted resume text"):
                        st.text_area(
                            "Extracted resume text",
                            value=extracted_text,
                            height=220,
                            key="resume_text_preview",
                        )

                    total_skills = sum(
                        len(skills)
                        for skills in results["skills"].values()
                    )

                    # Keep your existing metrics, ATS display,
                    # detected skills, education, experience,
                    # and job-matching UI below this point.



        except Exception as error:

            st.error(f"Job matching failed: {error}")



            match = st.session_state["job_match"]



            if (

                    match is not None

                    and st.session_state["resume_text_saved"]

                    == extracted_text

                ):

                    st.subheader("Your Skill Match")



                    score = max(

                        0,

                        min(100, int(match["match_score"])),

                    )



                    st.metric("Detected Skill Overlap", f"{score}%")

                    st.progress(score / 100)



                    st.caption(

                        "This is a detected skill-overlap score, not a hiring "

                        "probability or a complete assessment of experience."

                    )



                    m1, m2 = st.columns(2)



                    with m1:

                        st.markdown("**✅ Matching Skills**")

                        if match["matched_skills"]:

                            for skill in match["matched_skills"]:

                                st.write(f"• {skill}")

                        else:

                            st.info("No matching skills detected.")



                    with m2:

                        st.markdown("**📌 Skills to Develop**")

                        if match["missing_skills"]:

                            for skill in match["missing_skills"]:

                                st.write(f"• {skill}")

                        else:

                            st.success(

                                "No missing skills were detected by this matcher."

                            )



                    if not match["required_skills"]:

                        st.warning(

                            "No supported technical skills were detected "

                            "in this job description."

                        )



                    st.divider()

                    st.subheader("🧠 AI Career Recommendations")



                    if st.button("Generate AI Recommendations"):

                        with st.spinner(

                            "Qwen2.5 is preparing recommendations. "

                            "This may take a few minutes."

                        ):

                            try:

                                recommendations = generate_recommendations(

                                    resume_text=(

                                        st.session_state["resume_text_saved"]

                                    ),

                                    job_description=(

                                        st.session_state["job_description_saved"]

                                    ),

                                    matched_skills=match["matched_skills"],

                                    missing_skills=match["missing_skills"],

                                )



                                st.session_state["ai_recommendations"] = (

                                    recommendations

                                )



                            except Exception as error:

                                st.error(

                                    f"AI recommendation error: {error}"

                                )



                    if st.session_state["ai_recommendations"]:

                        st.markdown("### Your AI Recommendations")

                        st.markdown(

                            st.session_state["ai_recommendations"]

                        )



        except Exception as error:
            st.error(f"Resume analysis error: {error}")
# =========================================================# APPLICATION TRACKER# =========================================================
elif page == "Applications":

    st.title("📋 Application Tracker")

    st.caption(

        "Organize your opportunities and keep your job search moving."

    )
# ADD APPLICATION
    with st.expander("➕ Add a New Application", expanded=False):

        with st.form("add_job_application_form"):

            company = st.text_input("Company name")

            job_title = st.text_input("Job title")

            job_url = st.text_input("Job posting URL (optional)")

            application_date = st.date_input(

                "Application date",

                value=date.today(),

            )

            status = st.selectbox(

                "Application status",

                STATUS_OPTIONS,

                index=1,

            )

            notes = st.text_area("Notes (optional)")



            submitted = st.form_submit_button(

                "Save Application",

                type="primary",

            )



            if submitted:

                if not company.strip() or not job_title.strip():

                    st.error(

                        "Please enter both company name and job title."

                    )

                elif job_url.strip() and (

                    urlparse(job_url.strip()).scheme not in ("http", "https")

                    or not urlparse(job_url.strip()).netloc

                ):

                    st.error(

                        "Enter a valid job URL starting with http:// or https://."

                    )

                else:

                    try:

                        add_application(

                            company=company.strip(),

                            job_title=job_title.strip(),

                            job_url=job_url.strip(),

                            application_date=application_date.isoformat(),

                            status=status,

                            notes=notes.strip(),

                        )

                        st.success("Application saved successfully!")

                        st.rerun()

                    except Exception as error:

                        st.error(f"Could not save application: {error}")
# RELOAD AFTER ADD/UPDATE/DELETE
    try:

        applications = get_applications() or []

    except Exception as error:

        st.error(f"Could not refresh applications: {error}")

        applications = []



    st.divider()

    st.subheader("Find Applications")



    search_query = st.text_input(

        "Search by company or job title",

        placeholder="Type a company or job title...",

        key="application_search",

    )



    filter_status = st.selectbox(

        "Filter by status",

        ["All"] + STATUS_OPTIONS,

        key="application_status_filter",

    )



    query = search_query.strip().casefold()



    filtered_applications = [

        app for app in applications

        if (

            query in app["company"].casefold()

            or query in app["job_title"].casefold()

        )

        and (

            filter_status == "All"

            or app["status"] == filter_status

        )

    ]



    st.caption(

        f"Showing {len(filtered_applications)} of "

        f"{len(applications)} application(s)."

    )



    if not filtered_applications:

        st.info("No applications match your search or filter.")



    else:

        for application in filtered_applications:

            app_id = application["id"]



            with st.expander(

                f"{application['company']} — "

                f"{application['job_title']} · "

                f"{application['status']}"

            ):

                st.write(

                    f"**Application date:** "

                    f"{application['application_date']}"

                )



                if application.get("job_url"):

                    st.markdown(

                        f"[Open job posting]({application['job_url']})"

                    )



                if application.get("notes"):

                    st.write(f"**Notes:** {application['notes']}")



                with st.form(f"update_status_form_{app_id}"):

                    current_status = application["status"]

                    selected_index = (

                        STATUS_OPTIONS.index(current_status)

                        if current_status in STATUS_OPTIONS

                        else 1

                    )



                    new_status = st.selectbox(

                        "Update status",

                        STATUS_OPTIONS,

                        index=selected_index,

                    )



                    update_clicked = st.form_submit_button(

                        "Update Status"

                    )



                    if update_clicked:

                        try:

                            update_application_status(

                                app_id,

                                new_status,

                            )

                            st.success("Application status updated!")

                            st.rerun()

                        except Exception as error:

                            st.error(

                                f"Could not update status: {error}"

                            )
# DELETE WITH CONFIRMATION
                if st.session_state["confirm_delete_id"] != app_id:

                    if st.button(

                        "Delete Application",

                        key=f"delete_{app_id}",

                    ):

                        st.session_state["confirm_delete_id"] = app_id

                        st.rerun()



                else:

                    st.warning(

                        "Are you sure you want to delete this application?"

                    )



                    yes_col, no_col = st.columns(2)



                    with yes_col:

                        if st.button(

                            "Yes, delete",

                            key=f"confirm_yes_{app_id}",

                            type="primary",

                        ):

                            try:

                                delete_application(app_id)

                                st.session_state["confirm_delete_id"] = None

                                st.success("Application deleted.")

                                st.rerun()

                            except Exception as error:

                                st.error(

                                    f"Could not delete application: {error}"

                                )



                    with no_col:

                        if st.button(

                            "Cancel",

                            key=f"confirm_no_{app_id}",

                        ):

                            st.session_state["confirm_delete_id"] = None

                            st.rerun()
# =========================================================# FOOTER# =========================================================
st.divider()

st.caption(

    "CareerPilot AI · Built with Python, Streamlit, SQLite, "

    "and Ollama. AI-generated recommendations should be reviewed "

    "before making career decisions."

)
