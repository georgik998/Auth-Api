from typing import Any


def build_default_answer(
        status: bool = True,
        message: str = 'ok',
        data: Any = None
):
    return {
        'status': status,
        'message': message,
        'data': data,
    }
