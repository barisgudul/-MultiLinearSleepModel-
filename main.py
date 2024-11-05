import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
dataset = pd.read_csv("msleep.csv")

# Select a subset of columns for processing
subset = dataset.iloc[:, 6:11].values

# Handle missing values
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
imputer.fit(subset)
subset = imputer.transform(subset)
dataset.iloc[:, 6:11] = subset

# Combine columns using iloc
X = pd.concat([dataset.iloc[:, 2:3], dataset.iloc[:, 6:11]], axis=1).values
y = dataset.iloc[:, 5].values
print(X)

# Convert categorical data
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(), [0])], remainder="passthrough")
X = np.array(ct.fit_transform(X))
print(X)

# Split dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multiple Linear Regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predict test results
y_pred = regressor.predict(X_test)
np.set_printoptions(precision=7)

print(np.concatenate((y_test.reshape(len(y_test), 1),
                      y_pred.reshape(len(y_pred), 1)),
                     axis=1))
error = np.abs(y_test - y_pred)

# Visualization
plt.figure(figsize=(15, 8))
plt.plot(range(len(y_test)), y_test, label="Actual Sleep Duration", marker="o")
plt.plot(range(len(y_pred)), y_pred, label="Predicted Sleep Duration", marker="x")
plt.plot(range(len(error)), error, label="Difference", marker="s")
plt.xlabel("Data Point")
plt.ylabel("Sleep Duration (hours)")
plt.title("Difference Between Predicted and Actual Sleep Durations")
plt.legend()
plt.show()
