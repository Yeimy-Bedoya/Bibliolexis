from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='usuario')  # 'usuario' o 'admin'
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    prestamos = db.relationship('Prestamo', backref='usuario', lazy=True)
    
    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    editorial = db.Column(db.String(100))
    anio = db.Column(db.String(4))
    isbn = db.Column(db.String(20), unique=True)
    genero = db.Column(db.String(50))
    sinopsis = db.Column(db.Text)
    disponibles = db.Column(db.Integer, default=1)
    total = db.Column(db.Integer, default=1)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)
    
    def __repr__(self):
        return f'<Libro {self.titulo}>'

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='prestado')  # 'prestado', 'devuelto', 'vencido'
    
    def __repr__(self):
        return f'<Prestamo {self.id}>'

def setup_db():
    """Configura la base de datos y crea las tablas si no existen"""
    db.create_all()
    
    # Crear usuario administrador predeterminado si no existe
    from werkzeug.security import generate_password_hash
    
    admin_exists = Usuario.query.filter_by(nombre_usuario='admin').first()
    if not admin_exists:
        admin = Usuario(
            nombre='Administrador',
            apellido='Sistema',
            nombre_usuario='admin',
            correo='admin@bibliolexis.com',
            telefono='0000000000',
            contrasena=generate_password_hash('admin123'),
            rol='admin'
        )
        db.session.add(admin)
        db.session.commit()