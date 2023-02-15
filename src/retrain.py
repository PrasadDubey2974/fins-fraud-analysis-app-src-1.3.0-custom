import pandas as pd
from sklearn.metrics import average_precision_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.utils import resample
from functools import reduce
import pickle
from os import path

# if path.exists("xgboost_model.dat"):
#     quit()

print("Beginning Retrain")

def combine_rfs(rf_a, rf_b):
    rf_a.estimators_ += rf_b.estimators_
    rf_a.n_estimators = len(rf_a.estimators_)
    return rf_a

columns = [ 
    "amount", 
    "oldbalanceOrg", 
    "newbalanceOrig",  
    "oldbalanceDest", 
    "newbalanceDest",
    "CASH_IN",
    "CASH_OUT",
    "DEBIT",
    "PAYMENT",
    "TRANSFER"
]

def one_hot_encode_column(df, column):
    one_hot = pd.get_dummies(df.type)
    df = df.drop("type", axis=1)
    df = df.join(one_hot)

    return df

def upsample_isFraud(df):
    df_majority = df[df.isFraud==0]
    df_minority = df[df.isFraud==1]
    samples = len(df_majority)
    df_minotiry_resampled = resample(df_minority, replace=True, n_samples=samples)
    df_upsampled = pd.concat([df_majority, df_minotiry_resampled])

    return df_upsampled

def split_dataset(df, x_columns, y_columns):
    return df_upsampled[x_columns], df_upsampled[y_columns]

booster = None
model = None
iteration = 1
for df in pd.read_csv("SimulatedData.csv", chunksize=100000):
    # Encode type into 5 columns with 1-hot encoding
    df = one_hot_encode_column(df, "type")
    
    # upsample minority class to balance the dataset
    df_upsampled = upsample_isFraud(df)
    
    # Separate X and Y
    X, Y = split_dataset(df_upsampled, columns, ["isFraud"])

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    
    model = XGBClassifier()
    
    if iteration == 1:
        model.fit(X_train, Y_train, verbose=1)
    else:
        model.fit(X_train, Y_train, xgb_model=booster, verbose=True)

    booster = model.get_booster()

# test model and output score
iterations = 10
current_i = 1
for df in pd.read_csv("SimulatedData.csv", chunksize=100000):
    # Encode type into 5 columns with 1-hot encoding
    df = one_hot_encode_column(df, "type")
    
    # upsample minority class to balance the dataset
    df_upsampled = upsample_isFraud(df)

    # Separate X and Y
    X, Y = split_dataset(df_upsampled, columns, ["isFraud"])

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.75, random_state=24)

    probabilities = model.predict_proba(X_test)
    print(f"Test Iteration {current_i} - Score: {average_precision_score(Y_test, probabilities[:, 1])}")
    if current_i == iterations:
        break

    current_i += 1


pickle.dump(model, open("xgboost_model.dat", "wb"))

print("Retrain completed")