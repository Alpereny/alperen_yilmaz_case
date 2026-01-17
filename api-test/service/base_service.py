import json
import functools
import requests
from pydantic import BaseModel


class BaseService:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.request = functools.partial(self.session.request, timeout=timeout)

    def get(self, path: str, params: dict = None):
        return self.session.get(f"{self.base_url}{path}", params=params)

    def post(self, path: str, data):
        payload = self._serialize(data)
        return self.session.post(f"{self.base_url}{path}", json=payload)

    def post_form(self, path: str, data: dict):
        return self.session.post(f"{self.base_url}{path}", data=data)

    def put(self, path: str, data):
        payload = self._serialize(data)
        return self.session.put(f"{self.base_url}{path}", json=payload)

    def delete(self, path: str):
        return self.session.delete(f"{self.base_url}{path}")

    def _serialize(self, data) -> dict:
        if isinstance(data, dict):
            return data
        if isinstance(data, BaseModel):
            return json.loads(
                data.model_dump_json(by_alias=True, exclude_unset=True, exclude_none=True)
            )
        return data
