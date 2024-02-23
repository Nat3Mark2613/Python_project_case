tasks_dict = dict()

STOP_COMMANDS = [
    "exit",
    "stop",
    "quit",
    "e",
    "s",
    "q"
]
YES_STATES = [
    "y",
    "yes",
    "ya",
    "да",
    "ya ya, naturlich"
]


def name_input(commandlet="new") -> str:
    if commandlet == "new":
        try:
            name = input("Write down task name: ")
            return name
        except Exception:
            print("Try another task name!\n")
            return name_input(commandlet)
    else:
        try:
            name = input("Write down task name to cancel: ")
            if name not in tasks_dict:
                raise Exception
            return name
        except Exception:
            print("Try another task name!\n")
            return name_input(commandlet)


def duration_input() -> int:
    try:
        dur = int(input("Write down overall time in hours: "))
        return dur
    except Exception:
        print("Write down some numbers!\n")
        return duration_input()


def priority_input() -> int:
    try:
        priority = int(input("Write down task priority form 1(max) to 4(min): "))
        if 1 > priority > 4:
            raise Exception()
        return priority
    except Exception:
        print("Write down some numbers!\n")
        return priority_input()


def description_input() -> str:
    try:
        descr = input("Write down task description: ")
        return descr
    except Exception:
        print("Try another task description!\n")
        return description_input()


def new_task() -> None:
    name = name_input()
    description = description_input()
    priority = priority_input()
    tasks_dict[name] = {"dur": "not_set", "desc": description, "p": priority}
    print("Task created.")


def cancel_task() -> None:
    if tasks_dict:
        name = name_input("cancel")
        tasks_dict.pop(name)
        print("Task deleted.")
    else:
        print("You haven`t tasks add some with 'new'.")


def view_tasks() -> None:
    if tasks_dict:
        headers = ["Name", "Duration", "Description", "Priority"]

        # Данные для таблицы
        data = [
            [name, meta['dur'], meta['desc'], meta['p']]
            for name, meta in tasks_dict.items()
        ]

        command = input("Do you want to get list ordered by alphabet? [Y/N]: ")
        if command.lower() in YES_STATES:
            data = sorted(data, key=lambda row: row[0])

        column_widths = [
            max(len(str(item))
                for item in [
                    row[i] for row in [headers] + data
                ])
            for i in range(len(headers))
        ]

        header_row = " | ".join(f"{headers[i]:<{column_widths[i]}}" for i in range(len(headers)))
        print(header_row)
        print("-" * len(header_row))  # Разделитель

        # Форматирование и вывод данных
        for row in data:
            print(" | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row))))
    else:
        print("You haven`t tasks add some with 'new'.")


def set_time() -> None:
    total_time = duration_input()  # Предполагается, что это функция для ввода общего времени
    tasks_with_weights = [(name, 4 / meta['p']) for name, meta in tasks_dict.items()]
    total_weight = sum(weight for _, weight in tasks_with_weights)

    # Первоначальное распределение времени с округлением вниз
    for task_name, weight in tasks_with_weights:
        allocated_time = int((weight / total_weight) * total_time)  # Округление вниз
        tasks_dict[task_name]['dur'] = allocated_time

    # Вычисляем, сколько времени осталось после первоначального распределения
    allocated_time_sum = sum(tasks_dict[task_name]['dur'] for task_name in tasks_dict)
    remaining_time = total_time - allocated_time_sum

    # Распределение оставшегося времени, начиная с задач с наивысшим весом
    for task_name, _ in sorted(tasks_with_weights, key=lambda x: x[1], reverse=True):
        if remaining_time > 0:
            tasks_dict[task_name]['dur'] += 1
            remaining_time -= 1
        else:
            break

    print("Time allocated to each task. Have fun.")


def help_command():
    print("Send\nnew - to do new task\ncancel - to cancel task\nview - to view all tasks"
          "\ntime - to set time\nquit to quit")


def process_command(user_command: str):
    if user_command == "new":
        new_task()
    elif user_command == "cancel":
        cancel_task()
    elif user_command == "view":
        view_tasks()
    elif user_command == "time":
        set_time()
    elif user_command == 'help':
        help_command()
    else:
        print("Command not found. Write help to get help.")


def get_command():
    command = str(input("Your command: ")).lower()
    if command in STOP_COMMANDS:
        return False
    return command


def main_loop() -> None:
    while True:
        command = get_command()
        if not command:
            return
        process_command(command)


if __name__ == "__main__":
    print("Send\nnew - to do new task\ncancel - to cancel task\nview - to view all tasks"
          "\ntime - to set time\nquit to quit")
    main_loop()
