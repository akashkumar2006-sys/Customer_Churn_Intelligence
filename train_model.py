import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = "data/dataset.csv"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "churn_model.pkl"
)

MODEL_INFO_PATH = os.path.join(
    MODEL_DIR,
    "model_info.pkl"
)


# ============================================================
# START
# ============================================================

print("=" * 60)
print("CUSTOMER CHURN MODEL TRAINING")
print("=" * 60)


# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.exists(DATASET_PATH):

    print("\n❌ Dataset not found!")

    print(
        "Expected:",
        DATASET_PATH
    )

    raise SystemExit


print("\n☑ Dataset found!")


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = pd.read_csv(
        DATASET_PATH
    )

    print(
        "☑ Dataset loaded successfully!"
    )

except Exception as e:

    print(
        "\n❌ Error reading dataset:"
    )

    print(e)

    raise SystemExit


print("\nDataset shape:")
print(df.shape)


# ============================================================
# CLEAN DATA
# ============================================================

if "customerID" in df.columns:

    df = df.drop(
        columns=["customerID"]
    )


if "TotalCharges" in df.columns:

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )


df = df.dropna(
    subset=["Churn"]
)


df["Churn"] = df["Churn"].map({

    "No": 0,

    "Yes": 1

})


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df.drop(
    columns=["Churn"]
)

y = df["Churn"]


# ============================================================
# COLUMN TYPES
# ============================================================

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()


numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()


# ============================================================
# PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="median"
            )
        )

    ]

)


categorical_pipeline = Pipeline(

    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",

            OneHotEncoder(
                handle_unknown="ignore"
            )
        )

    ]

)


preprocessor = ColumnTransformer(

    transformers=[

        (
            "numeric",

            numeric_pipeline,

            numeric_features
        ),

        (
            "categorical",

            categorical_pipeline,

            categorical_features
        )

    ]

)


# ============================================================
# MODEL
# ============================================================

model = LogisticRegression(

    max_iter=1000,

    class_weight="balanced"

)


# ============================================================
# PIPELINE
# ============================================================

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",

            preprocessor
        ),

        (
            "model",

            model
        )

    ]

)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print(
    "\nTraining samples:",
    len(X_train)
)

print(
    "Testing samples:",
    len(X_test)
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

print(
    "☑ Model trained successfully!"
)


# ============================================================
# PREDICTIONS
# ============================================================

y_pred = pipeline.predict(
    X_test
)

y_probability = pipeline.predict_proba(
    X_test
)[:, 1]


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n" + "=" * 60)

print("MODEL PERFORMANCE")

print("=" * 60)

print(
    f"\nAccuracy : {accuracy * 100:.2f}%"
)

print(
    f"Precision: {precision * 100:.2f}%"
)

print(
    f"Recall   : {recall * 100:.2f}%"
)

print(
    f"F1 Score : {f1 * 100:.2f}%"
)

print(
    f"ROC-AUC  : {roc_auc * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "No Churn",
            "Churn"
        ],
        zero_division=0
    )
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\nCalculating feature importance...")


trained_preprocessor = pipeline.named_steps[
    "preprocessor"
]

trained_model = pipeline.named_steps[
    "model"
]


# Get transformed feature names.

feature_names = (
    trained_preprocessor
    .get_feature_names_out()
)


coefficients = (
    trained_model
    .coef_[0]
)


importance_df = pd.DataFrame({

    "feature":
        feature_names,

    "coefficient":
        coefficients,

    "absolute_importance":
        np.abs(coefficients)

})


# Sort by importance.

importance_df = (
    importance_df
    .sort_values(
        "absolute_importance",
        ascending=False
    )
)


# Keep top 20.

top_features = (
    importance_df
    .head(20)
    .copy()
)


# Convert NumPy values to normal Python
# values so they save cleanly.

feature_importance = []


for _, row in top_features.iterrows():

    feature_importance.append({

        "feature":
            str(row["feature"]),

        "coefficient":
            round(
                float(row["coefficient"]),
                4
            ),

        "importance":
            round(
                float(row["absolute_importance"]),
                4
            )

    })


print("\nTop churn factors:")

for item in feature_importance[:10]:

    print(
        item["feature"],
        "->",
        item["coefficient"]
    )


# ============================================================
# CREATE MODEL DIRECTORY
# ============================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    pipeline,
    MODEL_PATH
)


print(
    "\n☑ Model saved:",
    MODEL_PATH
)


# ============================================================
# MODEL INFORMATION
# ============================================================

model_info = {

    "model_name":
        "Logistic Regression",

    "training_samples":
        int(len(X_train)),

    "testing_samples":
        int(len(X_test)),

    "feature_count":
        int(len(X.columns)),

    "accuracy":
        round(
            accuracy * 100,
            2
        ),

    "precision":
        round(
            precision * 100,
            2
        ),

    "recall":
        round(
            recall * 100,
            2
        ),

    "f1_score":
        round(
            f1 * 100,
            2
        ),

    "roc_auc":
        round(
            roc_auc * 100,
            2
        ),

    "feature_importance":
        feature_importance

}


# ============================================================
# SAVE MODEL INFORMATION
# ============================================================

joblib.dump(
    model_info,
    MODEL_INFO_PATH
)


print(
    "☑ Model information saved:",
    MODEL_INFO_PATH
)


# ============================================================
# FINISHED
# ============================================================

print("\n" + "=" * 60)

print(
    "MODEL TRAINING COMPLETED SUCCESSFULLY!"
)

print("=" * 60)

print("\nGenerated files:")

print(
    "1.",
    MODEL_PATH
)

print(
    "2.",
    MODEL_INFO_PATH
)