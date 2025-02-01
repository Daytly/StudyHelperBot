main_menu_message = "Меню"

input_text_task_message = "Введите максимально подробное описание задачи в **одно** сообщение"

input_award_task_message = "Введите вознаграждение в рублях (Пример: 100р)"

input_award_task_emission_message = "Введите только число"

input_death_line_task_message = "Крайнюю дату"

final_create_task_message = "Отлично ваш заказ на рассмотрении"

stop_create_task_message = "Создание отменено"

task_message = "Текст: {0}\nНаграда: {1}\nКр.срок:{2}\n"

edit_task_message = "Текст: {0}\nНаграда: {1}\nКр.срок:{2}\n***Статус***\n{3}"


def create_edit_task_message(order):
    if order.is_completed_tack:
        message = edit_task_message.format(order.text, order.award, order.death_line.strftime("%Y-%m-%d"),
                                           "Завершено ✅")
    else:
        if order.executor is not None:
            message = edit_task_message.format(order.text, order.award, order.death_line.strftime("%Y-%m-%d"),
                                               f"Заказчик: {order.executor.phone_number} {"Подтверждено" if order.is_completed_executor else "В производстве"}\n"
                                               f"Вы: {"Получено" if order.is_completed_customer else "Не получено"}\n")
        else:
            message = edit_task_message.format(order.text, order.award, order.death_line.strftime("%Y-%m-%d"),
                                               f"Заказчик: Не определён")
    return message
