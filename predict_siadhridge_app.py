
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PredictADH", layout="centered")

st.title("🧪 PredictADH – Ridge Model for SIADH")

st.markdown("""
This app calculates the **probability of SIADH** using a Ridge regression model  
validated in our published study:  
**_Ciortea D.A. et al., “Impact of Hyponatremia and ADH Secretion in MIS-C and COVID-19: An Integrative Approach of Prognostic and Diagnostic Markers,” CIIMB, 2024_**
""")

st.markdown("### 🧬 Model formula:")
st.markdown(r'''
*Intercept* = -2.336  
$\beta_1$ = -0.603 (Serum sodium)  
$\beta_2$ = -0.185 (Serum osmolality)  
$\beta_3$ = +1.136 (U/P ratio)  
$\beta_4$ = +0.211 (Hospital stay)
''')

st.markdown("---")

# User inputs with number_input
na = st.number_input("Serum sodium (mmol/L)", value=135.0)
s_osm = st.number_input("Serum osmolality (mOsm/kg)", value=280.0)
up_ratio = st.number_input("U/P osmolality ratio", value=2.0)
hosp_days = st.number_input("Length of hospital stay (days)", value=7.0)

# Means and SDs from full cohort (Table 7)
mean_values = {'na': 137.59, 's_osm': 281.33, 'up_ratio': 1.96, 'hosp_days': 8.40}
std_values = {'na': 7.01, 's_osm': 6.81, 'up_ratio': 1.29, 'hosp_days': 6.86}

# Standardize inputs
z_na = (na - mean_values['na']) / std_values['na']
z_sosm = (s_osm - mean_values['s_osm']) / std_values['s_osm']
z_upratio = (up_ratio - mean_values['up_ratio']) / std_values['up_ratio']
z_hosp = (hosp_days - mean_values['hosp_days']) / std_values['hosp_days']

# Ridge regression formula (from Table 12)
intercept = -2.336
prob_score = intercept + (-0.603)*z_na + (-0.185)*z_sosm + (1.136)*z_upratio + (0.211)*z_hosp
probability = 1 / (1 + np.exp(-prob_score))

# Results
st.markdown("### 🎯 Predicted SIADH probability: **{:.2f}**".format(probability))

if probability < 0.33:
    st.success("🟢 Low probability of SIADH")
elif probability < 0.66:
    st.warning("🟠 Moderate probability of SIADH")
else:
    st.error("🔴 High probability of SIADH")

# Plot
fig, ax = plt.subplots(figsize=(5, 1.5))
ax.barh(['SIADH Probability'], [probability], color='royalblue')
ax.axvline(0.33, color='orange', linestyle='--', label='Moderate risk')
ax.axvline(0.66, color='red', linestyle='--', label='High risk')
ax.set_xlim([0, 1])
ax.set_xlabel("Probability")
ax.legend(loc='upper right')
st.pyplot(fig)
