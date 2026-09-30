import os, sys
sys.path.append(os.getcwd())
from app.api.routes.predict import get_pipeline
print("Starting get_pipeline...")
p = get_pipeline()
print("get_pipeline complete!")
if hasattr(p.fault_classifier, 'is_fitted') and p.fault_classifier.is_fitted:
    print("Fault classifier is fitted.")
if hasattr(p.temporal_ai, 'is_fitted') and p.temporal_ai.is_fitted:
    print("Temporal AI is fitted.")
