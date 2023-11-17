from pydantic import BaseModel


class Headers(BaseModel):
    client_id: str
    api_key: str
