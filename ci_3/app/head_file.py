import os

def read_file(file_path):
    if not os.path.exists(file_path):
        return {"error": "Файл не существует"}, 404
    if os.path.getsize(file_path) == 0:
        return {"error": "Файл пуст"}, 400
    with open(file_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}