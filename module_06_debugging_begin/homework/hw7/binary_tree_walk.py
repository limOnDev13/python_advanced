"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional, Literal
import re

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def get_value_branch(line: str, level: Literal['INFO', 'DEBUG']) -> int:
    """
    Функция из полученной строки возвращает значение на ветке
    :param line: Строка лога
    :type line: str
    :param level: Уровень лога
    :type level: Literal['INFO', 'DEBUG']
    :raise ValueError: Если в строке нет слов 'INFO' или 'DEBUG'
    :return: Значение на ветке
    :rtype: int
    """
    if level == 'INFO':
        match: re.Match = re.search(r'(Visiting <BinaryTreeNode\[)(\d+)]>', line)
        return int(match.group(2))
    elif level == 'DEBUG':
        match: re.Match = re.search(r'(Adding <BinaryTreeNode\[)(\d+)]>', line)
        return int(match.group(2))
    else:
        raise ValueError('Не верный формат лога или передана не та строка!')


def get_info_about_child_tree(line_child: str) -> tuple[str, int]:
    """
    Функция из полученной строки лога получает информацию о дочернем дереве
    :param line_child: Строка лога о дочернем дереве
    :type line_child: str
    :return: Направление ветви и значение на ней
    :rtype: tuple[str, int]
    """
    # Определим направление дочерней ветки
    if 'left' in line_child:
        branch_direction = 'left'
    elif 'right' in line_child:
        branch_direction = 'right'
    else:
        raise ValueError('Не верный формат лога или передана не та строка!')

    # Получим значение ветки. Формат всех логов одинаковый, поэтому можно воспользоваться re.
    # Если формат логов изменится, функция перестанет работать
    branch_value: int = get_value_branch(line_child, 'DEBUG')

    return branch_direction, branch_value


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    """
    Функция восстанавливает бинарное дерево по логам
    :param path_to_log_file: Путь до файла с логами
    :type path_to_log_file: str
    :return: Корень восстановленного дерева
    :rtype: BinaryTreeNode
    """
    restored_tree: dict[int, BinaryTreeNode] = dict()  # здесь будут храниться значение веток и сами ветки

    with open(path_to_log_file, 'r', encoding='utf-8') as file:
        lines: list[str] = [line.rstrip() for line in file]

        # сохраним значение корня дерева
        root_value = get_value_branch(lines[0], 'INFO')

        # Одновременно просмотрим три последовательные строки
        for line_num in range(len(lines) - 2):  # Чтобы не выйти за границы
            # нас интересуют только INFO логи, DEBUG логи будут автоматически просматриваться
            if 'INFO' in lines[line_num]:
                # Получим значение на родительской ветке
                parent_value: int = get_value_branch(lines[line_num], 'INFO')
                if parent_value not in restored_tree:
                    restored_tree[parent_value] = BinaryTreeNode(parent_value)

                # Проверим наличие дочерних веток
                if 'DEBUG' in lines[line_num + 1]:
                    direction, value = get_info_about_child_tree(lines[line_num + 1])
                    restored_tree[value] = BinaryTreeNode(value)
                    setattr(restored_tree[parent_value], direction, restored_tree[value])
                if 'DEBUG' in lines[line_num + 2]:
                    direction, value = get_info_about_child_tree(lines[line_num + 2])
                    restored_tree[value] = BinaryTreeNode(value)
                    setattr(restored_tree[parent_value], direction, restored_tree[value])

    # Вернем корень восстановленного дерева
    return restored_tree[root_value]


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(levelname)s:%(message)s",
    #     filename="walk_log_4.txt",
    #     filemode='w'
    # )
    #
    # root = get_tree(7)
    # walk(root)

    # Сравним имеющиеся лог файлы деревьев с лог файлами прохода восстановленных деревьев
    num = 4  # Номер имеющегося лог файла. Нужен для проверки (есть 1, 2, 3, 4 лог файлы)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename=f"restored_walk_log_{num}.txt",
        filemode='w'
    )
    walk(restore_tree(f'walk_log_{num}.txt'))

    with open(f'walk_log_{num}.txt', 'r', encoding='utf-8') as init_log:
        with open(f'restored_walk_log_{num}.txt', 'r', encoding='utf-8') as new_log:
            print(f'{num} Начальное и восстановленное деревья совпали? {init_log.read() == new_log.read()}')

