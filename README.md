# Darcy–Weisbach Pipeline Screening Model

This repository contains a Python-based hydraulic screening model for turbulent pipe flow.  
Full theory, assumptions, and validation are documented in Darcy_Weisbach_Model_Validation.pdf.

This README only explains how to run the model.

## What you need

To run this model you need:

- Python   
- Matplotlib  

Install matplotlib with:

pip install matplotlib

## How to run

From the folder containing pipeline_model.py, run:

python pipeline_model.py

The program will guide you through selecting a fluid, a pipe material, and entering the pipe length, diameter, and flow velocity.  
It will then run the hydraulic simulation and display plots.

## Validation

All equations, assumption, limitations, hand calculations, and verification are provided in:

Darcy_Weisbach_Model_Validation.pdf
