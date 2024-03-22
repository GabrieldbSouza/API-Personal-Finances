from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
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
  
@app.route('/')
def init():
  return redirect(url_for('login'))

@app.route('/login', methods = ['GET','POST'])
def login():
  email = request.form.get('email')
  password = request.form.get('password')
  user = User.query.filter_by(email=email, password=password).first()
  if user:
    return jsonify({'###': 'voce se conectou com sucesso!'})
  else:
    return render_template('login.html', error='Credenciais inválidas. Tente novamente.')

  return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def cadastro():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if not all([email, password, confirm_password]) and password != confirm_password:
      return jsonify({"ERRO!": 'Por favor, preencha todos os campos corretamente.'})
    
    if User.query.filter_by(email=email).first():
      return jsonify({"ERRO!": 'Este e-mail ja esta em uso. Tente novamente com outro.'})
    x = 'Seu nofrfrrfme'
    new_user = User(username=x, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

  return render_template('register.html')

@app.route('/transaction', methods = ['GET'])
def get_transaction():
  transaction = Transaction.query.all()
  
  return  jsonify([{'user_id': transaction.user_id, 'date': transaction.date, 'value': transaction.value} for transaction in transaction])

@app.route('/transaction/date', methods = ['GET'])
def get_transaction_date():
  start_date = request.args.get('start_date')
  end_date = request.args.get('end_date')
  transaction = Transaction.query.filter(Transaction.date.between(start_date, end_date)).all()
  
  return jsonify([{'user_id': transaction.user_id, 'date': transaction.date, 'value': transaction.value} for transaction in transaction])

@app.route('/transaction', methods = ['POST'])
def post_transacttion():
  data = request.get_json()
  new_transaction = Transaction(user_id = data['user_id'], date = datetime.strptime(data['date'], '%Y-%m-%d').date(), value = data['value'])
  db.session.add(new_transaction)
  db.session.commit()

  return jsonify({'message': 'Transação inserida'})

@app.route('/user', methods = ['POST'])
def post_user():
  data = request.get_json()
  new_user = User(username = data['username'],email = data['email' ],password = data['password'])
  db.session.add(new_user)
  db.session.commit()

  return  jsonify({'message': 'Usuário criado'})

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug = True)