#from flask import Flask, render_template
import os
#from flask import Flask
from flask import Flask, render_template, request, redirect, session, flash
#from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime  import  datetime
from flask import send_from_directory
from flask import jsonify
from flask_paginate import Pagination, get_page_args
from flask import Flask, session


app = Flask(__name__)
'''
@app.route('/')
def index():
  return render_template('index.html')
'''

#conectar a la Base de Datos
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:root@localhost/sitio_ifts_desarrollo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://pa8b6elekcqku7r9x7xb:pscale_pw_PZHwbfS8EIAEvJsOtquahViRpavf5pLGfFqDtvs0j7I@aws.connect.psdb.cloud/sitio_ifts_desarrollo'

app.secret_key = 'a'  # clave secreta
mysql = SQLAlchemy(app)


# Definir el modelo
class Libros(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(255))
    imagen = mysql.Column(mysql.String(255))
    url = mysql.Column(mysql.String(255))

# Definir el modelo para usuarios
class Usuarios(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(255))
    direccion = mysql.Column(mysql.String(255))
    mail = mysql.Column(mysql.String(255), unique=True)
    usuario = mysql.Column(mysql.String(255), unique=True)
    contrasena = mysql.Column(mysql.String(255))

class Productos(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    categoria = mysql.Column(mysql.String(50))  # Nueva columna para la categoría
    nombre = mysql.Column(mysql.String(255))
    imagen = mysql.Column(mysql.String(255))
    descripcion = mysql.Column(mysql.Text)
    precio = mysql.Column(mysql.Float)


# Aplicación Flask para crear tablas
with app.app_context():
    mysql.create_all()


@app.route('/')
def inicio():
    # Traer todos los productos de la base de datos
    productos = Productos.query.all()

    # Convertir los datos de productos en una lista de diccionarios
    productos_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos
    ]
    # Traer solo los productos de la categoría "Celulares"
    productos_celulares = Productos.query.filter_by(categoria='Celulares').all()

    # Traer solo los productos de la categoría "Consolas"
    productos_consolas = Productos.query.filter_by(categoria='Consolas').all()
    
   # Traer solo los productos de la categoría "Consolas"
    productos_tablets = Productos.query.filter_by(categoria='Tablets').all()

   # Traer solo los productos de la categoría "Consolas"
    productos_televisores = Productos.query.filter_by(categoria='Televisores').all()

   # Traer solo los productos de la categoría "Consolas"
    productos_auriculares = Productos.query.filter_by(categoria='auriculares').all()


    # Convertir los datos de productos en listas de diccionarios
    productos_celulares_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos_celulares
    ]

    productos_consolas_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos_consolas
    ]
    productos_televisores_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos_televisores
    ]
    productos_auriculares_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos_auriculares
    ]
    return render_template('sitio/index.html', productos=productos_data, productos_celulares=productos_celulares_data, productos_consolas=productos_consolas_data , productos_televisores=productos_televisores_data, productos_auriculares= productos_auriculares_data)


@app.route('/libros')
def libros():
    # Traer todos los libros de la base de datos
    libros = Libros.query.all()

    # Convertir los datos de libros en una lista de diccionarios
    libros_data = [
        {'imagen': libro.imagen, 'titulo': libro.nombre, 'descripcion': libro.url}
        for libro in libros
    ]

    return render_template('sitio/libros.html', libros=libros_data)

# Muestra la imagen guardada en templates/sitio/img
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

# Muestra la ruta estilos guardada en templates/sitio/css
@app.route('/css/<estilos>')
def estilos(estilos):
    print(estilos)
    return send_from_directory(os.path.join('templates/sitio/css'),estilos)

# Muestra la ruta js guardada en templates/sitio/js
@app.route('/js/<js>')
def js(js):
    print(js)
    return send_from_directory(os.path.join('templates/sitio/js'),js)


@app.route('/productos')
def productos():
    # Traer todos los productos de la base de datos
    productos = Productos.query.all()
# Obtener los parámetros de paginación de la URL
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Filtrar los productos a mostrar en la página actual
    productos_pagina = productos[offset : offset + per_page]

    # Configurar la paginación
    pagination = Pagination(page=page, per_page=per_page, total=len(productos), css_framework='bootstrap4')

    # Convertir los datos de productos en una lista de diccionarios
    productos_data = [
        {'imagen': producto.imagen, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos
    ]

    return render_template('sitio/productos.html', productos=productos_data, pagination=pagination)




@app.route('/descripcion')
def descripcion():
    return render_template('sitio/descripcion.html')


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/login')
def admin_login():
    return render_template('admin/login.html')


#-----------------------ADMIN-----------------------------

# Ruta para manejar el inicio de sesión
@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    # Busca al usuario en la base de datos
    usuario = Usuarios.query.filter_by(usuario=_usuario, contrasena=_password).first()

    if usuario:
        # Si se encuentra el usuario, inicia sesión
        session['usuario_id'] = usuario.id
        
        return redirect('/admin')  # Redirige a la página de administrador
    else:
        # Si no se encuentra el usuario, muestra un mensaje de error
        return render_template('admin/login.html', error='Credenciales incorrectas')

# Ruta para cerrar sesión
@app.route('/admin/logout')
def admin_logout():
    # Elimina la información del usuario de la sesión
    session.pop('usuario_id', None)
    return redirect('/admin/login')  # Redirige a la página de inicio de sesión

# Página de inicio de administrador protegida por inicio de sesión
@app.route('/admin')
def admin_index():
    # Verifica si el usuario ha iniciado sesión
    if 'usuario_id' in session:
        return render_template('admin/index.html')
    else:
        return redirect('/admin/login')  # Redirige a la página de inicio de sesión si no ha iniciado sesión



#-----------------------PRODUCTOS-----------------------------

@app.route('/admin/productos')
def admin_productos():
    productos = Productos.query.all()
    productos_data = [
        {'id': producto.id, 'nombre': producto.nombre, 'imagen': producto.imagen, 'descripcion': producto.descripcion, 'precio': producto.precio}
        for producto in productos
    ]
    return render_template('admin/productos.html', productos=productos_data)

@app.route('/admin/productos/guardar', methods=['POST'])
def admin_productos_guardar():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtDescripcion']
    _precio = request.form['txtPrecio']
    _categoria = request.form['txtCategoria']  # Asegúrate de tener un campo en tu formulario llamado 'txtCategoria'
    _archivo = request.files['txtImagen']

    tiempo = datetime.now()
    hora_actual = tiempo.strftime('%Y%H%M%S')

    if _archivo.filename != "":
        nuevo_nombre = hora_actual + "" + _archivo.filename
        _archivo.save("templates/sitio/img/" + nuevo_nombre)

    try:
        nuevo_producto = Productos(nombre=_nombre, imagen=nuevo_nombre, descripcion=_descripcion, precio=_precio, categoria=_categoria)
        mysql.session.add(nuevo_producto)
        mysql.session.commit()
    except Exception as e:
        print("Error al insertar en la base de datos:", str(e))
    finally:
        mysql.session.close()

    return redirect('/admin/productos')

@app.route('/admin/productos/borrar', methods=['POST'])
def admin_productos_borrar():
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        if producto_id:
            try:
                producto_a_borrar = Productos.query.get(producto_id)
                if producto_a_borrar:
                    imagen_a_borrar = producto_a_borrar.imagen
                    mysql.session.delete(producto_a_borrar)
                    mysql.session.commit()

                    if imagen_a_borrar:
                        ruta_imagen = os.path.join('templates/sitio/img', imagen_a_borrar)
                        if os.path.exists(ruta_imagen):
                            os.remove(ruta_imagen)

            except Exception as e:
                print("Error al borrar el producto de la base de datos:", str(e))
            finally:
                mysql.session.close()

    return redirect('/admin/productos')

@app.route('/admin/productos/editar', methods=['POST'])
def admin_productos_editar():
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        nuevo_nombre = request.form.get('nuevo_nombre')
        nueva_descripcion = request.form.get('nueva_descripcion')
        nuevo_precio = request.form.get('nuevo_precio')
        nueva_categoria = request.form.get('nueva_categoria')  # Asegúrate de tener un campo en tu formulario llamado 'nueva_categoria'
        nueva_imagen = request.files['nueva_imagen']

        if producto_id:
            try:
                producto_a_editar = Productos.query.get(producto_id)
                if producto_a_editar:
                    imagen_antigua = producto_a_editar.imagen

                    producto_a_editar.nombre = nuevo_nombre
                    producto_a_editar.descripcion = nueva_descripcion
                    producto_a_editar.precio = nuevo_precio
                    producto_a_editar.categoria = nueva_categoria  # Actualiza la categoría

                    if imagen_antigua:
                        ruta_imagen_antigua = os.path.join('templates/sitio/img', imagen_antigua)
                        if os.path.exists(ruta_imagen_antigua):
                            os.remove(ruta_imagen_antigua)

                    if nueva_imagen.filename != "":
                        tiempo = datetime.now()
                        nuevo_nombre_imagen = tiempo.strftime('%Y%H%M%S') + "_" + nueva_imagen.filename
                        nueva_imagen.save(os.path.join('templates/sitio/img', nuevo_nombre_imagen))
                        producto_a_editar.imagen = nuevo_nombre_imagen

                    mysql.session.commit()
            except Exception as e:
                print("Error al editar el producto en la base de datos:", str(e))
            finally:
                mysql.session.close()

    return redirect('/admin/productos')


#-----------------------Libros-----------------------------

#admin libros
@app.route('/admin/libros')
def admin_libros():
     #Traes todos los libros por mysql
    libros = Libros.query.all()

    # Imprimir datos de libros para depurar
    for libro in libros:
        print(f"ID: {libro.id}, Nombre: {libro.nombre}, Imagen: {libro.imagen}, URL: {libro.url}")

    # Convertir libros en una lista de diccionarios
    libros_data = [
        {'id': libro.id, 'nombre': libro.nombre, 'imagen': libro.imagen, 'url': libro.url}
        for libro in libros
    ]

    # Devuelve books_data como JSON (para fines de demostración)
    return render_template('admin/libros.html', libros=libros_data)


@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    _nombre = request.form['txtNombre']
    _url = request.form['txtUrl']
    _archivo = request.files['txtImagen']

    tiempo= datetime.now()
    horaactual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename != "":
        nuevoNombre= horaactual+""+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre) 

    try:
        nuevo_libro = Libros(nombre=_nombre, imagen=nuevoNombre, url=_url)
        mysql.session.add(nuevo_libro)
        mysql.session.commit()
    except Exception as e:
        print("Error al insertar en la base de datos:", str(e))
    finally:
        # Cierra la conexión
        mysql.session.close()

    print(_nombre)
    print(_url)
    print(nuevoNombre)
   # print(_archivo.filename)
    return redirect('/admin/libros')

