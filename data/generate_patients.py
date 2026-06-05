import numpy as np
import pandas as pd
import os

def generate_patient_stream(patient_id, condition, n_readings=200):
    """Generate realistic vitals with occasional anomalies."""
    baselines = {
        "diabetes":     {"glucose": 140, "bp_sys": 130, "heart_rate": 78},
        "hypertension": {"glucose": 95,  "bp_sys": 160, "heart_rate": 82},
        "cardiac":      {"glucose": 100, "bp_sys": 125, "heart_rate": 95},
    }
    b = baselines[condition]
    records = []
    for i in range(n_readings):
        anomaly = (i % 40 == 0)
        records.append({
            "patient_id":  patient_id,
            "timestamp":   (pd.Timestamp.now() + pd.Timedelta(minutes=i * 15)).isoformat(),
            "glucose":     round(b["glucose"] + np.random.normal(0, 10) + (60 if anomaly else 0), 1),
            "bp_sys":      round(b["bp_sys"]  + np.random.normal(0, 8)  + (30 if anomaly else 0), 1),
            "heart_rate":  round(b["heart_rate"] + np.random.normal(0, 5), 1),
            "condition":   condition,
            "anomaly":     anomaly,
        })
    return pd.DataFrame(records)


if __name__ == "__main__":
    patients = [
        (1, "diabetes"),
        (2, "hypertension"),
        (3, "cardiac"),
    ]
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    for pid, cond in patients:
        df = generate_patient_stream(pid, cond)
        path = os.path.join(os.path.dirname(__file__), f"patient_{pid}.csv")
        df.to_csv(path, index=False)
        print(f"Generated {len(df)} readings for patient {pid} ({cond}) → {path}")
