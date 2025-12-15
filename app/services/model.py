
# model helper: load/save wrappers for common formats
import joblib, os

def save_model(obj, path='models/model.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(obj, path)

def load_model(path='models/model.pkl'):
    if os.path.exists(path):
        return joblib.load(path)
    raise FileNotFoundError(path)
