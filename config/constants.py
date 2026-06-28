from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

FORECAST_HORIZON = 30  # forecast N days ahead
TRAIN_TEST_SPLIT_RATIO = 0.8
CV_FOLDS = 5
OPTUNA_N_TRIALS = 20  # 50 for production
