from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import xgboost as xgb
from sklearn.metrics import r2_score


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

    required_cols = ["Women_crime_arrested_2019", "Arrested_2021", current_input_col, current_output_col]
    if not all(col in merged_df.columns for col in required_cols):
        print(f"❌ Missing columns in dataframe.")
        return

    X_train = merged_df[["Women_crime_arrested_2019", "Arrested_2021", current_input_col]]
    Y_train = merged_df[current_output_col]

    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "LinearRegression": LinearRegression(),
        "SVR": SVR(),
        "XGBoost": xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
    }

    best_model_name = None
    best_r2_score = -np.inf
    best_model = None
    predictions = {}

    # Train and evaluate all models
    for model_name, model in models.items():
        model.fit(X_train, Y_train)
        pred = model.predict(X_train)
        r2 = r2_score(Y_train, pred)
        print(f"{model_name} R² Score: {r2:.4f}")

        if r2 > best_r2_score:
            best_r2_score = r2
            best_model_name = model_name
            best_model = model
            predictions[column_name] = np.round(model.predict(X_train)).astype(int)

    # Save the best model's predictions
    merged_df[column_name] = predictions[column_name]
    merged_df.to_csv(f"predicted_arrests_{target_year}.csv", index=False)
    print(f"✅ Best model: {best_model_name} with R² Score: {best_r2_score:.4f}")
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
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height * 0.98,
                f'{percent:.1f}%',
                ha='center',
                va='top',
                fontsize=6,
                rotation=90
            )
    plt.tight_layout()
    plt.show()
