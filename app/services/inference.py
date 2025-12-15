
# inference wrapper that tries to use functions from scripts/notebook_code.py
from importlib import util, machinery
import os, sys

# import the generated notebook_code module
nb_module_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'notebook_code.py')
nb_module_path = os.path.abspath(nb_module_path)

spec = util.spec_from_file_location('deepseek_notebook', nb_module_path)
nb = util.module_from_spec(spec)
spec.loader.exec_module(nb)

def load_model():
    # try common names used in notebooks
    for name in ('model', 'clf', 'model_obj', 'trainer'):
        if hasattr(nb, name):
            return getattr(nb, name)
    # no model found; return None
    return None

def predict(data, model=None):
    # try notebook-level functions
    for fn_name in ('predict', 'inference', 'run_inference'):
        if hasattr(nb, fn_name):
            try:
                return getattr(nb, fn_name)(data)
            except Exception as e:
                return {{'error': f'exception when calling {{fn_name}}: {{e}}'}}
    # fallback: if model object with predict exists
    if model is not None and hasattr(model, 'predict'):
        try:
            return model.predict(data)
        except Exception as e:
            return {{'error': f'model.predict failed: {{e}}'}}
    return {{'error':'no predict/inference function found in notebook_code. Open scripts/notebook_code.py to adapt.'}}
