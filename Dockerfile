FROM alexsp/mlflow-tracking-action

ENTRYPOINT ["python",  "/mlflow_tracking_get_runs.py"]