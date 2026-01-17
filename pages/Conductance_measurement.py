import streamlit as st
import matplotlib.pyplot as plt
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components
import io

st.set_page_config(page_title="Conductance Measurement Simulator", layout="wide")
st.title("🔬 Conductance Measurement Simulator")
st.write("Interactive virtual lab for studying electrolyte conductance")

# Sidebar
st.sidebar.header("Simulator Controls")
template_choice = st.sidebar.selectbox("Layout template", ["Default", "Compact"], index=0)
show_help = st.sidebar.checkbox("Show help panels", value=True)

tabs = st.tabs(["Theory","Experiments","Plots","Reports"])

# ---------------------------------------------------------------------
# THEORY TAB
# ---------------------------------------------------------------------
with tabs[0]:
    st.header("Theory")
    
    if template_choice == "Compact":
        st.markdown('<div style="font-size: 14px;">', unsafe_allow_html=True)

    st.subheader("AIM")
    st.write("""
    Studying conductance of electrolyte solutions at various concentrations and temperatures.
    """)

    st.subheader("PRINCIPLE")
    st.write("""
    A solution conducts electricity with the help of ions present in it (flow of charge). The movement
    of cations (positive charge) and anions (negative charge) contributes to total flow of charge.

    Depending on electrical conductivity, chemical substances are classified as:
    - **Strong electrolytes:** HCl, NaCl, HNO₃
    - **Weak electrolytes:** CH₃COOH, NH₄OH
    """)

    st.write("""
    Conductance depends on charge, concentration, mobility of ions and solvent effects.
    Conductance measurement is used for purity checks and determination of constants.
    """)

    st.subheader("Equivalent Conductivity at Infinite Dilution (25°C)")
    cations = pd.DataFrame({
        "Cation": ["H⁺", "K⁺", "Na⁺", "Ag⁺", "NH₄⁺", "Li⁺", "Ca²⁺", "Mg²⁺", "Zn²⁺"],
        "Λ (S·cm²·mol⁻¹)": [350.0, 73.5, 50.1, 59.5, 73.5, 38.7, 76.4, 53.0, 50.1]
    })
    st.write("**Cations**")
    st.table(cations)

    anions = pd.DataFrame({
        "Anion": ["OH⁻", "Cl⁻", "Br⁻", "I⁻", "NO₃⁻", "ClO₃⁻", "CH₃COO⁻", "SO₄²⁻", "HSO₄⁻"],
        "Λ (S·cm²·mol⁻¹)": [198.0, 76.3, 78.4, 76.8, 71.4, 80.0, 40.9, 69.3, 55.4]
    })
    st.write("**Anions**")
    st.table(anions)

    salts = pd.DataFrame({
        "Salt": ["HF", "HCl", "HBr", "HI", "KOH", "NaOH", "KCl", "NaCl"],
        "Λ (S·cm²·mol⁻¹)": [405.1, 426.1, 427.7, 426.4, 271.5, 247.7, 150.0, 145.0]
    })
    st.write("**Salts**")
    st.table(salts)

    if show_help:
        st.subheader("MATERIALS REQUIRED")
        st.write("""
        HCl, NaCl, KCl, deionised water, Conductometer, Thermometer (110°C),
        hot plate, pipette (20 mL), measuring jar (100 mL), beakers.
        """)

        st.subheader("PROCEDURE")
        st.write("""
        1. Prepare 0.1M solutions of HCl, NaCl, KCl and measure conductance.
        2. Take 20 mL of 0.1M NaCl.
        3. Add 4 mL water each time and measure conductance until 40 mL total.
        4. Study temperature effect for KCl at 0.1M.
        """)

    st.subheader("Observation Tables (Blank)")
    table1 = pd.DataFrame({
        "S.No": [1,2,3],
        "Solution": ["0.1M HCl","0.1M NaCl","0.1M KCl"],
        "Conductance Λ (S·cm²·mol⁻¹)": ["","",""],
        "Temperature (K)": ["","",""]
    })
    st.table(table1)

    table2 = pd.DataFrame({
        "S.No": [1,2,3,4,5,6],
        "Volume (mL)": ["20","24","28","32","36","40"],
        "Concentration (M)": ["0.1000","0.0833","0.0714","0.0625","0.0556","0.0500"],
        "Conductance Λ (S·cm²·mol⁻¹)": ["","","","","",""],
        "Temperature (K)": ["","","","","",""]
    })
    st.table(table2)

    if template_choice == "Compact":
        st.markdown('</div>', unsafe_allow_html=True)
    st.info("Proceed to the Experiment tab to perform this simulation.")

