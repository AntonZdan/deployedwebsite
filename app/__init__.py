from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='../templates')

    app.config['SECRET_KEY'] = 'labai-slapta-raktis'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///demo.db')

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from .models import Vartotojas, Irasas
    @login_manager.user_loader
    def load_user(user_id):
        return Vartotojas.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()
        if not Vartotojas.query.first():
            vart = Vartotojas(el_pastas='demo@demo.lt', slaptazodis='demo')
            db.session.add(vart)
            db.session.commit()
            for i in range(1, 21):
                ir = Irasas(suma=100 + i, pajamos=i % 2 == 0, vartotojas_id=vart.id, data=datetime.utcnow())
                db.session.add(ir)
            db.session.commit()
    return app
