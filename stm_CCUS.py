import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Interactive Carbon Emissions Model with CCUS")

# Sliders for user input
initial_emissions = st.sidebar.slider("Initial CO₂ Emissions (Mt)", min_value=500.0, max_value=2000.0, value=1000.0, step=50.0)
reduction_rate = st.sidebar.slider("Annual Reduction Rate (%)", min_value=0.0, max_value=5.0, value=1.5, step=0.1)
ccus_start = st.sidebar.slider("CCUS Start Year", min_value=2025, max_value=2045, value=2030, step=1)
ccus_capture = st.sidebar.slider("CCUS Growth Rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)

# Run the emissions model
years = list(range(2025, 2051))
emissions = []
ccus = []
net_emissions = []

current_emissions = initial_emissions
current_ccus = 0

for year in years:
    emissions.append(current_emissions)
    if year >= ccus_start:
        current_ccus += current_emissions * (ccus_capture / 100)
    ccus.append(min(current_ccus, current_emissions))
    net_emissions.append(max(current_emissions - current_ccus, 0))
    current_emissions *= (1 - reduction_rate / 100)

# Create dataframe and plot
df = pd.DataFrame({
    'Year': years,
    'Baseline Emissions': emissions,
    'CCUS Capture': ccus,
    'Net Emissions': net_emissions
})

st.line_chart(df.set_index('Year'))

# Optional: also show the raw data
if st.checkbox("Show raw data"):
    st.dataframe(df)

