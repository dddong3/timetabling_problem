from pydantic import BaseModel


class Classroom(BaseModel):
    size: int | None
    type: str | None
    id: str

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return f"{self.id}"

    def __hash__(self) -> int:
        return hash(self.id)
    
    # def __eq__(self, o: object) -> bool:
    #     return self.id == o.id
    
    # def __lt__(self, o: object) -> bool:
    #     return self.id < o.id