import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import xgboost as xgb
import textwrap
import io
import base64


# Load and preprocess the data
selected_columns = [
    "Sl. No.", "State/UT",
    "Indian Railways Act - Cases Registered",
    "Indian Railways Act - Persons Arrested",
    "Total (Indian Railways Act + RP(UP) Act) - Cases Registered",
    "Total (Indian Railways Act + RP(UP) Act) - Persons Arrested"
]

df_2021 = pd.read_csv("2021.csv")[selected_columns].copy()
df_2021["YEAR"] = 2021
df_2022 = pd.read_csv("2022.csv")[selected_columns].copy()
df_2022["YEAR"] = 2022

combined_df = pd.concat([df_2021, df_2022], ignore_index=True)
combined_df.fillna(0, inplace=True)

filtered_df = combined_df[["State/UT", "YEAR", "Total (Indian Railways Act + RP(UP) Act) - Persons Arrested"]]
pivot_df = filtered_df.pivot(index="State/UT", columns="YEAR", values="Total (Indian Railways Act + RP(UP) Act) - Persons Arrested")
pivot_df.columns = ["Arrested_2021", "Arrested_2022"]
pivot_df = pivot_df.reset_index()

df_2019 = pd.read_csv("state_level_crimes_2019.csv")[["State/UT", "Crime against Women Passengers"]]
df_2019.rename(columns={"Crime against Women Passengers": "Women_crime_arrested_2019"}, inplace=True)

merged_df = pd.merge(pivot_df, df_2019, on="State/UT", how="left")
merged_df.fillna(0, inplace=True)


def predict_arrests_for_year(target_year):
    if target_year <= 2022:
        print(f"No need to predict for {target_year}, actual data exists.")
        return

    base_year = 2022
    current_input_col = "Arrested_2022"
    current_output_col = "Arrested_2022"

    for year in range(2023, target_year):
        next_col = f"Predicted_Arrested_{year}"
        if next_col in merged_df.columns:
            current_input_col = next_col
            current_output_col = next_col
        else:
            print(f"❌ Missing prediction for {year}. Please predict sequentially.")
            return

    column_name = f"Predicted_Arrested_{target_year}"

    if column_name in merged_df.columns:
        print(f"✅ Prediction for {target_year} already exists.")
        return

    required_cols = ["Women_crime_arrested_2019", "Arrested_2021", current_input_col]
    if not all(col in merged_df.columns for col in required_cols):
        print(f"❌ Missing columns in dataframe.")
        return

    X_train = merged_df[required_cols]
    Y_train = merged_df[current_output_col]

    # Model training
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, Y_train)
    rf_predictions = rf_model.predict(X_train)
    print(f"RandomForest R² Score: {r2_score(Y_train, rf_predictions):.4f}")

    # Other models for comparison
    lr = LinearRegression().fit(X_train, Y_train)
    svr = SVR().fit(X_train, Y_train)
    xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42).fit(X_train, Y_train)

    print(f"Linear Regression R² Score: {r2_score(Y_train, lr.predict(X_train)):.4f}")
    print(f"SVR R² Score: {r2_score(Y_train, svr.predict(X_train)):.4f}")
    print(f"XGBoost R² Score: {r2_score(Y_train, xgb_model.predict(X_train)):.4f}")

    # Save final predictions
    merged_df[column_name] = np.round(rf_predictions).astype(int)
    merged_df.to_csv(f"predicted_arrests_{target_year}.csv", index=False)
    print(f"✅ Prediction for {target_year} saved to 'predicted_arrests_{target_year}.csv'")

    # Plotting
    plt.figure(figsize=(22, 10))
    bars = plt.bar(merged_df["State/UT"], merged_df[column_name], color="orange")
    plt.xticks(rotation=75, ha='right', fontsize=8)
    plt.yscale("log")
    plt.title(f"Predicted Railway Arrests in {target_year} (State-wise)")
    plt.xlabel("State/UT")
    plt.ylabel(f"Predicted Arrests in {target_year} (log scale)")
    total = merged_df[column_name].sum()
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            percent = (height / total) * 100
            plt.text(bar.get_x() + bar.get_width() / 2, height * 0.98,
                     f'{percent:.1f}%', ha='center', va='top', fontsize=6, rotation=90)
    plt.tight_layout()
    plt.show()


def plot_yearwise_rape_cases(selected_state, start_year=2023, end_year=2030):
    rape_data = {}
    try:
        for year in range(start_year, end_year):
            df = pd.read_csv(f"predicted_arrests_{year}.csv")
            col = f"Predicted_Arrested_{year}"
            row = df[df["State/UT"] == selected_state]
            if not row.empty:
                rape_data[year] = int(row[col].values[0])
    except Exception as e:
        print("Error loading or processing data:", e)
        return

    if not rape_data:
        print("No data available for plotting.")
        return

    years, arrests = zip(*rape_data.items())
    plt.figure(figsize=(10, 5))
    plt.plot(years, arrests, marker="o", color="darkred", linewidth=2)
    plt.title(f"{selected_state} - Predicted Railway Arrests ({start_year}–{end_year-1})")
    plt.xlabel("Year")
    plt.ylabel("Predicted Arrests")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_trend_2023_to_2030():
    try:
        trend = {}
        for year in range(2023, 2031):
            df = pd.read_csv(f"predicted_arrests_{year}.csv")
            col = f"Predicted_Arrested_{year}"
            trend[year] = df[col].sum()

        if not trend:
            print("No arrest prediction data available.")
            return

        years, totals = zip(*trend.items())
        plt.figure(figsize=(10, 5))
        plt.plot(years, totals, marker='o', color="teal", linewidth=2)
        plt.title("Total Predicted Railway Arrests (2023–2030)")
        plt.xlabel("Year")
        plt.ylabel("Total Arrests")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error loading predicted data: {e}")


def plot_line_plots_per_state():
    try:
        trend_df = merged_df[["State/UT", "Arrested_2021", "Arrested_2022"]].copy()
        for year in range(2023, 2031):
            df = pd.read_csv(f"predicted_arrests_{year}.csv")
            trend_df = pd.merge(trend_df, df[["State/UT", f"Predicted_Arrested_{year}"]].rename(
                columns={f"Predicted_Arrested_{year}": f"Arrested_{year}"}), on="State/UT", how="left")

        trend_df.set_index("State/UT", inplace=True)
        for state in trend_df.index:
            values = trend_df.loc[state].values
            years = list(range(2021, 2031))
            plt.figure(figsize=(8, 4))
            plt.plot(years, values, marker="o")
            plt.title(f"{state} - Railway Arrest Trend (2021–2030)")
            plt.xlabel("Year")
            plt.ylabel("Arrests")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print(f"Error generating plots: {e}")
