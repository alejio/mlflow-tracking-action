"""
Retrieves runs from MLflow corresponding to specific tags.

The purpose is to compare a candidate run with a specified baseline run within a PR workflow.
"""

import os
import mlflow
import logging
from typing import Any, Tuple, Optional


# Read Inputs
mlflow_tracking_uri = os.getenv("INPUT_MLFLOW_TRACKING_URI")
mlflow_username = os.getenv("INPUT_MLFLOW_TRACKING_USERNAME")
mlflow_password = os.getenv("INPUT_MLFLOW_TRACKING_PASSWORD")
experiment_id = os.getenv("INPUT_EXPERIMENT_ID")
baseline_run_query = os.getenv("INPUT_BASELINE_RUN_QUERY")
candidate_run_query = os.getenv("INPUT_CANDIDATE_RUN_QUERY")
debug = os.getenv("INPUT_DEBUG")

if debug:
    logging.root.setLevel(logging.DEBUG)
logging.debug(f"EXPERIMENT_ID: {experiment_id}")
logging.debug(f"BASELINE_RUN_QUERY: {baseline_run_query}")
logging.debug(f"CANDIDATE_RUN_QUERY: {candidate_run_query}")

# Validate inputs
assert isinstance(mlflow_tracking_uri, str), "tracking_uri must be valid"
assert isinstance(experiment_id, str), "experiment_id must be a string"
assert isinstance(baseline_run_query, str), "run query must be a string"
assert isinstance(candidate_run_query, str), "run query must be a string"


# Fetch the runs
def fetch_runs(
    tracking_uri: str,
    username: Optional[str],
    password: Optional[str],
    experiment_id: str,
    baseline_query: str,
    candidate_query: str,
) -> Tuple[Any, Any]:
    mlflow.set_tracking_uri(tracking_uri)
    os.environ["MLFLOW_TRACKING_USERNAME"] = username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = password
    baseline_run = mlflow.search_runs(
        experiment_ids=[experiment_id], filter_string=baseline_query
    )
    candidate_run = mlflow.search_runs(
        experiment_ids=[experiment_id], filter_string=candidate_query
    )

    assert len(baseline_run) != 0, "Baseline run not found"
    assert len(candidate_run) != 0, "Candidate run not found"

    return baseline_run.iloc[0], candidate_run.iloc[0]


# Fetch the runs
baseline_run, candidate_run = fetch_runs(
    mlflow_tracking_uri,
    mlflow_username,
    mlflow_password,
    experiment_id,
    baseline_run_query,
    candidate_run_query,
)


# Emit variables as outputs for other actions
print(
    f"::set-output name=BOOL_COMPLETE::{True if (baseline_run is not None) and (candidate_run is not None) else False}"
)
print(f"::set-output name=EXPERIMENT_ID::{experiment_id}")
print(f'::set-output name=BASELINE_RUNID::{baseline_run["run_id"]}')
print(
    f'::set-output name=BASELINE_TRAIN_ACCURACY::{baseline_run["metrics.training accuracy"]}'
)
print(
    f'::set-output name=BASELINE_TEST_ACCURACY::{baseline_run["metrics.test accuracy"]}'
)
print(
    f'::set-output name=BASELINE_ARTIFACT_URI::{baseline_run["artifact_uri"]}'
)
print(f'::set-output name=BASELINE_RUNID::{candidate_run["run_id"]}')
print(
    f'::set-output name=CANDIDATE_TRAIN_ACCURACY::{candidate_run["metrics.training accuracy"]}'
)
print(
    f'::set-output name=CANDIDATE_TEST_ACCURACY::{candidate_run["metrics.test accuracy"]}'
)
print(
    f'::set-output name=CANDIDATE_ARTIFACT_URI::{candidate_run["artifact_uri"]}'
)
