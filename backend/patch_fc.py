import re
with open('../skyguard/pipeline/fault_classifier.py', 'r', encoding='utf-8') as f:
    content = f.read()

methods = '''    def save(self, filepath: str):
        import joblib
        joblib.dump({"model": self.model, "encoder": self.label_encoder}, filepath)
        
    def load(self, filepath: str):
        import joblib
        import os
        if os.path.exists(filepath):
            data = joblib.load(filepath)
            self.model = data["model"]
            self.label_encoder = data["encoder"]
            self.is_fitted = True
            return True
        return False
'''
content = content.replace('    def classify(self, feature_vector: np.ndarray) -> Tuple[str, float, Dict[str, float]]:', methods + '\n    def classify(self, feature_vector: np.ndarray) -> Tuple[str, float, Dict[str, float]]:')

with open('../skyguard/pipeline/fault_classifier.py', 'w', encoding='utf-8') as f:
    f.write(content)
