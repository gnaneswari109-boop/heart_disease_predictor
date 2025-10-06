# train_logreg.py — updated for framingham.csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os

# 1. Create 'models' folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# 2. Load your dataset
df = pd.read_csv("data/framingham.csv", encoding="latin1")

# 3. Drop rows with missing target or features
df = df.dropna(subset=["TenYearCHD"])

# 4. Define features and target based on your dataset
features = [
    'age', 'male', 'cigsPerDay', 'totChol', 'sysBP', 'diaBP',
    'glucose', 'BPMeds', 'diabetes', 'prevalentStroke', 'heartRate'
]
target = "TenYearCHD"

X = df[features]
y = df[target]

# 5. Create preprocessing and modeling pipeline
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))
])

# 6. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 7. Train model
pipeline.fit(X_train, y_train)

# 8. Evaluate
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]
print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, y_proba))

# 9. Save model
joblib.dump(pipeline, "models/logreg_heart_model.joblib")
print("✅ Model trained and saved successfully.")


