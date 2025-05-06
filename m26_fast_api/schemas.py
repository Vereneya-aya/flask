from pydantic import BaseModel

class RecipeBase(BaseModel):
    title: str
    description: str
    ingredients: str
    cooking_time: int

class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int
    views: int

    class Config:
        orm_mode = True