# borrar libro de la base de datos y borrar el archivo de la imagen que esta en (templates/sitio/img)
@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    if request.method == 'POST':
        libro_id = request.form.get('libro_id')  # Obtén el ID del libro desde el formulario
        if libro_id:
            try:
                libro_a_borrar = Libros.query.get(libro_id)  # Consulta el libro por su ID
                if libro_a_borrar:
                    # Guarda el nombre del archivo antes de borrar el libro
                    imagen_a_borrar = libro_a_borrar.imagen

                    mysql.session.delete(libro_a_borrar)  # Elimina el libro de la sesión
                    mysql.session.commit()  # Confirma los cambios
                 # Borra el archivo de imagen asociado
                if imagen_a_borrar:
                    ruta_imagen = os.path.join('templates/sitio/img', imagen_a_borrar)
                    if os.path.exists(ruta_imagen):
                        os.remove(ruta_imagen)

            except Exception as e:
                print("Error al borrar el libro de la base de datos:", str(e))
            finally:
                mysql.session.close()  # Cierra la conexión a la base de datos

    return redirect('/admin/libros')


@app.route('/admin/libros/editar', methods=['POST'])
def admin_libros_editar():
    if request.method == 'POST':
        libro_id = request.form.get('libro_id')
        nuevo_nombre = request.form.get('nuevo_nombre')
        nuevo_url = request.form.get('nuevo_url')
        nueva_imagen = request.files['nueva_imagen']  # Cambia a request.files para manejar archivos

        if libro_id:
            try:
                libro_a_editar = Libros.query.get(libro_id)
                if libro_a_editar:
                    # Guarda el nombre de la imagen antigua antes de actualizar el libro
                    imagen_antigua = libro_a_editar.imagen

                    # Actualiza los datos del libro con la nueva información
                    libro_a_editar.nombre = nuevo_nombre
                    libro_a_editar.url = nuevo_url

                    # Borra la imagen antigua si existe
                    if imagen_antigua:
                        ruta_imagen_antigua = os.path.join('templates/sitio/img', imagen_antigua)
                        if os.path.exists(ruta_imagen_antigua):
                            os.remove(ruta_imagen_antigua)

                    # Guarda la nueva imagen si se proporciona
                    if nueva_imagen.filename != "":
                        tiempo = datetime.now()
                        nuevo_nombre_imagen = tiempo.strftime('%Y%H%M%S') + "_" + nueva_imagen.filename
                        nueva_imagen.save(os.path.join('templates/sitio/img', nuevo_nombre_imagen))
                        libro_a_editar.imagen = nuevo_nombre_imagen

                    mysql.session.commit()
            except Exception as e:
                print("Error al editar el libro en la base de datos:", str(e))
            finally:
                mysql.session.close()

    return redirect('/admin/libros')

