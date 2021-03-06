from datetime import datetime, time

def get_rings():
    with open("rings.txt", "r", encoding="utf-8") as f:
        rings = {1: [],
                 2: [],
                 3: [],
                 4: [],
                 5: []
                 }
        for line in f:
            lesson = line.strip().split("\t")
            weekday = int(lesson[0])
            lesson_begin = time(hour=int(lesson[1]), minute=int(lesson[2]))
            rings[weekday].append(lesson_begin)

    return rings


def get_schedule():
    with open("schedule.txt", "r", encoding="utf-8") as f:
        schedule = dict()
        for i in range(1, 6):
            schedule[i] = dict()
            for j in range(1, 11):
                schedule[i][j] = None

        for line in f:
            data = line.strip().split("\t")
            weekday = int(data[0])
            lesson_number = int(data[1])
            lesson = data[2]
            schedule[weekday][lesson_number] = lesson
    return schedule


def get_next_lesson(rings, weekday, curtime):
    next_lesson = None
    if weekday in [6, 7]:
        return None
    for n, lesson_time in enumerate(rings[weekday], 1):
        if curtime <= lesson_time:
            next_lesson = n
            break
    return next_lesson


if __name__ == '__main__':
    weekday = datetime.today().isoweekday()
    curtime = datetime.now().time()
    weekday = 6
    curtime = time(10, 30)
    schedule = get_schedule()

    rings = get_rings()
    next_lesson = get_next_lesson(rings, weekday, curtime)
    if next_lesson:
        today_schedule = schedule[weekday]
        for i in range(next_lesson, len(today_schedule)):
            if today_schedule[i]:
                print(f"Следующий урок '{today_schedule[i]}' в {rings[weekday][i - 1]}")
                break
        else:
            print("Сегодня уроков нет")
    else:
        print("Сегодня уроков  нет")
