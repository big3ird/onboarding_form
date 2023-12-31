import streamlit as st
from passlib.context import CryptContext
import requests
import json


st.markdown("""
<style>
    .question-text {
        color: #a364ff;
        font-size: 20px;
    }
    .question-text-head {
        color: #a364ff;
        font-size: 28px;
    }
    .css-1d391kg {
        background-color: #2196F3;
        color: white;
    }
    .input-field {
        width: 100%;
        padding: 5px;
        font-size: 16px;
    }
    .stTextInput > div {
        margin-top: -30px;
    }
    .stTextArea > div {
        margin-top: -30px;
    }
    .stSelectbox > div {
    margin-top: -30px;
    }
    .stNumberInput > div {
    margin-top: -30px;
    }
    .stDateInput > div {
    margin-top: -30px;
    }
</style>
""", unsafe_allow_html=True)


# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Store your hashed password here (you should hash it beforehand and not include it in plaintext).
SINGLE_PASSWORD_HASH = '$2b$12$FdTpWwKiKodVjGqCFDcXteZ8P/rhlKTKNwzKL1Rn4ugW8PXqbf/xu'

# Check the password against the hash
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

# Login form
def show_login_form():
    """Displays the login form."""
    st.markdown("### 🔒 Login Required")
    st.markdown("Please enter the password sent to your email 📧 :")

    with st.form("login_form"):
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button(label="Login")
        if submit_button:
            if verify_password(password, SINGLE_PASSWORD_HASH):
                st.session_state["authenticated"] = True
                st.experimental_rerun()
            else:
                st.error("The password is incorrect")

# Check if authenticated in session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Show login form if not authenticated
if not st.session_state["authenticated"]:
    show_login_form()
else:

# Title of the form
    st.title("Byteshift AI client integration")

# Form for collecting information
    with st.form(key='ai_automation_form'):
    # Question 1: Client name
        st.markdown('<p class="question-text">1. Who is the team member we will be working with?</p>', unsafe_allow_html=True)
        client_name = st.text_input("enter text", placeholder="First Name",label_visibility='hidden')
        client_email = st.text_input("enter text", placeholder="Email Address",label_visibility='hidden')
        company_name = st.text_input("enter text", placeholder="Name of your company", label_visibility='hidden')
    
    # Question 2: Project description
        st.markdown('<p class="question-text">2. From our previous meetings, please briefly outline your expectations of the service/outcome we are delivering:</p>', unsafe_allow_html=True)
        project_description = st.text_area("enter text", placeholder="e.g., 80% of our customer service staff's time is saved from engaging with capturing client information")

    # Question 3: AI exposure
        st.markdown('<p class="question-text">3. Do you have any experience with AI ?:</p>', unsafe_allow_html=True)
        ai_experience = st.text_area("enter text", placeholder="if yes, please breifly tell us, good or bad.",label_visibility='hidden')
    
    # Question 4: Industry type
        st.markdown('<p class="question-text">4. Please select your industry:</p>', unsafe_allow_html=True)
        industry_type = st.selectbox("enter text", options=["Technology", "Healthcare", "Finance", "Ecommerce", "Law", "Trade Services", "Other"], index=0)

    #Question 5: outline deadlines 
        st.markdown('<p class="question-text">5. Please confirm the final deadline for this project based on our previous meetings:</p>', unsafe_allow_html=True)
        deadline = st.date_input("")

    ##Question 6: other important notes
        st.markdown('<p class="question-text">6. If there is any other information you would like us to know, please enter here:</p>', unsafe_allow_html=True)
        notes = st.text_area("enter text", placeholder= "Questions, requests etc",label_visibility='hidden')
    
    ##break in form - for Website chatbots only
        st.divider()
        st.header("Please answer if we are deploying an AI assistant to your website")

    # Question 7.: chatbot hosting
        st.markdown('<p class="question-text-head">7. Where is your website located ? (wordpress, shopify etc).</p>',unsafe_allow_html=True)
        st.markdown('<p class="question-text"> We ask our clients to add us as admins into their website or hosting platforms so that we can integrate our solutions on your behalf. We will contact the person nominated above in regards to access (leave blank if not applicable)</p>', unsafe_allow_html=True)
        website_host = st.text_area("enter text",label_visibility='hidden')


    
    # Submit button
        submit_button = st.form_submit_button(label="Submit")

# This container will be used to display the confirmation message and emoji
    confirmation_container = st.empty()

# When the submit button is pressed
    if submit_button:
    # Convert the date to string in ISO format
        deadline_str = deadline.isoformat() if deadline is not None else None

    # Collect responses in a dictionary
        response_data = {
        "client_name": client_name,
        "client_email": client_email,
        "company_name": company_name,
        "project_description": project_description,
        "ai_experience": ai_experience,
        "industry_type": industry_type,
        "deadline": deadline_str,
        "notes": notes,
        "website_host": website_host
        }

     # Convert the responses to a JSON object
        response_json = json.dumps(response_data, default=str)  # The default=str argument will help to handle any other non-serializable objects

    # Send a POST request to the webhook
        webhook_url = "https://hook.us1.make.com/tdbbib93dc91rscw6tj51493i5vg4pg3"
        response = requests.post(webhook_url, json=response_data)
    
    # Check if the request was successful
        if response.status_code == 200:
            confirmation_container.success("Form submitted successfully! ✅ you may now close this page")
        else:
            confirmation_container.error("Failed to submit the form. Please try again. ❌")