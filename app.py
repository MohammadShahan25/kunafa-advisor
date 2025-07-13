import streamlit as st
import matplotlib.pyplot as plt
from datetime import date
from fpdf import FPDF
import urllib.request
import os
import io

# Download Logo
logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx_Vn_o8B1EQTwLxwIBPRDcbwidjzzWEVi2Rw0koU4ICvj-ttTd-CDhvgeIRd05m2xtuY&usqp=CAU"
logo_path = "kunafa_fullpage_logo.jpg"
urllib.request.urlretrieve(logo_url, logo_path)

st.set_page_config(page_title="Kunafa Bytes Finance Analyzer", layout="centered")
st.title("🍮 Kunafa Bytes Smart Finance Analyzer")

with st.form("finance_form"):
    st.subheader("Expenses")
    local = st.number_input("Local Purchase Rs.", min_value=0.0)
    pune = st.number_input("Pune Purchase Rs.", min_value=0.0)
    daily = st.number_input("Daily Purchase Rs.", min_value=0.0)
    rent = st.number_input("Rent Rs.", min_value=0.0)
    elec = st.number_input("Electricity Rs.", min_value=0.0)
    unex = st.number_input("Unexpected Costs Rs.", min_value=0.0)
    salary = st.number_input("Staff Salary Rs.", min_value=0.0)
    items = st.number_input("Furniture/Items Rs.", min_value=0.0)
    market = st.number_input("Marketing Rs.", min_value=0.0)
    tax = st.number_input("GST / Tax Deduction Rs.", min_value=0.0)

    st.subheader("Sales")
    zomato_sales = st.number_input("Zomato Sales Rs.", min_value=0.0)
    swiggy_sales = st.number_input("Swiggy Sales Rs.", min_value=0.0)
    zomato_commission = st.number_input("Zomato Commission Rs.", min_value=0.0)
    swiggy_commission = st.number_input("Swiggy Commission Rs.", min_value=0.0)
    dine_in = st.number_input("Dine-in Revenue Rs.", min_value=0.0)
    outdoor = st.number_input("Outdoor Revenue (Weddings, Events, Deliveries) Rs.", min_value=0.0)

    st.subheader("People")
    customers = st.number_input("Total Customers this month", min_value=1)
    staff = st.number_input("Total Staff", min_value=1)

    st.subheader("Metadata")
    city = st.text_input("City", value="Udaipur")
    month = st.text_input("Month", value="July")
    year = st.text_input("Year", value="2025")

    submitted = st.form_submit_button("Generate Report")

