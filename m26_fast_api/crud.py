from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, asc
from models import Recipe
from schemas import RecipeCreate

async def get_all_recipes(db: AsyncSession):
    result = await db.execute(
        select(Recipe).order_by(desc(Recipe.views), asc(Recipe.cooking_time))
    )
    return result.scalars().all()

async def get_recipe_by_id(db: AsyncSession, recipe_id: int):
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if recipe:
        recipe.views += 1
        await db.commit()
        await db.refresh(recipe)
    return recipe

async def create_recipe(db: AsyncSession, recipe_data: RecipeCreate):
    recipe = Recipe(**recipe_data.dict())
    db.add(recipe)
    await db.commit()
    await db.refresh(recipe)
    return recipe