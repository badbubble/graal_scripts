## Machine learning model

training
```bash
python -m venv .venv
source .venv/bin/active
pip install -r requirments.txt
mkdir models
python train_xgboost.py --data_dir data/ --output_dir models
```

inferencing
```bash
python train_xgboost.py --mode inference --model_path models/future-genetic_data_xgb.json --scaler_path models/future-genetic_data_scaler.joblib  --input_file data/future-genetic_data.csv --out
put_file ml_result.cs
```