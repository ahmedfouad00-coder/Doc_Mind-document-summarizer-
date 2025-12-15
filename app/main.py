
from fastapi import FastAPI
from app.services.inference import predict, load_model

app = FastAPI(title='deepseek - converted API')

@app.on_event('startup')
def startup_event():
    # load model or resources here if needed
    try:
        app.state.model = load_model()
    except Exception as e:
        print('Warning: load_model() failed on startup:', e)

@app.get('/')
def root():
    return {'status':'ok', 'service':'deepseek API'}

@app.post('/predict')
def run_predict(payload: dict):
    model = getattr(app.state, 'model', None)
    data = payload.get('data', None)
    if data is None:
        return {'error':'send JSON with key "data"'}
    result = predict(data, model=model)
    return {'prediction': result}
