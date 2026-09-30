# SkyGuard AI — Evaluation & Performance Report

## 1. Multi-Class Fault Classifier Metrics

```
              precision    recall  f1-score   support

       CLEAN       1.00      0.92      0.95       495
       SPIKE       0.75      0.75      0.75         4
      FROZEN       0.00      0.00      0.00         0
       DRIFT       0.00      0.00      0.00         0
COMM_FAILURE       0.00      0.00      0.00         0
INCONSISTENT       1.00      1.00      1.00         1

   micro avg       0.92      0.91      0.92       500
   macro avg       0.46      0.44      0.45       500
weighted avg       1.00      0.91      0.95       500

```

## 2. Self-Healing Imputation Accuracy

- **Temperature Imputation**: RMSE = `0.711°C`, MAE = `0.560°C`
- **Surface Pressure Imputation**: RMSE = `4.563 hPa`, MAE = `3.332 hPa`

## 3. Evaluation Setup Summary

- **Station Network**: 4 time-aligned Open-Meteo stations (2010-01-01 to 2024-02-20)
- **Test Set Window**: 2023-01-01 to 2024-02-20 (9,984 rows, ~13.7 months / 416 days)
- **Injected Anomaly Rate**: 4.0%
