from flask import Flask, render_template, request, send_file
import pandas as pd
import joblib
import os
import uuid

app = Flask(__name__)

# ============================================================
# PATHS
# ============================================================

MODEL_PATH = "models/churn_model.pkl"
MODEL_INFO_PATH = "models/model_info.pkl"
DATASET_PATH = "data/dataset.csv"

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "predictions"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ============================================================
# REQUIRED MODEL FEATURES
# ============================================================

REQUIRED_COLUMNS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges"
]
# ============================================================
# LOAD TRAINED MODEL
# ============================================================

print("=" * 60)
print("CUSTOMER CHURN INTELLIGENCE PLATFORM")
print("=" * 60)

# Check if trained model exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "churn_model.pkl not found. "
        "Please run train_model.py first."
    )

# Load trained model
model = joblib.load(MODEL_PATH)

print("☑ Churn model loaded successfully!")


# ============================================================
# LOAD MODEL INFORMATION
# ============================================================

if os.path.exists(MODEL_INFO_PATH):

    model_info = joblib.load(MODEL_INFO_PATH)

    print("☑ Model information loaded successfully!")

else:

    model_info = {}

    print("⚠ Model information file not found.")


print("=" * 60)
# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        model_info=model_info
    )


# ============================================================
# SINGLE CUSTOMER PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # COLLECT CUSTOMER DATA
        # ----------------------------------------------------

        customer_data = {

            "gender": request.form.get("gender"),

            "SeniorCitizen": int(
                request.form.get("SeniorCitizen")
            ),

            "Partner": request.form.get("Partner"),

            "Dependents": request.form.get("Dependents"),

            "tenure": int(
                request.form.get("tenure")
            ),

            "PhoneService": request.form.get("PhoneService"),

            "MultipleLines": request.form.get("MultipleLines"),

            "InternetService": request.form.get(
                "InternetService"
            ),

            "OnlineSecurity": request.form.get(
                "OnlineSecurity"
            ),

            "OnlineBackup": request.form.get(
                "OnlineBackup"
            ),

            "DeviceProtection": request.form.get(
                "DeviceProtection"
            ),

            "TechSupport": request.form.get(
                "TechSupport"
            ),

            "StreamingTV": request.form.get(
                "StreamingTV"
            ),

            "StreamingMovies": request.form.get(
                "StreamingMovies"
            ),

            "Contract": request.form.get(
                "Contract"
            ),

            "PaperlessBilling": request.form.get(
                "PaperlessBilling"
            ),

            "PaymentMethod": request.form.get(
                "PaymentMethod"
            ),

            "MonthlyCharges": float(
                request.form.get("MonthlyCharges")
            ),

            "TotalCharges": float(
                request.form.get("TotalCharges")
            )
        }


        # ----------------------------------------------------
        # CREATE DATAFRAME
        # ----------------------------------------------------

        input_df = pd.DataFrame(
            [customer_data]
        )


        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(
            input_df
        )[0]


        probability = model.predict_proba(
            input_df
        )[0][1]


        churn_probability = round(
            float(probability) * 100,
            2
        )


        # ----------------------------------------------------
        # DETERMINE RISK LEVEL
        # ----------------------------------------------------

        if churn_probability >= 70:

            risk_level = "High Risk"

        elif churn_probability >= 40:

            risk_level = "Medium Risk"

        else:

            risk_level = "Low Risk"


        # ----------------------------------------------------
        # PREDICTION TEXT
        # ----------------------------------------------------

        if (
            prediction == 1
            or str(prediction).lower() == "yes"
        ):

            prediction_text = (
                "Customer is likely to churn"
            )

        else:

            prediction_text = (
                "Customer is unlikely to churn"
            )


        # ----------------------------------------------------
        # SEND RESULT TO RESULT PAGE
        # ----------------------------------------------------

        return render_template(

            "result.html",

            prediction=prediction_text,

            churn_probability=churn_probability,

            risk_level=risk_level,

            customer_data=customer_data

        )


    except Exception as e:

        print(
            "Prediction error:",
            e
        )


        return render_template(

            "result.html",

            prediction="Unable to make prediction",

            churn_probability=0,

            risk_level="Unknown",

            customer_data={},

            error=str(e)

        )
# ============================================================
# BATCH PREDICTION PAGE
# ============================================================

@app.route("/batch")
def batch_page():

    return render_template(
        "batch.html"
    )


# ============================================================
# BATCH PREDICTION
# ============================================================

