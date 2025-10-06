import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Load your dataset
df = pd.read_csv("framingham.csv")

# Select features and target (example)
X = df[['age','sex','chestPain','restingBP','cholesterol','fastingBS',
        'restingECG','maxHR','exerciseAngina','oldpeak','stSlope','majorVessels']]
y = df['target']  # 1 = heart disease, 0 = no disease

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save the trained model
pickle.dump(model, open("heart_model.pkl", "wb"))
