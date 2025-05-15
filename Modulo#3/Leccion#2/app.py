from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity
# Configuracion de entorno de Flask
app = Flask(__name__)
app.secret_key = 'clave_super_secreta'
Principal(app)

# Configuracion de Flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Configuracion de Permisos 
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))


# Datos Simulados
usuarios = {
    'admin': {'password': '12345', 'role': 'admin'}, 
    'johndoe': {'password': 'secreto', 'role': 'user'}
}


# Roles y Permisos
roles_permissions = {
"admin": ["create", "read", "update", "delete"],
"user": ["read"]
}


# Clase de Usuario
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = usuarios[username]['role']

# Cargar usuario desde la sesión
@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

#Configuracion de verificacion de Identidad
@app.before_request
def before_request():
    if current_user.is_authenticated:
        identity_changed.send(app, identity=Identity(current_user.id))

#Sincroniza Flask_Principal y Flask_login 
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

# Ruta principal protegida
@app.route('/')
@login_required
def home():
    return render_template('home.html.jinja2', nombre=current_user.id)

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username'] # procesar usuario enviado
        password = request.form['password'] # procesar password enviado

        # validar si los datos enviados existen en la lista 'usuarios'
        if username in usuarios and usuarios[username]['password'] == password:
            user = Usuario(username)
            login_user(user)
            return redirect(url_for('home')) # redirigir a la página 'home.html'
        
        return render_template("error.html.jinja2", error_code=401, 
                               error_message="Invalid Credentials (error on username or password)!"), 401
    
    # página llamada sino se envian datos, método GET
    return render_template('login.html.jinja2') 

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('login'))

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_panel():
    return render_template('admin.html.jinja2', nombre=current_user.id)


# Funcion que verifica permisos 
def check_permission(role, action):
    if action in roles_permissions.get(role, []):
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)