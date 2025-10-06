import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("D:/expo/data/framingham.csv")

# Clean data
df.drop(['education'], axis=1, inplace=True)
df.rename(columns={'male': 'Sex_male'}, inplace=True)
df.dropna(inplace=True)

# Select features & target
X = df[['age', 'Sex_male', 'cigsPerDay', 'totChol', 'sysBP', 'glucose']]
y = df['TwoYearCHD']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=4)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, 'heart_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("✅ Model and scaler saved successfully.")
