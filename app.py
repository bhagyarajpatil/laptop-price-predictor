# app.py

import streamlit as st
import pickle
import numpy as np

# Page Config
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="centered"
)

# Custom CSS Styling
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

/* Title Styling */
h1 {
    text-align: center;
    color: #00ffd5 !important;
    font-size: 42px !important;
}

/* Selectbox and Input Labels */
label {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: bold;
}

/* Dropdown Boxes */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1f2c3d;
    border-radius: 10px;
    color: white;
}

/* Number Input */
.stNumberInput input {
    background-color: #1f2c3d;
    color: white;
    border-radius: 10px;
}

/* Slider */
.stSlider {
    color: #00ffd5;
}

/* Button Styling */
.stButton button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    padding: 12px 25px;
    width: 100%;
    transition: 0.3s;
}

.stButton button:hover {
    background: linear-gradient(to right, #ff512f, #dd2476);
    transform: scale(1.03);
}

/* Prediction Box */
.prediction {
    background-color: #00c853;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# Load Model
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Title
st.title("💻 Laptop Price Predictor")

# brand
company = st.selectbox('Brand', df['Company'].unique())

# type of laptop
type = st.selectbox('Type', df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM (in GB)', [2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No','Yes'])

# IPS
ips = st.selectbox('IPS Display', ['No','Yes'])

# screen size
screen_size = st.slider('Screen Size (in inches)', 10.0, 18.0, 13.0)

# resolution
resolution = st.selectbox(
    'Screen Resolution',
    [
        '1920x1080',
        '1366x768',
        '1600x900',
        '3840x2160',
        '3200x1800',
        '2880x1800',
        '2560x1600',
        '2560x1440',
        '2304x1440'
    ]
)

# cpu
cpu = st.selectbox('CPU', df['Cpu brand'].unique())

# HDD
hdd = st.selectbox('HDD (in GB)', [0,128,256,512,1024,2048])

# SSD
ssd = st.selectbox('SSD (in GB)', [0,8,128,256,512,1024])

# GPU
gpu = st.selectbox('GPU', df['Gpu brand'].unique())

# OS
os = st.selectbox('Operating System', df['os'].unique())

# Predict Button
if st.button('🔍 Predict Price'):

    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

    query = np.array([
        company,
        type,
        ram,
        weight,
        touchscreen,
        ips,
        ppi,
        cpu,
        hdd,
        ssd,
        gpu,
        os
    ])

    query = query.reshape(1, 12)

    predicted_price = int(np.exp(pipe.predict(query)[0]))

    st.markdown(
        f"""
        <div class="prediction">
            💰 Predicted Price: ₹ {predicted_price}
        </div>
        """,
        unsafe_allow_html=True
    )