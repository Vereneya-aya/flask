def is_adult(age):
    """Функция проверяет, является ли человек совершеннолетним (18+)."""
    if not isinstance(age, (int, float)):
        raise ValueError("Возраст должен быть числом")
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
    return age >= 18