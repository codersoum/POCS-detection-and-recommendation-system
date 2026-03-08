import pandas as pd
import numpy as np
import pickle as pk
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
try:
    dataset = pd.read_excel('PCOS_data_without_infertility.xlsx',sheet_name='Full_new')
    for columns in dataset.columns:
        if dataset[columns].dtype == 'object':
            dataset[columns]=pd.to_numeric(dataset[columns] , errors='coerce')
    dataset=dataset.fillna(dataset.mean())
    print(dataset)
    features=dataset.drop('PCOS (Y/N)', axis=1)
    target=dataset['PCOS (Y/N)']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    importances= model.feature_importances_
    feature_names=features.columns
    feature_importances_index=pd.Series(importances,index=feature_names).sort_values(ascending=False).head(7).index.tolist()
    model.fit(X_train[feature_importances_index], y_train)
    y_pred = model.predict(X_test[feature_importances_index])
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Confidence Scores for each feature:")
    for feature, importance in zip(feature_importances_index, model.feature_importances_[model.feature_importances_ != 0]):
        print(f"  {feature}: {importance:.4f}")
    with open('model.pkl', 'wb') as file:
        pk.dump(model, file)
    with open('features.pkl', 'wb') as file:
        pk.dump(feature_importances_index, file)
except Exception as e:
    print(f"An error occurred: {e}")