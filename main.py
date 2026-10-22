from stack import Stack


def is_brackets_balanced(expression: str) -> bool:
    """Проверяет парность скобок с помощью Stack.

    Учитываются скобки (), [] и {}. Остальные символы пропускаются.
    Пустая строка и строка без скобок согласованы. Закрывающая скобка
    допустима только как пара к последней ещё не закрытой открывающей
    того же вида. В конце незакрытых скобок не остаётся.

    :param expression: проверяемая строка
    :raises TypeError: аргумент не строка
    :return: True, если скобки расставлены верно
    """
    pass


def main():
    stack = Stack()
    for value in (1, 2, 2):
        stack.push(value)
    print("Вершина:", stack.peek())
    print("Снято:", stack.pop())
    expression = "3 + 2 * (5 - [4 / {2 + 1}])"
    print(expression, is_brackets_balanced(expression))


if __name__ == "__main__":
    main()
