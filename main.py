from Jarvis import JarvisAssistant
import re
import os
import random
import gmail
import pprint
import datetime
import requests
import sys
import wikipedia
import urllib.parse 
import webbrowser 
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from pywikihow import search_wikihow
from bs4 import BeautifulSoup
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config

obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["सर, हमेशा आपके लिए मौजूद हूं", "मैं तैयार हूं सर",
                 "आपकी इच्छा मेरी आज्ञा", "मैं आपकी क्या मदद कर सकता हूं सर?", "मैं ऑनलाइन हूं और तैयार हूं सर"]

EMAIL_DIC = {
    'myself': 'prajwalrajput16@gmail.com',
    'my official email': 'prajwalrajput16@gmail.com',
    'my second email': 'prajwalrajput16@gmail.com',
    'my official mail': 'prajwalrajput16@gmail.com',
    'my second mail': 'prajwalrajput16@gmail.com'
}

CALENDAR_STRS = ["मेरे पास क्या है", "क्या मेरे पास कोई योजना है?", "क्या मैं व्यस्त हूं?"]
# =======================================================================================================================================================


def speak(text):
    obj.tts(text)


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("क्षमा करें सर, मैं आपके प्रश्न का उत्तर नहीं ला सका। कृपया पुन: प्रयास करें")
        return None
    
def startup():
    speak("जार्विस को आरंभ किया जा रहा है")
    # speak("सभी सिस्टम अनुप्रयोग प्रारंभ जा रहा है")
    # speak("सभी ड्राइवरों को स्थापित किया और जांचना हो रहा है")
    # speak("इंटरनेट कनेक्शन की जाँच की जा रही है")
    # speak("एक मिनट रुकिए सर")
    # speak("सभी ड्राइवर सक्रिय हैं और चल रहे हैं")
    # speak("सभी सिस्टम सक्रिय कर दिए गए हैं")
    # speak("अब मैं ऑनलाइन हूं")
    hour = int(datetime.datetime.now().hour)
    
    



def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("शुभ प्रभात")
    elif hour>12 and hour<18:
        speak("शुभ दोपहर ")
    else:
        speak("शुभ संध्या")
    c_time = obj.tell_time()
    speak(f"वर्तमान में यह है  {c_time}")
    speak("मैं जार्विस हूं. ऑनलाइन और तैयार सर. कृपया मुझे बताएं कि मैं आपकी कैसे मदद कर सक्ती हूं")
   
