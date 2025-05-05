from werkzeug.security import generate_password_hash

# Configuración del admin
admin_password = "admin123"
hash = generate_password_hash(admin_password, method='sha256')
print("\nHash generado:", hash)
print("Contraseña:", admin_password)