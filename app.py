from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from datetime import datetime
from models import db, Usuario, Libro, Prestamo, setup_db

# Cargar variables de entorno
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mi_clave_secreta')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bibliolexis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Crear todas las tablas si no existen
with app.app_context():
    setup_db()

# Rutas para la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        user = Usuario.query.filter_by(nombre_usuario=usuario).first()
        
        try:
            if user and check_password_hash(user.contrasena, contrasena):
                login_user(user)
                flash('Has iniciado sesión correctamente', 'success')
                
                # Redireccionar según el rol del usuario
                if user.rol == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('dashboard'))
                    
        except ValueError:
            flash('Error en el formato de contraseña almacenada', 'error')
            return render_template('login.html')
            
        flash('Credenciales inválidas. Inténtalo de nuevo.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        correo = request.form['correo']
        telefono = request.form['telefono']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        
        # Validaciones básicas
        if contrasena != confirmar_contrasena:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('registro.html')
        
        # Verificar si el usuario ya existe
        user_exists = Usuario.query.filter_by(nombre_usuario=usuario).first()
        email_exists = Usuario.query.filter_by(correo=correo).first()
        
        if user_exists:
            flash('El nombre de usuario ya está en uso', 'error')
            return render_template('registro.html')
        
        if email_exists:
            flash('El correo electrónico ya está registrado', 'error')
            return render_template('registro.html')
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=usuario,
            correo=correo,
            telefono=telefono,
            contrasena=generate_password_hash(contrasena, method='pbkdf2:sha256'),
            rol='usuario'
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Te has registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/dashboard')
@login_required
def dashboard():
    libros = Libro.query.all()
    return render_template('dashboard.html', libros=libros)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('dashboard'))
    
    # Estadísticas generales
    total_libros = Libro.query.count()
    total_usuarios = Usuario.query.filter_by(rol='usuario').count()
    prestamos_activos = Prestamo.query.filter_by(estado='prestado').count()
    
    # Información detallada
    ultimos_usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).limit(5).all()
    ultimos_prestamos = Prestamo.query.order_by(Prestamo.fecha_prestamo.desc()).limit(5).all()
    libros_populares = Libro.query.join(Prestamo).group_by(Libro.id)\
        .order_by(db.func.count(Prestamo.id).desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_libros=total_libros,
                         total_usuarios=total_usuarios,
                         prestamos_activos=prestamos_activos,
                         ultimos_usuarios=ultimos_usuarios,
                         ultimos_prestamos=ultimos_prestamos,
                         libros_populares=libros_populares)

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Rutas para la gestión de libros
@app.route('/libros')
@login_required
def libros():
    libros = Libro.query.all()
    return render_template('libros.html', libros=libros)

@app.route('/libro/<int:id>')
@login_required
def ver_libro(id):
    libro = Libro.query.get_or_404(id)
    return render_template('ver_libro.html', libro=libro)

@app.route('/libro/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_libro():
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        editorial = request.form['editorial']
        anio = request.form['anio']
        isbn = request.form['isbn']
        genero = request.form['genero']
        sinopsis = request.form['sinopsis']
        cantidad = int(request.form['cantidad'])
        
        nuevo_libro = Libro(
            titulo=titulo,
            autor=autor,
            editorial=editorial,
            anio=anio,
            isbn=isbn,
            genero=genero,
            sinopsis=sinopsis,
            disponibles=cantidad,
            total=cantidad
        )
        
        db.session.add(nuevo_libro)
        db.session.commit()
        
        flash('Libro añadido correctamente', 'success')
        return redirect(url_for('libros'))
    
    return render_template('nuevo_libro.html')

@app.route('/libro/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    if current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('dashboard'))
        
    libro = Libro.query.get_or_404(id)
    
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.autor = request.form['autor']
        libro.editorial = request.form['editorial']
        libro.anio = request.form['anio']
        libro.isbn = request.form['isbn']
        libro.genero = request.form['genero']
        libro.sinopsis = request.form['sinopsis']
        
        # Actualizar la cantidad si ha cambiado
        nueva_cantidad = int(request.form['cantidad'])
        diferencia = nueva_cantidad - libro.total
        libro.total = nueva_cantidad
        libro.disponibles += diferencia
        
        db.session.commit()
        
        flash('Libro actualizado correctamente', 'success')
        return redirect(url_for('ver_libro', id=libro.id))
    
    return render_template('editar_libro.html', libro=libro)

@app.route('/prestamos')
@login_required
def prestamos():
    if current_user.rol == 'admin':
        # Administradores ven todos los préstamos
        prestamos = Prestamo.query.all()
    else:
        # Usuarios solo ven sus préstamos
        prestamos = Prestamo.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('prestamos.html', prestamos=prestamos)

@app.route('/prestar/<int:libro_id>', methods=['GET', 'POST'])
@login_required
def prestar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    
    if libro.disponibles <= 0:
        flash('No hay ejemplares disponibles de este libro', 'error')
        return redirect(url_for('ver_libro', id=libro_id))
    
    if request.method == 'POST':
        fecha_prestamo = datetime.now()
        fecha_devolucion = datetime.strptime(request.form['fecha_devolucion'], '%Y-%m-%d')
        
        nuevo_prestamo = Prestamo(
            usuario_id=current_user.id,
            libro_id=libro.id,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion=fecha_devolucion,
            estado='prestado'
        )
        
        # Actualizar disponibilidad del libro
        libro.disponibles -= 1
        
        db.session.add(nuevo_prestamo)
        db.session.commit()
        
        flash('Libro prestado correctamente', 'success')
        return redirect(url_for('prestamos'))
    
    return render_template('prestar_libro.html', libro=libro)

@app.route('/devolver/<int:prestamo_id>')
@login_required
def devolver_libro(prestamo_id):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    
    # Verificar que el préstamo sea del usuario actual o que sea administrador
    if prestamo.usuario_id != current_user.id and current_user.rol != 'admin':
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('prestamos'))
    
    prestamo.estado = 'devuelto'
    prestamo.fecha_devolucion_real = datetime.now()
    
    # Actualizar disponibilidad del libro
    libro = Libro.query.get(prestamo.libro_id)
    libro.disponibles += 1
    
    db.session.commit()
    
    flash('Libro devuelto correctamente', 'success')
    return redirect(url_for('prestamos'))

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)