from __future__ import annotations

import streamlit as st

from model import (
    ModelState,
    compute_fluxes,
    equation_text,
    preset_values,
    scenario_dataframe,
    sensitivity_analysis,
    validate_state,
)
from plots import create_comparison_plot, create_pathway_figure, plot_sensitivity


st.set_page_config(page_title="SCD RBC Metabolic Simulation", layout="wide")


def default_state() -> dict:
    return {
        "total_glucose_flux": 100.0,
        "glycolysis_fraction": 0.90,
        "ppp_fraction": 0.10,
        "disease_stress": 1.0,
        "atp_coefficient": 0.50,
        "nadph_coefficient": 0.80,
        "ros_protection_coefficient": 0.35,
        "bpg_coefficient": 0.45,
    }


if "settings" not in st.session_state:
    st.session_state.settings = default_state()


preset_names = ["Normal RBC", "SCD-like", "Simulated Intervention"]
selected_preset = st.sidebar.selectbox("Preset condition", preset_names)

if st.sidebar.button("Apply preset"):
    st.session_state.settings = preset_values()[selected_preset].copy()

st.title("In-Silico Metabolic Engineering of Red Blood Cell Metabolism in Sickle Cell Disease")
st.caption("Educational simulation prototype for an undergraduate case study")

st.markdown(
    "This dashboard is a simplified educational model. It is not a clinical model and does not predict patient outcomes or validate a therapy."
)

st.markdown("## 1. PROJECT OVERVIEW")
st.write(
    "This educational simulation explores how altered glucose partitioning in red blood cell metabolism can influence ATP, NADPH, ROS, and 2,3-BPG in a simplified sickle cell disease-like metabolic state."
)

st.markdown("## 2. METABOLIC PATHWAY")
pathway_text = """
GLUCOSE
   |
   +---- GLYCOLYSIS ----> ATP
   |
   +---- PPP -----------> NADPH ----> Antioxidant protection
   |
   +---- 2,3-BPG branch
"""
st.code(pathway_text, language="text")

st.markdown("## 3. MODEL ASSUMPTIONS")
st.markdown(
    """
    - These values are normalized arbitrary units and are not clinical measurements.
    - Total glucose flux = 100 arbitrary units.
    - Glycolysis fraction + PPP fraction is constrained to remain within the model assumption range.
    - SCD-like state is represented as increased oxidative stress and altered glucose partitioning.
    - Intervention is a computational flux-rebalancing experiment, not a proven therapy.
    """
)

st.markdown("## 4. SIMULATION CONTROLS")
settings = st.session_state.settings

with st.form("sim_form"):
    total_glucose_flux = st.slider("Total glucose flux", 10.0, 200.0, value=float(settings["total_glucose_flux"]), step=1.0)
    glycolysis_fraction = st.slider("Glycolysis fraction", 0.0, 1.0, value=float(settings["glycolysis_fraction"]), step=0.01)
    ppp_fraction = st.slider("PPP fraction", 0.0, 1.0, value=float(settings["ppp_fraction"]), step=0.01)
    disease_stress = st.slider("Disease oxidative stress", 0.0, 3.0, value=float(settings["disease_stress"]), step=0.05)
    atp_coefficient = st.slider("ATP coefficient", 0.0, 1.0, value=float(settings["atp_coefficient"]), step=0.01)
    nadph_coefficient = st.slider("NADPH coefficient", 0.0, 1.5, value=float(settings["nadph_coefficient"]), step=0.01)
    ros_protection_coefficient = st.slider("ROS protection coefficient", 0.0, 1.0, value=float(settings["ros_protection_coefficient"]), step=0.01)
    bpg_coefficient = st.slider("2,3-BPG coefficient", 0.0, 1.0, value=float(settings["bpg_coefficient"]), step=0.01)

    submitted = st.form_submit_button("Update simulation")

if submitted:
    glycolysis_fraction, ppp_fraction = validate_state(glycolysis_fraction, ppp_fraction)
    st.session_state.settings = {
        "total_glucose_flux": float(total_glucose_flux),
        "glycolysis_fraction": float(glycolysis_fraction),
        "ppp_fraction": float(ppp_fraction),
        "disease_stress": float(disease_stress),
        "atp_coefficient": float(atp_coefficient),
        "nadph_coefficient": float(nadph_coefficient),
        "ros_protection_coefficient": float(ros_protection_coefficient),
        "bpg_coefficient": float(bpg_coefficient),
    }

