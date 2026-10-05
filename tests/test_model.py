import math

import numpy as np
import pandas as pd

from model import ModelState, compute_fluxes, enforce_fraction_pair, preset_values, validate_state


def test_fraction_pair_sums_to_one():
    glyco, ppp = validate_state(0.75, 0.25)
    assert math.isclose(glyco + ppp, 1.0, rel_tol=1e-9, abs_tol=1e-9)


def test_increasing_ppp_increases_nadph_when_other_parameters_are_fixed():
    state_low = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.90,
        ppp_fraction=0.10,
        disease_stress=1.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    state_high = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.75,
        ppp_fraction=0.25,
        disease_stress=1.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    low = compute_fluxes(state_low)
    high = compute_fluxes(state_high)
    assert high["NADPH"] > low["NADPH"]


def test_ros_never_becomes_negative():
    state = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.95,
        ppp_fraction=0.05,
        disease_stress=10.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.10,
        bpg_coefficient=0.45,
    )
    result = compute_fluxes(state)
    assert result["ROS"] >= 0.0


def test_increasing_glucose_flux_increases_glycolytic_flux():
    state_low = ModelState(
        total_glucose_flux=50,
        glycolysis_fraction=0.80,
        ppp_fraction=0.20,
        disease_stress=1.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    state_high = ModelState(
        total_glucose_flux=100,
        glycolysis_fraction=0.80,
        ppp_fraction=0.20,
        disease_stress=1.0,
        atp_coefficient=0.50,
        nadph_coefficient=0.80,
        ros_protection_coefficient=0.35,
        bpg_coefficient=0.45,
    )
    low = compute_fluxes(state_low)
    high = compute_fluxes(state_high)
    assert high["glycolysis_flux"] > low["glycolysis_flux"]


def test_preset_conditions_work_correctly():
    presets = preset_values()
    assert set(presets.keys()) == {"Normal RBC", "SCD-like", "Simulated Intervention"}
    assert presets["Normal RBC"]["glycolysis_fraction"] == 0.90
    assert presets["SCD-like"]["ppp_fraction"] == 0.05
    assert presets["Simulated Intervention"]["ppp_fraction"] == 0.20


def test_fraction_pair_validation_caps_total_at_one():
    glyco, ppp = enforce_fraction_pair(0.90, 0.40)
    assert glyco + ppp <= 1.0
