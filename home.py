import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

st.set_page_config(page_title="ChemLabSimulator", layout="wide", page_icon="🧪")

st.title("🧪 Welcome to ChemLabSimulator")
st.markdown("""
    <div style="
        padding: 20px;
        border-radius: 12px;
        background: linear-gradient(135deg, #e8e8ef 0%, #f0f0f5 100%);
        border: 1px solid #d0d0d5;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
        color: #1a1a1a;
    ">
        <h3 style="margin-bottom:10px; color:#1a1a1a;">👋 Welcome!</h3>
        <p style="margin-top:10px; color:#1a1a1a; font-size:16px;">
            ChemLabSimulator is an interactive platform designed to help students and enthusiasts explore and simulate various chemistry experiments in a virtual laboratory environment. Dive into conductance measurements and electrochemical experiments with real-time data visualization and analysis.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Available Experiments")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="padding:15px; border-radius:8px; background:#f8f9fa; border-left:4px solid #007bff;">
        <h4 style="color: black;">🔬 Conductance Measurement</h4>
        <p style="color: black;">Study the conductance of electrolyte solutions at various concentrations and temperatures. Perform virtual experiments with HCl, NaCl, and KCl.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding:15px; border-radius:8px; background:#f8f9fa; border-left:4px solid #28a745;">
        <h4 style="color: black;">⚡ Electrochemistry</h4>
        <p style="color: black;">Explore the Daniell Cell and verify the Nernst equation. Measure EMF and determine unknown concentrations potentiometrically.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

file_path = "images/Laboratory.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            animation = json.load(f)
            st_lottie(animation, speed=1, height=400, key="chemistry")
        except Exception as e:
            st.error(f"Error loading animation: {e}")
            st.info("🧪 Chemistry animation would be displayed here.")
else:
    st.error(f"Animation file not found: {file_path}")
    st.info("🧪 Chemistry animation would be displayed here.")

st.markdown("---")
st.markdown("**Navigate using the sidebar to start your experiments!**")