# if __name__ == "__main__":


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        wish()

        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)
                

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"सर अभि समय है  {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': "C:\Program Files\Google\Chrome\Application\chrome.exe",
                    'notepad': "C:\\Windows\\notepad.exe",
                    'code': "P:\\New Folder\\Microsoft VS Code\\Code.exe"
                    
                }

                app = command.split(' ')[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('आपके लिए  ' + app + 'लॉन्च हो रही है सर')
                    obj.launch_any_app(path_of_app=path)

            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'ठीक है सर!! प्रारंभिक  {domain}')
                print(open_result)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                       "क्षमा करें सर। मैं आपकी क्वेरी को अपने डेटाबेस से लोड नहीं कर सका। कृपया पुनः प्रयास करें")
            
            elif 'wikipedia' in command:
                speak('विकिपीडिया खोज रही हूँ...')
                query = command.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("विकिपीडिया के अनुसार")
                print(results)
                speak(results)

            elif "buzzing" in command or "news" in command or "headlines" in command:
                news_res = obj.news(2)
                speak('स्रोतः टाइम्स ऑफ इंडिया')
                speak('आज की सुर्खियाँ हैं..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res)-2:
                        break
                speak('ये थीं प्रमुख सुर्खियाँ, आपका दिन शुभ हो सर!!..')
            # elif "buzzing" in command or "news" in command or "headlines" in command:
            #     news_res = obj.news(language='hi')  # Specify Hindi as the language
            #     speak('स्रोत: द टाइम्स ऑफ़ इंडिया')
            #     speak('आज की टॉप हेडलाइंस हैं..')
            #     for index, articles in enumerate(news_res):
            #         pprint.pprint(articles['title'])
            #         speak(articles['title'])  # Assuming speak function supports Hindi text
            #         if index == len(news_res) - 2:
            #             break
            #     speak('ये थे टॉप हेडलाइंस, शुभ दिन हो!!..')


            # elif 'search google for' in command:
            #     obj.search_anything_google(command)
                
            elif 'google search' in command:
                import wikipedia as googleScrap
                query = command.replace("jarvis","")
                query = command.replace("google search","")
                query = command.replace("google","")
                speak("यह वही है जो मुझे वेब पर मिला!")
                pywhatkit.search(query)

                try:
                    result = googleScrap.summary(query,2)
                    speak(result)

                except:
                    speak("कोई बोलने योग्य डेटा उपलब्ध नहीं!")
            
            elif "gana" in command or "hit some music" in command:
                music_dir = "C:\\Users\\prajwal\\Downloads\\music"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"ठीक है सर, यूट्यूब पर  {video} चला रही हूँ ")
                pywhatkit.playonyt(video)

            elif "email" in command or "send email" in command:
                sender_email = config.sender_email
                sender_password = config.sender_password

                try:
                    speak("आप किसे ईमेल करना चाहते हैं सर?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:

                        speak("विषय क्या है सर?")
                        subject = obj.mic_input()
                        speak("क्या कहूँ?")
                        message = obj.mic_input()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        obj.send_mail(sender_email, sender_password,
                                      receiver_email, msg)
                        speak("ईमेल सफलतापूर्वक भेज दिया गया है")
                        time.sleep(2)

                    else:
                        speak(
                            "मुझे अपने डेटाबेस में अनुरोधित व्यक्ति का ईमेल नहीं मिला। कृपया किसी भिन्न नाम से पुनः प्रयास करें")

                except:
                    speak("क्षमा करें श्रीमान। आपका मेल नहीं भेजा जा सका. कृपया पुन: प्रयास करें")

            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)
            
            elif "what is" in command or "who is" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)

            elif "what do i have" in command or "do i have plans" or "am i busy" in command:
                obj.google_calendar_events(command)

            if "make a note" in command or "write this down" in command or "remember this" in command:
                speak("आप मुझसे क्या लिखवाना चाहेंगे?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("मैंने उसे नोट कर लिया है")

            elif "close the note" in command or "close notepad" in command:
                speak("ठीक है सर, नोटपैड बंद कर रहा हूँ")
                os.system("taskkill /f /im notepad++.exe")

            if "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "system" in command:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            elif 'how to' in command:
                speak("इंटरनेट से डेटा प्राप्त करना!")
                op = query.replace("jarvis","")
                max_result = 1
                how_to_func = search_wikihow(op,max_result)
                assert len(how_to_func) == 1
                how_to_func[0].print()
                speak(how_to_func[0].summary)
            
            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(ip)
                speak(f"Your ip address is {ip}")
                
            elif 'my location' in command:
                speak("ठीक है सर, एक सेकंड रुकें!")
                webbrowser.open('https://www.google.com/maps/@28.7091225,77.2749958,15z')

            elif "switch the window" in command:
                speak("ठीक है सर, विंडो स्विच कर रही हूँ")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

           

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("By what name do you want to save the screenshot?")
                name = obj.mic_input()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been succesfully captured")

            elif "show me the screenshot" in command:
                try:
                    img = Image.open('D://JARVIS//JARVIS_2.0//' + name)
                    img.show(img)
                    speak("Here it is sir")
                    time.sleep(2)

                except IOError:
                    speak("Sorry sir, I am unable to display the screenshot")

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden")

            elif "visible" in command or "make files visible" in command:
                os.system("attrib -h /s /d")
                speak("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")

            # if "calculate" in command or "what is" in command:
            #     query = command
            #     answer = computational_intelligence(query)
            #     speak(answer)

            

            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("ठीक है सर, ऑफ़लाइन जा रही हूँ। आपके साथ काम करके अच्छा लगा")
                sys.exit()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:\\Users\\prajwal\\OneDrive\\Desktop\\NJ\\JARVIS-master\\JARVIS-master\\Jarvis\\utils\\images\\live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:\\Users\\prajwal\\OneDrive\\Desktop\\NJ\\JARVIS-master\\JARVIS-master\\Jarvis\\utils\\images\\initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
