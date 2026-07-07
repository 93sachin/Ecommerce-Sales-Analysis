import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# Create models folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("data/data.csv", encoding="ISO-8859-1")

# Data preprocessing
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Sales"] = df["Quantity"] * df["UnitPrice"]

# Monthly sales
monthly = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))["Sales"]
      .sum()
      .reset_index()
)

# Create month number
monthly["Month"] = range(1, len(monthly) + 1)

# Train model
X = monthly[["Month"]]
y = monthly["Sales"]

model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "models/sales_model.pkl")

# Predict next 3 months
future = pd.DataFrame({
    "Month": [len(monthly)+1, len(monthly)+2, len(monthly)+3]
})

prediction = model.predict(future)

print("\n========= NEXT 3 MONTH SALES FORECAST =========")

for i, value in enumerate(prediction, start=1):
    print(f"Month +{i}: ${value:,.2f}")

print("\nModel saved successfully!")