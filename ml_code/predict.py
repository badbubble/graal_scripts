import pandas as pd
import numpy as np
import xgboost as xgb
import joblib

def predict_data(model_path, input_path, output_path):
    booster = xgb.Booster()
    booster.load_model(model_path)

    data = pd.read_csv(input_path, sep="@", names= ['funcName', 'probability', 'relevance', 'inliningBonus', 'nodes',
               'lowLevelGraphSize', 'invokes', 'inliningDepth', 'isIntrinsic',
               'shouldInline', 'hasSubstitution', 'inlineEverything', 'isTracing',
               'fullyProcessed', 'nodesToMaximumNodesRatio', 'lowLevelGraphSizeToThresholdRatio',
               'invokesToLimitRatio', 'probabilityRelevanceInteraction',
               'nodesInliningBonusInteraction', 'decision'])
    
    print(f"Initial shape: {data.shape}")
    
    function_names = data["funcName"].map(lambda x: x.split("#")[1])
    
    # replace infinite values with NaN
    data = data.replace([np.inf, -np.inf], np.nan)
    
    data = data.dropna()
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    mask = (data[numeric_columns].abs() <= 10000).all(axis=1)
    data = data[mask]
    
    print(f"Shape after cleaning and filtering: {data.shape}")
    
    feature_cols = [col for col in data.columns if col not in ['funcName', 'decision']]
    X = data[feature_cols]
    
    dtest = xgb.DMatrix(X)
    
    probabilities = booster.predict(dtest)
    predictions = (probabilities > 0.5).astype(int)
    
    results = pd.DataFrame({
        'funcName':  data["funcName"].map(lambda x: x.split("#")[1]),
        'predicted_decision': predictions,
        'real': data['decision'],
    })
    
    results.to_csv(output_path, index=False, sep='@')
    print(f"Results saved to {output_path}")
    
    print("\nPrediction Summary:")
    print(f"Total predictions: {len(predictions)}")
    print(f"Predicted 0s: {sum(predictions == 0)}")
    print(f"Predicted 1s: {sum(predictions == 1)}")

if __name__ == "__main__":
    MODEL_PATH = "inlining_decision_model.json"
    INPUT_PATH = "../data/akka-uct_data_r12.csv" 
    OUTPUT_PATH = "../ml_results/predictions.csv"
    
    predict_data(MODEL_PATH, INPUT_PATH, OUTPUT_PATH)