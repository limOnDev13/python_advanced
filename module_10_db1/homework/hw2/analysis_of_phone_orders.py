import sqlite3


def find_colours_and_num_orders() -> dict[str, int]:
    """Функция возвращает словарь, где ключи - цвет, значение - количество покупок данного цвета"""
    with sqlite3.connect('hw_2_database.db') as conn:
        cursor = conn.cursor()

        select_orders_query: str = """
        SELECT table_phones.colour, COUNT(table_checkout.id)
        FROM table_phones, table_checkout
        WHERE table_phones.id = table_checkout.phone_id
        GROUP BY table_phones.colour
        """
        cursor.execute(select_orders_query)
        result = cursor.fetchall()

        result_dict: dict[str, int] = dict()
        for colour, num in result:
            result_dict[colour] = result_dict[colour] + num if colour in result_dict else num

        # В бд покупок может не быть каких-то цветов - добавим их в словарь с количеством 0
        select_all_colours_query: str = """
        SELECT colour
        FROM table_phones
        GROUP BY colour
        """
        cursor.execute(select_all_colours_query)
        result = cursor.fetchall()
        for colour_tuple in result:
            if colour_tuple[0] not in result_dict:
                result_dict[colour_tuple[0]] = 0

        return result_dict


def solution_of_task(hist_of_colours: dict[str, int]) -> list:
    """Функция отвечает на вопросы задания"""
    answers: list = list()

    # 1) Телефоны какого цвета чаще всего покупают?
    answers.append(max(hist_of_colours, key=lambda colour: hist_of_colours[colour]))
    # 2) Какие телефоны чаще покупают: красные или синие?
    answers.append(max(['красный', 'синий'], key=lambda colour: hist_of_colours[colour]))
    # 3) Какой самый непопулярный цвет телефона?
    answers.append(min(hist_of_colours, key=lambda colour: hist_of_colours[colour]))
    return answers


def create_md_file_with_answers(answers: list, output_file: str = 'report.md') -> None:
    """
    Функция создает файл .md с ответами на вопросы из задания
    :param output_file: Имя output файла
    :param answers: Список ответов
    :return: None
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write('## Задача 2. Исследование продаж телефонов\n')

        for num, answer in enumerate(answers):
            output.write(f'{num + 1}. {answer}\n')


if __name__ == '__main__':
    answers_on_questions: list = solution_of_task(find_colours_and_num_orders())
    create_md_file_with_answers(answers_on_questions)
