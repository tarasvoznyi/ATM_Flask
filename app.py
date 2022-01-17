from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'THISISSUPPOSEDROBESECRET!'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    number = db.Column(db.NUMERIC(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    pin = db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Users %r>' % self.id


class Money(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Money %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/support')
def support():
    return render_template("support.html")


@app.route('/user/<string:name>/<int:bank_card>/<int:amount_of_money>')
def user(name, bank_card, amount_of_money):
    return "User page: " + " Client name is " + name + " , " + "His bank card is " + str(
        bank_card) + " , " + "His amount of money is " + str(amount_of_money) + " dollars"


@app.route('/Sign_in')
def sign_in():
    return render_template("Sign_in.html")


@app.route('/Registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        pin = request.form['pin']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']

        users = Users(first_name=first_name, last_name=last_name, username=username, pin=pin,  number=number,   email=email, password=password, )
        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/Card')
        except:
            return "ERROR MOTHERFUCKER"
    else:
        return render_template("Registration.html")


@app.route('/Card')
def card():
    return render_template("Card.html")


@app.route('/Admin')
def admin():
    return render_template('Admin.html')


@app.route('/Users')
def users():
    users = Users.query.order_by(Users.id).all()
    return render_template("Users.html", users=users)


@app.route('/Data')
def data():
    return render_template("Data.html")


@app.route('/Sum', methods=['POST', 'GET'])
def sum():
    if request.method == "POST":
        balance = request.form['balance']
        amount = request.form['amount']
       #result = request.form['result']
        money = Money(amount=amount, balance=balance)

        try:
            db.result = db.balance + db.amount
            db.session.add(money)
            db.session.commit()
            return redirect('/Cash_in')
        except:
            return redirect('/Card')
    return render_template("Sum.html")


@app.route('/Sum1', methods=['POST', 'GET'])
def sum1():
    if request.method == "POST":
        balance = request.form['balance']
        amount = request.form['amount']
        #result = request.form['result']
        money = Money(amount=amount, balance=balance)

        try:
            db.result = db.balance - db.amount
            db.session.add(money)
            db.session.commit()
            #return "Your current balance is: " + str(db.result)
            return redirect('/Cash_out')
        except:
            return redirect('/Card')
    return render_template("Sum1.html")


@app.route('/Users/<int:id>')
def users_detail(id):
    users = Users.query.get(id)
    return render_template("Users_detail.html", users=users)


@app.route('/Users/<int:id>/delete')
def users_delete(id):
    users = Users.query.get_or_404(id)

    try:
        db.session.delete(users)
        db.session.commit()
        return redirect('/Users')
    except:
        return "An ERROR has occurred"


@app.route('/Cash_in',methods=['POST', 'GET'])
def cash_in():
    money = Money.query.get(id)
    return render_template("Cash_in.html", money=money)


@app.route('/Cash_out',methods=['POST', 'GET'])
def cash_out():
    money = Money.query.get(id)
    return render_template("Cash_out.html", money=money)


if __name__ == "__main__":
    app.run(debug=True)