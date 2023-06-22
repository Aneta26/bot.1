import json
from question import Question 
from extension import *
from colorama import init, Fore, Back
init()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Bot(metaclass=Singleton):
    
    strategy: Question
    
    def __init__(self) -> None:
        with open('settings.json', 'r') as f:
            self.settings =json.load(f)
                
    def setStrategy(self, strategy: Question):
        self.strategy = strategy
    
    def start(self):
        self.setStrategy(InitQuestion(self.settings)) 
        while True:
            self.strategy.writeMessege()
            
            if not self.strategy.isFunction:
                self.strategy.writeList()
                
            if not self.strategy.isNeedInput and self.strategy.isFunction:
                self.strategy.setInput(None)
                self.setStrategy(self.strategy.upTopic)
            else:
                inp = input()
                self.strategy.log(inp, 'користувач')
                
                if inp == 'назад':
                    self.setStrategy(self.strategy.upTopic)
                    continue
                elif inp == 'вихід':
                    self.strategy.print("Бувайте!")
                    break
                elif inp == 'допомога':
                    self.strategy.print(Back.GREEN+ Fore.LIGHTRED_EX +"Щоб вийти, напишіть «вихід». Для повернення назад напишіть «назад».")
                elif self.strategy.isFunction:
                    self.strategy.setInput(inp)
                    self.setStrategy(self.strategy.upTopic)
                elif inp in self.strategy.topics:
                    self.setStrategy(self.strategy.topics[inp])
                    self.strategy.writeRandomGreeting()
                    continue
                else:
                    self.strategy.print(Back.LIGHTRED_EX+ Fore.YELLOW +"Помилка, такого варіанту немає. Спробуйте ще.")
 