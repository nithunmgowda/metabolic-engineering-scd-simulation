# Streamlit educational metabolic simulation for sickle cell disease
# This module stores simplified equations and model logic for the educational simulation.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd


BASELINE_ROS = 5.0


@dataclass
class ModelState:
    total_glucose_flux: float
    glycolysis_fraction: float
    ppp_fraction: float
    disease_stress: float
    atp_coefficient: float
    nadph_coefficient: float
    ros_protection_coefficient: float
    bpg_coefficient: float

    def __post_init__(self) -> None:
        self.total_glucose_flux = float(self.total_glucose_flux)
        self.glycolysis_fraction = float(self.glycolysis_fraction)
        self.ppp_fraction = float(self.ppp_fraction)
        self.disease_stress = float(self.disease_stress)
        self.atp_coefficient = float(self.atp_coefficient)
        self.nadph_coefficient = float(self.nadph_coefficient)
        self.ros_protection_coefficient = float(self.ros_protection_coefficient)
        self.bpg_coefficient = float(self.bpg_coefficient)


def enforce_fraction_pair(glycolysis_fraction: float, ppp_fraction: float) -> tuple[float, float]:
    """Keep the pair within biologically meaningful bounds and ensure total does not exceed 1."""
    glycolysis_fraction = max(0.0, min(float(glycolysis_fraction), 1.0))
    ppp_fraction = max(0.0, min(float(ppp_fraction), 1.0))

    total = glycolysis_fraction + ppp_fraction
    if total > 1.0:
        ppp_fraction = max(0.0, 1.0 - glycolysis_fraction)
    return glycolysis_fraction, ppp_fraction


def compute_fluxes(state: ModelState) -> Dict[str, float]:
    """Compute a single model output set using simplified model equations."""
    glyco, ppp = enforce_fraction_pair(state.glycolysis_fraction, state.ppp_fraction)

    glycolysis_flux = state.total_glucose_flux * glyco
    ppp_flux = state.total_glucose_flux * ppp

    atp = state.atp_coefficient * glycolysis_flux
    nadph = state.nadph_coefficient * ppp_flux
    ros = max(0.0, BASELINE_ROS + state.disease_stress - state.ros_protection_coefficient * nadph)
    bpg = state.bpg_coefficient * glycolysis_flux

    return {
        "glycolysis_fraction": glyco,
        "ppp_fraction": ppp,
        "glycolysis_flux": glycolysis_flux,
        "ppp_flux": ppp_flux,
        "ATP": atp,
        "NADPH": nadph,
        "ROS": ros,
        "2,3-BPG": bpg,
    }


def sensitivity_analysis(
    total_glucose_flux: float,
    disease_stress: float,
    atp_coefficient: float,
    nadph_coefficient: float,
    ros_protection_coefficient: float,
    bpg_coefficient: float,
    ppp_values: List[float] | None = None,
) -> pd.DataFrame:
    """Create a sensitivity table for PPP fractions between 0.05 and 0.30."""
    if ppp_values is None:
        ppp_values = np.linspace(0.05, 0.30, 11).tolist()

    rows = []
    for ppp in ppp_values:
        glyco = 1.0 - ppp
        state = ModelState(
            total_glucose_flux=total_glucose_flux,
            glycolysis_fraction=glyco,
            ppp_fraction=ppp,
            disease_stress=disease_stress,
            atp_coefficient=atp_coefficient,
            nadph_coefficient=nadph_coefficient,
            ros_protection_coefficient=ros_protection_coefficient,
            bpg_coefficient=bpg_coefficient,
        )
        output = compute_fluxes(state)
        rows.append(
            {
                "PPP_fraction": round(ppp, 4),
                "PPP_flux": round(output["ppp_flux"], 4),
                "Glycolysis_fraction": round(output["glycolysis_fraction"], 4),
                "ATP": round(output["ATP"], 4),
                "NADPH": round(output["NADPH"], 4),
                "ROS": round(output["ROS"], 4),
                "2,3-BPG": round(output["2,3-BPG"], 4),
            }
        )
    return pd.DataFrame(rows)


