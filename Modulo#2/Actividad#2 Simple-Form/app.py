from flask import Flask, render_template, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"


class RegistrationForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(min=3, message="El nombre debe contener 3 o mas caracteres.")])
    email = StringField("Correo", validators=[DataRequired(), Email(message="Correo inválido.")])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6, message="La contraseña debe tener minimo 6 caracteres.")])
    confirm_password = PasswordField("Confirmar Contraseña", validators=[DataRequired(), EqualTo('password', message="Las contraseñas deben coincidir.")])
    submit = SubmitField("Registrar")
    
    
@app.route("/", methods=["POST"])
def index():
    form = RegistrationForm()  
    if form.validate_on_submit():  
        return redirect(url_for("mensaje")) 
    return render_template("index.html", form=form)

@app.route("/mensaje")
def mensaje():
    return jsonify({"mensaje": "Usuario registrado correctamente"})


if __name__ == "__main__":
    app.run(debug=True)