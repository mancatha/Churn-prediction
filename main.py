from fastapi import FastAPI, Query
import joblib
from pydantic import BaseModel
import pandas as pd
from fastapi import HTTPException
import warnings
from sklearn.exceptions import DataConversionWarning


app = FastAPI(title="Customer Churn Analysis API")

class ChurnFeatures(BaseModel):
    REGION: str
    TENURE: str
    MONTANT: float
    FREQUENCE_RECH: float
    REVENUE: float
    ARPU_SEGMENT: float
    FREQUENCE: float
    DATA_VOLUME: float
    ON_NET: float
    ORANGE: float
    TIGO: float
    REGULARITY: float
    FREQ_TOP_PACK: float

    

# Load your model
pipeline_1 = joblib.load('model/dt.joblib')
pipeline = joblib.load('model/gb.joblib')
pipeline_2 = joblib.load('model/xgb.joblib')




    # Define the available models
models = {
    
    "dt": pipeline_1,
    "gb": pipeline,
    "xgb": pipeline_2,
    }


@app.get('/')
def home():
   return "Customer churn"


@app.get('/info')
def appinfo():
    return 'Customer churn prediction: This is my interface'

@app.post('/predict_churn')
def predict_churn(
    churn_features: ChurnFeatures,
    selected_model: str = Query("dt", description="Select the model for prediction")
):
    # Convert input features to a DataFrame
    df = pd.DataFrame([churn_features.model_dump()])

   # Check if the specified model is valid
    if selected_model not in models:
        return {"error": "Invalid model specified"}

    # Perform prediction using the selected pipeline
    try:
        selected_pipeline = models[selected_model]
        probabilities = selected_pipeline.predict_proba(df)
        probability_score = probabilities[0][1]
    except AttributeError:
        probability_score = None
    
    # Interpret prediction based on probability score
    churn_status = " Customer Churn" if probability_score == 1 else "Customer Not Churn" 

    # Create a dictionary for the response
    prediction_data = {
        "selected_model": selected_model,
        "probability_score": probability_score,
        "churn_status": churn_status,
    }

    return prediction_data
