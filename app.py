import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf

# -----------------------------
# Function to calculate RFID ROI
# -----------------------------
def calculate_rfid_roi(inputs):
    revenue = inputs["items_per_year"] * inputs["average_unit_retail"]
    
    # Revenue uplift from improved availability
    accuracy_delta = inputs["inventory_accuracy_rfid"] - inputs["inventory_accuracy_current"]
    out_of_stock_recovery = revenue * accuracy_delta * 0.045
    
    # Markdown savings
    markdown_savings = revenue * (inputs["current_markdown_pct"] - inputs["rfid_markdown_pct"])
    
    # Shrink savings
    shrink_savings = revenue * (inputs["current_shrink_pct"] - inputs["rfid_shrink_pct"])
    
    # Labor savings (75% reduction assumption)
    labor_savings = (inputs["inventory_counts_per_year"] *
                     inputs["labor_hours_per_count"] *
                     inputs["labor_cost_per_hour"] *
                     0.75)
    
    total_annual_benefit = out_of_stock_recovery + markdown_savings + shrink_savings + labor_savings
    
    # Cash flow modeling
    cash_flows = [-inputs["initial_deployment_cost"]] + \
                 [total_annual_benefit - inputs["annual_ongoing_cost"] for _ in range(inputs["years"])]
    
    npv = npf.npv(inputs["discount_rate"], cash_flows)
    roi = (sum(cash_flows[1:]) - inputs["initial_deployment_cost"]) / inputs["initial_deployment_cost"]
    
    # Payback period (quarters)
    cumulative = -inputs["initial_deployment_cost"]
    quarters = 0
    quarterly_net = (total_annual_benefit - inputs["annual_ongoing_cost"]) / 4
    
    while cumulative < 0 and quarters < inputs["years"] * 4:
        cumulative += quarterly_net
        quarters += 1
    
    return {
        "Annual Revenue": revenue,
        "Out-of-Stock Recovery": out_of_stock_recovery,
        "Markdown Savings": markdown_savings,
        "Shrink Savings": shrink_savings,
        "Labor Savings": labor_savings,
        "Total Annual Benefit": total_annual_benefit,
        "ROI (%)": roi * 100,
        "NPV": npv,
        "Payback Period (quarters)": quarters
    }

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="RFID ROI Calculator", layout="wide")
st.title("RFID ROI Calculator")
st.write("Estimate potential ROI from implementing RFID technology in your stores.")

# ------------
# Input widgets
# ------------
st.header("Scenario Inputs")

items_per_year = st.number_input("Items Sold per Year", min_value=0, value=980_000, step=10_000)
average_unit_retail = st.number_input("Average Unit Retail (USD)", min_value=0.0, value=10.0, step=0.5)

inventory_accuracy_current = st.slider("Current Inventory Accuracy (%)", 50, 95, 66) / 100
inventory_accuracy_rfid = st.slider("Inventory Accuracy with RFID (%)", 80, 99, 95) / 100

current_markdown_pct = st.slider("Current Markdown (%)", 0.0, 50.0, 10.0) / 100
rfid_markdown_pct = st.slider("Expected Markdown with RFID (%)", 0.0, 50.0, 7.0) / 100

current_shrink_pct = st.number_input("Current Shrink (% of Revenue)", min_value=0.0, max_value=50.0, value=0.45) / 100
rfid_shrink_pct = st.number_input("Expected Shrink with RFID (% of Revenue)", min_value=0.0, max_value=50.0, value=0.20) / 100

inventory_counts_per_year = st.number_input("Number of Inventory Counts per Year", min_value=0, value=13)
labor_hours_per_count = st.number_input("Labor Hours per Count", min_value=0, value=178)
labor_cost_per_hour = st.number_input("Labor Cost per Hour (USD)", min_value=0.0, value=15.0)

initial_deployment_cost = st.number_input("Initial Deployment Cost (USD)", min_value=0, value=1_100_000)
annual_ongoing_cost = st.number_input("Annual Ongoing Cost (USD)", min_value=0, value=69_000)
discount_rate = st.slider("Discount Rate (%)", 0.0, 20.0, 10.0) / 100
years = st.number_input("Investment Horizon (Years)", min_value=1, value=5)

# ----------------
# Build inputs dict
# ----------------
inputs = {
    "items_per_year": items_per_year,
    "average_unit_retail": average_unit_retail,
    "inventory_accuracy_current": inventory_accuracy_current,
    "inventory_accuracy_rfid": inventory_accuracy_rfid,
    "current_markdown_pct": current_markdown_pct,
    "rfid_markdown_pct": rfid_markdown_pct,
    "current_shrink_pct": current_shrink_pct,
    "rfid_shrink_pct": rfid_shrink_pct,
    "inventory_counts_per_year": inventory_counts_per_year,
    "labor_hours_per_count": labor_hours_per_count,
    "labor_cost_per_hour": labor_cost_per_hour,
    "initial_deployment_cost": initial_deployment_cost,
    "annual_ongoing_cost": annual_ongoing_cost,
    "discount_rate": discount_rate,
    "years": years
}

# ----------------
# Calculate and display results
# ----------------
if st.button("Calculate ROI"):
    results = calculate_rfid_roi(inputs)
    
    st.subheader("Key Metrics")
    st.metric("ROI (%)", f"{results['ROI (%)']:.1f}")
    st.metric("Net Present Value (USD)", f"${results['NPV']:,}")
    st.metric("Payback Period (quarters)", f"{results['Payback Period (quarters)']}")
    st.metric("Total Annual Benefit (USD/yr)", f"${results['Total Annual Benefit']:,}")
    
    st.subheader("Breakdown of Benefits")
    # Create a safe table without $ or parentheses in keys
    df = pd.DataFrame({
        "Benefit": [
            "Out-of-Stock Recovery",
            "Markdown Savings",
            "Shrink Savings",
            "Labor Savings"
        ],
        "Amount (USD)": [
            results["Out-of-Stock Recovery"],
            results["Markdown Savings"],
            results["Shrink Savings"],
            results["Labor Savings"]
        ]
    })
    st.table(df)

    st.markdown("### Next Step")
    st.write("If you want to implement RFID in your stores, consider booking a consultation to validate your scenario and maximize ROI.")
