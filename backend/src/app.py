import os
from flask_cors import CORS
from forms import ExpenseForm
from dotenv import load_dotenv
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

uri = os.environ['MONGO_URI']
#uri = os.environ.get('MONGO_URI')
client = MongoClient(uri)

CORS(app)

expensesCollection = client.budgetAdmin.expenses


@app.route("/")
def index():
    return "Main route"


@app.route("/expenses", methods=['POST'])
def createExpenses():
    # form = ExpenseForm(request.json)
    # if not form.validate():
    #     return jsonify({'error': form.errors}), 400
    result = expensesCollection.insert_one({
        'name': request.json['name'],
        'date': request.json['date'],
        'price': request.json['price'],
        'category': request.json['category']
    })
    return jsonify(str(result.inserted_id))
    print(str(result.inserted_id))


@app.route("/expenses", methods=['GET'])
def getExpenses():
    expenses = []
    for doc in expensesCollection.find():
        expenses.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'date': doc['date'],
            'price': doc['price'],
            'category': doc['category']
        })
    return jsonify(expenses)


@app.route("/expense/<id>", methods=['GET'])
def getExpense(id):
    expense = expensesCollection.find_one({'_id': ObjectId(id)})
    return jsonify({
        'msg': 'Expense found',
        '_id': str(ObjectId(expense['_id'])),
        'name': expense['name'],
        'date': expense['date'],
        'price': expense['price'],
        'category': expense['category']
    })


@app.route("/expenses/<id>", methods=['DELETE'])
def deleteExpense(id):
    expensesCollection.delete_one({'_id': ObjectId(id)})
    return jsonify({
        'msg': 'Expense deleted',
    })


@app.route("/expenses/<id>", methods=['PUT'])
def updateExpense(id):
    expensesCollection.update_one({'_id': ObjectId(id)}, {"$set": {
        'name': request.json['name'],
        'date': request.json['date'],
        'price': request.json['price'],
        'category': request.json['category']
    }})
    return jsonify({
        'msg': 'Expense updated',
    })


if __name__ == "__main__":
    app.run(debug=True)