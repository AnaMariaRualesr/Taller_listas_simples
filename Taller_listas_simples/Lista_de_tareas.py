# Simple Linked List Workshop — Data Structures

import tkinter as tk
from tkinter import messagebox


class Node:
    def __init__(self, task, priority="Normal"):
        self.task      = task
        self.priority  = priority
        self.completed = False
        self.next      = None


class TaskList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def append(self, task, priority="Normal"):
        new_node = Node(task, priority)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail      = new_node

    def prepend(self, task, priority="Normal"):
        new_node      = Node(task, priority)
        new_node.next = self.head
        self.head     = new_node
        if self.tail is None:
            self.tail = new_node

    def toggle_completed(self, task):
        current = self.head
        while current is not None:
            if current.task == task:
                current.completed = not current.completed
                return True
            current = current.next
        return False

    def delete(self, task):
        if self.is_empty():
            return False
        if self.head.task == task:
            if self.head is self.tail:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.next
            return True
        previous = self.head
        current  = self.head.next
        while current is not None:
            if current.task == task:
                previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                return True
            previous = current
            current  = current.next
        return False

    def search(self, text):
        current  = self.head
        position = 1
        while current is not None:
            if text.lower() in current.task.lower():
                return current, position
            current  = current.next
            position += 1
        return None, -1

    def count_total(self):
        count   = 0
        current = self.head
        while current is not None:
            count  += 1
            current = current.next
        return count

    def count_completed(self):
        count   = 0
        current = self.head
        while current is not None:
            if current.completed:
                count += 1
            current = current.next
        return count

    def count_by_priority(self, priority):
        count   = 0
        current = self.head
        while current is not None:
            if current.priority == priority:
                count += 1
            current = current.next
        return count


BG_APP     = "#f5f0ff"
BG_HEADER  = "#ede4ff"
BG_INPUT   = "#fdf8ff"
BG_CARD    = "#ffffff"
BG_CARD_OK = "#f0fff8"

ACCENT     = "#9b72cf"
ACCENT2    = "#b98ee8"
GREEN      = "#6dbf8f"
YELLOW     = "#e8b84b"
PEACH      = "#e8916a"
BLUE_SOFT  = "#74b3ce"
RED_SOFT   = "#d96b7a"

TEXT_DARK  = "#3b3054"
TEXT_DIM   = "#a89bbf"
TEXT_DONE  = "#b8aed0"

PRIORITY_COLOR = {"Alta": PEACH, "Normal": BLUE_SOFT, "Baja": GREEN}

F_TITLE = ("Helvetica", 18, "bold")
F_SUB   = ("Helvetica", 9)
F_LABEL = ("Helvetica", 10, "bold")
F_BTN   = ("Helvetica", 9,  "bold")
F_SMALL = ("Helvetica", 9)
F_BADGE = ("Helvetica", 8,  "bold")


