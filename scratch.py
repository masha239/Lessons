from pymongo import MongoClient


class Lesson:
    lesson_id = 0

    def __init__(self, hier='', meaning=''):
        self.lesson_id = Lesson.lesson_id
        Lesson.lesson_id += 1
        self.hier = hier
        self.meaning = meaning
        self.next_lessons = []
        self.prev_lessons = []

    def fill_from_dict(self, doc):
        self.lesson_id = doc['lesson_id']
        self.hier = doc['hier']
        self.meaning = doc['meaning']
        self.prev_lessons = doc['prev_lessons']
        self.next_lessons = doc['next_lessons']


def make_lessons():
    lessons = []

    lessons.append(Lesson('一', '1'))
    lessons.append(Lesson('二', '2'))
    lessons.append(Lesson('三', '3'))
    lessons.append(Lesson('个', 'Единица, штука, целое'))
    lessons.append(Lesson('人', 'Человек'))
    lessons.append(Lesson('一个人', 'Один человек'))
    lessons.append(Lesson('人人', 'Все, каждый'))
    lessons.append(Lesson('日', 'Солнце, день'))
    lessons.append(Lesson('日日', 'Каждый день (как и 天天)'))
    lessons.append(Lesson('月', 'Луна, месяц'))
    lessons.append(Lesson('水', 'Вода, жидкость, река, море, поток'))
    lessons.append(Lesson('山', 'Горы, хребет, могила'))
    lessons.append(Lesson('山水', 'Пейзаж'))
    lessons.append(Lesson('大', 'Большой'))
    lessons.append(Lesson('大人', 'Взрослый'))
    lessons.append(Lesson('小', 'Маленький'))
    lessons.append(Lesson('口', 'Рот, губы, отверстие'))
    lessons.append(Lesson('大口', 'Большой глоток'))
    lessons.append(Lesson('人口', 'Население'))
    lessons.append(Lesson('山口', 'Горный перевал'))
    lessons.append(Lesson('才', 'Талант'))
    lessons.append(Lesson('口才', 'Красноречие'))
    lessons.append(Lesson('火', 'Огонь, Марс (планета)'))
    lessons.append(Lesson('大火', 'Большое пламя'))
    lessons.append(Lesson('小火', 'Маленькое пламя'))
    lessons.append(Lesson('山火', 'Лесной пожар'))
    lessons.append(Lesson('火山', 'Вулкан'))

    # Тут добавляем связь вручную!
    lesson1 = Lesson('田', 'Поле')
    lesson2 = Lesson('力', 'Сила')
    lesson3 = Lesson('男', 'Мужчина')
    lessons.append(lesson1)
    lessons.append(lesson2)
    lessons.append(lesson3)

    lessons.append(Lesson('女', 'Женщина'))
    lessons.append(Lesson('工', 'Работа'))
    lessons.append(Lesson('天', 'Небо, день'))
    lessons.append(Lesson('天天', 'Каждый день (как и 日日)'))
    lessons.append(Lesson('今', 'Сейчас'))
    lessons.append(Lesson('今天', 'Сегодня'))
    lessons.append(Lesson('牛', 'Корова, крупный рогатый скот'))
    lessons.append(Lesson('小牛', 'Теленок'))
    lessons.append(Lesson('马', 'Лошадь'))
    lessons.append(Lesson('人马', 'Войско, армия'))
    lessons.append(Lesson('羊', 'Баран, овца, мелкий рогатый скот'))
    lessons.append(Lesson('山羊', 'Горная коза'))
    lessons.append(Lesson('木', 'Дерево'))
    lessons.append(Lesson('工人', 'Рабочий'))
    lessons.append(Lesson('木工', 'Столяр, плотник'))
    lessons.append(Lesson('开', 'Открыть, начать'))
    lessons.append(Lesson('开口', 'Говорить'))
    lessons.append(Lesson('心', 'Сердце, душа, дух'))
    lessons.append(Lesson('门', 'Дверь'))
    lessons.append(Lesson('开门', 'Открыть дверь'))
    lessons.append(Lesson('十', 'Десять'))
    lessons.append(Lesson('十一', 'Одиннадцать'))
    lessons.append(Lesson('十二', 'Двенадцать'))
    lessons.append(Lesson('十三', 'Тринадцать'))
    lessons.append(Lesson('二十', 'Двадцать'))
    lessons.append(Lesson('三十', 'Тридцать'))
    lessons.append(Lesson('百', 'Сотня'))
    lessons.append(Lesson('手', 'Рука'))
    lessons.append(Lesson('手工', 'Ремесло'))
    lessons.append(Lesson('一手', 'В одиночку, единолично'))
    lessons.append(Lesson('生', 'Рождение'))
    lessons.append(Lesson('生日', 'День рождения'))
    lessons.append(Lesson('一生', 'Всю свою жизнь'))

    # Добавим связи
    for lesson in lessons:
        lesson.next_lessons = [x.lesson_id for x in lessons if x.hier.find(lesson.hier) != -1 and x is not lesson]
        lesson.prev_lessons = [x.lesson_id for x in lessons if lesson.hier.find(x.hier) != -1 and x is not lesson]

    lesson1.next_lessons.append(lesson3.lesson_id)
    lesson2.next_lessons.append(lesson3.lesson_id)
    lesson3.prev_lessons.append(lesson1.lesson_id)
    lesson3.prev_lessons.append(lesson2.lesson_id)

    # Отсортируем по возрастанию сложности
    lessons.sort(key=lambda x:len(x.hier))

    db = MongoClient()['ch_lessons']
    coll_lessons = db['lessons']
    coll_lessons.insert_many(map(lambda x: x.__dict__, lessons))


def get_lessons():
    db = MongoClient()['ch_lessons']
    coll_lessons = db['lessons']

    # Вот это можно сделать лучше?
    for doc in coll_lessons.find():
        lesson = Lesson()
        lesson.fill_from_dict(doc)
        yield lesson


if __name__ == '__main__':
    make_lessons()