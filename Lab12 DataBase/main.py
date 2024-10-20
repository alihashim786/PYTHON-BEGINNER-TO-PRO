# # # from flask import Flask

# # # app = Flask(__name__)


# # # @app.route('/about')
# # # def about():
# # #     return 'this about here, this is the home page!'

# # # @app.route('/')
# # # def home():
# # #     return 'Hello, here you are seeing the first python website by Syed Ali Hashim!'

# # # if __name__ == '__main__':
# # #     app.run(debug=True)

# # from flask import Flask, render_template

# # app = Flask(__name__)

# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # @app.route('/about')
# # def about():
# #     return render_template('about.html')

# # if __name__ == '__main__':
# #     app.run(debug=True)

# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from flask import Flask
# from flask import render_template
# from flask_wtf.csrf import CSRFProtect

# app = Flask(__name__)

# csrf = CSRFProtect(app)

# # Set a secret key for your Flask app
# app.config['SECRET_KEY'] = 'pailab'

# class MyForm(FlaskForm):
#     name = StringField('Name')
#     submit = SubmitField('Submit')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/forms', methods=['GET', 'POST'])
# def form():
#     form = MyForm()

#     if form.validate_on_submit():
#         name = form.name.data
#         return f'Form submitted with name: {name}'

#     return render_template('form.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email=db.Column(db.String(20), unique=False, nullable=False)
    address= db.Column(db.String(20), unique=False, nullable=False)
    course= db.Column(db.String(20), unique=False, nullable=False)

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

if __name__ == '__main__':
    # This condition ensures that the following code is only executed
    # when the script is run directly (not imported as a module).
    # It will create the database tables when the script is run.
    # Create the Flask app context
    with app.app_context():
        # Create the database tables when the script is run
        db.create_all() #sirf aik dafa chalane k liye ye line chahiye hoti hai when data base will be created then we no longer need this line to get or send data
        
        u1=User(username='Ali Hashim', email='i220554@nu.edu.pk',address='Mars',course='Lahori PAI')
        u2=User(username='Muhammad Umer', email='i220644@nu.edu.pk',address='Venus',course='Data Structures')
        #jitni dafa below two lines run hogi users add hote jaye gay like pehlui dafa run hone par 2 users the databaseme 2nd time run hone par
        #4 users hojaye gay  two new one and two previous ones
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
    app.run(debug=True)

    