# ---------------------------------------------------------------------
# EXPERIMENT TAB
# ---------------------------------------------------------------------
with tabs[1]:
    st.header("Experiment")

    # session states
    if 'table1' not in st.session_state:
        st.session_state.table1 = []
    if 'table2' not in st.session_state:
        st.session_state.table2 = []
        st.session_state.current_volume = 20
        st.session_state.initial_moles = 0.1 * 0.02
    if 'temp_table' not in st.session_state:
        st.session_state.temp_table = []

    # constants
    Λ0 = {"HCl": 426.1, "NaCl": 145.0, "KCl": 150.0}
    k_const = {"HCl": 200, "NaCl": 120, "KCl": 140}
    T0 = 298
    alpha = 0.015  # K^-1 more realistic

    st.subheader("A) Conductance of 0.1M Electrolytes")
    salt = st.selectbox("Select electrolyte", ["HCl","NaCl","KCl"])
    if st.button("Measure Conductance (0.1M)"):
        C = 0.1
        Λ_val = Λ0[salt] - k_const[salt] * math.sqrt(C)
        Λ_val = round(Λ_val,2)
        st.session_state.table1.append((salt, Λ_val, T0))
        st.success(f"Measured Λ = {Λ_val} S·cm²·mol⁻¹ at {T0}K")

    df1 = pd.DataFrame(st.session_state.table1, columns=["Salt","Conductance Λ (S·cm²·mol⁻¹)","Temperature (K)"])
    st.table(df1)
    st.download_button("Download Table 1 CSV", df1.to_csv(index=False), "table1.csv")

    if st.button("Reset Table 1 Data"):
        st.session_state.table1 = []

    st.subheader("B) Serial Dilution of NaCl")
    st.write(f"Current Volume = {st.session_state.current_volume} mL")

    colD1, colD2 = st.columns(2)
    with colD1:
        if st.button("Add 4 mL Water"):
            if st.session_state.current_volume < 40:
                st.session_state.current_volume += 4
            else:
                st.warning("Maximum 40 mL reached!")

    with colD2:
        if st.button("Measure Conductance (Diluted)"):
            V = st.session_state.current_volume/1000
            C = st.session_state.initial_moles / V
            Λ_val = Λ0["NaCl"] - k_const["NaCl"]*math.sqrt(C)
            Λ_val = round(Λ_val,2)
            st.session_state.table2.append((st.session_state.current_volume, round(C,4), Λ_val, T0))
            st.success(f"Measured Λ = {Λ_val} S·cm²·mol⁻¹ at {T0}K")

    df2 = pd.DataFrame(st.session_state.table2,
                       columns=["Volume (mL)","Concentration (M)","Conductance Λ (S·cm²·mol⁻¹)","Temperature (K)"])
    st.table(df2)
    st.download_button("Download Table 2 CSV", df2.to_csv(index=False), "dilution.csv")

    if st.button("Reset Dilution Data"):
        st.session_state.table2 = []
        st.session_state.current_volume = 20

    st.subheader("C) Temperature Effect on KCl (0.1M)")
    T = st.slider("Temperature (K)", min_value=298, max_value=338, value=298)
    if st.button("Measure Conductance (Temp)"):
        C = 0.1
        Λ25 = Λ0["KCl"] - k_const["KCl"]*math.sqrt(C)
        ΛT = Λ25 * (1 + alpha*(T-T0))
        ΛT = round(ΛT,2)
        st.session_state.temp_table.append((T,ΛT))
        st.success(f"Measured Λ = {ΛT} S·cm²·mol⁻¹ at {T}K")

    dfT = pd.DataFrame(st.session_state.temp_table, columns=["Temperature (K)","Conductance Λ (S·cm²·mol⁻¹)"])
    st.table(dfT)
    st.download_button("Download Temp CSV", dfT.to_csv(index=False), "temp.csv")

    if st.button("Reset Temperature Data"):
        st.session_state.temp_table = []

