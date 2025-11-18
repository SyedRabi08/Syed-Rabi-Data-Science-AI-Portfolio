#!/usr/bin/env python3

"""
Laptop Price Prediction: A Complete Machine Learning Analysis Script

This script performs a comprehensive analysis of laptop pricing based on hardware
specifications. It systematically develops and evaluates several regression models
to identify the most accurate predictor for laptop prices.

Models Implemented:
1. Simple Linear Regression
2. Multiple Linear Regression
3. Polynomial Regression (1st, 3rd, and 5th degree)
4. Multi-variable Polynomial Pipeline

The script outputs performance metrics (R-squared, MSE) and generates
visualizations for each model.
"""

# --- 1. IMPORT LIBRARIES ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import warnings
from io import StringIO
import requests

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

# --- 2. DEFINE HELPER FUNCTIONS ---
def PlotPolly(model, independent_variable, dependent_variable, Name):
    """
    Generates a plot for a polynomial fit.
    """
    x_new = np.linspace(independent_variable.min(), independent_variable.max(), 100)
    y_new = model(x_new)

    plt.figure(figsize=(10, 6))
    plt.plot(independent_variable, dependent_variable, '.', x_new, y_new, '-')
    plt.title(f'Polynomial Fit for Price ~ {Name}')
    ax = plt.gca()
    ax.set_facecolor((0.898, 0.898, 0.898))
    plt.xlabel(Name)
    plt.ylabel('Price of laptops')
    plt.show()

# --- 3. MAIN ANALYSIS FUNCTION ---
def main():
    """
    Main function to run the entire data analysis workflow.
    """
    # --- DATA ACQUISITION AND LOADING ---
    print("--- 1. Loading Dataset ---")
    path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-Coursera/laptop_pricing_dataset_mod2.csv"
    try:
        response = requests.get(path)
        response.raise_for_status()  # Raise an exception for bad status codes
        # Use StringIO to read the text content of the response as a file
        data = StringIO(response.text)
        df = pd.read_csv(data, header=0)
        print("Dataset loaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        return

    # Display the first 5 rows
    print("\nThe first 5 rows of the dataframe:")
    print(df.head())

    # --- SIMPLE LINEAR REGRESSION (SLR) ---
    print("\n--- 2. Simple Linear Regression (CPU_frequency) ---")
    lm = LinearRegression()
    X = df[['CPU_frequency']]
    Y = df['Price']
    lm.fit(X, Y)
    Yhat = lm.predict(X)

    # Visualization for SLR
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df['Price'], color="r", label="Actual Value", fill=True)
    sns.kdeplot(x=Yhat, color="b", label="Fitted Values", fill=True)
    plt.title('Actual vs Fitted Values for Price (SLR)')
    plt.xlabel('Price')
    plt.ylabel('Proportion of laptops')
    plt.legend()
    plt.show()

    # Evaluation for SLR
    mse_slr = mean_squared_error(df['Price'], Yhat)
    r2_score_slr = lm.score(X, Y)
    print(f'The R-square for Linear Regression is: {r2_score_slr:.4f}')
    print(f'The mean square error of price and predicted value is: {mse_slr:.2f}')

    # --- MULTIPLE LINEAR REGRESSION (MLR) ---
    print("\n--- 3. Multiple Linear Regression ---")
    lm1 = LinearRegression()
    Z = df[['CPU_frequency','RAM_GB','Storage_GB_SSD','CPU_core','OS','GPU','Category']]
    lm1.fit(Z, Y)
    Y_hat = lm1.predict(Z)

    # Visualization for MLR
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df['Price'], color="r", label="Actual Value", fill=True)
    sns.kdeplot(x=Y_hat, color="b", label="Fitted Values", fill=True)
    plt.title('Actual vs Fitted Values for Price (MLR)')
    plt.xlabel('Price')
    plt.ylabel('Proportion of laptops')
    plt.legend()
    plt.show()

    # --- POLYNOMIAL REGRESSION (SINGLE VARIABLE) ---
    print("\n--- 4. Polynomial Regression (CPU_frequency) ---")
    X_poly = df[['CPU_frequency']].to_numpy().flatten()
    Y_poly = df['Price']

    # Create polynomial models
    f1 = np.polyfit(X_poly, Y_poly, 1)
    p1 = np.poly1d(f1)
    f3 = np.polyfit(X_poly, Y_poly, 3)
    p3 = np.poly1d(f3)
    f5 = np.polyfit(X_poly, Y_poly, 5)
    p5 = np.poly1d(f5)

    # Visualize polynomial fits
    print("Displaying polynomial fit plots...")
    PlotPolly(p1, X_poly, Y_poly, 'CPU_frequency (1st Degree)')
    PlotPolly(p3, X_poly, Y_poly, 'CPU_frequency (3rd Degree)')
    PlotPolly(p5, X_poly, Y_poly, 'CPU_frequency (5th Degree)')

    # Evaluate polynomial models
    r_squared_1 = r2_score(Y_poly, p1(X_poly))
    print(f'The R-square value for 1st degree polynomial is: {r_squared_1:.4f}')
    print(f'The MSE value for 1st degree polynomial is: {mean_squared_error(Y_poly, p1(X_poly)):.2f}')

    r_squared_3 = r2_score(Y_poly, p3(X_poly))
    print(f'The R-square value for 3rd degree polynomial is: {r_squared_3:.4f}')
    print(f'The MSE value for 3rd degree polynomial is: {mean_squared_error(Y_poly, p3(X_poly)):.2f}')

    r_squared_5 = r2_score(Y_poly, p5(X_poly))
    print(f'The R-square value for 5th degree polynomial is: {r_squared_5:.4f}')
    print(f'The MSE value for 5th degree polynomial is: {mean_squared_error(Y_poly, p5(X_poly)):.2f}')

    # --- MULTI-VARIABLE POLYNOMIAL PIPELINE ---
    print("\n--- 5. Multi-variable Polynomial Pipeline ---")
    Input = [('scale', StandardScaler()), ('polynomial', PolynomialFeatures(include_bias=False)), ('model', LinearRegression())]
    pipe = Pipeline(Input)
    Z_float = Z.astype(float)
    pipe.fit(Z_float, Y)
    ypipe = pipe.predict(Z_float)

    # Evaluate the pipeline model
    mse_pipe = mean_squared_error(Y, ypipe)
    r2_pipe = r2_score(Y, ypipe)
    print(f'MSE for multi-variable polynomial pipeline is: {mse_pipe:.2f}')
    print(f'R^2 for multi-variable polynomial pipeline is: {r2_pipe:.4f}')
    
    print("\n--- Analysis Complete ---")


# --- 6. SCRIPT ENTRY POINT ---
if __name__ == "__main__":
    main()
