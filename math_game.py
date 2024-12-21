import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import os  # Для работы с путями
from playsound import playsound


class MathQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("Математический квест")
        self.score = 0
        self.age = None
        self.correct_answer = None
        self.sounds_path = os.path.dirname(__file__)  # Текущая папка программы
        self.create_widgets()

    def create_widgets(self):
        # Запрос возраста
        self.label_age = tk.Label(self.root, text="Выберите возраст ребенка (3-7):", font=("Arial", 18))
        self.label_age.pack(pady=10)

        self.age_buttons = []
        for i in range(3, 8):
            btn = tk.Button(self.root, text=str(i), font=("Arial", 18), command=lambda x=i: self.set_age(x))
            btn.pack(side=tk.LEFT, padx=5)
            self.age_buttons.append(btn)

        # Заголовок задания
        self.label_task = tk.Label(self.root, text="", font=("Arial", 24))
        self.label_task.pack(pady=20)

        # Кнопки для ввода ответов
        self.answer_buttons = []
        for _ in range(4):
            btn = tk.Button(self.root, text="", font=("Arial", 18), width=5, command=lambda b=_: self.check_answer(b))
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        # Результат проверки
        self.label_result = tk.Label(self.root, text="", font=("Arial", 18))
        self.label_result.pack(pady=10)

        # Счётчик очков
        self.label_score = tk.Label(self.root, text="Очки: 0", font=("Arial", 18))
        self.label_score.pack(pady=10)

        # Скрыть элементы до установки возраста
        self.toggle_game_widgets(False)

    def toggle_game_widgets(self, visible):
        widgets = [self.label_task, *self.answer_buttons, self.label_result, self.label_score]
        for widget in widgets:
            if visible:
                widget.pack(pady=10)
            else:
                widget.pack_forget()

    def set_age(self, age):
        self.age = age
        self.label_age.pack_forget()
        for btn in self.age_buttons:
            btn.pack_forget()
        self.toggle_game_widgets(True)
        self.new_task()

    def generate_task(self):
        if self.age == 3:
            num1, num2 = random.randint(1, 10), random.randint(1, 10)
            operation = random.choice(['+', '-'])
            if operation == '-':
                num1, num2 = max(num1, num2), min(num1, num2)
        elif self.age == 4:
            num1, num2 = random.randint(0, 20), random.randint(0, 20)
            operation = random.choice(['+', '-'])
            if operation == '-':
                num1, num2 = max(num1, num2), min(num1, num2)
        elif self.age == 5:
            num1, num2 = random.randint(0, 50), random.randint(0, 50)
            operation = random.choice(['+', '-'])
            result = num1 - num2 if operation == '-' else num1 + num2
            while result < -10:
                num1, num2 = random.randint(0, 50), random.randint(0, 50)
                result = num1 - num2 if operation == '-' else num1 + num2
        elif self.age == 6:
            num1, num2 = random.randint(0, 100), random.randint(0, 100)
            operation = random.choice(['+', '-', '*'])
            if operation == '*':
                num1, num2 = random.randint(0, 9), random.randint(0, 9)
            else:
                result = num1 - num2 if operation == '-' else num1 + num2
                while result < -20:
                    num1, num2 = random.randint(0, 100), random.randint(0, 100)
                    result = num1 - num2 if operation == '-' else num1 + num2
        elif self.age == 7:
            num1, num2 = random.randint(0, 200), random.randint(0, 200)
            operation = random.choice(['+', '-', '*'])
            if operation == '*':
                num1, num2 = random.randint(-9, 9), random.randint(-9, 9)
            else:
                result = num1 - num2 if operation == '-' else num1 + num2
                while result < -50:
                    num1, num2 = random.randint(0, 200), random.randint(0, 200)
                    result = num1 - num2 if operation == '-' else num1 + num2

        return num1, num2, operation

    def new_task(self):
        self.label_result.config(text="")
        for btn in self.answer_buttons:
            btn.config(bg="SystemButtonFace", state=tk.NORMAL)

        self.num1, self.num2, self.operation = self.generate_task()
        if self.operation == '+':
            self.correct_answer = self.num1 + self.num2
        elif self.operation == '-':
            self.correct_answer = self.num1 - self.num2
        elif self.operation == '*':
            self.correct_answer = self.num1 * self.num2

        self.label_task.config(text=f"{self.num1} {self.operation} {self.num2} = ?")

        answers = [self.correct_answer]
        while len(answers) < 4:
            fake_answer = random.randint(self.correct_answer - 10, self.correct_answer + 10)
            if fake_answer != self.correct_answer and fake_answer not in answers:
                answers.append(fake_answer)
        random.shuffle(answers)

        for i, btn in enumerate(self.answer_buttons):
            btn.config(text=str(answers[i]), command=lambda b=btn: self.check_answer(b))

    def check_answer(self, btn):
        selected_answer = int(btn.cget("text"))
        for button in self.answer_buttons:
            button.config(state=tk.DISABLED)

        if selected_answer == self.correct_answer:
            btn.config(bg="green")
            self.label_result.config(text="ПРАВИЛЬНО!", fg="green")
            self.score += 1
            playsound(os.path.join(self.sounds_path, "correct.mp3"))
        else:
            btn.config(bg="red")
            self.label_result.config(text=f"НЕПРАВИЛЬНО! Правильный ответ: {self.correct_answer}", fg="red")
            self.score = max(0, self.score - 1)
            playsound(os.path.join(self.sounds_path, "wrong.mp3"))

            for button in self.answer_buttons:
                if int(button.cget("text")) == self.correct_answer:
                    button.config(bg="green")

        self.label_score.config(text=f"Очки: {self.score}")
        delay = 8 - self.age
        threading.Thread(target=self.delayed_task_switch, args=(delay,)).start()

    def delayed_task_switch(self, delay):
        time.sleep(delay)
        self.new_task()


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuest(root)
    root.mainloop()
