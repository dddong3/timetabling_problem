from typing import List

from pydantic import BaseModel


class ChromosomeFiles(BaseModel):
    files: List[str]
