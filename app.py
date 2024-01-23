import streamlit as st
import pandas as pd
import requests

# Function to predict churn using FastAPI
def predict_churn_interface(TENURE, MONTANT, FREQUENCE_RECH, REVENUE, ARPU_SEGMENT, FREQUENCE,
                             DATA_VOLUME, ON_NET, ORANGE, TIGO, REGULARITY, FREQ_TOP_PACK, REGION, selected_model):

    # Create input_data dictionary
    input_data = {
        "TENURE": TENURE,
        "REGION": REGION,
        "MONTANT": MONTANT,
        "FREQUENCE_RECH": FREQUENCE_RECH,
        "REVENUE": REVENUE,
        "ARPU_SEGMENT": ARPU_SEGMENT,
        "FREQUENCE": FREQUENCE,
        "DATA_VOLUME": DATA_VOLUME,
        "ON_NET": ON_NET,
        "ORANGE": ORANGE,
        "TIGO": TIGO,
        "REGULARITY": REGULARITY,
        "FREQ_TOP_PACK": FREQ_TOP_PACK,
        "selected_model": selected_model  # Add selected_model to input_data
    }

    # Send data to FastAPI for prediction
    response = requests.post("http://127.0.0.1:8000/predict_churn", json=input_data)
    prediction_data = response.json()

    # Extract probability score and churn status from the API response
    probability_score = prediction_data.get("probability_score", "N/A")
    churn_status = prediction_data.get("churn_status", "N/A")
   

     # Display prediction result in Streamlit
    st.write(f"Prediction: {churn_status}")
    st.write(f"Probability Score: {probability_score}")
    st.write(f"selected_model: {selected_model}")

# Set up interface
# Adding title with color
st.markdown("<h2 style='color: blue;'>Churn Prediction App</h2>", unsafe_allow_html=True)
# Adding sidebar with description
st.sidebar.markdown("## App Description")
st.sidebar.write("This app predicts churn using the provided input features.")
st.sidebar.write("Adjust the sliders to input your data and click 'Predict' to get the result.")

# Adding columns
left_column, right_column = st.columns(2)

# Inputs
input_data = {
    "TENURE": left_column.selectbox("What is the duration of your network?", ['I 18-21 month', 'K > 24 months', 'G 12-15 months',
                                                                              'J 21-24 months', 'H 15-18 months', 'F 9-12 months',
                                                                              'E 6-9 months', 'D 3-6 months']),
    "REGION": right_column.selectbox("What is Region are you from?",['MATAM', 'DAKAR', 'SAINT-LOUIS', 'TAMBACOUNDA', 'FATICK', 'LOUGA', 'KAFFRINE',
                                                                    'THIES', 'DIOURBEL', 'KOLDA', 'KAOLACK', 'ZIGUINCHOR', 'SEDHIOU', 'KEDOUGOU']),
    "MONTANT": left_column.slider("What is your top-amount?", 0, 800, 0),
    "FREQUENCE_RECH": left_column.slider("What is the number of times you refilled your bundle?", 0, 200, 0),
    "REVENUE": right_column.slider("What is your monthly income", 0, 10000, 200),
    "ARPU_SEGMENT": right_column.slider("What is your income over 90 days / 3", 0, 500000, 0),
    "FREQUENCE": right_column.slider("How often do you use the service", 0, 200, 0),
    "DATA_VOLUME": right_column.slider("How many times do you have connections", 0, 1000, 0),
    "ON_NET": left_column.slider("How many times do you do inter expresso calls", 0, 1000, 0),
    "ORANGE": left_column.slider("How many times do you use orange to make calls (tigo)", 0, 100, 0),
    "TIGO": right_column.slider("How many times do you use tigo networks", 0, 100, 0),
    "REGULARITY": left_column.slider("How many times are you active for 90 days", 0, 100, 0),
    "FREQ_TOP_PACK": left_column.slider("How many times have you been activated to the top pack packages", 0, 1000, 0),
}
 
  # Dropdown for model selection
selected_model = st.sidebar.selectbox("Select Model", ["xgb", "dt", "gb"], key="model_selector")

# Call prediction function when a button is clicked
if st.button("Predict", key="predict_button", help="Click to predict"):
    # Make sure selected_model is added to input_data 
    input_data["selected_model"] = selected_model  # Use the same key here
    predict_churn_interface(**input_data)

