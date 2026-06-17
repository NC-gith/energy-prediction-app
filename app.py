import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
import json

PROJECT_ID = "758158295023"
LOCATION = "us-central1"
ENDPOINT_ID = "749313326038646784"

st.title("Energy Consumption Prediction App")

zipcode = st.text_input("Zip Code", "91901")
month = st.number_input("Month", min_value=1, max_value=12, value=7)
customer_class = st.selectbox("Customer Class", ["A", "R", "C", "I"])
total_customers = st.number_input("Total Customers", min_value=0.0, value=0.0)
average_kwh = st.number_input("Average kWh", min_value=0.0, value=0.0)

if st.button("Predict Total kWh"):
    credentials_info = json.loads(st.secrets["gcp_service_account"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}",
        credentials=credentials
    )

    instance = {
        "ZipCode": str(zipcode),
        "Month": float(month),
        "CustomerClass": str(customer_class),
        "TotalCustomers": float(total_customers),
        "AveragekWh": float(average_kwh)
    }

    prediction = endpoint.predict(instances=[instance])

    st.success(f"Predicted Total kWh: {prediction.predictions[0]}")
