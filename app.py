import numpy as np
import numpy_financial as npf

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
        "Annual Revenue ($)": revenue,
        "Out-of-Stock Recovery ($/yr)": out_of_stock_recovery,
        "Markdown Savings ($/yr)": markdown_savings,
        "Shrink Savings ($/yr)": shrink_savings,
        "Labor Savings ($/yr)": labor_savings,
        "Total Annual Benefit ($/yr)": total_annual_benefit,
        "ROI (%)": roi * 100,
        "NPV ($)": npv,
        "Payback Period (quarters)": quarters
    }
