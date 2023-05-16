from flask import Flask, render_template, redirect, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import redis
import openai
import os
from flask import send_file

load_dotenv()
app = Flask(__name__)

redis_url = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
app.secret_key = '147258369'
openai.api_key = os.getenv('CHAVE')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv("EMAIL"),
    "MAIL_PASSWORD": os.getenv("SENHA")
}

app.config.update(mail_settings)
mail = Mail(app)


class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem


def enviar_email_ia(nome, email, pergunta, msg):
    msg = Message(
        subject=f'{nome} enviou uma mensagem no Portfólio',
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[email],
        body=f'''
                Pergunta feita para a IA: {pergunta}

                {msg}
                '''
    )

    mail.send(msg)


def resposta_chat_gpt(pergunta: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=pergunta,
        max_tokens=1024
    )
    resultado = response["choices"][0]["text"].replace("\n", " ")
    return resultado


class IA:
    def __init__(self, pergunta):
        self.pergunta = pergunta


@app.route('/')
def index():
    conn.incr('visitas')
    return render_template('index.html', visitas=str(int(conn.get('visitas'))))


@app.route('/visitas')
def visitas():
    return conn.get('visitas')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject=f'{formContato.nome} enviou uma mensagem no Portfólio',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=['rafael.ferreira.s@hotmail.com.br', app.config.get("MAIL_USERNAME")],
            body=f'''
            {formContato.nome} com o email {formContato.email}, te enviou a seguinte mensagem:

            {formContato.mensagem}
            '''
        )

        mail.send(msg)
        flash('Mensagem enviada com sucesso!', 'sucess')
    return redirect('/')


@app.route('/download', methods=['GET', 'POST'])
def chat():
    file = 'static/pdf/cv.pdf'
    send_file(file, as_attachment=True)
    '''//if request.method == 'POST':
        formIA = IA(request.form["pergunta"])
        mensagem_output = resposta_chat_gpt(formIA.pergunta)
        flash(f'{mensagem_output}', 'answer')
        enviar_email_ia('IA', 'ia@teste.com', formIA.pergunta, mensagem_output)'''
    return redirect('/')


if __name__ == '__main__':
    app.run('localhost', 4449, debug=True)
