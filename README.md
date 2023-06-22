# Чатбот

Запустіть `main.py`:
```
python main.py
```
## Параметри в файлі `settings.json`
Ім'я вказується у полі `"name"`. Розмова зберігається в файл `dialogue-{time/date}.txt`. Та в файл, вказаний у `"log"` .


## Розширення тем

Нові теми наслідувати від `BaseQuestion`. В `self.name` вкажіть назву теми, а в `writeMessege()` - повідомлення при вході в тему. Вивід тексту через `self.print()`

```python
class YourQuestion(BaseQuestion):
    def __init__(self, parent):
        super().__init__(parent)

        self.name = "ім'я"

    def writeMessege(self):
        self.print(f"тема: {self.name}")

```

### Спецефічно для теми
Метод `writeList`  - повідомлення  підтем. Підтеми вказати y словнику `self.topics`
```python
class YourQuestion(BaseQuestion):
    def __init__(self, parent):
        super().__init__(parent)
        self.topics = {
            'тема А': A_Question(self),
        }
    def writeList(self):
        self.print(f"список: {str.join(', ', self.topics)}.")
```
## Для функції
Встановіть поле `self.isFunction = True`. В `processText` робіть решту. Щоб отримати ввід, встановіть `self.isNeedInput = True`, і якщо напаки то `False`. Ввід вводиться y `self.input`
```python
class ExampleQuestion(BaseQuestion):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "qwerty"
        self.isFunction = True

    def processText(self):
        self.print(f"{self.input}")
```
