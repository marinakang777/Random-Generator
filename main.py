import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Предопределённые задачи
DEFAULT_TASKS = [
    ("Прочитать статью", "учеба"),
    ("Сделать зарядку", "спорт"),
    ("Ответить на письма", "работа"),
    ("Выучить 10 новых слов", "учеба"),
    ("Пробежка 2 км", "спорт"),
    ("Составить отчёт", "работа")
]

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x500")

        # Данные
        self.tasks = []          # Все задачи (история)
        self.filtered_tasks = [] # Отфильтрованные задачи
        self.current_filter = "все"

        # Загрузка истории из JSON
        self.load_history()

        # GUI элементы
        self.create_widgets()

        # Обновление списка отображаемых задач
        self.refresh_task_list()

    def create_widgets(self):
        # Рамка генерации
        frame_gen = tk.Frame(self.root)
        frame_gen.pack(pady=10)

        self.generate_btn = tk.Button(frame_gen, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack()

        # Рамка фильтра
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(pady=5)

        tk.Label(frame_filter, text="Фильтр по типу:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="все")
        filter_menu = ttk.Combobox(frame_filter, textvariable=self.filter_var, values=["все", "учеба", "спорт", "работа"], state="readonly")
        filter_menu.pack(side=tk.LEFT, padx=5)
        filter_menu.bind("<<ComboboxSelected>>", self.apply_filter)

        # Список задач с прокруткой
        frame_list = tk.Frame(self.root)
        frame_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, height=15)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Рамка добавления новой задачи
        frame_add = tk.Frame(self.root)
        frame_add.pack(pady=10)

        tk.Label(frame_add, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(frame_add, width=25)
        self.new_task_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_add, text="Тип:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="учеба")
        type_menu = ttk.Combobox(frame_add, textvariable=self.type_var, values=["учеба", "спорт", "работа"], width=8, state="readonly")
        type_menu.pack(side=tk.LEFT, padx=5)

        self.add_btn = tk.Button(frame_add, text="Добавить задачу", command=self.add_task)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка очистки истории
        self.clear_btn = tk.Button(self.root, text="Очистить историю", command=self.clear_history, fg="red")
        self.clear_btn.pack(pady=5)

    def generate_task(self):
        if not self.tasks:
            messagebox.showwarning("Нет задач", "Добавьте хотя бы одну задачу в список!")
            return

        # Выбираем случайную задачу из ВСЕХ (не из отфильтрованных)
        random_task = random.choice(self.tasks)
        task_text = f"{random_task['text']} [{random_task['type']}]"
        messagebox.showinfo("Новая задача", f"Ваша задача:\n{task_text}")

    def add_task(self):
        new_text = self.new_task_entry.get().strip()
        new_type = self.type_var.get()

        if not new_text:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return

        # Проверка на дубликат (опционально)
        self.tasks.append({"text": new_text, "type": new_type})
        self.save_history()
        self.refresh_task_list()
        self.new_task_entry.delete(0, tk.END)

    def apply_filter(self, event=None):
        self.current_filter = self.filter_var.get()
        self.refresh_task_list()

    def refresh_task_list(self):
        """Обновляет отображаемый список задач в Listbox"""
        self.task_listbox.delete(0, tk.END)

        if self.current_filter == "все":
            self.filtered_tasks = self.tasks
        else:
            self.filtered_tasks = [t for t in self.tasks if t["type"] == self.current_filter]

        for task in self.filtered_tasks:
            self.task_listbox.insert(tk.END, f"{task['text']} [{task['type']}]")

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.tasks = []
            self.save_history()
            self.refresh_task_list()

    def save_history(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 0:
            with open("tasks.json", "r", encoding="utf-8") as f:
                try:
                    self.tasks = json.load(f)
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            # Загружаем предопределённые задачи
            self.tasks = [{"text": t[0], "type": t[1]} for t in DEFAULT_TASKS]
            self.save_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