#-----------------------USUARIOS-----------------------------

@app.route('/admin/usuarios')
def admin_usuarios():
    # Trae todos los usuarios de la base de datos
    usuarios = Usuarios.query.all()

    # Convierte los datos de usuarios en una lista de diccionarios
    usuarios_data = [
        {'id': usuario.id, 'nombre': usuario.nombre, 'direccion': usuario.direccion, 'mail': usuario.mail}
        for usuario in usuarios
    ]

    return render_template('admin/usuarios.html', usuarios=usuarios_data)


@app.route('/admin/usuarios/guardar', methods=['POST'])
def admin_usuarios_guardar():
    _nombre = request.form['txtNombre']
    _direccion = request.form['txtDireccion']
    _mail = request.form['txtMail']
    _usuario = request.form['txtUsuario']
    _contrasena = request.form['txtContrasena']

    try:
        nuevo_usuario = Usuarios(nombre=_nombre, direccion=_direccion, mail=_mail, usuario=_usuario, contrasena=_contrasena)
        mysql.session.add(nuevo_usuario)
        mysql.session.commit()
        flash('Usuario agregado exitosamente', 'success')
    except Exception as e:
            flash(f'Error al agregar usuario: {str(e)}', 'danger')
    finally:
        mysql.session.close()

    return redirect('/admin/usuarios')

@app.route('/admin/usuarios/borrar', methods=['POST'])
def admin_usuarios_borrar():
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')  # Obtén el ID del usuario desde el formulario
        if usuario_id:
            try:
                usuario_a_borrar = Usuarios.query.get(usuario_id)  # Consulta el usuario por su ID
                if usuario_a_borrar:
                    mysql.session.delete(usuario_a_borrar)  # Elimina el usuario de la sesión
                    mysql.session.commit()  # Confirma los cambios

            except Exception as e:
                print("Error al borrar el usuario de la base de datos:", str(e))
            finally:
                mysql.session.close()  # Cierra la conexión a la base de datos

    return redirect('/admin/usuarios')


@app.route('/admin/usuarios/editar', methods=['POST'])
def admin_usuarios_editar():
    if request.method == 'POST':
        usuario_id = request.form.get('usuario_id')
        nuevo_nombre = request.form.get('nuevo_nombre')
        nueva_direccion = request.form.get('nueva_direccion')
        nuevo_mail = request.form.get('nuevo_mail')
        nuevo_usuario = request.form.get('nuevo_usuario')
        nueva_contrasena = request.form.get('nueva_contrasena')

        if usuario_id:
            try:
                usuario_a_editar = Usuarios.query.get(usuario_id)
                if usuario_a_editar:
                    # Actualiza los datos del usuario con la nueva información
                    usuario_a_editar.nombre = nuevo_nombre
                    usuario_a_editar.direccion = nueva_direccion
                    usuario_a_editar.mail = nuevo_mail
                    usuario_a_editar.usuario = nuevo_usuario
                    usuario_a_editar.contrasena = nueva_contrasena

                    mysql.session.commit()
            except Exception as e:
                print("Error al editar el usuario en la base de datos:", str(e))
            finally:
                mysql.session.close()

    return redirect('/admin/usuarios')  # Corregir la redirección a /admin/usuarios




#-----------------------CARRITO-----------------------------






if __name__ == '__main__':
  app.run(port=5000)
