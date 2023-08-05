from http import HTTPStatus


class Response:
    def __init__(self, status: int):
        self.status = HTTPStatus(status)

    def wrap(self, field: str, data: dict) -> dict:
        response = dict()
        response[field] = data
        return response

    def success(self, data: dict) -> dict:
        return self.wrap(field="success", data=data)

    def error(self, error: HTTPStatus, detail: str = "") -> dict:
        error_data = {
            "type": error.name,
            "code": error.value,
            "status": self.status.value,
            "title": self.status.phrase,
            "detail": detail,
        }
        return self.wrap(field="error", data=error_data)
