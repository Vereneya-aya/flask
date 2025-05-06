from typing import Dict, Any

author_get_doc: Dict[str, Any] = {
    "tags": ["Authors"],
    "summary": "Получить список авторов",
    "responses": {
        "200": {
            "description": "Список авторов",
            "schema": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/Author"
                }
            }
        }
    },
    "definitions": {
        "Author": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        }
    }
}