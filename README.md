# Bibliolexis - Sistema de Gestión de Biblioteca

Bibliolexis es un sistema completo de gestión de biblioteca desarrollado con Flask y MySQL, diseñado para facilitar la organización, préstamo y seguimiento de colecciones de libros para bibliotecas de diferentes tamaños.

## Características

- Sistema de autenticación de usuarios (registro e inicio de sesión)
- Gestión completa de libros (añadir, editar, buscar)
- Sistema de préstamos y devoluciones
- Perfiles de usuario
- Panel de administración
- Interfaz responsiva y moderna

## Requisitos

- Python 3.8+
- MySQL Server
- Pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/bibliolexis.git
   cd bibliolexis
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura la base de datos:
   - Crea una base de datos MySQL llamada `bibliolexis`
   - Configura las credenciales en el archivo `.env`

5. Ejecuta la aplicación:
   ```
   python app.py
   ```

6. Accede a la aplicación en tu navegador: `http://localhost:5000`

## Estructura del Proyecto

- `app.py`: Punto de entrada de la aplicación
- `models.py`: Definiciones de los modelos de datos
- `templates/`: Plantillas HTML para las vistas
- `static/`: Archivos estáticos (CSS, JS, imágenes)

## Usuario Administrador Predeterminado

La aplicación crea automáticamente un usuario administrador:
- Usuario: admin
- Contraseña: admin123

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.