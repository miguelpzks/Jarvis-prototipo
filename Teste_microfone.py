import speech_recognition as sr

# Inicializa o reconhecedor
reconhecedor = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Testando microfone... fale algo!")
    reconhecedor.adjust_for_ambient_noise(source)  # ajusta ao ruído do ambiente
    audio = reconhecedor.listen(source)

try:
    print("✅ Você disse: " + reconhecedor.recognize_google(audio, language="pt-BR"))
except sr.UnknownValueError:
    print("⚠️ Não consegui entender o que você disse.")
except sr.RequestError:
    print("❌ Erro ao se conectar ao serviço de reconhecimento de voz.")
