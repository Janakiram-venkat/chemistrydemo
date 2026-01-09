import streamlit as st
import matplotlib.pyplot as plt 
import math 
st.set_page_config(page_title="Chemistry simulator", layout="wide")
st.title("Chemistry simulator")
st.write("Interactive virtual lab")

tabs = st.tabs(["Theory","Experiments","Plots","Reports"])
with tabs[0]:
    st.header("Theory")
    st.subheader("AIM")
    st.write("""
    Studying conductance of electrolyte solutions at various concentrations and temperatures.
    """)
    st.subheader("PRINCIPLE")
    st.write("""
    A solution conducts electricity with the help of ions present in it (flow of charge). The movement of cations 
    (positive charge) in one direction and anions (negative charge) in another direction adds up resulting the total 
    flow of charge. Depending on the electrical conductivity, chemical substances can be classified as strong 
    electrolyte (compounds with high dissociation capability such as HCl, NaCl, HNO3 etc.) and weak electrolyte 
    (compounds with low dissociation constant such as CH3COOH, NH4OH etc.).

    Conductance of an electrolyte solution depends on several factors such as charge, concentration, and mobility of 
    both the cations and anions present in solution. Additionally, solvent has an important role; as an example, NaCl 
    is a strong electrolyte in water but a weak electrolyte in propane.
    """)
    st.write("""
    Conductance of an electrolyte-solution can be measured precisely by a Conductometer. It is an important tool to 
    measure the ion-content of the solution, hence, the nature and concentration of the electrolyte.
    """)
    st.write("""
    Conductance measurement is used in industry for checking purity of distilled water or other chemicals and for 
    determination of physical constants such as ionization constant, equilibrium constant, reaction rate constant etc.
    """)
    st.write("""
    A conductometric titration involves measurement of the conductivity after successive addition of the titrant 
    reagent. The end point is obtained from a plot of conductivity (varies during reaction) against volume of titrant 
    added. The end point of neutralization, complexation, precipitation, displacement and decomposition reactions 
    involving electrolytes can be determined precisely. But redox reactions cannot be followed by conductance method.

    The main advantages of this method are that it can be used for (i) turbid and colored solutions, (ii) very dilute 
    solutions and (iii) incomplete reactions and no suitable indicator.
    """)
    st.subheader("Equivalent conductivity of some ions and salts in water at infinite dilution at 25°C")

    import pandas as pd

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
    st.subheader("MATERIALS REQUIRED")
    st.write("""
    (a) HCl acid  
    (b) NaCl salt  
    (c) KCl salt  
    (d) deionised water  

    Conductometer, 110°C Thermometer, Electrical hot plate.  
    100 mL measuring jar, 20 mL pipette, 250 mL Beakers (4 nos.), 500 mL Beaker (water bath), glass rod.
    """)
    st.subheader("PROCEDURE")
    st.write("""
    1. Prepare 100 mL aqueous solutions of HCl, NaCl and KCl in 0.1M concentration. Measure the conductance of each 
       solution at same temperature. Record in Table 1.

    2. Take exactly 20 mL aqueous 0.1M NaCl solution and measure the conductivity.

    3. Add exactly 4 mL of deionized water, mix thoroughly and measure the conductivity.

    4. Repeat the above step FOUR times (solution volume from 20 mL changes: 24, 28, 32, 36 and 40 mL) and record in 
       Table 2.
    """)

    # OBSERVATION TABLES
    st.subheader("OBSERVATION AND CALCULATION")

    st.write("**Table 1: Conductance of various salts of 0.1M solutions**")
    table1 = pd.DataFrame({
        "S.No": [1, 2, 3],
        "Solution": ["0.1M HCl", "0.1M NaCl", "0.1M KCl"],
        "Conductance (Λ)": ["", "", ""],
        "Temperature (K)": ["", "", ""]
    })
    st.table(table1)

    st.write("**Table 2: Variation of conductance with respect to NaCl solution concentration**")
    table2 = pd.DataFrame({
        "S.No": [1, 2, 3, 4, 5, 6],
        "Solution Volume (mL)": ["20", "24", "28", "32", "36", "40"],
        "Concentration (M)": ["0.1000", "0.0833", "0.0714", "0.0625", "0.0556", "0.0500"],
        "Conductance (Λ)": ["", "", "", "", "", ""],
        "Temperature (K)": ["", "", "", "", "", ""]
    })
    st.table(table2)

    # RESULT
    st.subheader("RESULT")
    st.write("""
    From table 1 data, the cation, which has the highest conducting ability is …….

    Compared the conductance vs. varying NaCl concentration.

    The conductance of 0.1M KCl with variation of temperature is studied.
    """)

    st.info("Proceed to the Experiment tab to perform this simulation.")
   
