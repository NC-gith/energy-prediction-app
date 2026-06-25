import streamlit as st
from google.cloud import aiplatform
from google.oauth2 import service_account
import json

PROJECT_ID = "758158295023"
LOCATION = "us-central1"
ENDPOINT_ID = "749313326038646784"

st.set_page_config(page_title="Energy Prediction App", page_icon="⚡", layout="centered")

st.title("⚡ Energy Consumption Prediction")
st.write("Predict monthly total electricity consumption using a Vertex AI AutoML regression model.")

st.sidebar.header("Project Information")
st.sidebar.write("**Model:** Vertex AI AutoML Regression")
st.sidebar.write("**Target:** Total kWh")
st.sidebar.write("**Inputs:** ZipCode, Month, Customer Class, Total Customers, Average kWh")

zipcode = st.text_input("Zip Code", "91901")

month_name = st.selectbox(
    "Month",
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"]
)
month = ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"].index(month_name) + 1

customer_class = st.selectbox(
    "Customer Class",
    ["A", "R", "C", "I"],
    help="Use the same class codes used in the original dataset."
)

total_customers = st.number_input("Total Customers", min_value=0.0, value=0.0, step=1.0)
average_kwh = st.number_input("Average kWh", min_value=0.0, value=0.0, step=1.0)

st.divider()

if st.button("Predict Total kWh"):
    if total_customers == 0 and average_kwh == 0:
        st.warning("This record represents zero customers and zero average consumption. Prediction may be close to zero or unstable.")
    
    try:
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
        predicted_value = prediction.predictions[0]

        st.success("Prediction completed successfully.")
        st.metric("Predicted Total kWh", f"{float(predicted_value):,.2f} kWh")

        st.write("### Input Summary")
        st.write(instance)

    except Exception as e:
        st.error("Prediction could not be completed.")
        st.write("Reason:")
        st.code(str(e))
        st.info("If the Vertex AI endpoint is undeployed or credentials are not connected, the app interface will still work but prediction will not run.")
