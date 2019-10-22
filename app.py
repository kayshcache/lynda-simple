from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from os import path, walk
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)
basedir = path.abspath(path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' \
        + path.join(basedir, 'mydatabase.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print('Database created, hmm')

@app.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('Database dropped, man')

@app.cli.command('seed_db')
def seed_db():
    menu_item_one = Meal(meal_name='Spam, Eggs, Sausage, and Spam',
            spam_count=2)
    menu_item_two = Meal(meal_name='Egg, Bacon, Spam, and Sausage',
            spam_count=1)
    menu_item_three = Meal(meal_name='Spam, Spam, Spam, Spam, ' \
            'Spam, Baked Beans, Spam, Spam, and Spam',
            spam_count=8)
    db.session.add(menu_item_one)
    db.session.add(menu_item_two)
    db.session.add(menu_item_three)

    test_customer = Customer(name='Terry',
            email='terry_g@pythonbbc.co.uk')
    db.session.add(test_customer)
    db.session.commit()
    print('Database seeded')

@app.route('/api')
def super_simple():
    return jsonify(message='No no')


def load_dirs_to_watch():
    extra_dirs = ['./app.py']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

@app.route('/meals', methods=['GET'])
def meals():
    menu = Meal.query.all()
    result = meals_schema.dump(menu)
    return jsonify(result)

# Database models
class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

class Meal(db.Model):
    __tablename__ = 'meals'
    meal_id = Column(Integer, primary_key=True)
    meal_name = Column(String)
    spam_count = Column(Integer)

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


class MealSchema(ma.Schema):
    class Meta:
        fields = ('menu_id', 'meal_name', 'spam_count')


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

meal_schema = MealSchema()
meals_schema = MealSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)

SKIT_SPAM = 'https://www.youtube.com/watch?v=jrZyZn5nVks'

