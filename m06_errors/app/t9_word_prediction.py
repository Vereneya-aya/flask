from itertools import product


def load_words(filepath='fixtures/words.txt'):
    """Загружаем список слов в виде множества для быстрого поиска."""
    with open(filepath, 'r') as f:
        words = set(word.strip().lower() for word in f if word.strip())
    return words


def get_letter_combinations(digits):
    """Генерируем все возможные комбинации букв для введённой последовательности цифр."""
    keypad = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    letter_groups = [keypad[digit] for digit in digits]
    return ("".join(letters) for letters in product(*letter_groups))


def my_t9(digits):
    """Основная функция: возвращает список слов, соответствующих введённым цифрам."""
    if not digits or not all(d in '23456789' for d in digits):
        return []  # Проверяем, что только допустимые цифры

    words = load_words()
    possible_words = get_letter_combinations(digits)
    return [word for word in possible_words if word in words]


# Пример
print(my_t9("22736368"))  # Должно вернуть ['basement'] (если слово есть в словаре)
