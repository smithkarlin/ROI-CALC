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
    st.header("Warehouse / DC RFID ROI")

shipments_per_year = st.number_input(
    "Annual shipments",
    min_value=0,
    value=500_000,
    help="How many boxes or orders your warehouse ships in one year."
)

lost_shipment_rate = st.number_input(
    "Lost or mis-shipped rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=1.0,
    help="Out of 100 shipments, how many are lost or sent to the wrong place."
)

avg_shipment_cost = st.number_input(
    "Average cost per shipment ($)",
    min_value=0.0,
    value=120.0,
    help="How much money you lose when one shipment goes missing or is shipped incorrectly."
)

rfid_loss_reduction_pct = st.number_input(
    "Loss reduction with RFID (%)",
    min_value=0.0,
    max_value=100.0,
    value=50.0,
    help="How much RFID reduces lost shipments. If RFID cuts losses in half, enter 50%."
)

warehouse_headcount = st.number_input(
    "Warehouse headcount",
    min_value=0,
    value=50,
    help="How many people currently work in the warehouse."
)

avg_fully_loaded_cost = st.number_input(
    "Average fully loaded cost per employee ($/year)",
    min_value=0.0,
    value=65_000.0,
    help="What one employee costs per year including pay, benefits, and taxes."
)

headcount_reduction = st.number_input(
    "Headcount reduction with RFID",
    min_value=0,
    value=5,
    help="How many fewer people you expect to need after RFID improves efficiency."
)
rfid_annual_cost = st.number_input(
    "Estimated annual RFID program cost ($)",
    min_value=0.0,
    value=250_000.0,
    help="About how much you think RFID would cost per year, including tags, hardware, software, and support."
)

 # --- Calculations ---
lost_shipments = shipments_per_year * (lost_shipment_rate / 100)
annual_loss_cost = lost_shipments * avg_shipment_cost
loss_savings = annual_loss_cost * (rfid_loss_reduction_pct / 100)
labor_savings = headcount_reduction * avg_fully_loaded_cost
total_annual_benefit = loss_savings + labor_savings
net_annual_value = total_annual_benefit - rfid_annual_cost

# --- Outputs ---
st.subheader("Estimated Annual Benefit")
st.write(f"Lost shipment savings: ${loss_savings:,.0f}")
st.write(f"Labor savings: ${labor_savings:,.0f}")
st.divider()

st.subheader("Total Annual RFID Benefit")
st.write(f"${total_annual_benefit:,.0f}")
st.subheader("Net Annual Value")
st.write(f"${net_annual_value:,.0f}")


