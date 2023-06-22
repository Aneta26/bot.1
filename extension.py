from collections import Counter
import json
import os
import string
import time
import bs4

import requests
from question import Question
import datetime
import random
import math
from colorama import Back, Fore, init
init()


class BaseQuestion(Question):
    def __init__(self, parent: 'Question') -> None:
        self.upTopic = parent
        self.botName = parent.botName
        self.logPath = parent.logPath
        self.logName = parent.logName

    def writeRandomGreeting(self):
        if random.random() < 0.3:
            self.print(f"Ваша тема {self.name} дуже цікава!")

    def writeMessege(self):
        self.print(f"Ви вибрали {self.name}.")


class InitQuestion(Question):
    def __init__(self, settings: dict) -> None:
        super().__init__(settings)
        self.topics = {
            'математика': MathQuestion(self),
            'фізика': PhysicsQuestion(self),
            'філологія': LangQuestion(self),
            'географія': GeographyQuestion(self),
            'робота з текстом': TextQuestion(self),
            'загальні': GeneralQuestion(self),
            'інші':  OthersQuestion(self),
        }
        self.upTopic = self

    def writeMessege(self):
        self.print(f"Привіт, я {self.botName}.")

    def writeList(self):
        self.print(
            f"Задайте питання з цих тем: {Back.GREEN+Fore.WHITE+ str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")

class OthersQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'Додаткові варіанти'
        self.topics = {
            "втрати русні": RusniQuestion(self),
            "вірш Шевченка": RhymQuestion(self),
            "код сторінки гугл": GoogleQuestion(self),
            "погода в Києві сьогодні": WeatherQuestion(self),
            "новини": NewsQuestion(self),
            "футбол": FootballQuestion(self),
            
        }

    def writeList(self):
        self.print(f"Вам доступні варіанти: {Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")

class FootballQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'футбол'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете почути новини про футбол?")

    def processText(self):
        soup = bs4.BeautifulSoup(requests.get("https://www.ua-football.com/ua/").text, 'html.parser')  
        
        news = soup.find_all('span', class_="d-block")
         
        text = "\n".join([(i.text).replace('\n', " ") for i in news])
        self.print(text)
        
        
class RusniQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'втрати русні'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете почути втрати русні?))")

    def processText(self):
        data = json.loads(requests.get('https://russianwarship.rip/api/v2/statistics/latest').text)['data']
        self.print(f"Втрати русні на {data['date']}")  
        self.print(f"Особовий склад: {data['stats']['personnel_units']}")
        self.print(f"Танки: {data['stats']['tanks']}")
        self.print(f"БТР: {data['stats']['armoured_fighting_vehicles']}")   
        self.print(f"Арта: {data['stats']['artillery_systems']}")   
        self.print(f"Літаки: {data['stats']['planes']}")   
        self.print(f"Вертольоти: {data['stats']['helicopters']}")   
        self.print(f"Кораблі: {data['stats']['warships_cutters']}")   
        self.print(f"Крилаті ракети: {data['stats']['cruise_missiles']}")   
              
class NewsQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'новини'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете почути новини?")

    def processText(self):
        soup = bs4.BeautifulSoup(requests.get("https://espreso.tv/").text, 'html.parser')  
        
        news = soup.find_all('div', class_='news-tape-item')
        
        text = "\n".join([(i.find('div', class_="time").text+" "+i.find('div', class_="content").text).replace('\n', " ") for i in news])
        self.print(text)
    
class WeatherQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'погода в Києві сьогодні'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете дізнатися погоду в Києві сьогодні?")

    def processText(self):
        html = requests.get("https://ua.sinoptik.ua/погода-київ").text
        text = html.split('<div class="description">')[1].split('</div>')[0]
        
        self.print(text)
    
class RhymQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'вірш Шевченка'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете почути вірш Шевченка?")

    def processText(self):
        self.print("""Сонце гріє, вітер віє
З поля на долину,
Над водою гне з вербою
Червону калину,
На калині одиноке
Гніздечко гойдає.
А де ж дівся соловейко?
Не питай, не знає.""")
        
        
class GoogleQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'код сторінки гугл'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви хочете побачити код сторінки гугл?")

    def processText(self):
        self.print(requests.get("https://google.com").text)
class MathQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'математика'
        self.topics = {
            "довжини дуги кола": DugaQuestion(self),
            "відстань від точки до прямої": LineDistQuestion(self),
            "площа прямокутника": RectSQuestion(self),
            "площа кола": CircleSQuestion(self),
            "число Фібоначі": FibQuestion(self),
          
        }

    def writeList(self):
        self.print(
            f"Вам доступні наступні обрахунки: {Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")

class DugaQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'довжини дуги кола'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок довжини дуги кола.")
        self.print(
            "Введіть радіус кола та кут в радіанах через пробіл (наприклад, 5 30).")

    def processText(self):
        r, a = [float(i) for i in self.input.split()]
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(r*a))
        
        
class LineDistQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'відстань від точки до прямої'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок відстані від точки до прямої.")
        self.print(
            "Введіть координати точки та 2-х точок на прямій через пробіл")

    def processText(self):
        x1, y1, x2, y2, x3, y3 = [float(i) for i in self.input.split()]
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(abs((y2-y1)*x3-(x2-x1)*y3+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)))
     
     
     
class RectSQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'площа прямокутника'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок площі прямокутника.")
        self.print(
            "Введіть довжини сторін прямокутника через пробіл")

    def processText(self):
        a, b = [float(i) for i in self.input.split()]
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(a*b))

class CircleSQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'площа кола'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок площі кола.")
        self.print(
            "Введіть радіус кола")

    def processText(self):
        r = float(self.input)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(math.pi*r**2))
        
        
class FibQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'число Фібоначі'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок числа Фібоначі.")
        self.print(
            "Введіть номер числа Фібоначі")

    def processText(self):
        n = int(self.input)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(round(((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5))))) # формула Біне

class GeographyQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'географія'
        self.topics = {
            "найбільша кількість кордонів": BorderQuestion(self),
            "найбільшу кількість озер": LakeQuestion(self),
            "країна з Сахарою": SakharaQuestion(self),
            "координати точки по азимуту": AzQuestion(self),
        }

    def writeList(self):
        self.print(
            f"Вам доступні наступні обрахунки: {Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")


class BorderQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'Країна з найбільшою кількістю кордонів'
        self.isFunction = True
        self.isNeedInput = False


    def writeMessege(self):
        self.print("Ви обрали країну з найбільшою кількістю кордонів.")
        
    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str("Китай"))
        
class LakeQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'Країна з найбільшою кількістю озер'
        self.isFunction = True
        self.isNeedInput = False


    def writeMessege(self):
        self.print("Ви обрали питання про найбільшу кількість озер.")
        
    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str("Канада"))
        
        
class SakharaQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'Країна з Сахарою'
        self.isFunction = True
        self.isNeedInput = False


    def writeMessege(self):
        self.print("Ви обрали питання про країну з Сахарою.")
        
    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str("Марокко"))
    

class AzQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'Координати точки по азимуту'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали питання про координати точки по азимуту.")
        self.print(
            "Введіть координати точки, відстань, азимут через пробіл.")
    
    def processText(self):  
        x, y, d, a = [float(i) for i in self.input.split()]
        x1, y1 =  x + d*math.cos(a), y + d*math.sin(a)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                     Fore.WHITE + str(x1) + " " + str(y1))


class LangQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'філологія'
        self.isNeedInput = True
        self.topics = {
            "дієслова в давальному відмінку": VerbQuestion(self),
        }

    def writeList(self):
        self.print(
            f"Вам доступні наступні теми: {Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")

class VerbQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'дієслова в давальному відмінку'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Правила утворення дієслів у давальному відмінку в українській мові .")
       
    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + """У давальному відмінку однини іменники другої відміни мають закінчення -ові, -еві, -єві або -у, -ю. Прізвища, що мають суфікси -ов, -ев, -єв, -ів, -їв, у давальному відмінку однини закінчуються тільки на -у """)
        
        


class TextQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'робота з текстовими файлами'
        self.topics = {
            "підрахувати повтор": RepeatQuestion(self),
            "латинські слова більше 10 повторів ": OftenQuestion(self), 
            "містять літеру": LetterQuestion(self), 
            "вивести в алф порядку": AlphQuestion(self), 
            "кількість слів з цифрами": NumCountQuestion(self), 
            "видалити слова з цифрами": DelNumQuestion(self), 
        }

    def writeList(self):
        self.print(
            f"Вам доступні наступні функції: {Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")


class RepeatQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'підрахувати повтор'
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали підрахувати повтори слів у тексті. Введіть ім'я вхідного та вихідного файлу: ")

    def processText(self):
        f1, f2 = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(Counter(words)))
        with open(f2, 'w') as f:
            f.write(str(Counter(words)))
        
        
class OftenQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'латинські слова більше 10 повторів '
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали знайти складені з латинських літер слова, які у тексті зустрічаються більше 10 разів. Введіть ім'я вхідного файлу: ")

    def processText(self):
        f1, f2 = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
            upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            lower = "abcdefghijklmnopqrstuvwxyz"
            # тальки латинські літери
            latin = upper + lower
            # слова, які зустрічаються більше 10 разів
            often = []
            for word in words:
                if word.isalpha() and all([letter in latin for letter in word]):
                    if words.count(word) > 10:
                        often.append(word)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX + Fore.WHITE + str(often))
        with open(f2, 'w') as f:
            f.write(str(often))
        
       
class LetterQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'містять літеру'
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали знайти слова, які містять введену літеру. Введіть ім'я вхідного файлу, літеру: ")

    def processText(self):
        f1, f2, letter = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
        words_with_letter = []
        for word in words:
            if letter in word:
                words_with_letter.append(word)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(words_with_letter))
        with open(f2, 'w') as f:
            f.write(str(words_with_letter))
        
class AlphQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'вивести в алф порядку'
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали вивести слова в алфавітному порядку. Введіть ім'я вхідного та вихідного файлу: ")

    def processText(self):
        f1, f2 = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
        words.sort()
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(words))
        with open(f2, 'w') as f:
            f.write(str(words))


class NumCountQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'кількість слів з цифрами'
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали кількість слів, які містять цифри. Введіть ім'я вхідного та вихідного файлу: ")

    def processText(self):
        f1, f2 = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
        num_count = 0
        for word in words:
            if any([letter.isdigit() for letter in word]):
                num_count += 1
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(num_count))
        with open(f2, 'w') as f:
            f.write(str(num_count))
    
class DelNumQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'видалити слова з цифрами'
        self.isFunction = True
        self.isNeedInput = True

    def writeMessege(self):
        self.print("Ви обрали видалити слова, які містять цифри. Введіть ім'я вхідного та вихідного файлу: ")

    def processText(self):
        f1, f2 = self.input.split()
        with open(f1, 'r') as f:
            text = f.read()
            words = text.split()
        words_without_num = []
        for word in words:
            if not any([letter.isdigit() for letter in word]):
                words_without_num.append(word)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(words_without_num))
        with open(f2, 'w') as f:
            f.write(str(words_without_num))
    
    
    
    
    
class GeneralQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'загальні питання'
        self.topics = {
            "котра година": HourQuestion(self),
            "пора року": SeasonQuestion(self),
            "зачитати вірш": ReadQuestion(self),
            "зачитати анекдот": JokeQuestion(self),
            
        }

    def writeMessege(self):
        self.print("Ви обрали загальні питання.")

    def writeList(self):
        self.print(
            f"Вам доступні наступні теми: {Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE+ str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")


class HourQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'котра година'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви обрали виведення години.")

    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX + Fore.WHITE +
                   str(datetime.datetime.now().hour))
    
class SeasonQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'пора року'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви обрали виведення пори року.")

    def processText(self):
        month = datetime.datetime.now().month
        if month in [12, 1, 2]:
            season = "зима"
        elif month in [3, 4, 5]:
            season = "весна"
        elif month in [6, 7, 8]:
            season = "літо"
        else:
            season = "осінь"
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX + Fore.WHITE + season)

class ReadQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'зачитати вірш (5 різних)'
        self.isFunction = True
        self.isNeedInput = False

    def writeMessege(self):
        self.print("Ви обрали зачитати вірш.")
        
    def processText(self):
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX + Fore.WHITE + "Зачитую вірш:")
        # 5 віршів
        poems = [ 
                 """Життя іде і все без коректур.
І час летить, не стишує галопу.
Давно нема маркізи Помпадур,
і ми живем уже після потопу.
Не знаю я, що буде після нас,
в які природа убереться шати.
Єдиний, хто не втомлюється, – час.
А ми живі, нам треба поспішати.
Зробити щось, лишити по собі,
а ми, нічого, – пройдемо, як тіні,
щоб тільки неба очі голубі
цю землю завжди бачили в цвітінні.
Щоб ці ліси не вимерли, як тур,
щоб ці слова не вичахли, як руди.
Життя іде і все без коректур,
і як напишеш, так уже і буде.
Але не бійся прикрого рядка.
Прозрінь не бійся, бо вони як ліки.
Не бійся правди, хоч яка гірка,
не бійся смутків, хоч вони як ріки.
Людині бійся душу ошукать,
бо в цьому схибиш – то уже навіки.
 - Ліна Костенко""",
""" Страшні слова, коли вони мовчать
Страшні слова, коли вони мовчать,
коли вони зненацька причаїлись,
коли не знаєш, з чого їх почать,
бо всі слова були уже чиїмись.

Хтось ними плакав, мучивсь, болів,
із них почав і ними ж і завершив.
Людей мільярди і мільярди слів,
а ти їх маєш вимовити вперше!

Все повторялось: і краса, й потворність.
Усе було: асфальти й спориші.
Поезія – це завжди неповторність,
якийсь безсмертний дотик до душі.

- Ліна Костенко""", 
""" А й правда, крилатим ґрунту не треба.
Землі немає, то буде небо.
Немає поля, то буде воля.
Немає пари, то будуть хмари.
В цьому, напевно, правда пташина…
А як же людина? А що ж людина?
Живе на землі. Сама не літає.
А крила має. А крила має!
Вони, ті крила, не з пуху-пір'я,
А з правди, чесноти і довір'я.
У кого – з вірності у коханні.
У кого – з вічного поривання.
У кого – з щирості до роботи.
У кого – з щедрості на турботи.
У кого – з пісні, або з надії,
Або з поезії, або з мрії.
Людина нібито не літає…
А крила має. А крила має!
- Ліна Костенко""",

""" Ще назва є, а річки вже немає.
Усохли верби, вижовкли рови,
і дика качка тоскно обминає
рудиментарні залишки багви.

І тільки степ, і тільки спека, спека,
і озерянин проблиски скупі.
І той у небі зморений лелека,
і те гніздо лелече на стовпі.

Куди ти ділась, річенько? Воскресни!
У берегів потріскались вуста.
Барвистих лук не знають твої весни,
і світить спека ребрами моста.

Стоять мости над мертвими річками.
Лелека зробить декілька кругів.
Очерети із чорними свічками
ідуть уздовж колишніх берегів...

 - Ліна Костенко""",
""" Поезія згубила камертон.
Хтось диригує ліктями й коліном.
Задеренчав і тон, і обертон,
і перша скрипка пахне нафталіном.
Поезія згубила камертон.
Перецвілась, бузкова і казкова.
І дивиться, як скручений пітон,
скрипковий ключ в лякливі очі слова.
У правди заболіла голова
од часнику, політики й гудрону.
Із правдою розлучені слова
кудись біжать по сірому перону.
Відходять вірші, наче поїзди.
Гримлять на рейках бутафорські строфи.
Але куди? Куди вони, куди?!
Поезія на грані катастрофи.
І чи зупиним, чи наздоженем?
Вагони йдуть, спасибі коліщаткам...
Але ж вони в майбутнє порожнем!
Як ми у вічі глянемо нащадкам?!
 - Ліна Костенко""",

        ]
            
            
        for i in range(5):
            self.print(Back.LIGHTMAGENTA_EX + Fore.WHITE + poems[i])
            time.sleep(1)
        self.print("Вірші зачитано.")
    
class JokeQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'жарт'
        self.isFunction = True
        self.isNeedInput = False
    
    def writeMessege(self):
        self.print("Ви хочете почути жарт?")
        
    def processText(self):
        self.print("Що буде, якщо з'їсти камінь?")
        self.print("Відповідь: зуби зламаєш.")
    
    

class PhysicsQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'фізика'
        self.topics = {
            "закон тяжіння": NewtonQuestion(self),
            "рівняння Ейнштейна": EinstainQuestion(self),
            "рівняння неозначеності": HeizenbergQuestion(self),
            "формула Ампера": AmperQuestion(self),
        }

    def writeList(self):
        self.print(
            f"Вам доступні наступні обрахунки: {Back.GREEN+Fore.WHITE+str.join(Back.RESET+Fore.RESET+', '+Back.GREEN+Fore.WHITE, self.topics)}.")

class NewtonQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'закон тяжіння'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали обрахунок сили тяжіння.")
        self.print(
            "Введіть масу першого тіла, масу другого тіла та відстань між ними через пробіл.")

    def processText(self):
        m1, m2, r = [float(i) for i in self.input.split()]
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(6.67408*10**(-11)*m1*m2/r**2))


class EinstainQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'рівняння Ейнштейна'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали рівняння Ейнштейна.")
        self.print(
            "Введіть масу тіла, що перетворюється в енергію (кг)")

    def processText(self):
        m = float(self.input)
        c = 299792458
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(m*c**2))
        
class HeizenbergQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'рівняння неозначеності'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали рівняння неозначеності.")
        self.print(
            "Введіть похибку вимірювання (м).")

    def processText(self):
        x = float(self.input)
        h = 6.62607015*10**(-34)
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +  Fore.WHITE + str(h/(4*math.pi*x)))

class AmperQuestion(BaseQuestion):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name = 'формула Ампера'
        self.isFunction = True

    def writeMessege(self):
        self.print("Ви обрали формулу Ампера.")
        self.print(
            "Введіть - магнітна сталу, струмб та відстань до провідника через пробіл.")
    
    def processText(self):
        mu, I, r = [float(i) for i in self.input.split()]
        self.print("Відповідь: " + Back.LIGHTMAGENTA_EX +
                   Fore.WHITE + str(2*mu*I/r))


