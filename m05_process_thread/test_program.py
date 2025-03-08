
import sys

# Вывод в стандартный вывод (stdout)
print("Привет из test_program.py!")

# Вывод в поток ошибок (stderr)
print("Это сообщение об ошибке!", file=sys.stderr)

# Пример в TestProgram.py

def greet():
    print("Привет из TestProgram.py!")

if __name__ == "__main__":
    greet()