with tabs[1]:
    st.header("Experiment")

    import math

    # initialize session state
    if 'table1' not in st.session_state:
        st.session_state.table1 = []

    if 'table2' not in st.session_state:
        st.session_state.table2 = []
        st.session_state.current_volume = 20  # mL
        st.session_state.initial_moles = 0.1 * 0.02  # 0.1M * 20mL → 0.002 mol

    if 'temp_table' not in st.session_state:
        st.session_state.temp_table = []

    L0 = {"HCl": 426.1, "NaCl": 145.0, "KCl": 150.0}
    k_const = {"HCl": 200, "NaCl": 120, "KCl": 140}
    T0 = 298
    alpha = 0.02

    st.subheader("A) Conductance of 0.1M Electrolytes")

    salt = st.selectbox("Select electrolyte", ["HCl", "NaCl", "KCl"], key="salt_select")
    button_a = st.button("Measure Conductance (0.1M)")

    if button_a:
        C = 0.1
        L_val = L0[salt] - k_const[salt] * math.sqrt(C)
        st.session_state.table1.append((salt, round(L_val, 2), T0))

        st.success(f"Conductance measured: {round(L_val, 2)} mS/cm at {T0}K")

    st.write("Recorded Data:")
    st.table(pd.DataFrame(st.session_state.table1, columns=["Salt", "Conductance (mS/cm)", "Temperature (K)"]))


    st.subheader("B) Serial Dilution of NaCl")

    st.write(f"Current Volume: {st.session_state.current_volume} mL")

    colD1, colD2 = st.columns(2)

    with colD1:
        if st.button("Add 4 mL DI Water"):
            if st.session_state.current_volume < 40:
                st.session_state.current_volume += 4
            else:
                st.warning("Maximum dilution reached (40 mL).")

    with colD2:
        if st.button("Measure Conductance (Diluted NaCl)"):
            V = st.session_state.current_volume / 1000
            C = st.session_state.initial_moles / V
            L_val = L0["NaCl"] - k_const["NaCl"] * math.sqrt(C)
            st.session_state.table2.append((st.session_state.current_volume, round(C, 4), round(L_val, 2), T0))
            st.success(f"Conductance measured: {round(L_val, 2)} mS/cm at {T0}K")

    st.write("Dilution Data:")
    st.table(pd.DataFrame(st.session_state.table2, columns=["Volume (mL)", "Concentration (M)", "Conductance (mS/cm)", "Temperature (K)"]))

    st.subheader("C) Temperature Effect on KCl")
    T = st.slider("Temperature (K)", 298, 338, 298)
    if st.button("Measure Conductance (Temp Effect)"):
        C = 0.1
        L_c = L0["KCl"] - k_const["KCl"] * math.sqrt(C)
        L_T = L_c * (1 + alpha * (T - T0))
        st.session_state.temp_table.append((T, round(L_T, 2)))
        st.success(f"Conductance measured: {round(L_T, 2)} mS/cm at {T}K")

    st.write("Temperature Data:")
    st.table(pd.DataFrame(st.session_state.temp_table, columns=["Temperature (K)", "Conductance (mS/cm)"]))

