import streamlit as st
from math import log, exp
import matplotlib.pyplot as plt
import random
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.title("⚡ Electrochemistry Simulator")
st.write("Daniell Cell and Nernst Equation Experiments")

# Sidebar controls
st.sidebar.header("Simulator Controls")
template_choice = st.sidebar.selectbox("Layout template", ["Default", "Compact"], index=0)
show_help = st.sidebar.checkbox("Show help panels", value=True)

def lbl2conc(lbl):
    if lbl == "Sample":
        return st.session_state.sample_conc
    return float(lbl.split()[0])

# Constants
conc_anode = 0.1

tabs = st.tabs(["Theory", "Experiment", "Plots", "Results"])

with tabs[0]:
    st.header("Aim")
    st.markdown("""
To build a Daniell electrochemical cell, to verify the Nernst equation and to find the  
copper (II) ion concentration in an unknown CuSO₄ sample solution by potentiometry.
""")

    st.header("Principle")
    st.markdown("""
The Daniell Cell (invented in 1836 by John Daniell) was the first practical source of electricity, providing a reliable and constant voltage. It consists of two half-cells: zinc electrode in zinc sulfate solution and copper electrode in copper sulfate solution, connected by a salt bridge.

**Cell Reaction:** Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s)  
**Standard EMF:** E° = 1.10 V

The Nernst equation relates the cell potential to the concentrations of the reactants and products:

**E = E° - (RT/nF) ln Q**

For this cell, Q = [Zn²⁺]/[Cu²⁺], so:

**E = 1.10 - (0.0257) ln([Zn²⁺]/[Cu²⁺]) V** at 25°C

By measuring EMF at different concentrations and plotting E vs ln([Zn²⁺]/[Cu²⁺]), we can verify the Nernst equation and determine unknown concentrations.
""")

    img_path = "images/electrochem.png"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        if template_choice == "Compact":
            st.image(img, width=400)
        else:
            st.image(img, width="content")
    else:
        st.warning("Daniell Cell diagram not found. Please ensure 'images/electrochem.png' exists.")

    st.markdown("""
Two 50 mL beakers are used as half-cells. The salt bridge is a rolled filter paper having both ends in contact with each solution. A few drops of 1.5M KNO₃ are added to wet the paper at the center to ensure ionic conductivity. A multimeter is used to measure the EMF of the cell.

**(left = black cable) Zn | Zn²⁺ (0.10 M) || Cu²⁺ (0.10 M) | Cu (red cable = right)**

Since the oxidation reaction always happens at the anode, a spontaneous reaction (galvanic cell) will give a positive EMF.
""")

    st.subheader("Materials Required")
    st.write("""
Multimeter, Copper rod, Zinc rod, 0.1 M Zinc sulphate solution, 0.1 M, 0.01 M and 0.001 M Copper sulphate solutions,
1.5M KNO₃ solution, filter paper strip, 50 mL beakers (2).
""")

    st.header("Procedure")
    st.markdown("""
1. Pour 0.1 M ZnSO₄ solution into a beaker containing the zinc electrode.  
2. Pour CuSO₄ solution into another beaker with the copper electrode.  
3. Connect both half-cells using a salt bridge.  
4. Connect multimeter electrodes ensuring positive EMF reading.  
5. Measure EMF for different CuSO₄ concentrations.  
6. Plot EMF vs ln([Zn²⁺]/[Cu²⁺]).  
7. Determine unknown sample concentration using graph.  
""")
    st.info("Proceed to the Experiment tab to perform this simulation.")