@app.route("/batch_predict", methods=["POST"])
def batch_predict():

    try:

        # ----------------------------------------------------
        # CHECK UPLOADED FILE
        # ----------------------------------------------------

        if "file" not in request.files:

            return render_template(
                "batch.html",
                error="No file was uploaded."
            )


        file = request.files["file"]


        if file.filename == "":

            return render_template(
                "batch.html",
                error="Please select a CSV file."
            )


        if not file.filename.lower().endswith(".csv"):

            return render_template(
                "batch.html",
                error="Please upload a CSV file."
            )


        # ----------------------------------------------------
        # SAVE UPLOADED FILE
        # ----------------------------------------------------

        unique_name = (
            str(uuid.uuid4()) + ".csv"
        )

        input_path = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )

        file.save(input_path)


        # ----------------------------------------------------
        # READ CSV
        # ----------------------------------------------------

        df = pd.read_csv(
            input_path
        )


        # ----------------------------------------------------
        # CHECK REQUIRED COLUMNS
        # ----------------------------------------------------

        missing_columns = [

            column

            for column in REQUIRED_COLUMNS

            if column not in df.columns

        ]


        if missing_columns:

            return render_template(

                "batch.html",

                error=(
                    "Missing columns: "
                    + ", ".join(missing_columns)
                )

            )


        # ----------------------------------------------------
        # PREPARE DATA FOR MODEL
        # ----------------------------------------------------

        prediction_input = df[
            REQUIRED_COLUMNS
        ].copy()


        # ----------------------------------------------------
        # CONVERT NUMERIC COLUMNS
        # ----------------------------------------------------

        numeric_columns = [

            "SeniorCitizen",
            "tenure",
            "MonthlyCharges",
            "TotalCharges"

        ]


        for column in numeric_columns:

            prediction_input[column] = pd.to_numeric(

                prediction_input[column],

                errors="coerce"

            )


        # ----------------------------------------------------
        # CHECK INVALID VALUES
        # ----------------------------------------------------

        if prediction_input.isnull().any().any():

            invalid_columns = (

                prediction_input.columns[
                    prediction_input.isnull().any()
                ].tolist()

            )


            return render_template(

                "batch.html",

                error=(
                    "Invalid or missing values found in: "
                    + ", ".join(invalid_columns)
                )

            )


        # ----------------------------------------------------
        # MAKE PREDICTIONS
        # ----------------------------------------------------

        predictions = model.predict(
            prediction_input
        )


        probabilities = model.predict_proba(
            prediction_input
        )[:, 1]


        # ----------------------------------------------------
        # ADD CHURN PREDICTION
        # ----------------------------------------------------

        df["ChurnPrediction"] = [

            "Yes"

            if (
                prediction == 1
                or str(prediction).lower() == "yes"
            )

            else "No"

            for prediction in predictions

        ]


        # ----------------------------------------------------
        # ADD CHURN PROBABILITY
        # ----------------------------------------------------

        df["ChurnProbability"] = (

            probabilities * 100

        ).round(2)


        # ----------------------------------------------------
        # RISK LEVEL FUNCTION
        # ----------------------------------------------------

        def get_risk(probability):

            if probability >= 70:

                return "High Risk"

            elif probability >= 40:

                return "Medium Risk"

            else:

                return "Low Risk"


        # ----------------------------------------------------
        # ADD RISK LEVEL
        # ----------------------------------------------------

        df["RiskLevel"] = [

            get_risk(
                float(probability) * 100
            )

            for probability in probabilities

        ]


        # ----------------------------------------------------
        # SAVE PREDICTION FILE
        # ----------------------------------------------------

        output_name = (

            "churn_predictions_"

            + str(uuid.uuid4())[:8]

            + ".csv"

        )


        output_path = os.path.join(

            OUTPUT_FOLDER,

            output_name

        )


        df.to_csv(

            output_path,

            index=False

        )


        # ----------------------------------------------------
        # CALCULATE SUMMARY
        # ----------------------------------------------------

        total_customers = len(df)


        churn_count = int(

            (
                df["ChurnPrediction"] == "Yes"
            ).sum()

        )


        no_churn_count = (

            total_customers

            - churn_count

        )


        high_risk_count = int(

            (
                df["RiskLevel"] == "High Risk"
            ).sum()

        )


        medium_risk_count = int(

            (
                df["RiskLevel"] == "Medium Risk"
            ).sum()

        )


        low_risk_count = int(

            (
                df["RiskLevel"] == "Low Risk"
            ).sum()

        )


        # ----------------------------------------------------
        # CREATE PREVIEW
        # ----------------------------------------------------

        preview = df.head(50).to_dict(
            orient="records"
        )


        # ----------------------------------------------------
        # SHOW BATCH RESULT
        # ----------------------------------------------------

        return render_template(

            "batch_result.html",

            total_customers=total_customers,

            predicted_churn=churn_count,

            predicted_stay=no_churn_count,

            high_risk=high_risk_count,

            medium_risk=medium_risk_count,

            low_risk=low_risk_count,

            preview=preview,

            download_file=output_name

        )


    except Exception as e:

        print(
            "Batch prediction error:",
            e
        )


        return render_template(

            "batch.html",

            error=str(e)

        )
