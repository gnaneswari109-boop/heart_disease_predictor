import streamlit as st
import pandas as pd
import joblib
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
import random
from datetime import datetime
from datetime import datetime, timedelta
# Normal/reference ranges
# ------------------------
normal_ranges = {
    "totChol": "125-200 mg/dL",
    "sysBP": "90-120 mm Hg",
    "diaBP": "60-80 mm Hg",
    "glucose": "70-100 mg/dL",
    "BMI": "18.5-24.9"
}
# ------------------- Initialize Session State -------------------
if "percent" not in st.session_state:
    st.session_state.percent = None
if "appt_confirmed" not in st.session_state:
    st.session_state.appt_confirmed = False
if "appt_details" not in st.session_state:
    st.session_state.appt_details = ""

    
primaryColor="#df7448"
backgroundColor="#bfd8d2"
secondaryBackgroundColor="#dcb239"
textColor="#fedcd2"

import streamlit as st

# --- Pastel Theme CSS ---
st.markdown("""
    <style>
    /* Main page background */
    [data-testid="stAppViewContainer"] {
        background-color: #bfd8d2;  /* backgroundColor */
        color: #fedcd2;             /* textColor */
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #dcb239;  /* secondaryBackgroundColor */
        color: #fedcd2;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #df7448;  /* primaryColor */
        color: #fedcd2;
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #e36e35;
        color: white;
    }

    /* Cards / Containers */
    .card {
        background-color: #dcb239;  /* secondaryBackgroundColor */
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
        color: #333333;
    }

    /* Titles */
    h1, h2, h3 {
        color: #df7448;  /* primaryColor */
    }

    /* Inputs */
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #df7448;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Main app background */
    .css-18e3th9 {  /* Streamlit main content area */
        background-color: #FAFAFA;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
    background-color: #dcb239;
    color: #8B0000;   /* dark red text in sidebar */
    }


    /* Card styling */
    .card {
        background-color: #E3F2FD;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #F8BBD0;
        color: #333333;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 8px 16px;
    }
    div.stButton > button:first-child:hover {
        background-color: #F48FB1;
        color: white;
    }

    /* Titles & headers */
    h1, h2, h3, h4, h5 {
    color: #8B0000;  /* dark red headers */
    font-weight: 600;
    }


    /* Inputs */
    .stTextInput, .stNumberInput, .stSelectbox {
        background-color:#DCB239;
        border-radius: 10px;
        border: 1px solid #B2EBF2;
    }
    </style>
""", unsafe_allow_html=True)




# Load your trained model (adjust path if needed)
model = joblib.load("models/logreg_heart_model.joblib")

st.set_page_config(page_title="️ Heart Disease Predictor", layout="centered")

