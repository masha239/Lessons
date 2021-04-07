from tkinter import *
from learn import Teacher
import tkinter.font as tkFont


class MyFrame:
    def __init__(self, master):
        self.master = master

        self.master.title("Уроки")
        self.master.geometry('900x500')
        self.master['bg'] = '#F5F5DC'

        self.teacher = Teacher()
        self.characters = StringVar()
        self.about = StringVar()

        self.lbl_characters = Label(self.master, textvariable=self.characters, font=("Arial bold", "100"), bg='#F5F5DC', fg='#990033')
        self.lbl_characters.pack()
        self.lbl_characters.place(height=120, width=360, x=270, y=150)

        self.lbl_about = Label(self.master, textvariable=self.about, bg='#F5F5DC', fg='#990033')
        self.lbl_about.grid()
        self.lbl_about.place(height=50, width=500, x=200, y=280)
        font_about = tkFont.Font(family="Georgia", size=20, slant="italic")
        self.lbl_about.configure(font=font_about)

        self.button_backward = Button(self.master, text="<", font=("Arial bold", "30"), command=self.move_backward, bg='#99CCFF', fg='#990033')
        self.button_backward.pack()
        self.button_backward.place(bordermode=OUTSIDE, height=80, width=80, x=50, y=170)

        self.button_forward = Button(self.master, text=">", font=("Arial bold", "30"), command=self.move_forward, bg='#99CCFF', fg='#990033')
        self.button_forward.pack()
        self.button_forward.place(bordermode=OUTSIDE, height=80, width=80, x=770, y=170)

        self.prev_lessons_buttons = []
        self.next_lessons_buttons = []

        self.prev_lessons_bar = Frame(self.master, bg='#F5F5DC')
        self.next_lessons_bar = Frame(self.master, bg='#F5F5DC')

        self.master.bind('<Left>', self.move_forward)
        self.master.bind('<Right>', self.move_backward)
        self.update()

    def update(self):

        lesson = self.teacher.get_current_lesson()
        self.characters.set(lesson.hier)
        self.about.set(lesson.meaning)
        if not self.teacher.can_move_forward():
            self.button_forward['bg'] = 'lightgray'
        else:
            self.button_forward['bg'] = '#99CCFF'
        if not self.teacher.can_move_backward():
            self.button_backward['bg'] = 'lightgray'
        else:
            self.button_backward['bg'] = '#99CCFF'

        next_lessons = lesson.next_lessons
        prev_lessons = lesson.prev_lessons

        self.prev_lessons_bar = Frame(self.master, bg='#F5F5DC')
        self.prev_lessons_bar.place(height=100, width=130 * len(prev_lessons), x=(900 - 130 * len(prev_lessons)) // 2,
                                    y=35)

        self.next_lessons_bar = Frame(self.master, bg='#F5F5DC')
        self.next_lessons_bar.place(height=100, width=130 * len(next_lessons), x=(900 - 130 * len(next_lessons)) // 2,
                                    y=350)

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
                      font=("Arial bold", "20"),
                      command=lambda: self.move_to(lesson_id),
                      bg='#CC99FF',
                      fg='#990033')

    def create_next_button(self, lesson_id):
        return Button(self.next_lessons_bar,
                      text=self.teacher.get_lesson(lesson_id).hier,
                      font=("Arial bold", "20"),
                      command=lambda: self.move_to(lesson_id),
                      bg='#CC99FF',
                      fg='#990033')

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


root = Tk()
frame = MyFrame(root)
root.mainloop()