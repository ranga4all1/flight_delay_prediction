# Flight Delay prediction
As people increasingly choose to travel by air, the amount of flights that fail to take off on time also increases. This growth exacerbates the crowded situation at airports and causes financial difficulties within the airline industry. Air transportation delay indicates the lack of efficiency of the aviation system. It is a high cost to both airline companies and their passengers.

Predicting flight delays can improve airline operations and passenger satisfaction, which will result in a positive impact on the economy.

## Dataset
The dataset used for this analysis contains data about flights leaving from JFK airport between one year from `November 2019` to `December 2020`. It can be obtained from open data at https://www.kaggle.com/deepankurk/flight-take-off-data-jfk-airport. It includes 28820 lines of individual flight information with 23 columns. 

Any airline flights that departed or arrived 15 min late at their destination to be considered as delayed. Prediction of flight delays can be conducted on the variable `DEP_DELAY` (renamed as `IS_DELAYED`) by binary classification.

## Files included in this repo
1. `README.md` -  readme file with description of the problem and instructions on how to run the project
2. `notebook.ipynb` - dataset download, data cleaning, preprocessing, EDA, model selection and parameter tuning
3. `train.py` - training final model, saving it to file using BentoML
4. `service.py` - loading the model for inference(prediction), serving it via a web service using BentoML
5. `bentofile.yaml` - file with dependencies for building bento 

## Steps
1. Download dataset
2. Data cleaning and preprocessing
3. EDA
4. Model exploration and selection
5. Train final model
6. Save trained model using BentoML
7. Load saved model and serve it locally for prediction testing via swagger UI web service using BentoML
8. Build bento to create docker image, verify docker image, containerize docker image using bentoML and test locally using JSON/POST
9. Push container image to **GCP Container Registry**
10. Deploy to **Google cloud Run** (serverless offering by GCP) and verify/test deployed service by accessing public endpoint URL. 

### Notes:
 - Alternatively this model can be deployed as an API endpoint on the cloud using `bentoctl` -  supporting AWS SageMaker, AWS Lambda, EC2, Google Compute Engine, Google cloud run, Azure, Heroku and more.
 - CAUTION: Deploying model to clould services may **incurr charges** unless you use free tier (if available). Verify before deployment, delete after deployment to avoid recurring charges etc. 

### How to run this project?
 Prerequisite: Docker. If not installed already, install locally using https://docs.docker.com/

1. Clone the repo
```
git clone https://github.com/ranga4all1/flight_delay_prediction.git
```
2. Install all dependencies required for this project
```
pip install opendatasets scikit-learn xgboost pandas numpy bentoml 
```
3. Run `train.py' and supply your kaggle credentials when prompted (for dataset download from kaggle)
```
cd flight_delay_prediction
python train.py
```
3. Verify model saved by bentoML exists
```
bentoml models list
```
4. Load saved model and serve it locally for prediction testing via swagger UI web service using BentoML. 
```
cd flight_delay_prediction_service_bentoml
bentoml serve service.py:svc --reload
```
    - Go to http://0.0.0.0:3000
    - Click on Service APIs -> POST -> Try it out. Fill out 'request body' with JSON input and click -> Execute
    - Check 'Response body' - e. g. 

        {
        "status": "NOT DELAYED"
        }

    - Use this json input for testing. Modify values to test multiple times and obtain various results - "DELAYED". "MAYBE", "NOT DELAYED"

    {
    "month": 11,
    "day_of_month": 21,
    "day_of_week": 4,
    "carrier_code": "dl",
    "dest": "bos",
    "scheduled_duration": 80,
    "distance": 187,
    "scheduled_departure": 420,
    "actual_dep_time": 420,
    "scheduled_arrival": 500,
    "temperature": 39,
    "dew_point": 33,
    "humidity": 79,
    "wind": "nne",
    "wind_speed": 3,
    "wind_gust": 0,
    "pressure": 30.2,
    "condition": "fair",
    "flt_sch_arrival": 41,
    "flt_sch_departure": 31,
    "taxi_out": 27
    }


5. Build a Bento - run the `bentoml build` CLI command from the same directory
```
bentoml build
```
6. Verify bento
```
bentoml list
```
7. Serve production ready bento locally and test
```
bentoml serve flight_delay_classifier:latest --production
```
8. Containerize bento
```
bentoml containerize flight_delay_classifier:latest
```
9. Verify docker container created
```
docker images
```
10. Run the docker image to start the BentoServer and test
```
docker run -it --rm -p 3000:3000 flight_delay_classifier:latest serve --production
```
11. Deploy to **Google cloud run** using `bentoctl` or manually using this guide - https://docs.bentoml.org/en/0.13-lts/deployment/google_cloud_run.html

Note: This project has been deployed to 'Google cloud run' and is available at this URL: https://flight-delay-prediction-service-4wgcgnt6oq-wn.a.run.app
This deployment will be tear down after 2 weeks.

## References
- Docker:  https://docs.docker.com/ 
- BentoML:  https://docs.bentoml.org/en/latest/index.html
- bentoctl: https://github.com/bentoml/bentoctl
- GCP Container Registry: https://cloud.google.com/container-registry
- Google cloud Run: https://cloud.google.com/run