def compare_scenarios() -> Dict[str, Dict[str, float]]:
    """Return the baseline scenario definitions used in the dashboard."""
    normal = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.90,
        ppp_fraction=0.10,
        disease_stress=1.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    scd = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.95,
        ppp_fraction=0.05,
        disease_stress=1.8,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    intervention = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.80,
        ppp_fraction=0.20,
        disease_stress=1.4,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )

    outputs = {
        "Normal RBC": compute_fluxes(normal),
        "SCD-like": compute_fluxes(scd),
        "Simulated Intervention": compute_fluxes(intervention),
    }
    return outputs


def preset_values() -> Dict[str, Dict[str, float]]:
    """Return preset control values for the Streamlit app."""
    return {
        "Normal RBC": {
            "total_glucose_flux": 100.0,
            "glycolysis_fraction": 0.90,
            "ppp_fraction": 0.10,
            "disease_stress": 1.0,
            "atp_coefficient": 0.50,
            "nadph_coefficient": 0.80,
            "ros_protection_coefficient": 0.35,
            "bpg_coefficient": 0.45,
        },
        "SCD-like": {
            "total_glucose_flux": 100.0,
            "glycolysis_fraction": 0.95,
            "ppp_fraction": 0.05,
            "disease_stress": 1.8,
            "atp_coefficient": 0.50,
            "nadph_coefficient": 0.80,
            "ros_protection_coefficient": 0.35,
            "bpg_coefficient": 0.45,
        },
        "Simulated Intervention": {
            "total_glucose_flux": 100.0,
            "glycolysis_fraction": 0.80,
            "ppp_fraction": 0.20,
            "disease_stress": 1.4,
            "atp_coefficient": 0.50,
            "nadph_coefficient": 0.80,
            "ros_protection_coefficient": 0.35,
            "bpg_coefficient": 0.45,
        },
    }


def scenario_dataframe(states: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    rows = []
    for name, values in states.items():
        model = ModelState(**values)
        output = compute_fluxes(model)
        rows.append(
            {
                "Scenario": name,
                "Glycolysis": round(output["glycolysis_fraction"], 4),
                "PPP": round(output["ppp_fraction"], 4),
                "ATP": round(output["ATP"], 4),
                "NADPH": round(output["NADPH"], 4),
                "ROS": round(output["ROS"], 4),
                "2,3-BPG": round(output["2,3-BPG"], 4),
            }
        )
    return pd.DataFrame(rows)


def equation_text() -> List[str]:
    return [
        "Simplified model equations",
        "1. glycolysis_flux = glucose_flux × glycolysis_fraction",
        "2. ppp_flux = glucose_flux × ppp_fraction",
        "3. ATP = ATP_COEFFICIENT × glycolysis_flux",
        "4. NADPH = NADPH_COEFFICIENT × ppp_flux",
        "5. ROS = baseline_ROS + disease_stress − ROS_PROTECTION_COEFFICIENT × NADPH; values are kept at or above zero",
        "6. 2,3-BPG = BPG_COEFFICIENT × glycolysis_flux",
    ]


def validate_state(glycolysis_fraction: float, ppp_fraction: float) -> tuple[float, float]:
    """Ensure the two fractions satisfy the model assumption glycolysis + PPP = 1 where possible."""
    glyco, ppp = enforce_fraction_pair(glycolysis_fraction, ppp_fraction)
    total = glyco + ppp
    if total < 1.0:
        ppp = 1.0 - glyco
    return glyco, ppp


__all__ = [
    "BASELINE_ROS",
    "ModelState",
    "compute_fluxes",
    "enforce_fraction_pair",
    "validate_state",
    "sensitivity_analysis",
    "compare_scenarios",
    "preset_values",
    "scenario_dataframe",
    "equation_text",
]


if __name__ == "__main__":
    print("Model module loaded successfully.")
    print("Example outputs:")
    st = ModelState(100, 0.9, 0.1, 1.0, 0.5, 0.8, 0.35, 0.45)
    print(compute_fluxes(st))
