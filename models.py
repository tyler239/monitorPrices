from typing import List
from pydantic import BaseModel


class assetRecord(BaseModel) :
    values : List[float]
    token : str
    trend : str