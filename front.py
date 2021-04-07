from tkinter import *
from learn import Teacher
import tkinter.font as tkfont


COLOR_BEIGE = '#F5F5DC'
COLOR_VOILET = '#CC99FF'
COLOR_PINK = '#990033'
COLOR_GRAY = 'lightgray'
COLOR_BLUE = '#99CCFF'
FONT_MAIN_HIER = ("Arial bold", "100")
FONT_MOVE = ("Arial bold", "25")


def get_formula(n):
    return (900 - 130 * n) // 2


class MyFrame:
    def __init__(self, master):
        self.master = master

        self.master.title("Уроки")
        self.master.geometry('900x500')
        self.master['bg'] = COLOR_BEIGE

        self.teacher = Teacher()
        self.characters = StringVar()
        self.about = StringVar()

        self.lbl_characters = Label(self.master,
                                    textvariable=self.characters,
                                    font=FONT_MAIN_HIER,
                                    bg=COLOR_BEIGE,
                                    fg=COLOR_PINK)
        self.lbl_characters.pack()
        self.lbl_characters.place(height=120, width=360, x=270, y=150)

        self.lbl_about = Label(self.master, textvariable=self.about, bg=COLOR_BEIGE, fg=COLOR_PINK)
        self.lbl_about.grid()
        self.lbl_about.place(height=50, width=700, x=100, y=280)
        font_about = tkfont.Font(family="Georgia", size=30, slant="italic")
        self.lbl_about.configure(font=font_about)

        self.button_backward = Button(self.master,
                                      text="<",
                                      font=FONT_MOVE,
                                      command=self.move_backward,
                                      bg=COLOR_BLUE,
                                      fg=COLOR_PINK)
        self.button_backward.pack()
        self.button_backward.place(bordermode=OUTSIDE, height=80, width=80, x=50, y=170)

        self.button_forward = Button(self.master, text=">",
                                     font=FONT_MOVE,
                                     command=self.move_forward,
                                     bg=COLOR_BLUE,
                                     fg=COLOR_PINK)
        self.button_forward.pack()
        self.button_forward.place(bordermode=OUTSIDE, height=80, width=80, x=770, y=170)

        self.prev_lessons_buttons = []
        self.next_lessons_buttons = []

        self.prev_lessons_bar = Frame(self.master, bg=COLOR_BEIGE)
        self.next_lessons_bar = Frame(self.master, bg=COLOR_BEIGE)

        self.update()

    def update(self):
        lesson = self.teacher.get_current_lesson()
        self.characters.set(lesson.hier)
        self.about.set(lesson.meaning)
        if not self.teacher.can_move_forward():
            self.button_forward['bg'] = COLOR_GRAY
        else:
            self.button_forward['bg'] = COLOR_BLUE
        if not self.teacher.can_move_backward():
            self.button_backward['bg'] = COLOR_GRAY
        else:
            self.button_backward['bg'] = COLOR_BLUE

        next_lessons = lesson.next_lessons
        prev_lessons = lesson.prev_lessons

        self.prev_lessons_bar = Frame(self.master, bg=COLOR_BEIGE)
        self.prev_lessons_bar.place(height=100, width=130 * len(prev_lessons), x=get_formula(len(prev_lessons)), y=35)

        self.next_lessons_bar = Frame(self.master, bg=COLOR_BEIGE)
        self.next_lessons_bar.place(height=100, width=130 * len(next_lessons), x=get_formula(len(prev_lessons)), y=350)

        for button in self.prev_lessons_buttons:
            button.destroy()
        self.prev_lessons_buttons = [self.create_prev_button(lesson_id) for lesson_id in prev_lessons]

        for button in self.next_lessons_buttons:
            button.destroy()
        self.next_lessons_buttons = [self.create_next_button(lesson_id) for lesson_id in next_lessons]

        for idx, button in enumerate(self.prev_lessons_buttons):
            button.pack(side=LEFT)
            button.place(height=80, width=120, x=idx * 130, y=10)

        for idx, button in enumerate(self.next_lessons_buttons):
            button.pack(side=LEFT)
            button.place(height=80, width=120, x=idx * 130, y=10)

    def create_prev_button(self, lesson_id):
        return Button(self.prev_lessons_bar,
                      text=self.teacher.get_lesson(lesson_id).hier,
                      font=FONT_MOVE,
                      command=lambda: self.move_to(lesson_id),
                      bg=COLOR_VOILET,
                      fg=COLOR_PINK)

    def create_next_button(self, lesson_id):
        return Button(self.next_lessons_bar,
                      text=self.teacher.get_lesson(lesson_id).hier,
                      font=FONT_MOVE,
                      command=lambda: self.move_to(lesson_id),
                      bg=COLOR_VOILET,
                      fg=COLOR_PINK)

    def move_backward(self):
        if self.teacher.can_move_backward():
            self.teacher.move_backward()
            self.update()

    def move_forward(self):
        if self.teacher.can_move_forward():
            self.teacher.move_forward()
            self.update()

    def move_to(self, lesson_id):
        try:
            self.teacher.move_to(lesson_id)
            self.update()
        except ValueError as err:
            raise err