with tabs[1]:
    st.header("Experiment")

    def nernst(E0, R, T, n, F, anode, cathode):
        return E0 - (R * T) / (n * F) * log(anode / cathode)

    conc_map = {"0.1 M": 0.1, "0.01 M": 0.01, "0.001 M": 0.001}

    Enot = 1.10
    R, T, n, F = 8.314, 298, 2, 96485

    conc_choice = st.selectbox("Select CuSO₄ concentration:", list(conc_map.keys()))

    # persistent sample concentration
    if "sample_conc" not in st.session_state:
        st.session_state.sample_conc = random.uniform(0.001, 0.1)

    sample_conc = st.session_state.sample_conc

    if "exp_data" not in st.session_state:
        st.session_state.exp_data = {}
    cols = st.columns(2)
    with cols[0]:
        if st.button("Add Experiment Data"):
            emf = nernst(Enot, R, T, n, F, conc_anode, conc_map[conc_choice])
            st.session_state.exp_data[conc_choice] = emf

            st.success("Data added")
    with cols[1]:
        if st.button("Add Sample Data"):
            emf = nernst(Enot, R, T, n, F, conc_anode, sample_conc)
            st.session_state.exp_data["Sample"] = emf
            st.success("Sample added")

    if st.session_state.exp_data:
        data_list = [{"Concentration (M)": k,"[Zn²⁺]/[Cu²⁺]": conc_anode/lbl2conc(k), "ln([Zn²⁺]/[Cu²⁺])": log(conc_anode/lbl2conc(k)), "EMF (V)": v} for k, v in st.session_state.exp_data.items()]
        df = pd.DataFrame(data_list)
        st.dataframe(df)
        st.download_button("Download Data as CSV", df.to_csv(index=False).encode('utf-8'), "experiment_data.csv", "text/csv")
    else:
        st.info("No experiment data added yet.")
    if st.button("Clear Data"):
        st.session_state.exp_data = {}
        st.session_state.sample_conc = random.uniform(0.001, 0.1)
        st.success("Cleared")


with tabs[2]:
    if st.session_state.exp_data:
        data = st.session_state.exp_data
        labels = list(data.keys())
        emf_vals = list(data.values())

        concs = [lbl2conc(lbl) for lbl in labels]
        x_vals = [log(conc_anode/c) for c in concs]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=emf_vals, mode='lines+markers', name='Data Points',
                                 hovertemplate='ln([Zn²⁺]/[Cu²⁺]): %{x:.2f}<br>EMF: %{y:.3f} V<extra></extra>'))
        if "Sample" in labels:
            i = labels.index("Sample")
            fig.add_vline(x=x_vals[i], line_dash="dash", annotation_text="Sample",
                          annotation_position="top right")
        fig.update_layout(
            title="EMF vs ln Concentration Ratio",
            xaxis_title="ln([Zn²⁺]/[Cu²⁺])",
            yaxis_title="EMF (V)",
            showlegend=False
        )
        st.plotly_chart(fig)
    else:
        st.info("No experiment data to plot yet.")


with tabs[3]:
    st.header("Results")

    if "Sample" not in st.session_state.exp_data:
        st.warning("Add sample data to compute results.")
    else:
        st.markdown("""<div style="border: 2px solid #4CAF50; padding: 20px; border-radius: 10px; background-color: #f0f8f0;">""", unsafe_allow_html=True)
        emf_sample = st.session_state.exp_data["Sample"]

        # regression using known standards
        standards = [(lbl2conc(k), v) for k, v in st.session_state.exp_data.items() if k != "Sample"]
        conc_std = [c for c,_ in standards]
        emf_std = [e for _,e in standards]
        x_std = [log(conc_anode/c) for c in conc_std]

        if len(x_std) < 2:
            st.error("Please add at least two standard measurements before adding the sample.")
        else:
            m, b = np.polyfit(x_std, emf_std, 1)
            x_sample = (emf_sample - b) / m
            cu_conc = conc_anode / exp(x_sample)

            st.success(f"Calculated Sample CuSO₄ Concentration ≈ **{cu_conc:.4f} M**")

            st.write("""
(a) Nernst equation verified by observing change in EMF with concentration.  
(b) Unknown sample concentration estimated using calibration plot.  
""")
        st.markdown("</div>", unsafe_allow_html=True)
