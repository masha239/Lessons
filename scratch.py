import itertools

from pymongo import MongoClient
import uuid


class Lesson:

    def __init__(self, hier='', meaning=''):
        self.hier = hier
        self.meaning = meaning
        self.next_lessons = []
        self.prev_lessons = []
        self.lesson_id = uuid.uuid1()

    def fill_from_dict(self, doc):
        self.__dict__ = doc

    @staticmethod
    def unmarshall(dictionary):
        result = Lesson()
        result.__dict__ = dictionary
        return result

    @staticmethod
    def chain(a, b):
        if a.hier in b.hier:
            a.next_lessons.append(b.lesson_id)
            b.prev_lessons.append(a.lesson_id)

        elif b.hier in a.hier:
            b.next_lessons.append(a.lesson_id)
            a.prev_lessons.append(b.lesson_id)


def make_lessons():

    lesson1 = Lesson('田', 'Поле')
    lesson2 = Lesson('力', 'Сила')
    lesson3 = Lesson('男', 'Мужчина')

    abnormal_lessons = [lesson1, lesson2, lesson3]
    normal_lessons = [
        Lesson('一', '1'),
        Lesson('二', '2'),
        Lesson('三', '3'),
        Lesson('个', 'Единица, штука, целое'),
        Lesson('人', 'Человек'),
        Lesson('一个人', 'Один человек'),
        Lesson('人人', 'Все, каждый'),
        Lesson('日', 'Солнце, день'),
        Lesson('日日', 'Каждый день (как и 天天)'),
        Lesson('月', 'Луна, месяц'),
        Lesson('水', 'Вода, жидкость, река, море, поток'),
        Lesson('山', 'Горы, хребет, могила'),
        Lesson('山水', 'Пейзаж'),
        Lesson('大', 'Большой'),
        Lesson('大人', 'Взрослый'),
        Lesson('小', 'Маленький'),
        Lesson('口', 'Рот, губы, отверстие'),
        Lesson('大口', 'Большой глоток'),
        Lesson('人口', 'Население'),
        Lesson('山口', 'Горный перевал'),
        Lesson('才', 'Талант'),
        Lesson('口才', 'Красноречие'),
        Lesson('火', 'Огонь, Марс (планета)'),
        Lesson('大火', 'Большое пламя'),
        Lesson('小火', 'Маленькое пламя'),
        Lesson('山火', 'Лесной пожар'),
        Lesson('火山', 'Вулкан'),
        Lesson('女', 'Женщина'),
        Lesson('工', 'Работа'),
        Lesson('天', 'Небо, день'),
        Lesson('天天', 'Каждый день (как и 日日)'),
        Lesson('今', 'Сейчас'),
        Lesson('今天', 'Сегодня'),
        Lesson('牛', 'Корова, крупный рогатый скот'),
        Lesson('小牛', 'Теленок'),
        Lesson('马', 'Лошадь'),
        Lesson('人马', 'Войско, армия'),
        Lesson('羊', 'Баран, овца, мелкий рогатый скот'),
        Lesson('山羊', 'Горная коза'),
        Lesson('木', 'Дерево'),
        Lesson('工人', 'Рабочий'),
        Lesson('木工', 'Столяр, плотник'),
        Lesson('开', 'Открыть, начать'),
        Lesson('开口', 'Говорить'),
        Lesson('心', 'Сердце, душа, дух'),
        Lesson('门', 'Дверь'),
        Lesson('开门', 'Открыть дверь'),
        Lesson('十', 'Десять'),
        Lesson('十一', 'Одиннадцать'),
        Lesson('十二', 'Двенадцать'),
        Lesson('十三', 'Тринадцать'),
        Lesson('二十', 'Двадцать'),
        Lesson('三十', 'Тридцать'),
        Lesson('百', 'Сотня'),
        Lesson('手', 'Рука'),
        Lesson('手工', 'Ремесло'),
        Lesson('一手', 'В одиночку, единолично'),
        Lesson('生', 'Рождение'),
        Lesson('生日', 'День рождения'),
        Lesson('一生', 'Всю свою жизнь')
    ]

    lessons = normal_lessons + abnormal_lessons

    # Добавим связи
    for a, b in itertools.combinations(lessons, 2):
        Lesson.chain(a, b)

    lesson1.next_lessons.append(lesson3.lesson_id)
    lesson2.next_lessons.append(lesson3.lesson_id)
    lesson3.prev_lessons.append(lesson1.lesson_id)
    lesson3.prev_lessons.append(lesson2.lesson_id)

    with MongoClient() as db:
        client = db['ch_lessons']
        coll_lessons = client['lessons']
        if coll_lessons.count_documents({}) > 0:
            raise Exception("Collection 'lessons' isn't empty!")
        coll_lessons.insert_many(x.__dict__ for x in lessons)


def get_lessons():
    with MongoClient() as db:
        client = db['ch_lessons']
        coll_lessons = client['lessons']
        res = list(map(Lesson.unmarshall, coll_lessons.find()))
        res.sort(key=lambda x:len(x.hier))
        return res


if __name__ == '__main__':
    make_lessons()