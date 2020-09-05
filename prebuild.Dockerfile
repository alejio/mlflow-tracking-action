FROM python:3.7.6

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY mlflow_tracking_get_runs.py /mlflow_tracking_get_runs.py
RUN chmod u+x /mlflow_tracking_get_runs.py

ENTRYPOINT ["python",  "/mlflow_tracking_get_runs.py"]