# CSS Styling
st.markdown(
    """
    <style>
    /* Full page background image */
    body {
        background-image: url("https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=1471&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow-x: hidden;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* White semi-transparent overlay container */
    .overlay-container {
        background: rgba(255, 255, 255, 0.85);
        max-width: 600px;
        margin: 4rem auto;
        padding: 2.5rem 3rem;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
    section.main {
    background-color: rgba(255,255,255,0.85);
    margin: 3rem auto;
    max-width: 600px;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

    /* Heart emoji styling */
    .heart-symbol {
        font-size: 6rem;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #b22222;
    }

    /* Title styling */
    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        color: #8b0000;
    }

    /* Prediction result box styling */
    .result {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
        color: #8b0000;
        margin-top: 2rem;
        padding: 1.2rem 1.8rem;
        border-radius: 12px;
        background: #ffe5e5;
        box-shadow: 0 4px 16px rgba(139, 0, 0, 0.4);
    }

    /* Label styling */
    label {
        font-weight: 600;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True
)
import streamlit as st
import base64

# Load and encode GIF
file_ = open("heart.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")

# Create two columns: left for GIF, right for text
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/gif;base64,{data_url}" width="500"
                 style="border-radius:70%; box-shadow:0 4px 12px rgba(0,0,0,0.3);" />
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("""
    <h1 style="
        text-align:center;
        font-size:50px;
        font-family: 'Great Vibes', cursive;
        background: linear-gradient(90deg, #b22222, #ff6699);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;">
        HEART DISEASE PREDICTOR
    </h1>
    """, unsafe_allow_html=True)

# 📝 Add welcome message and description
st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #e91e63; line-height: 1.7; margin-bottom: 2rem;">
    <b>Welcome to the HEART DISEASE RISK PREDICTOR !</b><br><br>
    This tool uses health-related data to estimate your <b>2-year risk</b> of developing heart disease.<br><br>
    Fill in your details below and click <b>"Predict Risk"</b> to get started.
</div>
""", unsafe_allow_html=True)


# 🔺 Add headline or subtitle above the heart
st.markdown("""
<div style='text-align:center; font-size: 1.2rem; font-weight: 500; color: #444; margin-bottom: 0.5rem;'>
    💡 Powered by Machine Learning | Framingham Risk Model
</div>
""", unsafe_allow_html=True)
# Inputs with emojis
warm_red = "#8B0000"

age = st.number_input("👶 Age", min_value=1, max_value=100, value=50)
male = st.selectbox("👨‍⚕️ Gender", options=[("Male", 1), ("Female", 0)], index=0, format_func=lambda x: x[0])[1]
cigsPerDay = st.number_input("🚬 Cigarettes Per Day", min_value=0, max_value=100, value=0)
totChol = st.number_input("🩸 Total Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
# Main question
BPMeds = st.selectbox(
    "💊 Are you taking blood pressure medication?", 
    options=[("No", 0), ("Yes", 1)],
    index=0,
    format_func=lambda x: x[0]
)[1]

# Sub-questions with indentation
if BPMeds == 1:
    st.markdown('<div style="margin-left: 30px;color:{warm_red};">**Please provide your current blood pressure levels:**</div>', unsafe_allow_html=True)
    sysBP = st.number_input("💓 Systolic Blood Pressure (mm Hg)", min_value=80, max_value=250, value=120, key="sysBP")
    diaBP = st.number_input("🩺 Diastolic Blood Pressure (mm Hg)", min_value=50, max_value=150, value=80, key="diaBP")
else:
    sysBP = None
    diaBP = None

# Main question
diabetes = st.selectbox(
    "🧬 Do you have diabetes?", 
    options=[("No", 0), ("Yes", 1)],
    index=0,
    format_func=lambda x: x[0]
)[1]

# Sub-questions with indentation
if diabetes == 1:
    st.markdown('<div style="margin-left: 30px;color:{warm_red};">**Please enter your current blood glucose level:**</div>', unsafe_allow_html=True)
    glucose = st.number_input("🍬 Blood Glucose (mg/dL)", min_value=50, max_value=300, value=85, key="glucose")
else:
    glucose = None



prevalentStroke = st.selectbox("🧠 History of Stroke?", options=[("No", 0), ("Yes", 1)], index=0, format_func=lambda x: x[0])[1]
heartRate = st.number_input("❤️ Heart Rate (beats per minute)", min_value=40, max_value=200, value=70)
BMI = st.number_input("⚖️ BMI (Body Mass Index)", min_value=10.0, max_value=60.0, value=22.0, step=0.1) 





# Prediction button & output
if st.button("🔍 Predict Risk"):
    input_df = pd.DataFrame({
        "age": [age],
        "male": [male],
        "cigsPerDay": [cigsPerDay],
        "totChol": [totChol],
        "sysBP": [sysBP],
        "diaBP": [diaBP],
        "glucose": [glucose],
        "BPMeds": [BPMeds],
        "diabetes": [diabetes],
        "prevalentStroke": [prevalentStroke],
        "heartRate": [heartRate],
        #"BMI": [BMI],   

    })

# Get prediction probability (probability of class = 1)
    proba = model.predict_proba(input_df)[0][1]

# Convert to percentage
    percent = round(proba * 100, 2)
    st.session_state.percent = percent

# Add interpretation based on risk percent
    if percent < 30:
        risk_level = '<p style="color:green; font-size:30px; font-weight:bold;">✅ Low Risk – You\'re likely safe for now.</p>'
    elif percent < 70:
        risk_level = '<p style="color:orange; font-size:30px; font-weight:bold;">⚠️ Moderate Risk – Consider monitoring your health.</p>'
    else:
        risk_level = '<p style="color:red; font-size:30px; font-weight:bold;">🚨 High Risk – Please consult a doctor.</p>'
# Show result with styling
    st.markdown(f"""
    <div class="result">
        ❤️ Your estimated 2-year heart disease risk is: <strong>{percent}%</strong><br><br>
        {risk_level}
    </div>
""", unsafe_allow_html=True)
     # ----------------- Interpretation -----------------
    if percent < 30:
        risk_text = "✅ Low Risk – Maintain a healthy heart"
        diet_plan = [
            "Eat fruits and vegetables daily",
            "Exercise for 30 minutes regularly",
            "Drink plenty of water",
            "Avoid processed foods",
            "Regular BP and cholesterol checks"
        ]
    elif percent < 70:
        risk_text = "⚠️ Moderate Risk – Improve your lifestyle"
        diet_plan = [
            "Reduce salt, sugar, and oil intake",
            "Eat oats, whole grains, and lentils",
            "Exercise 5 times per week",
            "Limit caffeine and alcohol",
            "Track BP and glucose regularly"
        ]
    else:
        risk_text = "🚨 High Risk – Consult a doctor immediately"
        diet_plan = [
            "Consult a cardiologist",
            "Follow a low-fat, low-salt diet",
            "Avoid smoking and alcohol",
            "Practice meditation",
            "Monitor heart rate daily"
        ]

       # ----------------- Show Diet Plan -----------------

    diet_html = f"""
    <div style='background-color:#f0f0f0; padding:20px; border-radius:15px; margin-top:20px;'>
    <h4 style='text-align:center; color:#C2185B;'>🥗 Personalized Diet Plan</h4>
    <ul style='color:#000000; font-size:16px;'>
    """
    for item in diet_plan:
        diet_html += f"<li style='margin:5px 0;'>{item}</li>"
    diet_html += "</ul></div>"

    st.markdown(diet_html, unsafe_allow_html=True)


    # --- Link prediction to diet recommendation ---
    if percent < 30:
        diet_type = "Balanced Diet"
        diet_data = {"Protein": 16.5, "Fats": 14.2, "Carbs": 55.0, "Fiber": 4.8}
        diet_percent = {"Protein": 70, "Fats": 65, "Carbs": 80, "Fiber": 60}
        gauge_color = "#00cc66"   # green
    elif 30 <= percent < 60:
        diet_type = "Heart-Healthy Diet"
        diet_data = {"Protein": 18.0, "Fats": 10.5, "Carbs": 50.0, "Fiber": 6.0}
        diet_percent = {"Protein": 75, "Fats": 55, "Carbs": 70, "Fiber": 70}
        gauge_color = "#ffaa00"   # yellow/orange
    else:
        diet_type = "Low-Fat, Low-Sugar Diet"
        diet_data = {"Protein": 20.0, "Fats": 8.0, "Carbs": 45.0, "Fiber": 7.0}
        diet_percent = {"Protein": 85, "Fats": 40, "Carbs": 60, "Fiber": 80}
        gauge_color = "#ff3333"   # red

    # --- Display diet plan based on risk ---
    st.markdown("---")
    st.markdown(f'<h2 style="color:#DF744A;">{diet_type}</h2>', unsafe_allow_html=True)


    import plotly.graph_objects as go

    fig = go.Figure()

    for i, nutrient in enumerate(diet_data.keys()):
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=diet_percent[nutrient],
            number={'suffix': "%", 'font': {'color': "#ffffff"}},
            title={'text': nutrient + f"<br>{diet_data[nutrient]} g", 'font': {'color': "#00c3ff"}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "#999"},
                'bar': {'color': gauge_color},
                'bgcolor': "#222222",
                'borderwidth': 2,
                'bordercolor': "#444444"
            },
            domain={'x': [i*0.25, (i+1)*0.25], 'y': [0, 1]}
        ))

    fig.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
        margin=dict(l=20, r=20, t=50, b=20),
        height=280,
        paper_bgcolor="#111111",
        plot_bgcolor="#111111"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Calorie bar chart (linked with risk level) ---
    import pandas as pd

    if percent < 30:
        calories = [2200, 2300, 2100, 2250, 2150, 2200, 2100]
    elif 30 <= percent < 60:
        calories = [2000, 1900, 1950, 2050, 2000, 2100, 1900]
    else:
        calories = [1800, 1750, 1850, 1900, 1800, 1700, 1750]

    days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
    df = pd.DataFrame({'Day': days, 'Calories': calories})
    df.set_index('Day', inplace=True)

    st.markdown('<h3 style="color:#DF744A;">🔥 Weekly Calorie Intake Recommendation</h3>', unsafe_allow_html=True)

    st.bar_chart(df)




    # ----------------- PDF Generation -----------------
    def generate_diet_pdf(percent, diet_plan, risk_text, appt_details=None):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from io import BytesIO

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 80, "Heart Health Risk Report")

        # Risk section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 130, f"Predicted Risk: {percent}%")
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 160, risk_text)

        # Diet Plan section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 200, "🥗 Personalized Diet Plan:")
        y = height - 230
        c.setFont("Helvetica", 12)
        for item in diet_plan:
            c.drawString(70, y, f"• {item}")
            y -= 20

        # Appointment section (if available)
        if appt_details:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y - 20, "🩺 Doctor Appointment:")
            y -= 50
            c.setFont("Helvetica", 12)
            for line in appt_details.split("\n"):
                c.drawString(70, y, line)
                y -= 20

        c.showPage()
        c.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
        user_data = {
        "totChol": totChol,
        "sysBP": sysBP if sysBP is not None else "N/A",
        "diaBP": diaBP if diaBP is not None else "N/A",
        "glucose": glucose if glucose is not None else "N/A",
        "BMI": bmi
    }


    pdf_data = generate_diet_pdf(percent, diet_plan, risk_text, appt_details=st.session_state.appt_details if st.session_state.appt_confirmed else None)
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Heart_Report.pdf"><button style="padding:10px 25px; border:none; border-radius:10px; background-color:#C2185B; color:white; font-size:16px; cursor:pointer;">📥 Download Heart Report as PDF</button></a>'
    st.markdown(href, unsafe_allow_html=True)




   # ------------------ Doctor Appointment ------------------
