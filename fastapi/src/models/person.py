from typing import Optional, List
from models.base_model import ESModel


class ESPerson(ESModel):
    id: str
    name: str
    film_ids: Optional[List[str]]
