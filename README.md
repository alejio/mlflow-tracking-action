# GitHub Action That Retrieves Model Runs From MLflow Tracking

MLflow Tracking [homepage](https://www.mlflow.org/docs/latest/tracking.html/)

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Usage](#usage)
  - [Example](#example)
  - [Inputs](#inputs)
    - [Mandatory Inputs](#mandatory-inputs)
  - [Outputs](#outputs)
- [Features of This Action](#features-of-this-action)
  - [Querying Model Runs](#querying-model-runs)

<!-- /TOC -->

## Usage

### Example

```yaml
name: Get Runs From MLflow Tracking remote server
on: [issue_comment]

jobs:
  get-runs:
    if: (github.event.issue.pull_request != null) &&  contains(github.event.comment.body, '/get-runs')
    runs-on: ubuntu-latest

    steps:
  - name: Get Runs Using tags
    uses: alejio/mlflow-tracking-action@master
    with:
      MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
      EXPERIMENT_ID: "0"
      BASELINE_RUN_QUERY: "tags.live='1'"
      CANDIDATE_RUN_QUERY: "production_ready='1'"
```

### Inputs

#### Mandatory Inputs

  1. `MLFLOW_TRACKING_URI`: The tracking URI of your MLflow remote server, including username and password. Example "http://ec2-1-2-345-678.eu-west-2.compute.amazonaws.com".
  2. `MLFLOW_TRACKING_USERNAME`: Username for MLflow server authentication.
  3. `MLFLOW_TRACKING_PASSWORD`: Password for MLflow server authentication.
  4. `EXPERIMENT_ID`:  The MLflow experiment_id against which relevant runs were executed.
  5. `BASELINE_RUN_QUERY`: Baseline run query string for using in `mlflow.search_runs` `filter_string` param.
  6. `CANDIDATE_RUN_QUERY`: Candidate run query string for using in `mlflow.search_runs` `filter_string` param.

### Outputs

You can reference the outputs of an action using [expression syntax](https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions).

1. `BOOL_COMPLETE`: True if both runs were fetched successfully.
2. `BASELINE_TRAIN_ACCURACY`: Training accuracy of baseline run.
3. `BASELINE_TEST_ACCURACY`: Training accuracy of baseline run.
4. `BASELINE_ARTIFACT_URI`: Artifact URI for baseline run.
5. `CANDIDATE_TRAIN_ACCURACY`: Training accuracy of baseline run.
6. `CANDIDATE_TEST_ACCURACY`: Training accuracy of baseline run.
7. `CANDIDATE_ARTIFACT_URI`: Artifact URI for baseline run.

## Features of This Action

### Querying Model Runs

This action fetches 2 model runs:

1. **Baseline run**: The baseline run corresponds to the currently deployed live model that we are looking to replace with the candidate.
2. **Candidate run**: The candidate run corresponds to a model that aims to replace the currently live one.

## Keywords

 MLOps, Machine Learning, Data Science
