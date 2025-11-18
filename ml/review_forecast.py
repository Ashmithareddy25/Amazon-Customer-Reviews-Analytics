import pandas as pd
import os
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/cleaned_reviews.csv"
FORECAST_DAYS = 30
OUTPUT_CSV = "reports/review_forecast.csv"
OUTPUT_PLOT = "reports/review_forecast.png"

print("📥 Loading cleaned reviews...")
df = pd.read_csv(INPUT_PATH)
df['review_date'] = pd.to_datetime(df['review_date'])

# Aggregate daily review counts
daily = df.groupby('review_date').size().rename("review_count").to_frame()

# Ensure continuous date index
daily = daily.asfreq('D', fill_value=0)

print("📊 Fitting SARIMAX model (this may take a bit)...")
model = SARIMAX(daily['review_count'], order=(1,1,1), seasonal_order=(1,1,1,7))
result = model.fit(disp=False)

# Forecast
future_index = pd.date_range(
    start=daily.index[-1] + pd.Timedelta(days=1),
    periods=FORECAST_DAYS,
    freq='D'
)
forecast = result.get_forecast(steps=FORECAST_DAYS)
pred_mean = forecast.predicted_mean
pred_ci = forecast.conf_int()

forecast_df = pd.DataFrame({
    "date": future_index,
    "predicted_reviews": pred_mean.values,
    "lower": pred_ci.iloc[:, 0].values,
    "upper": pred_ci.iloc[:, 1].values
})

os.makedirs("reports", exist_ok=True)
forecast_df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Saved forecast to {OUTPUT_CSV}")

# Optional plot
plt.figure(figsize=(10, 4))
plt.plot(daily.index, daily['review_count'], label="Historical")
plt.plot(forecast_df["date"], forecast_df["predicted_reviews"], label="Forecast")
plt.legend()
plt.title("Daily Review Count Forecast")
plt.tight_layout()
plt.savefig(OUTPUT_PLOT)
print(f"📈 Plot saved to {OUTPUT_PLOT}")