# ============================================================
# MODEL PERFORMANCE
# ============================================================

@app.route("/model_info")
def model_performance():

    # Make sure model_info is a dictionary
    if isinstance(model_info, dict):

        info = model_info

    else:

        info = {}


    # --------------------------------------------------------
    # SEND MODEL INFORMATION TO HTML PAGE
    # --------------------------------------------------------

    return render_template(

        "model_info.html",

        model_name=info.get(
            "model_name",
            "Machine Learning Model"
        ),

        training_samples=info.get(
            "training_samples",
            "N/A"
        ),

        feature_count=info.get(
            "feature_count",
            "N/A"
        ),

        accuracy=info.get(
            "accuracy",
            "N/A"
        ),

        precision=info.get(
            "precision",
            "N/A"
        ),

        recall=info.get(
            "recall",
            "N/A"
        ),

        f1_score=info.get(
            "f1_score",
            "N/A"
        ),

        roc_auc=info.get(
            "roc_auc",
            "N/A"
        )

    )   
# ============================================================
# ANALYTICS DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    try:

        # ----------------------------------------------------
        # CHECK DATASET
        # ----------------------------------------------------

        if not os.path.exists(DATASET_PATH):

            return render_template(

                "dashboard.html",

                error="Dataset not found."

            )


        # ----------------------------------------------------
        # LOAD DATASET
        # ----------------------------------------------------

        df = pd.read_csv(
            DATASET_PATH
        )


        # ----------------------------------------------------
        # OVERALL STATISTICS
        # ----------------------------------------------------

        total_customers = len(df)


        churned_customers = int(

            (
                df["Churn"] == "Yes"
            ).sum()

        )


        retained_customers = (

            total_customers

            - churned_customers

        )


        if total_customers > 0:

            churn_rate = round(

                (
                    churned_customers
                    / total_customers
                ) * 100,

                2

            )

        else:

            churn_rate = 0


        # ----------------------------------------------------
        # CONTRACT ANALYSIS
        # ----------------------------------------------------

        contract_data = []


        for contract in (

            df["Contract"]
            .dropna()
            .unique()

        ):

            group = df[
                df["Contract"] == contract
            ]


            customers = len(group)


            churned = int(

                (
                    group["Churn"] == "Yes"
                ).sum()

            )


            if customers > 0:

                rate = round(

                    (
                        churned
                        / customers
                    ) * 100,

                    2

                )

            else:

                rate = 0


            contract_data.append({

                "contract": contract,

                "customers": customers,

                "churned": churned,

                "churn_rate": rate

            })


        # ----------------------------------------------------
        # INTERNET SERVICE ANALYSIS
        # ----------------------------------------------------

        internet_data = []


        for service in (

            df["InternetService"]
            .dropna()
            .unique()

        ):

            group = df[
                df["InternetService"] == service
            ]


            customers = len(group)


            churned = int(

                (
                    group["Churn"] == "Yes"
                ).sum()

            )


            if customers > 0:

                rate = round(

                    (
                        churned
                        / customers
                    ) * 100,

                    2

                )

            else:

                rate = 0


            internet_data.append({

                "internet_service": service,

                "customers": customers,

                "churned": churned,

                "churn_rate": rate

            })


        # ----------------------------------------------------
        # PAYMENT METHOD ANALYSIS
        # ----------------------------------------------------

        payment_data = []


        for method in (

            df["PaymentMethod"]
            .dropna()
            .unique()

        ):

            group = df[
                df["PaymentMethod"] == method
            ]


            customers = len(group)


            churned = int(

                (
                    group["Churn"] == "Yes"
                ).sum()

            )


            if customers > 0:

                rate = round(

                    (
                        churned
                        / customers
                    ) * 100,

                    2

                )

            else:

                rate = 0


            payment_data.append({

                "payment_method": method,

                "customers": customers,

                "churned": churned,

                "churn_rate": rate

            })

        # ----------------------------------------------------
        # RENDER DASHBOARD
        # ----------------------------------------------------

        return render_template(

            "dashboard.html",

            total_customers=total_customers,

            churned_customers=churned_customers,

            retained_customers=retained_customers,

            churn_rate=churn_rate,

            contract_data=contract_data,

            internet_data=internet_data,

            payment_data=payment_data

        )


    except Exception as e:

        print(
            "Dashboard error:",
            e
        )


        return render_template(

            "dashboard.html",

            error=str(e)

        ) 
