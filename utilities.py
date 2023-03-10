"""
This module contains utility functions.

author: Chinedu Ezeofor
"""

# Standard imports
import numpy as np
import pandas as pd

# Sklearn
from sklearn import metrics
from sklearn.pipeline import Pipeline

from pydantic import BaseModel
import mlflow

# Built-in
import typing as tp
import warnings


def eval_metrics(actual: np.ndarray, pred: np.ndarray) -> tp.Tuple:
    """This is used to evaluate the performance of the model."""
    rmse = metrics.mean_squared_error(actual, pred, squared=False)
    mse = metrics.mean_squared_error(actual, pred, squared=True)
    mae = metrics.mean_absolute_error(actual, pred)
    r2 = metrics.r2_score(actual, pred)

    return (rmse, mse, mae, r2)


Estimator = tp.Union[Pipeline, tp.Any]  # Alias for estimator


class Experiment(BaseModel):
    """This contains the experiment meta data"""

    experiment_name: str
    run_name: str
    model_name: str
    tracking_uri: str


class TrainingData(BaseModel):
    """This is the training data."""

    X_train: tp.Union[pd.DataFrame, np.ndarray]
    X_validate: tp.Union[pd.DataFrame, np.ndarray]
    y_train: tp.Union[pd.Series, np.ndarray]
    y_validate: tp.Union[pd.Series, np.ndarray]

    class Config:
        arbitrary_types_allowed = True


def run_experiment(
    *, experiment: Experiment, estimator: Estimator, training_data: TrainingData
) -> None:
    """This is used to track an MLFlow experiment.

    Params:
    -------
    experiment (Experiment): Experiment object which contains the experiment meta data.
    estimator (Estimator): Estimator object which contains the estimator meta data.
    training_data (TrainingData): Data used for training and validation.

    Returns:
    --------
    None
    """

    from urllib.parse import urlparse
    import warnings
    import logging

    warnings.filterwarnings("ignore")  # Required

    delim = "::"
    format_ = f"%(levelname)s {delim} %(asctime)s {delim} %(message)s"

    logging.basicConfig(level=logging.INFO, format=format_)

    logger = logging.getLogger(__name__)

    # Config
    mlflow.set_tracking_uri(experiment.tracking_uri)
    mlflow.set_experiment(experiment.experiment_name)

    with mlflow.start_run(run_name=experiment.run_name):
        mlflow.sklearn.autolog()
        logger.info(f"========= Training {experiment.model_name!r} =========")
        estimator.fit(training_data.X_train, training_data.y_train)

        # Make predictions
        y_pred = estimator.predict(training_data.X_validate)

        (rmse, mse, mae, r2) = eval_metrics(
            actual=training_data.y_validate, pred=y_pred
        )
        print(f" Model name: {experiment.model_name}")
        print(f"  RMSE: {rmse}")
        print(f"  MSE: {mse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        # Log params/metrics on MLFlow
        # I'm using autolog

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":

            # Register the model
            mlflow.sklearn.log_model(
                estimator, "model", registered_model_name=experiment.model_name
            )
        else:
            mlflow.sklearn.log_model(estimator, "model")
    logger.info(f"========= Training {experiment.model_name!r} Done! =========")
    