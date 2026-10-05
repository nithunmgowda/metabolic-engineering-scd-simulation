# metabolic-engineering-scd-simulation

## Project description
This project is an educational simulation for a 2-month undergraduate case study focused on red blood cell metabolism in sickle cell disease. It uses simplified, normalized model equations to explore how glucose flux partitioning between glycolysis and the pentose phosphate pathway affects ATP, NADPH, ROS, and 2,3-BPG.

## Biological background
Red blood cells rely on glucose metabolism to support essential functions. In a simplified educational model:

- Glucose can be directed toward glycolysis, which contributes to ATP generation.
- Glucose can also be directed toward the pentose phosphate pathway (PPP), which contributes to NADPH generation.
- NADPH supports antioxidant and redox protection.
- Oxidative stress is represented as a simplified stress term that is partially offset by NADPH-supported protection.
- 2,3-BPG is represented as a glycolytic branch output related to oxygen affinity in the simplified model.

This is not a validated biochemical model of sickle cell disease and should not be interpreted as a clinical predictor.

## Literature-supported biological facts
The following are general biological concepts important to the educational framing of the project:

- RBCs depend on glucose metabolism for ATP generation.
- The pentose phosphate pathway contributes to NADPH production.
- NADPH supports antioxidant defense systems.
- Sickle cell disease is associated with elevated oxidative stress and altered redox balance.
- 2,3-BPG is a metabolite associated with hemoglobin oxygen affinity.

These concepts are used here in a simplified educational context only.

## Model assumptions
This project uses normalized, arbitrary units unless explicitly tied to a literature-supported parameter.

Important assumptions:

- Total glucose flux = 100 arbitrary units.
- Glycolysis fraction + PPP fraction = 1 in the model formulation.
- Disease oxidative stress is represented by a simplified scalar factor.
- ATP, NADPH, ROS, and 2,3-BPG are computed from simplified equations.
- The intervention is represented as a flux-rebalancing computational experiment, not as a proven therapy.
- The scenario values (e.g., 0.90/0.10, 0.95/0.05, and PPP increases from 0.05 to 0.25) are model assumptions, not experimental measurements.

## Simplified model equations
These are simplified model equations used for educational simulation only:

1. glycolysis_flux = glucose_flux × glycolysis_fraction
2. ppp_flux = glucose_flux × ppp_fraction
3. ATP = ATP_COEFFICIENT × glycolysis_flux
4. NADPH = NADPH_COEFFICIENT × ppp_flux
5. ROS = baseline_ROS + disease_stress − ROS_PROTECTION_COEFFICIENT × NADPH
   - Values are constrained to remain non-negative in the model.
6. 2,3-BPG = BPG_COEFFICIENT × glycolysis_flux

## Installation instructions
```bash
pip install -r requirements.txt
```

## How to run
```bash
streamlit run app.py
```

## Interpretation
The dashboard is designed to show that, under the model assumptions:

- Higher simulated NADPH indicates greater modeled antioxidant-supporting capacity.
- Lower simulated ROS indicates lower modeled oxidative stress.
- Increasing PPP contribution can increase simulated NADPH and may reduce modeled ROS in this simplified educational framework.

The model does not claim that any intervention cures sickle cell disease or is clinically proven.

## Limitations
- This is not a validated biochemical kinetic model.
- It is not a patient-specific clinical simulator.
- It does not represent enzyme kinetics, transcriptional regulation, or full metabolic network complexity.
- It is for learning and conceptual exploration only.

## Disclaimer
This project is an educational simplified model created for an undergraduate case study. It is not a clinical model, not a treatment simulator, and not a validated prediction tool for patient outcomes.

## Folder structure
```text
metabolic-engineering-scd-simulation/
├── app.py
├── model.py
├── plots.py
├── requirements.txt
├── README.md
└── tests/
    └── test_model.py
```
