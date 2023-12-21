from datetime import datetime, timedelta


def get_mounth_depth_of_report() -> list:
    # Получаем текущую дату
    current_date = datetime.now()

    # Определяем начальную дату как текущую дату минус один год
    start_date = current_date - timedelta(days=182)

    # Создаем список для хранения всех дат за последний год
    date_list = []

    # Перебираем все даты от начальной до текущей
    while start_date <= current_date:
        # Добавляем дату в формате "год-месяц" в список
        date_list.append(start_date.strftime("%Y-%m"))
        # Переходим к следующему месяцу
        start_date += timedelta(days=1)

    # Выводим полученный список дат
    date_list = sorted(list(set(date_list)))
    return date_list
