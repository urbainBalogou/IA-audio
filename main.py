from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import pyttsx3
import speech_recognition as sr

class TTSApp(App):
    def build(self):
        self.voice_type = 'male'
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.text_input = TextInput(hint_text='Entrez le texte ici', size_hint=(1, 0.2))
        layout.add_widget(self.text_input)

        self.filename_input = TextInput(hint_text='Nom du fichier (sans extension)', size_hint=(1, 0.1))
        layout.add_widget(self.filename_input)

        self.listen_button = Button(text='Écouter', size_hint=(1, 0.2))
        self.listen_button.bind(on_press=self.listen_text)
        layout.add_widget(self.listen_button)

       # self.voice_button = Button(text='Changer la voix', size_hint=(1, 0.2))
       # self.voice_button.bind(on_press=self.change_voice)
       # layout.add_widget(self.voice_button)

        self.save_button = Button(text='Extraire en MP3', size_hint=(1, 0.2))
        self.save_button.bind(on_press=self.save_audio)
        layout.add_widget(self.save_button)

        self.speech_to_text_button = Button(text='Reconnaissance Vocale', size_hint=(1, 0.2))
        self.speech_to_text_button.bind(on_press=self.speech_to_text)
        layout.add_widget(self.speech_to_text_button)

        self.status_label = Label(text='', size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        return layout

    def set_voice(self, engine, voice_type):
        voices = engine.getProperty('voices')
        for voice in voices:
            if voice_type in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    def change_voice(self, instance):
        self.voice_type = 'female' if self.voice_type == 'male' else 'male'
        self.status_label.text = f"Voix changée en {self.voice_type.capitalize()}."

    def listen_text(self, instance):
        text = self.text_input.text
        if text:
            try:
                engine = pyttsx3.init()
                self.set_voice(engine, self.voice_type)
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                self.status_label.text = f"Erreur lors de la lecture: {str(e)}"
            finally:
                engine.stop()
                del engine
            self.status_label.text = "Lecture terminée."
        else:
            self.status_label.text = "Veuillez entrer le texte à lire."

    def save_audio(self, instance):
        text = self.text_input.text
        filename = self.filename_input.text
        if text and filename:
            try:
                output_file = f"{filename}.mp3"
                engine = pyttsx3.init()
                self.set_voice(engine, self.voice_type)
                engine.save_to_file(text, output_file)
                engine.runAndWait()
            except Exception as e:
                self.status_label.text = f"Erreur lors de l'enregistrement: {str(e)}"
            finally:
                engine.stop()
                del engine
            self.status_label.text = f"Fichier audio enregistré : {output_file}"
        else:
            self.status_label.text = "Veuillez entrer le texte et le nom du fichier."

    def speech_to_text(self, instance):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.status_label.text = "Écoute en cours..."
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="fr-FR")
                self.text_input.text = text
                self.status_label.text = "Reconnaissance vocale réussie."
        except sr.UnknownValueError:
            self.status_label.text = "Impossible de comprendre l'audio."
        except sr.RequestError as e:
            self.status_label.text = f"Erreur de service de reconnaissance vocale: {str(e)}"
        except Exception as e:
            self.status_label.text = f"Erreur lors de la reconnaissance vocale: {str(e)}"
        finally:
            self.status_label.text += " (Session terminée)"

if __name__ == '__main__':
    TTSApp().run()
