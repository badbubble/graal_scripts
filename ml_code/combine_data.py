import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
from pathlib import Path
import itertools
import joblib

NOTBUILT_BENCHMARKS = [
    "als_data",
    "chi-square_data",
    "db-shootout_data",
    "dec-tree_data",
    "dooty_data",
    "finagle-chriper_data",
    "finagle-http_data",
    "log-regression_data",
    "movie-lens_data",
    "navie-bayes_data",
    "neo4j-analytics_data",
    "page-rank_data",
    "philososphers_data",
    "reactors_data",
    "scala-stm-bench7_data",
    "scrabble_data",
]

def load_csv_file(file_path):
    """Load a single CSV file without headers and handle duplicate function names."""
    columns = ['funcName', 'probability', 'relevance', 'inliningBonus', 'nodes',
               'lowLevelGraphSize', 'invokes', 'inliningDepth', 'isIntrinsic',
               'shouldInline', 'hasSubstitution', 'inlineEverything', 'isTracing',
               'fullyProcessed', 'nodesToMaximumNodesRatio', 'lowLevelGraphSizeToThresholdRatio',
               'invokesToLimitRatio', 'probabilityRelevanceInteraction',
               'nodesInliningBonusInteraction', 'decision']
    
    try:
        df = pd.read_csv(file_path, header=None, names=columns, dtype={
            'funcName': str,
            'probability': float,
            'relevance': float,
            'inliningBonus': float,
            'nodes': int,
            'lowLevelGraphSize': int,
            'invokes': float,
            'inliningDepth': int,
            'isIntrinsic': int,
            'shouldInline': int,
            'hasSubstitution': int,
            'inlineEverything': int,
            'isTracing': int,
            'fullyProcessed': int,
            'nodesToMaximumNodesRatio': float,
            'lowLevelGraphSizeToThresholdRatio': float,
            'invokesToLimitRatio': float,
            'probabilityRelevanceInteraction': float,
            'nodesInliningBonusInteraction': float,
            'decision': int
        }, sep='@')

        return df
        
    except Exception as e:
        print(f"Error loading file {file_path}: {str(e)}")
        raise
        

def load_benchmark_data(data_dir):
    """Load and combine data from all NOTBUILT benchmarks."""
    all_data = []
    data_dir = Path(data_dir)
    
    for benchmark in NOTBUILT_BENCHMARKS:
        file_path = data_dir / f"{benchmark}.csv"
        if file_path.exists():
            print(f"Loading {file_path}")
            df = load_csv_file(file_path)
            all_data.append(df)
    
    if not all_data:
        raise ValueError("No benchmark data files found")
            
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Total combined rows: {len(combined_df)}")
    combined_df = combined_df.drop_duplicates()
    combined_df.to_csv("data/data.csv", index=False, encoding='utf-8', sep='@')

    return combined_df

if __name__ == "__main__":
    load_benchmark_data("data/")