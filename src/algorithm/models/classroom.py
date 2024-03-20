from pydantic import BaseModel


class Classroom(BaseModel):
    size: int | None
    type: str | None
    id: str

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return f"{self.id}"
