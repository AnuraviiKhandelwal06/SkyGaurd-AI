import os, sys
sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
pipeline = SkyGuardPipeline()
model_dir = os.path.join(os.getcwd(), "../skyguard/models")
fc_loaded = pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
temp_loaded = pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
print('fc_loaded:', fc_loaded, 'temp_loaded:', temp_loaded)
