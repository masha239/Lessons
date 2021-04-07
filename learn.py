from scratch import get_lessons


class Teacher:
    def __init__(self):
        self.lessons = [lesson for lesson in get_lessons()]
        if len(self.lessons) == 0:
            raise ValueError('There is no lessons!')
        self.current = 0

    def get_current_lesson(self):
        return self.lessons[self.current]

    def get_lesson(self, lesson_id):
        try:
            lessons_ids = [lesson.lesson_id for lesson in self.lessons]
            return self.lessons[lessons_ids.index(lesson_id)]
        except ValueError as err:
            raise err

    def can_move_forward(self):
        return self.current < len(self.lessons) - 1

    def can_move_backward(self):
        return self.current > 0

    def move_forward(self):
        if self.can_move_forward():
            self.current += 1
        else:
            raise IndexError("Can't move forward!")

    def move_backward(self):
        if self.can_move_backward():
            self.current -= 1
        else:
            raise IndexError("Can't move backward!")

    def move_to(self, lesson_id):
        try:
            lessons_ids = [lesson.lesson_id for lesson in self.lessons]
            self.current = lessons_ids.index(lesson_id)
        except ValueError as err:
            raise err
