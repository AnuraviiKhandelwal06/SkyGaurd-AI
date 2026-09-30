import re
with open('../skyguard/pipeline/temporal_ai.py', 'r', encoding='utf-8') as f:
    content = f.read()

methods = '''    def save(self, filepath: str):
        import joblib, os
        import torch
        base_dir = os.path.dirname(filepath)
        os.makedirs(base_dir, exist_ok=True)
        joblib.dump({"scaler": self.scaler, "iso": self.iso_forest, "thresh": self.threshold_mse}, filepath + "_sklearn.pkl")
        if self.use_pytorch and self.lstm_model is not None:
            torch.save(self.lstm_model.state_dict(), filepath + "_lstm.pt")
            
    def load(self, filepath: str):
        import joblib, os
        import torch
        if os.path.exists(filepath + "_sklearn.pkl"):
            data = joblib.load(filepath + "_sklearn.pkl")
            self.scaler = data["scaler"]
            self.iso_forest = data["iso"]
            self.threshold_mse = data.get("thresh", 0.5)
            self.is_fitted = True
            
            if self.use_pytorch and os.path.exists(filepath + "_lstm.pt"):
                self.lstm_model = LSTMAutoencoder(self.seq_len, len(self.features))
                self.lstm_model.load_state_dict(torch.load(filepath + "_lstm.pt", weights_only=True))
                self.lstm_model.eval()
            return True
        return False
'''
content = content.replace('    def evaluate_window(self, window_df: pd.DataFrame) -> Dict[str, Any]:', methods + '\n    def evaluate_window(self, window_df: pd.DataFrame) -> Dict[str, Any]:')

with open('../skyguard/pipeline/temporal_ai.py', 'w', encoding='utf-8') as f:
    f.write(content)
