from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personalfinances.sqlite' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

# Definição dos modelos
class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(20), unique = True, nullable = False)
  email = db.Column(db.String(100), unique = True, nullable = False)
  password = db.Column(db.String(100), nullable = False)
  
  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"    
  
class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  date = db.Column(db.Date, nullable = False)
  value = db.Column(db.Float, nullable = False)

  def __repr__(self):
    return f"Transaction('{self.date}', '{self.value}')"

# Definição das rotas
@app.route('/transaction', methods = ['GET'])
def get_transaction():
  transaction = Transaction.query.all()
  
  return  jsonify(transaction)

@app.route('/transaction/date', methods = ['GET'])
def get_transaction_date():
  start_date = request.args.get('starr_date')
  end_date = request.args.get('end_date')
  
  transaction = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
  
  return jsonify(transaction)

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug = True)