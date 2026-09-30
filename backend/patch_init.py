with open('app/services/ingestion_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_replacement = '''
        # Load ML Pipeline
        try:
            from skyguard.main_pipeline import SkyGuardPipeline
            from app.api.routes.predict import generate_dummy_training_data
            
            pipeline = SkyGuardPipeline()
            train_df = generate_dummy_training_data()
            pipeline.fit(train_df)
            pipeline.temporal_ai.threshold_mse = 3.0
            pipeline.recent_history = train_df.to_dict("records")[-24:]
        except ImportError as e:
'''
content = content.replace('''
        # Load ML Pipeline
        try:
            from skyguard.main_pipeline import SkyGuardPipeline
            pipeline = SkyGuardPipeline()
        except ImportError as e:''', import_replacement)

with open('app/services/ingestion_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