class App:
    def __init__(self, root):
        self.root      = root
        self.task_list = TaskList()
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        self.root.title("Gestor de Tareas · Lista Enlazada Simple")
        self.root.geometry("800x660")
        self.root.configure(bg=BG_APP)
        self.root.resizable(False, False)

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG_HEADER, padx=28, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="✅  Gestor de Tareas",
                 font=F_TITLE, bg=BG_HEADER, fg=ACCENT).pack(anchor="w")
        tk.Label(header,
                 text="Listas Enlazadas Simples  ·  Estructuras de Datos  ·  Python POO",
                 font=F_SUB, bg=BG_HEADER, fg=TEXT_DIM).pack(anchor="w", pady=(2, 0))

        input_panel = tk.Frame(self.root, bg=BG_INPUT, padx=24, pady=14)
        input_panel.pack(fill="x")

        row1 = tk.Frame(input_panel, bg=BG_INPUT)
        row1.pack(fill="x")

        tk.Label(row1, text="Nueva tarea:", font=F_LABEL,
                 bg=BG_INPUT, fg=TEXT_DARK).pack(side="left", padx=(0, 8))

        self.entry = tk.Entry(row1, font=("Helvetica", 11),
                              bg=BG_CARD, fg=TEXT_DARK,
                              insertbackground=ACCENT,
                              relief="solid", bd=1, width=38,
                              highlightthickness=1,
                              highlightcolor=ACCENT,
                              highlightbackground="#ddd5f0")
        self.entry.pack(side="left", ipady=5, padx=(0, 14))
        self.entry.bind("<Return>", lambda e: self._on_append())

        tk.Label(row1, text="Prioridad:", font=F_LABEL,
                 bg=BG_INPUT, fg=TEXT_DARK).pack(side="left", padx=(0, 6))

        self.priority_var = tk.StringVar(value="Normal")
        for label, color in [("Alta", PEACH), ("Normal", BLUE_SOFT), ("Baja", GREEN)]:
            tk.Radiobutton(row1, text=label, variable=self.priority_var,
                           value=label, font=F_BTN,
                           bg=BG_INPUT, fg=color,
                           selectcolor=BG_CARD,
                           activebackground=BG_INPUT,
                           relief="flat").pack(side="left", padx=3)

        row2 = tk.Frame(input_panel, bg=BG_INPUT)
        row2.pack(fill="x", pady=(10, 0))

        buttons = [
            ("＋  Agregar al final",  self._on_append,    ACCENT,    "#fff"),
            ("⬆  Agregar al inicio", self._on_prepend,   ACCENT2,   "#fff"),
            ("🔍  Buscar",           self._on_search,    YELLOW,    "#fff"),
            ("📊  Estadísticas",     self._on_stats,     BLUE_SOFT, "#fff"),
        ]
        for label, command, bg, fg in buttons:
            tk.Button(row2, text=label, command=command, font=F_BTN,
                      bg=bg, fg=fg, relief="flat", padx=12, pady=5,
                      cursor="hand2", activebackground=TEXT_DIM,
                      activeforeground="#fff", bd=0).pack(side="left", padx=4)

        tk.Frame(self.root, bg="#ddd5f0", height=1).pack(fill="x")

        container = tk.Frame(self.root, bg=BG_APP)
        container.pack(fill="both", expand=True, padx=20, pady=12)

        self.canvas   = tk.Canvas(container, bg=BG_APP, highlightthickness=0)
        scrollbar     = tk.Scrollbar(container, orient="vertical",
                                     command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.cards_frame   = tk.Frame(self.canvas, bg=BG_APP)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.cards_frame, anchor="nw"
        )
        self.cards_frame.bind("<Configure>", self._on_frame_resize)
        self.canvas.bind("<Configure>",      self._on_canvas_resize)
        self.canvas.bind_all("<MouseWheel>", self._on_scroll)

        self.status_var = tk.StringVar(value="Lista vacía")
        status_bar      = tk.Frame(self.root, bg=BG_HEADER, padx=20, pady=6)
        status_bar.pack(fill="x", side="bottom")
        tk.Label(status_bar, textvariable=self.status_var, font=F_SMALL,
                 bg=BG_HEADER, fg=TEXT_DIM, anchor="w").pack(fill="x")

        self._refresh()

    def _on_frame_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_scroll(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _read_input(self):
        return self.entry.get().strip(), self.priority_var.get()

    def _clear_input(self):
        self.entry.delete(0, "end")

    def _on_append(self):
        task, priority = self._read_input()
        if not task:
            messagebox.showwarning("Aviso", "Escribe una tarea antes de agregar.")
            return
        self.task_list.append(task, priority)
        self._clear_input()
        self._refresh()
        self.status_var.set(f"✔  '{task}' agregada al final  ·  Prioridad: {priority}")

    def _on_prepend(self):
        task, priority = self._read_input()
        if not task:
            messagebox.showwarning("Aviso", "Escribe una tarea antes de agregar.")
            return
        self.task_list.prepend(task, priority)
        self._clear_input()
        self._refresh()
        self.status_var.set(f"⬆  '{task}' agregada al inicio  ·  Prioridad: {priority}")

    def _on_toggle(self, task):
        self.task_list.toggle_completed(task)
        self._refresh()

    def _on_delete(self, task):
        self.task_list.delete(task)
        self._refresh()
        self.status_var.set(f"🗑  '{task}' eliminada de la lista")

    def _on_search(self):
        text, _ = self._read_input()
        if not text:
            messagebox.showwarning("Aviso", "Escribe el texto a buscar.")
            return
        node, position = self.task_list.search(text)
        if node:
            points_to = "último nodo (apunta a NULL)" \
                        if node.next is None else f"'{node.next.task}'"
            status    = "Completada ✔" if node.completed else "Pendiente ⏳"
            messagebox.showinfo("Tarea encontrada",
                f"Tarea     : {node.task}\n"
                f"Posición  : #{position}\n"
                f"Prioridad : {node.priority}\n"
                f"Estado    : {status}\n"
                f"Apunta a  : {points_to}")
        else:
            messagebox.showinfo("Sin resultados",
                f"No se encontró ninguna tarea con '{text}'.")

    def _on_stats(self):
        total     = self.task_list.count_total()
        completed = self.task_list.count_completed()
        pending   = total - completed
        high      = self.task_list.count_by_priority("Alta")
        normal    = self.task_list.count_by_priority("Normal")
        low       = self.task_list.count_by_priority("Baja")
        first     = "—" if self.task_list.is_empty() else self.task_list.head.task
        last      = "—" if self.task_list.is_empty() else self.task_list.tail.task

        messagebox.showinfo("Estadísticas · Lista Enlazada",
            f"{'─'*34}\n"
            f"  Total de tareas   :  {total}\n"
            f"  Completadas       :  {completed}\n"
            f"  Pendientes        :  {pending}\n"
            f"{'─'*34}\n"
            f"  Prioridad Alta    :  {high}\n"
            f"  Prioridad Normal  :  {normal}\n"
            f"  Prioridad Baja    :  {low}\n"
            f"{'─'*34}\n"
            f"  Primera tarea     :  {first}\n"
            f"  Última tarea      :  {last}\n"
            f"  Lista vacía       :  {'Sí' if self.task_list.is_empty() else 'No'}\n"
            f"{'─'*34}")

    def _refresh(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if self.task_list.is_empty():
            tk.Label(self.cards_frame,
                     text="Aún no hay tareas  ·  ¡Agrega la primera! 🌱",
                     font=("Helvetica", 11, "italic"),
                     bg=BG_APP, fg=TEXT_DIM).pack(pady=40)
        else:
            current = self.task_list.head
            while current is not None:
                self._build_card(current)
                current = current.next

        total     = self.task_list.count_total()
        completed = self.task_list.count_completed()
        self.status_var.set(
            f"Total: {total}   ·   Completadas: {completed}   ·   "
            f"Pendientes: {total - completed}   ·   "
            f"Alta: {self.task_list.count_by_priority('Alta')}   "
            f"Normal: {self.task_list.count_by_priority('Normal')}   "
            f"Baja: {self.task_list.count_by_priority('Baja')}"
        )

    def _build_card(self, node):
        bg_card   = BG_CARD_OK if node.completed else BG_CARD
        task_name = node.task

        card = tk.Frame(self.cards_frame, bg=bg_card,
                        highlightthickness=1,
                        highlightbackground="#e2d8f5")
        card.pack(fill="x", padx=6, pady=4)

        check_icon  = "☑" if node.completed else "☐"
        check_color = GREEN if node.completed else "#c5bcd8"
        tk.Button(card, text=check_icon,
                  font=("Helvetica", 17),
                  bg=bg_card, fg=check_color,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg_card,
                  command=lambda t=task_name: self._on_toggle(t)
                  ).pack(side="left", padx=(10, 4), pady=10)

        text_color = TEXT_DONE if node.completed else TEXT_DARK
        text_font  = ("Helvetica", 11, "overstrike") if node.completed \
                     else ("Helvetica", 11)
        tk.Label(card, text=node.task,
                 font=text_font, bg=bg_card, fg=text_color,
                 anchor="w").pack(side="left", fill="x",
                                  expand=True, padx=(0, 10), pady=10)

        badge_color = PRIORITY_COLOR.get(node.priority, BLUE_SOFT)
        tk.Label(card, text=f"  {node.priority}  ",
                 font=F_BADGE, bg=badge_color, fg="#fff",
                 padx=4, pady=3).pack(side="left", padx=(0, 10), pady=10)

        tk.Button(card, text="🗑",
                  font=("Helvetica", 13),
                  bg=bg_card, fg=RED_SOFT,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=bg_card,
                  activeforeground="#c0392b",
                  command=lambda t=task_name: self._on_delete(t)
                  ).pack(side="right", padx=(0, 12), pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()