with tabs[2]:
    st.header("Plots")
    st.subheader("Concentration vs conductance for NaCl dilution")
    if len(st.session_state.get("table2",[]))>0:
        df = pd.DataFrame(st.session_state.table2, columns=["Volume (mL)", "Concentration (M)", "Conductance (mS/cm)", "Temperature (K)"])

        fig, ax = plt.subplots()
        ax.plot(df["Concentration (M)"], df["Conductance (mS/cm)"], marker='o',linestyle='-')
        ax.set_xlabel("Concentration (M)")
        ax.set_ylabel("Conductance (mS/cm)")
        ax.set_title("Concentration vs Conductance for NaCl Dilution")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("No data available for NaCl dilution plot. Please perform the experiment first.")
    if len(st.session_state.get("temp_table",[]))>0:
        st.subheader("Temperature vs conductance for KCl")
        df_temp = pd.DataFrame(st.session_state.temp_table, columns=["Temperature (K)", "Conductance (mS/cm)"])

        fig2, ax2 = plt.subplots()
        ax2.plot(df_temp["Temperature (K)"], df_temp["Conductance (mS/cm)"], marker='o',linestyle='-')
        ax2.set_xlabel("Temperature (K)")
        ax2.set_ylabel("Conductance (mS/cm)")
        ax2.set_title("Temperature vs Conductance for KCl")
        ax2.grid(True)
        st.pyplot(fig2)
    else:
        st.info("No data available for KCl temperature plot. Please perform the experiment first.")
with tabs[3]:
    st.header("Report")

    st.subheader("Recorded Tables")

    # Table 1
    st.markdown("**Table 1: Conductance of 0.1M Solutions**")
    if len(st.session_state.table1) > 0:
        st.table(pd.DataFrame(st.session_state.table1, columns=["Salt", "Conductance (mS/cm)", "Temperature (K)"]))
    else:
        st.info("No data recorded yet.")

    # Table 2
    st.markdown("**Table 2: Variation of Conductance with NaCl Dilution**")
    if len(st.session_state.table2) > 0:
        st.table(pd.DataFrame(st.session_state.table2, columns=["Volume (mL)", "Concentration (M)", "Conductance (mS/cm)", "Temperature (K)"]))
    else:
        st.info("No dilution data recorded yet.")

    # Temperature table
    st.markdown("**Temperature Data (KCl)**")
    if len(st.session_state.temp_table) > 0:
        st.table(pd.DataFrame(st.session_state.temp_table, columns=["Temperature (K)", "Conductance (mS/cm)"]))
    else:
        st.info("No temperature data recorded yet.")

    st.subheader("Result")

    st.write("""
    From table 1 data, the cation which has the highest conducting ability is __________.

    Compared the conductance vs varying NaCl concentration.

    The conductance of 0.1M KCl with variation of temperature is studied.
    """)
    show_interpret = st.checkbox("Show Interpretation")

    if show_interpret:

        st.subheader("Interpretation")

        # INTERPRET 1: Highest conducting ion
        interpretation = []

        # Determine if student measured HCl
        salts_measured = [x[0] for x in st.session_state.table1]

        if "HCl" in salts_measured:
            df1 = pd.DataFrame(st.session_state.table1, columns=["Salt", "Conductance", "Temp"])
            max_salt = df1.loc[df1['Conductance'].idxmax(), 'Salt']
            if max_salt == "HCl":
                interpretation.append("H⁺ ion shows the highest conducting ability among measured ions.")
            else:
                interpretation.append(f"{max_salt} shows highest conductance among measured salts.")
        else:
            interpretation.append("H⁺ typically shows highest conductivity among common cations.")
        if len(st.session_state.table2) > 1:
            interpretation.append("Conductance decreases with dilution of NaCl due to reduced ion concentration.")
        if len(st.session_state.temp_table) > 1:
            interpretation.append("Conductance of KCl increases with temperature due to increased ion mobility.")

        for line in interpretation:
            st.write("- " + line)