# ============================================================
# DOWNLOAD SAMPLE CSV
# ============================================================

@app.route("/download_sample")
def download_sample():

    try:

        # ----------------------------------------------------
        # CREATE SAMPLE CUSTOMER DATA
        # ----------------------------------------------------

        sample_data = pd.DataFrame({

            "customerID": [
                "SAMPLE-001",
                "SAMPLE-002",
                "SAMPLE-003"
            ],

            "gender": [
                "Female",
                "Male",
                "Female"
            ],

            "SeniorCitizen": [
                0,
                0,
                1
            ],

            "Partner": [
                "No",
                "Yes",
                "No"
            ],

            "Dependents": [
                "No",
                "Yes",
                "No"
            ],

            "tenure": [
                2,
                34,
                12
            ],

            "PhoneService": [
                "Yes",
                "Yes",
                "Yes"
            ],

            "MultipleLines": [
                "No",
                "No",
                "Yes"
            ],

            "InternetService": [
                "Fiber optic",
                "DSL",
                "Fiber optic"
            ],

            "OnlineSecurity": [
                "No",
                "Yes",
                "No"
            ],

            "OnlineBackup": [
                "No",
                "No",
                "Yes"
            ],

            "DeviceProtection": [
                "No",
                "Yes",
                "No"
            ],

            "TechSupport": [
                "No",
                "No",
                "No"
            ],

            "StreamingTV": [
                "Yes",
                "No",
                "Yes"
            ],

            "StreamingMovies": [
                "Yes",
                "No",
                "Yes"
            ],

            "Contract": [
                "Month-to-month",
                "One year",
                "Month-to-month"
            ],

            "PaperlessBilling": [
                "Yes",
                "No",
                "Yes"
            ],

            "PaymentMethod": [
                "Electronic check",
                "Mailed check",
                "Electronic check"
            ],

            "MonthlyCharges": [
                70.70,
                56.95,
                85.50
            ],

            "TotalCharges": [
                141.40,
                1889.50,
                1026.00
            ]

        })


        # ----------------------------------------------------
        # SAVE SAMPLE FILE
        # ----------------------------------------------------

        file_path = os.path.join(

            OUTPUT_FOLDER,

            "sample_customer_data.csv"

        )


        sample_data.to_csv(

            file_path,

            index=False

        )


        # ----------------------------------------------------
        # SEND FILE TO USER
        # ----------------------------------------------------

        return send_file(

            file_path,

            as_attachment=True,

            download_name="sample_customer_data.csv"

        )


    except Exception as e:

        print(
            "Sample CSV error:",
            e
        )

        return (
            "Unable to create sample CSV: "
            + str(e),
            500
        )


# ============================================================
# DOWNLOAD PREDICTION FILE
# ============================================================

@app.route("/download/<filename>")
def download(filename):

    try:

        # ----------------------------------------------------
        # BUILD FILE PATH
        # ----------------------------------------------------

        file_path = os.path.join(

            OUTPUT_FOLDER,

            filename

        )


        # ----------------------------------------------------
        # CHECK FILE EXISTS
        # ----------------------------------------------------

        if not os.path.exists(file_path):

            return (
                "Prediction file not found.",
                404
            )


        # ----------------------------------------------------
        # SEND FILE
        # ----------------------------------------------------

        return send_file(

            file_path,

            as_attachment=True

        )


    except Exception as e:

        print(
            "Download error:",
            e
        )

        return (
            "Unable to download file: "
            + str(e),
            500
        )
# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("STARTING CUSTOMER CHURN INTELLIGENCE PLATFORM")
    print("=" * 60)

    print()
    print("Flask server is starting...")
    print()
    print("Open this address in your browser:")
    print("http://127.0.0.1:5000")
    print()

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )                                
     
