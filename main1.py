# Вариант 5 (не разобралась с запросом для API в 4 варианте)
import json, time
import pyttsx3, pyaudio, vosk, requests



class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('vosk_model')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(text=text)
    print(text)

def get_random_user(request):
    try:
        response = requests.get('https://randomuser.me/api/')
        data = response.json()
        user = data['results'][0]
        if request == 'name':
            name = user['name']
            speak(f"Name: {name['title']} {name['first']} {name['last']}")
        else:
            speak(f"{request}: {user[request]}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except:
        speak("Wrong command")

def record():
    rec = Recognize()
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak('hi, say the command you want: name, email, phone, gender')
    time.sleep(0.5)
    rec.stream.start_stream()
    for text in text_gen:
        if text == 'stop':
            speak('bye bye')
            quit()
        else:
            print(f'You said: {text}')
            get_random_user(text)

record()