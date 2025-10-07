import streamlit as st
import pandas as pd
import joblib
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import base64



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

import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# ----- check file -----
file_name = "heartbeat.mp3"
if not os.path.exists(file_name):
    st.error(f"Audio file not found: {file_name}. Put heartbeat.mp3 in the same folder as app.py")
else:
    # encode audio to base64
    data_b64 = base64.b64encode(open(file_name, "rb").read()).decode("utf-8")

    # HTML + JS (just a big heart emoji, no circle)
    html = f"""
    <div style="text-align:center; margin:20px;">
        <button id="toggleBtn" style="
            background:transparent; border:none; cursor:pointer;
            font-size:80px; line-height:1;">
            ❤️
        </button>
    </div>

    <audio id="hb" loop>
      <source src="data:audio/mp3;base64,{data_b64}" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>

    <script>
      const audio = document.getElementById('hb');
      const btn = document.getElementById('toggleBtn');
      let playing = false;

      btn.addEventListener('click', () => {{
        if (!playing) {{
          audio.volume = 0.4;
          audio.play();
          btn.style.transform = "scale(1.2)";
          playing = true;
        }} else {{
          audio.pause();
          audio.currentTime = 0;
          btn.style.transform = "scale(1)";
          playing = false;
        }}
      }});
    </script>
    """

    components.html(html, height=150)

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
age = st.number_input("👶 Age", min_value=1, max_value=100, value=50)
male = st.selectbox("👨‍⚕️ Gender", options=[("Male", 1), ("Female", 0)], index=0, format_func=lambda x: x[0])[1]
cigsPerDay = st.number_input("🚬 Cigarettes Per Day", min_value=0, max_value=100, value=0)
totChol = st.number_input("🩸 Total Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
sysBP = st.number_input("💓 Systolic Blood Pressure (mm Hg)", min_value=80, max_value=250, value=120)
diaBP = st.number_input("🩺 Diastolic Blood Pressure (mm Hg)", min_value=50, max_value=150, value=80)
glucose = st.number_input("🍬 Glucose (mg/dL)", min_value=50, max_value=300, value=85)
BPMeds = st.selectbox("💊 On Blood Pressure Medication?", options=[("No", 0), ("Yes", 1)], index=0, format_func=lambda x: x[0])[1]
diabetes = st.selectbox("🧬 Diabetes?", options=[("No", 0), ("Yes", 1)], index=0, format_func=lambda x: x[0])[1]
prevalentStroke = st.selectbox("🧠 History of Stroke?", options=[("No", 0), ("Yes", 1)], index=0, format_func=lambda x: x[0])[1]
heartRate = st.number_input("❤️ Heart Rate (beats per minute)", min_value=40, max_value=200, value=70)

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
    })

# Get prediction probability (probability of class = 1)
    proba = model.predict_proba(input_df)[0][1]

# Convert to percentage
    percent = round(proba * 100, 2)

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
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from io import BytesIO
    import base64

    def generate_diet_pdf(percent):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 20)
        p.drawString(150, height - 80, "Heart Health Risk Report")

        p.setFont("Helvetica", 14)
        p.drawString(50, height - 130, f"Predicted Risk: {percent}%")

        # Customize based on risk
        y = height - 180
        if percent < 30:
            p.setFillColorRGB(0.13, 0.55, 0.13)
            p.drawString(50, y, "✅ Low Risk – Keep your heart healthy!")
            tips = [
                "• Eat fruits and vegetables daily",
                "• Exercise for 30 minutes",
                "• Drink enough water",
                "• Avoid processed food",
                "• Regular BP and cholesterol checks",
            ]
        elif percent < 70:
            p.setFillColorRGB(0.9, 0.5, 0)
            p.drawString(50, y, "⚠️ Moderate Risk – Improve your lifestyle!")
            tips = [
                "• Reduce salt, sugar, and oil",
                "• Eat oats, whole grains, and lentils",
                "• Exercise 5 times per week",
                "• Limit caffeine and alcohol",
                "• Track BP and glucose regularly",
            ]
        else:
            p.setFillColorRGB(0.8, 0.1, 0.1)
            p.drawString(50, y, "🚨 High Risk – Consult a doctor!")
            tips = [
                "• Consult a cardiologist",
                "• Follow a low-fat, low-salt diet",
                "• Avoid smoking and alcohol",
                "• Practice meditation",
                "• Monitor heart rate daily",
            ]

        p.setFillColorRGB(0, 0, 0)
        y -= 40
        for tip in tips:
            p.drawString(70, y, tip)
            y -= 25

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        return pdf
    pdf_data = generate_diet_pdf(percent)
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Heart_Report.pdf" style="text-decoration:none;"><button style="padding:10px 25px; border:none; border-radius:10px; background-color:#C2185B; color:white; font-size:16px; cursor:pointer;">📥 Download Diet Plan as PDF</button></a>'
    st.markdown(href, unsafe_allow_html=True)

