import re
with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_get_pipeline = '''def get_pipeline():
    global pipeline
    if pipeline is None:
        pipeline = SkyGuardPipeline()
        train_df = generate_dummy_training_data()
        pipeline.fit(train_df)
        pipeline.temporal_ai.threshold_mse = 3.0
        pipeline.recent_history = train_df.to_dict("records")[-24:]
    return pipeline'''

new_get_pipeline = '''def get_pipeline():
    global pipeline
    if pipeline is None:
        import os
        pipeline = SkyGuardPipeline()
        model_dir = os.path.join(os.path.dirname(__file__), "../../../skyguard/models")
        
        has_models = False
        if os.path.exists(model_dir):
            fc_loaded = pipeline.fault_classifier.load(os.path.join(model_dir, "classifier.pkl"))
            temp_loaded = pipeline.temporal_ai.load(os.path.join(model_dir, "temporal"))
            if fc_loaded and temp_loaded:
                has_models = True
                
        if not has_models:
            train_df = generate_dummy_training_data()
            pipeline.fit(train_df)
            pipeline.temporal_ai.threshold_mse = 3.0
            
        # We always need some recent history
        train_df = generate_dummy_training_data()
        pipeline.recent_history = train_df.to_dict("records")[-24:]
    return pipeline'''

content = content.replace(old_get_pipeline, new_get_pipeline)

# Fix generate_dummy_training_data to return a realistic history, NOT a perfect sine wave.
# Because the prompt said: "Train Stage 2 on realistic clean history (not a perfect sine wave)"
old_gen = '''def generate_dummy_training_data():
    start = datetime.now() - timedelta(hours=100)
    data = []
    for i in range(100):
        data.append({
            "time": (start + timedelta(hours=i)).isoformat(),
            "temperature_2m": 25.0 + np.sin(i / 24.0) * 5,
            "relative_humidity_2m": 50.0 + np.cos(i / 24.0) * 10,
            "surface_pressure": 1013.0 + np.sin(i / 12.0) * 2,
            "pressure_msl": 1013.0 + np.sin(i / 12.0) * 2 + 21.1,
            "anomaly_type": "CLEAN"
        })
    return pd.DataFrame(data)'''

new_gen = '''def generate_dummy_training_data(hours=100):
    import numpy as np
    start = datetime.now() - timedelta(hours=hours)
    data = []
    for i in range(hours):
        # Add some random noise so it's realistic, not a perfect curve
        data.append({
            "time": (start + timedelta(hours=i)).isoformat(),
            "temperature_2m": 25.0 + np.sin(i / 24.0) * 5 + np.random.normal(0, 0.5),
            "relative_humidity_2m": 50.0 + np.cos(i / 24.0) * 10 + np.random.normal(0, 1.0),
            "surface_pressure": 1013.0 + np.sin(i / 12.0) * 2 + np.random.normal(0, 0.5),
            "pressure_msl": 1013.0 + np.sin(i / 12.0) * 2 + 21.1 + np.random.normal(0, 0.5),
            "anomaly_type": "CLEAN"
        })
    return pd.DataFrame(data)'''

content = content.replace(old_gen, new_gen)
with open('app/api/routes/predict.py', 'w', encoding='utf-8') as f:
    f.write(content)