if submitted:
    expenses = {
        "Local Purchase": local,
        "Pune Purchase": pune,
        "Daily Purchase": daily,
        "Rent": rent,
        "Electricity": elec,
        "Unexpected Costs": unex,
        "Salary": salary,
        "Furniture/Items": items,
        "Marketing": market,
        "Zomato Commission": zomato_commission,
        "Swiggy Commission": swiggy_commission,
        "GST / Tax": tax
    }

    income_sources = {
        "Dine-in": dine_in,
        "Outdoor (Events & Delivery)": outdoor,
        "Zomato": zomato_sales,
        "Swiggy": swiggy_sales
    }

    total_expenses = sum(expenses.values())
    total_income = sum(income_sources.values())
    net_profit = total_income - total_expenses
    profit_margin = (net_profit / total_income * 100) if total_income else 0
    expense_ratio = (total_expenses / total_income * 100) if total_income else 0
    marketing_roi = (total_income / market) if market else 0
    avg_spend_per_customer = total_income / customers if customers else 0
    profit_per_staff = net_profit / staff if staff else 0
    avg_daily_profit = net_profit / 30
    projected_annual_profit = net_profit * 12
    break_even_income = total_expenses
    recommended_savings = total_income * 0.15

    st.success("Report Generated!")
    st.metric("Net Profit", f"Rs.{net_profit:,.2f}", delta=f"{profit_margin:.2f}% margin")
    st.metric("Total Income", f"Rs.{total_income:,.2f}")
    st.metric("Total Expenses", f"Rs.{total_expenses:,.2f}")
    st.metric("Avg Spend per Customer", f"Rs.{avg_spend_per_customer:,.2f}")
    st.metric("Profit per Staff", f"Rs.{profit_per_staff:,.2f}")

    # Charts
    st.subheader("📊 Financial Charts")
    chart_paths = []

    # Expense Pie Chart
    fig1, ax1 = plt.subplots()
    ax1.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
    fig1.savefig("chart1.png")
    chart_paths.append("chart1.png")

    # Income Bar Chart
    fig2, ax2 = plt.subplots()
    ax2.bar(income_sources.keys(), income_sources.values(), color='teal')
    ax2.set_ylabel("Revenue (Rs.)")
    ax2.set_title("Income Sources")
    st.pyplot(fig2)
    fig2.savefig("chart2.png")
    chart_paths.append("chart2.png")

    # Profit Breakdown Chart
    fig3, ax3 = plt.subplots()
    ax3.bar(["Income", "Expenses", "Net Profit"], [total_income, total_expenses, net_profit], color=['green', 'red', 'blue'])
    ax3.set_title("Profit Breakdown")
    st.pyplot(fig3)
    fig3.savefig("chart3.png")
    chart_paths.append("chart3.png")

    # Zomato vs Swiggy Sales
    fig4, ax4 = plt.subplots()
    ax4.bar(["Zomato", "Swiggy"], [zomato_sales, swiggy_sales], color=['orange', 'purple'])
    ax4.set_title("Zomato vs Swiggy")
    st.pyplot(fig4)
    fig4.savefig("chart4.png")
    chart_paths.append("chart4.png")

    # Top 5 Expenses
    top5 = dict(sorted(expenses.items(), key=lambda item: item[1], reverse=True)[:5])
    fig5, ax5 = plt.subplots()
    ax5.barh(list(top5.keys()), list(top5.values()), color='tomato')
    ax5.invert_yaxis()
    ax5.set_title("Top 5 Expense Categories")
    st.pyplot(fig5)
    fig5.savefig("chart5.png")
    chart_paths.append("chart5.png")

    # PDF Export
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Kunafa Bytes Finance Report", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"City: {city}\nMonth: {month} {year}\nDate: {date.today()}\n\nNet Profit: Rs.{net_profit:,.2f}\nProfit Margin: {profit_margin:.2f}%\nTotal Income: Rs.{total_income:,.2f}\nTotal Expenses: Rs.{total_expenses:,.2f}\nMarketing ROI: {marketing_roi:.2f}x\nAverage Spend per Customer: Rs.{avg_spend_per_customer:.2f}\nProfit per Staff: Rs.{profit_per_staff:.2f}\nAnnual Projected Profit: Rs.{projected_annual_profit:,.2f}")
    for img in chart_paths:
        pdf.add_page()
        pdf.image(img, x=10, y=30, w=180)

    pdf_path = "finance_report.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("📥 Download Full PDF Report", f, file_name=pdf_path)

    # Clean Up
    for c in chart_paths:
        os.remove(c)
    os.remove(pdf_path)
    os.remove(logo_path)

    # Prompt for AI Analysis
    st.subheader("💬 Prompt for Strategic AI Analysis")
    analysis_prompt = f"""
You are a business analyst AI helping Kunafa Bytes (Udaipur & Ahmedabad branches), a dessert restaurant that earns via dine-in, delivery, and outdoor stalls at weddings/events.

Monthly Financial Report:
- Local Purchase: Rs.{local}
- Pune Purchase: Rs.{pune}
- Daily Purchase: Rs.{daily}
- Rent: Rs.{rent}
- Electricity: Rs.{elec}
- Unexpected Costs: Rs.{unex}
- Salary: Rs.{salary}
- Furniture/Items: Rs.{items}
- Marketing: Rs.{market}
- Zomato Commission: Rs.{zomato_commission}
- Swiggy Commission: Rs.{swiggy_commission}
- GST / Tax: Rs.{tax}

Income:
- Dine-in: Rs.{dine_in}
- Outdoor Events & Delivery: Rs.{outdoor}
- Zomato Sales: Rs.{zomato_sales}
- Swiggy Sales: Rs.{swiggy_sales}

Summary:
- Total Income: Rs.{total_income:,.2f}
- Total Expenses: Rs.{total_expenses:,.2f}
- Net Profit: Rs.{net_profit:,.2f}
- Profit Margin: {profit_margin:.2f}%
- Expense Ratio: {expense_ratio:.2f}%
- Marketing ROI: {marketing_roi:.2f}x
- Avg. Spend/Customer: Rs.{avg_spend_per_customer:.2f}
- Profit per Staff: Rs.{profit_per_staff:.2f}
- Avg. Daily Profit: Rs.{avg_daily_profit:.2f}
- Projected Annual Profit: Rs.{projected_annual_profit:,.2f}
- Break-even Income: Rs.{break_even_income:,.2f}

Please provide:
1. A brief financial health check.
2. Overspending or red flags.
3. Suggestions to cut costs or improve profit.
4. Marketing or tech recommendations for a dessert restaurant.
"""
    st.code(analysis_prompt, language="markdown")
