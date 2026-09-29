import os

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\pipeline\temporal_ai.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_cold_start = '''        if len(window_df) < self.seq_len:
            # Padding if shorter than seq_len
            pad_rows = self.seq_len - len(window_df)
            padded_head = pd.DataFrame([window_df.iloc[0].to_dict()] * pad_rows)
            window_df = pd.concat([padded_head, window_df], ignore_index=True)

        window_df = window_df.tail(self.seq_len)
        data_clean = self._to_scale_invariant(window_df)

        # 1. Rolling Z-Score of the last timestep relative to the 24-hour window
        means = np.mean(data_clean[:-1], axis=0) if len(data_clean) > 1 else np.mean(data_clean, axis=0)
        stds = np.std(data_clean[:-1], axis=0) + 1e-6'''

good_cold_start = '''        # Cold Start Guard
        if len(window_df) < 3:
            return {
                "lstm_mse": 0.0,
                "threshold_mse": self.threshold_mse,
                "iso_forest_score": 0.0,
                "max_z_score": 0.0,
                "z_scores": {f: 0.0 for f in self.features},
                "is_temporal_anomaly": False
            }

        if len(window_df) < self.seq_len:
            # Padding if shorter than seq_len
            pad_rows = self.seq_len - len(window_df)
            padded_head = pd.DataFrame([window_df.iloc[0].to_dict()] * pad_rows)
            window_df = pd.concat([padded_head, window_df], ignore_index=True)

        window_df = window_df.tail(self.seq_len)
        data_clean = self._to_scale_invariant(window_df)

        # 1. Rolling Z-Score of the last timestep relative to the 24-hour window
        means = np.mean(data_clean[:-1], axis=0) if len(data_clean) > 1 else np.mean(data_clean, axis=0)
        stds = np.std(data_clean[:-1], axis=0)
        # Guard against zero variance in padded cold starts
        stds = np.maximum(stds, [0.5, 2.0, 1.0, 1.0])'''

content = content.replace(bad_cold_start, good_cold_start)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("temporal_ai patched successfully")
