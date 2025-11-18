# Laptop Price Prediction: A Machine Learning Analysis

![Laptop Price Analysis](https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=2070&auto=format&fit=crop) <!-- You can replace this with a relevant image or a screenshot from your notebook -->

## Project Overview

This project delves into the complex relationship between laptop hardware specifications and their market price. By systematically applying and comparing various regression models—from simple linear regression to a sophisticated multi-variable polynomial pipeline—I developed a highly accurate predictive model. The final model successfully explains over 71% of the price variance, demonstrating the power of machine learning in decoding pricing strategies within the consumer electronics market.

## Key Skills & Technologies

- **Languages & Libraries:** Python, Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning:** Scikit-Learn
- **Modeling Techniques:**
    - Simple Linear Regression
    - Multiple Linear Regression
    - Polynomial Regression
    - Feature Engineering (PolynomialFeatures)
    - Feature Scaling (StandardScaler)
    - Model Pipelines
- **Evaluation Metrics:** R-squared (R²), Mean Squared Error (MSE)
- **Data Visualization:** Distribution Plots (KDE), Polynomial Fit Curves

## Problem Statement

How accurately can we predict a laptop's market price based solely on its hardware specifications? This project aims to answer that question by identifying the most influential features and the most effective modeling technique to capture the often non-linear relationships between components and cost.

## Methodology

The analysis followed a structured, progressive approach:

1.  **Data Acquisition & Preparation:** Loaded a clean dataset of laptop specifications and prices.
2.  **Baseline Modeling:** Established a simple linear regression model using only `CPU_frequency` to set a performance baseline.
3.  **Multi-Feature Modeling:** Developed a multiple linear regression model incorporating all key features (`CPU_frequency`, `RAM_GB`, `Storage_GB_SSD`, `CPU_core`, `OS`, `GPU`, `Category`).
4.  **Non-Linear Exploration:** Applied polynomial regression to test for non-linear relationships with the primary feature.
5.  **Advanced Pipeline:** Constructed a `scikit-learn` pipeline that chains feature scaling, polynomial feature generation, and linear regression to model complex interactions between all variables.
6.  **Evaluation:** Each model was rigorously evaluated using R-squared and Mean Squared Error, with results visualized using distribution plots to compare actual vs. predicted prices.

## Key Findings

- **Single Feature is Insufficient:** Using only `CPU_frequency` resulted in a poor model (R² = 0.134).
- **Multiple Features Matter:** A multiple linear regression model significantly improved performance (R² = 0.508).
- **Non-Linearity is Key:** The most accurate model was the **multi-variable polynomial pipeline**, which achieved an impressive **R² of 0.717** and an MSE of 94,993.
- **Feature Interactions are Crucial:** The success of the polynomial pipeline indicates that the price is not just a sum of parts but is heavily influenced by how those parts interact (e.g., a high-end GPU's value is amplified by a high-end CPU).

## How to Run This Project

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install Dependencies:** It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You should create a `requirements.txt` file with the following content for easy setup:)*
    ```
    pandas
    numpy
    matplotlib
    seaborn
    scikit-learn
    jupyterlab
    ```

3.  **Launch Jupyter Lab:**
    ```bash
    jupyter lab
    ```

4.  **Open and Run the Notebook:** Navigate to `your-notebook-name.ipynb` in the Jupyter Lab interface and run the cells sequentially to reproduce the analysis.

## Future Improvements

- **Incorporate Categorical Features:** Apply one-hot encoding to features like `OS`, `GPU`, and `Category` for potentially richer insights.
- **Time-Series Analysis:** Introduce data on release dates to model price depreciation over time.
- **Brand Analysis:** Include manufacturer as a feature to quantify brand premium.
- **Advanced Models:** Experiment with more complex models like Random Forest or Gradient Boosting to see if performance can be further improved.
