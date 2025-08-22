import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import json
import time
import pywhatkit
import datetime
import smtplib
from email.message import EmailMessage

def speak(text):
    print(f"Jarvis: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # voz masculina
    engine.setProperty("rate", 180)
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # evita travar o áudio

# === PALAVRA DE ATIVAÇÃO ===
WAKE_WORD = "jarvis"

def listen():
    """Escuta e retorna o que foi dito em texto"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language="pt-BR").lower()
        print(f"Você: {comando}")
        return comando
    except:
        return ""

# === SISTEMA DE APPS DINÂMICOS ===
APPS_FILE = "apps.json"

def carregar_apps():
    if os.path.exists(APPS_FILE):
        with open(APPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_apps(apps):
    with open(APPS_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4, ensure_ascii=False)

apps = carregar_apps()

if not apps:
    apps = {
        "calculadora": "calc.exe",
        "bloco de notas": "notepad.exe",
        "paint": "mspaint.exe",
        "explorador": "explorer.exe"
    }
    salvar_apps(apps)

def abrir_app(nome):
    if nome in apps:
        caminho = apps[nome]
        try:
            os.startfile(caminho)
            speak(f"Abrindo {nome}")
        except Exception as e:
            speak(f"Não consegui abrir {nome}. Verifique o caminho.")
    else:
        speak(f"Não conheço o app {nome}. Você pode me ensinar.")

# === FUNÇÕES EXISTENTES ===
def enviar_whatsapp(numero, mensagem, hora=None, minuto=None):
    agora = datetime.datetime.now()
    if hora in None:
        hora = agora.hour
    if minuto in None:
        minuto = agora.minute + 1 # Enviar mesnagem um minuto depois (para dar tempo de abrir o whatsapp)
        pywhatkit.sendwhatmsg(numero, mensagem, hora, minuto)
        speak(f"Mensagem enviada para {numero}")

def enviar_email(destinatario, assunto, mensagem):
    EMAIL = "miguelmoural826@gmail.com"
    SENHA = "1214161820ml"
    
    email_msg = EmailMessage()
    email_msg['From'] = EMAIL
    email_msg['To'] = destinatario
    email_msg['Subject'] = assunto
    email_msg.set_content(mensagem)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, SENHA)
        smtp.send_message(email_msg)
        
    speak(f"E-mail enviado para {destinatario}")

def pesquisar(termo):
    url = f"https://www.google.com/search?q={termo}"
    webbrowser.open(url)
    speak(f"Pesquisando por {termo}")

def tocar_musica(termo):
    url = f"https://www.youtube.com/results?search_query={termo}"
    webbrowser.open(url)
    speak(f"Tocando {termo} no YouTube")

# === LOOP PRINCIPAL COM ATIVAÇÃO POR VOZ ===
def main():
    speak("Jarvis ativado. Diga meu nome para me chamar.")
    while True:
        print("Aguardando palavra de ativação...")
        comando = listen()

        if WAKE_WORD in comando:
            speak("Estou ouvindo. O que deseja?")
            
            # agora escuta o comando real
            comando = listen()

            if "sair" in comando or "desligar" in comando:
                speak("Até logo, Desenvolvedor!")
                break
                
            elif "pesquise por" in comando:
                termo = comando.replace("pesquise por", "").strip()
                pesquisar(termo)
                
            elif "enviar mensagem" in comando:
                speak("Qual é o numero do contato?")
                numero = listen()
                speak("Qual é a mensagem?")
                mensagem = listen()
                enviar_whatsapp(numero, mensagem)

            elif "enviar email" in comando:
                speak("Para quem devo enviar?")
                destinatario = listen()
                speak("Qual o assunto?")
                assunto = listen()
                speak("Qual é a mensagem?")
                mensagem = listen()
                enviar_email(destinatario, assunto, mensagem)
            
            elif "tocar" in comando or "toque" in comando:
                termo = comando.replace("toque", "").replace("tocar", "").strip()
                tocar_musica(termo)

            elif "abrir" in comando or "abra" in comando:
                nome = comando.replace("abrir", "").replace("abra", "").strip()
                abrir_app(nome)

            elif "memorize que" in comando and "abre em" in comando:
                try:
                    partes = comando.replace("memorize que", "").strip().split("abre em")
                    nome = partes[0].strip()
                    caminho = partes[1].strip()
                    apps[nome] = caminho
                    salvar_apps(apps)
                    speak(f"Ok, memorize que {nome} abre em {caminho}")
                except:
                    speak("Não entendi o comando de memorização.")

            else:
                if comando != "":
                    speak("Desculpe, ainda não sei como responder a isso.")
        
        # opcional: evitar loop muito rápido
        time.sleep(0.5)

if __name__ == "__main__":
    main()