# ---------------------------------------------------------------------
# PLOTS TAB
# ---------------------------------------------------------------------
with tabs[2]:
    st.header("Plots")

    df2 = pd.DataFrame(st.session_state.get("table2",[]),
                       columns=["Volume (mL)","Concentration (M)","Conductance Λ (S·cm²·mol⁻¹)","Temperature (K)"])
    
    if len(df2)>=2:
        df2["Concentration (M)"] = df2["Concentration (M)"].astype(float)
        df2["Conductance Λ (S·cm²·mol⁻¹)"] = df2["Conductance Λ (S·cm²·mol⁻¹)"].astype(float)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df2["Concentration (M)"],
            y=df2["Conductance Λ (S·cm²·mol⁻¹)"],
            mode="markers+lines",
            name="Measured"
        ))

        coeffs = np.polyfit(df2["Concentration (M)"], df2["Conductance Λ (S·cm²·mol⁻¹)"], 1)
        xfit = np.linspace(df2["Concentration (M)"].min(), df2["Concentration (M)"].max(), 50)
        yfit = np.polyval(coeffs, xfit)

        fig.add_trace(go.Scatter(x=xfit,y=yfit,mode="lines",line=dict(dash="dash"),name="Trend"))

        fig.update_layout(title="NaCl: Variation of Conductance with Concentration",
                          xaxis_title="Concentration (M)",
                          yaxis_title="Conductance Λ (S·cm²·mol⁻¹)",
                          template="plotly_white")
        fig.update_xaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Perform dilution experiment to view plot.")

    if len(dfT:=pd.DataFrame(st.session_state.get("temp_table",[]),
                     columns=["Temperature (K)","Conductance Λ (S·cm²·mol⁻¹)"])) >=1:

        dfT["Temperature (K)"] = dfT["Temperature (K)"].astype(float)
        dfT["Conductance Λ (S·cm²·mol⁻¹)"] = dfT["Conductance Λ (S·cm²·mol⁻¹)"].astype(float)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=dfT["Temperature (K)"],
                                  y=dfT["Conductance Λ (S·cm²·mol⁻¹)"],
                                  mode="markers+lines", name="Measured"))
        
        if len(dfT)>=2:
            coeffs2 = np.polyfit(dfT["Temperature (K)"], dfT["Conductance Λ (S·cm²·mol⁻¹)"],1)
            xfit = np.linspace(dfT["Temperature (K)"].min(), dfT["Temperature (K)"].max(),50)
            yfit = np.polyval(coeffs2, xfit)
            fig2.add_trace(go.Scatter(x=xfit,y=yfit,mode="lines",line=dict(dash="dash"),name="Trend"))

        fig2.update_layout(title="KCl: Conductance vs Temperature",
                           xaxis_title="Temperature (K)",
                           yaxis_title="Conductance Λ (S·cm²·mol⁻¹)",
                           template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------
# REPORT TAB
# ---------------------------------------------------------------------
with tabs[3]:
    st.header("Report")

    st.subheader("Table 1: 0.1M Solutions")
    df1 = pd.DataFrame(st.session_state.table1,
                       columns=["Salt","Conductance Λ (S·cm²·mol⁻¹)","Temperature (K)"])
    st.table(df1)

    st.subheader("Table 2: NaCl Dilution")
    df2 = pd.DataFrame(st.session_state.table2,
                       columns=["Volume (mL)","Concentration (M)","Conductance Λ (S·cm²·mol⁻¹)","Temperature (K)"])
    st.table(df2)

    st.subheader("Temperature Data (KCl)")
    dfT = pd.DataFrame(st.session_state.temp_table,
                       columns=["Temperature (K)","Conductance Λ (S·cm²·mol⁻¹)"])
    st.table(dfT)

    st.subheader("Result")
    st.write("""
    From table 1, the cation with the highest conducting ability can be identified.
    Conductance vs concentration for NaCl is compared.
    Conductance of 0.1M KCl with variation of temperature is studied.
    """)

    show = st.checkbox("Show Interpretation")
    if show:
        st.subheader("Interpretation")
        if len(df1)>0:
            max_salt = df1.loc[df1['Conductance Λ (S·cm²·mol⁻¹)'].idxmax(),'Salt']
            st.write(f"- Highest conducting salt measured: **{max_salt}**")
        if len(df2)>1:
            st.write("- Conductance increases with dilution due to increased ion mobility at lower concentration.")
        if len(dfT)>1:
            st.write("- Conductance increases with temperature due to enhanced ion mobility.")
