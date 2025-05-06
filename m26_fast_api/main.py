from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import models, crud, schemas
from database import Base, engine, get_db

app = FastAPI(title="Кулинарная книга API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/recipes", response_model=list[schemas.RecipeOut])
async def read_recipes(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_recipes(db)

@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def read_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    recipe = await crud.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe

@app.post("/recipes", response_model=schemas.RecipeOut, status_code=201)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_recipe(db, recipe)


# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc