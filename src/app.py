from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from xgboost import XGBClassifier, Booster
import pickle
import numpy as np
import pandas as pd 

app = Flask(__name__)
api = Api(app)
print("App Loading")
model = pickle.load(open("xgboost_model.dat", "rb"))
print("Model Loaded")

json_columns = [ 
    "transaction_amount",
    "old_balance_originator",
    "new_balance_originator",
    "old_balance_destination",
    "new_balance_destination",
    "type"
]

model_columns = [ 
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

def check_type(type):
    if type not in ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]:
        abort(400, "Type not allowed")

class Healthcheck(Resource):

    @staticmethod
    def get():
        return "I'm Alive!", 200


class FraudModel(Resource):

    # json format
    # {
    #     "transaction_amount": decimal,
    #     "old_balance_originator": decimal,
    #     "new_balance_originator": decimal,
    #     "old_balance_destination": decimal,
    #     "new_balance_destination": decimal,
    #     "type": string["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
    # }

    @staticmethod
    def post():
        posted_data = request.get_json()

        data = request.json
        missing_columns = []
        for key in data:
            if key not in json_columns:
                missing_columns.append(key)

        if len(missing_columns) > 0:
            error_message = f"Bad Request. Missing fields {', '.join(missing_columns)}"
            abort(400, error_message)

        check_type(data["type"])

        input_data = {
            "amount": [data["transaction_amount"]],
            "oldbalanceOrg": [data["old_balance_originator"]],
            "newbalanceOrig": [data["new_balance_originator"]],
            "oldbalanceDest": [data["old_balance_destination"]],
            "newbalanceDest": [data["new_balance_destination"]],
            "CASH_IN": [1 if data["type"].upper() == "CASH_IN" else 0],
            "CASH_OUT": [1 if data["type"].upper() == "CASH_OUT" else 0],
            "DEBIT": [1 if data["type"].upper() == "DEBIT" else 0],
            "PAYMENT": [1 if data["type"].upper() == "PAYMENT" else 0],
            "TRANSFER": [1 if data["type"].upper() == "TRANSFER" else 0]
        }

        input_df = pd.DataFrame(input_data)
        output = model.predict(input_df)
        return jsonify({"isFraud": str(output[0] == 1)})


api.add_resource(FraudModel, '/predict')
api.add_resource(Healthcheck, '/healthcheck')

print("App Started. Thanks!")

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 8000, debug=True)

