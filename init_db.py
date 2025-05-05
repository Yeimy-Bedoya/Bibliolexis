from app import app
from models import db, setup_db
with app.app_context():
    db.create_all()
    setup_db()
    print("Base de datos inicializada correctamente.")