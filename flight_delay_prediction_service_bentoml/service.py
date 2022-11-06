# JFL flight delay service deployment with bentoml

import numpy as np

import bentoml
from bentoml.io import JSON

model_ref = bentoml.xgboost.get("flight_delay_prediction_model:4hcrkocziwoxpvpc")
dv = model_ref.custom_objects['dictVectorizer']

model_runner = model_ref.to_runner()

svc = bentoml.Service("flight_delay_classifier", runners=[model_runner])


@svc.api(input=JSON(), output=JSON())
async def classify(application_data):
    vector = dv.transform(application_data)
    prediction = await model_runner.predict.async_run(vector)
    print(prediction)
    result = prediction[0]

    if result > 0.5:
        return {
            "status": "DELAYED"
        }
    elif result > 0.25:
        return {
            "status": "MAYBE"
        }
    else:
        return {
            "status": "NOT DELAYED"
        }