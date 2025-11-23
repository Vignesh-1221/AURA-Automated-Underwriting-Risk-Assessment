import joblib
import os

class ModelLoader:
    _model = None

    @classmethod
    def load_model(cls, model_path: str):
        """Singleton pattern to load model only once."""
        if cls._model is None:
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}. Run train_model.py first.")
            print(f"🧠 Loading AI Model from {model_path}...")
            cls._model = joblib.load(model_path)
        return cls._model