current_state = ModelState(**st.session_state.settings)
current_flux = compute_fluxes(current_state)

st.markdown("## 5. NORMAL vs SCD vs INTERVENTION")
scenario_data = scenario_dataframe({
    "Normal RBC": {
        "total_glucose_flux": 100.0,
        "glycolysis_fraction": 0.90,
        "ppp_fraction": 0.10,
        "disease_stress": 1.0,
        "atp_coefficient": current_state.atp_coefficient,
        "nadph_coefficient": current_state.nadph_coefficient,
        "ros_protection_coefficient": current_state.ros_protection_coefficient,
        "bpg_coefficient": current_state.bpg_coefficient,
    },
    "SCD-like": {
        "total_glucose_flux": 100.0,
        "glycolysis_fraction": 0.95,
        "ppp_fraction": 0.05,
        "disease_stress": 1.8,
        "atp_coefficient": current_state.atp_coefficient,
        "nadph_coefficient": current_state.nadph_coefficient,
        "ros_protection_coefficient": current_state.ros_protection_coefficient,
        "bpg_coefficient": current_state.bpg_coefficient,
    },
    "Simulated Intervention": {
        "total_glucose_flux": current_state.total_glucose_flux,
        "glycolysis_fraction": current_state.glycolysis_fraction,
        "ppp_fraction": current_state.ppp_fraction,
        "disease_stress": current_state.disease_stress,
        "atp_coefficient": current_state.atp_coefficient,
        "nadph_coefficient": current_state.nadph_coefficient,
        "ros_protection_coefficient": current_state.ros_protection_coefficient,
        "bpg_coefficient": current_state.bpg_coefficient,
    },
})
st.dataframe(scenario_data, use_container_width=True)

st.markdown("## 6. SENSITIVITY ANALYSIS")
sens_df = sensitivity_analysis(
    total_glucose_flux=current_state.total_glucose_flux,
    disease_stress=current_state.disease_stress,
    atp_coefficient=current_state.atp_coefficient,
    nadph_coefficient=current_state.nadph_coefficient,
    ros_protection_coefficient=current_state.ros_protection_coefficient,
    bpg_coefficient=current_state.bpg_coefficient,
)
st.dataframe(sens_df, use_container_width=True)

fig_sens, _ = plot_sensitivity(sens_df)
st.pyplot(fig_sens)

st.markdown("## 7. RESULTS")
metric_cols = st.columns(4)
with metric_cols[0]:
    st.metric("ATP", f"{current_flux['ATP']:.2f}")
with metric_cols[1]:
    st.metric("NADPH", f"{current_flux['NADPH']:.2f}")
with metric_cols[2]:
    st.metric("ROS", f"{current_flux['ROS']:.2f}")
with metric_cols[3]:
    st.metric("2,3-BPG", f"{current_flux['2,3-BPG']:.2f}")

comparison_fig = create_comparison_plot(scenario_data)
st.pyplot(comparison_fig)

st.markdown("## 8. INTERPRETATION")
st.write(
    "Higher simulated NADPH indicates greater modeled antioxidant-supporting capacity. Lower simulated ROS indicates lower modeled oxidative stress."
)
st.write(
    "The simulation suggests that, under the model assumptions, increasing PPP contribution increases simulated NADPH and may reduce modeled oxidative stress."
)
st.write(
    "This is an educational simulation, not a statement that a treatment is proven to work in patients."
)

st.markdown("## 9. LIMITATIONS")
st.markdown(
    """
    - This is a simplified normalized model and not a validated biochemical kinetic model.
    - It does not include full red blood cell metabolic regulation or enzyme kinetics.
    - It does not account for patient-specific genotype, oxygenation, or clinical severity.
    - It should not be used to predict actual treatment outcomes or patient survival.
    - The model assumptions are intentionally educational and non-clinical.
    """
)

st.markdown("## MODEL EQUATIONS")
for eq in equation_text():
    st.write(eq)

st.markdown("## PATHWAY VISUALIZATION")
pathway_fig = create_pathway_figure(current_state)
st.pyplot(pathway_fig)

st.warning(
    "Educational purpose only: This simulation is a simplified educational model designed for teaching and hypothesis generation. It does not represent clinical care, treatment guidance, or validated patient-specific predictions."
)
