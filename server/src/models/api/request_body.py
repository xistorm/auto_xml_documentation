from pydantic import BaseModel


class RequestBody(BaseModel):
    code_text: str
    language: str | None = None
