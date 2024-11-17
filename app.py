from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz


# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

# Configuração do banco de dados MySQL usando variáveis de ambiente
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Rota para a página Home
@app.route("/")
@app.route("/home")
def home():
    return render_template("html/home.html")


# Rota para a página Quem Somos
@app.route("/quem-somos")
def quem_somos():
    return render_template("html/quem-somos.html")


# Modelo de Contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone("America/Sao_Paulo"))
    )

    def __repr__(self):
        return f"<Contato {self.nome}>"


# Criar o banco de dados
with app.app_context():
    db.create_all()


# Rota de Contato com método POST
@app.route("/contato", methods=["GET", "POST"])
def contato():
    mensagens = Contato.query.order_by(Contato.data_criacao.desc()).limit(5).all()

    if request.method == "POST":
        # Recuperar dados do formulário
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")

        # Criar novo registro de contato
        novo_contato = Contato(nome=nome, email=email, mensagem=mensagem)

        # Salvar no banco de dados
        db.session.add(novo_contato)
        db.session.commit()

        # Redirecionar para evitar reenvio de formulário
        return redirect(url_for("contato"))

    return render_template("html/contato.html", mensagens=mensagens)


if __name__ == "__main__":
    app.run(debug=True)