doctors = [
    {"name":"Dr. Arjun Sharma","hospital":"Apollo Heart Centre","location":"Delhi"},
    {"name":"Dr. Meera Iyer","hospital":"Fortis Hospital","location":"Bangalore"},
    {"name":"Dr. Rohan Gupta","hospital":"AIIMS","location":"New Delhi"},
    {"name":"Dr. Kavita Rao","hospital":"Medanta","location":"Gurugram"},
    {"name":"Dr. Vivek Nair","hospital":"Narayana Health","location":"Bangalore"}
]

if st.session_state.percent is not None:
    st.markdown("---")
    st.markdown('<h1 style="color:#DF744A;">🩺 Book / Auto-assign a Doctor Appointment</h1>', unsafe_allow_html=True)

    if not st.session_state.appt_confirmed:
        if st.button("✅ Auto-assign & Confirm Appointment", key="appt_btn"):
            selected = random.choice(doctors)
            days = random.randint(1,7)
            appt_dt = datetime.now() + timedelta(days=days)
            hour = random.randint(9,17)
            minute = random.choice([0,15,30,45])
            appt_dt = appt_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)

            st.session_state.appt_details = (
                f"Your appointment has been fixed with **{selected['name']}** on "
                f"**{appt_dt.strftime('%d-%m-%Y')} at {appt_dt.strftime('%I:%M %p')}**.\n"
                f"📍 Hospital: {selected['hospital']} — {selected['location']}"
            )
            
            st.markdown(f'<span style="color:#006400;">{st.session_state.appt_details}</span>', unsafe_allow_html=True)
        

    if st.session_state.appt_confirmed:
        st.success(st.session_state.appt_details)


        



