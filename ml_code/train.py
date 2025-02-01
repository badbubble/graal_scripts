import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# create the dataset
data = pd.read_csv("data/data.csv", sep="@")

numeric_columns = data.select_dtypes(include=[np.number]).columns
mask = (data[numeric_columns].abs() <= 10000).all(axis=1)
data = data[mask]

data = data.replace([np.inf, -np.inf], np.nan).dropna()
data = data.dropna()




function_names = data["funcName"]

# split features and target
X = data.drop(['funcName', 'decision'], axis=1)
y = data['decision']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(
    learning_rate=0.1,
    max_depth=3,
    n_estimators=100,
    objective='binary:logistic',
    random_state=42
)

# train
model.fit(X_train, y_train)

# pred
y_pred = model.predict(X_test)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)

# feature importance
plt.figure(figsize=(12, 6))
sns.barplot(x='importance', y='feature', data=feature_importance.head(10))
plt.title('Top 10 Most Important Features')
plt.tight_layout()
plt.savefig("importance.png")

# confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.tight_layout()
plt.show()

# make predictions on new data
def predict_inlining(model, new_data):
    prediction = model.predict(new_data)
    probability = model.predict_proba(new_data)
    return prediction[0], probability[0]


model.save_model('inlining_decision_model.json')