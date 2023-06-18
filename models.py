from typing import List
from pydantic import BaseModel


class assetRecord(BaseModel) :
    values : List[float]
    max_value : float
    min_value : float
    token : str