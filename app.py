import streamlit as st

st.set_page_config(page_title="Energy Prediction App", page_icon="⚡", layout="centered")

st.title("⚡ Energy Consumption Prediction App")
st.write("This app predicts total electricity consumption using a Google Vertex AI AutoML regression model.")

st.sidebar.header("Project Information")
st.sidebar.write("**Model:** Vertex AI AutoML Regression")
st.sidebar.write("**Target:** Total kWh")
st.sidebar.write("**Status:** Web interface ready")
st.sidebar.write("**Note:** This demo version estimates Total kWh using Total Customers × Average kWh.")

zipcode = st.text_input("Zip Code", "91901")

month_name = st.selectbox(
    "Month",
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"]
)

customer_class = st.selectbox("Customer Class", ["A", "R", "C", "I"])
total_customers = st.number_input("Total Customers", min_value=0.0, value=0.0, step=1.0)
average_kwh = st.number_input("Average kWh", min_value=0.0, value=0.0, step=1.0)

st.divider()

if st.button("Predict Total kWh"):
    estimated_value = total_customers * average_kwh

    st.success("Demo prediction generated.")
    st.metric("Estimated Total kWh", f"{estimated_value:,.2f} kWh")

    st.write("### Input Summary")
    st.write({
        "ZipCode": zipcode,
        "Month": month_name,
        "CustomerClass": customer_class,
        "TotalCustomers": total_customers,
        "AveragekWh": average_kwh
    })
