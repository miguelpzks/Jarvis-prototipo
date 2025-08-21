import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import json

def speak(text):
    print(f"Jarvis: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # voz masculina
    engine.setProperty("rate", 180)
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # evita travar o áudio

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language="pt-BR").lower()
        print(f"Você: {comando}")
        return comando
    except:
        return ""

# === NOVO: SISTEMA DE APPS DINÂMICOS ===
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

# --- alguns exemplos iniciais ---
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

# === FUNÇÕES JÁ EXISTENTES ===
def pesquisar(termo):
    url = f"https://www.google.com/search?q={termo}"
    webbrowser.open(url)
    speak(f"Pesquisando por {termo}")

def tocar_musica(termo):
    url = f"https://www.youtube.com/results?search_query={termo}"
    webbrowser.open(url)
    speak(f"Tocando {termo} no YouTube")

# === LOOP PRINCIPAL ===
def main():
    speak("Olá, eu sou o Jarvis. Como posso ajudar?")
    while True:
        comando = listen()

        if "sair" in comando or "desligar" in comando:
            speak("Até logo, Desenvolvedor!")
            break

        elif "pesquise por" in comando:
            termo = comando.replace("pesquise por", "").strip()
            pesquisar(termo)

        elif "tocar" in comando:
            termo = comando.replace("toque", "").strip()
            tocar_musica(termo)

        # --- NOVO: abrir app ---
        elif "abrir" in comando or "abra" in comando:
            nome = comando.replace("abrir", "").strip()
            abrir_app(nome)

        # --- NOVO: ensinar app ---
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

if __name__ == "__main__":
    main()
