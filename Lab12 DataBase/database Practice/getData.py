from main import User, app, db

with app.app_context():
    all_users = User.query.all()
    for user in all_users:
        print(user.email)
