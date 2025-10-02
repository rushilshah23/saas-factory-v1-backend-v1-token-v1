from dataclasses import dataclass
from src.common.helpers.status_codes import StatusCodes
from typing import Any

@dataclass
class CustomResponse:
    status_code:StatusCodes
    message:str
    error:bool = False
    data:Any = None

    def to_dict(self):
        return {
            'status_code':self.status_code.value,
            'message':self.message,
            'data':self.data,
            'error':self.error
        }