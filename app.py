import streamlit as st

st.set_page_config(page_title="RFID ROI Calculator", layout="centered")

st.title("RFID ROI Calculator")

# --- Select use case ---
use_case = st.selectbox(
    "Select your operation type:",
    ["Retail Store", "Warehouse / Distribution Center"]
)

st.divider()

# ======================
# RETAIL CALCULATOR
# ======================
if use_case == "Retail Store":
    st.header("Retail RFID ROI")

    items_per_year = st.number_input(
        "Annual units sold",
        min_value=0,
        value=1_000_000
    )

    avg_unit_retail = st.number_input(
        "Average unit retail ($)",
        min_value=0.0,
        value=25.0
    )

    shrink_rate = st.number_input(
        "Current shrink (%)",
        min_value=0.0,
        max_value=100.0,
        value=1.5
    )

    assumed_shrink_reduction = 0.30  # 30%

    annual_revenue = items_per_year * avg_unit_retail
    shrink_savings = annual_revenue * (shrink_rate / 100) * assumed_shrink_reduction

    st.subheader("Estimated Annual Benefit")
    st.write(f"Shrink reduction savings: ${shrink_savings:,.0f}")

# ======================
# WAREHOUSE CALCULATOR
# ======================
else:
    st.header("Warehouse RFID ROI")

    shipments_per_year = st.number_input(
        "Annual shipments",
        min_value=0,
        value=500_000
    )

    labor_cost_per_shipment = st.number_input(
        "Labor cost per shipment ($)",
        min_value=0.0,
        value=3.50
    )

    labor_reduction_pct = st.number_input(
        "Labor reduction with RFID (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0
    )

    annual_labor_cost = shipments_per_year * labor_cost_per_shipment
    labor_savings = annual_labor_cost * (labor_reduction_pct / 100)

    st.subheader("Estimated Annual Benefit")
    st.write(f"Labor savings: ${labor_savings:,.0f}")
