from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

import models
import schemas
from database import engine, async_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # shutdown
    await engine.dispose()


async def get_db():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


app = FastAPI(lifespan=lifespan)


@app.post('/recipes', response_model=schemas.RecipeWithDetailedInfo)
async def add_recipe(recipe: schemas.RecipeIn, session: AsyncSession = Depends(get_db)) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())

    async with session.begin():
        session.add(new_recipe)

    return new_recipe


@app.get('/recipes', response_model=List[schemas.RecipeFromTop])
async def get_list_recipes(session: AsyncSession = Depends(get_db)) -> List[models.Recipe]:
    async with session.begin():
        res = await session.execute(select(models.Recipe.title, models.Recipe.views, models.Recipe.cooking_time)
                                    .order_by(models.Recipe.views.desc()).order_by(models.Recipe.cooking_time))
        return res.all()


@app.get('/recipes/{recipe_id}', response_model=Union[schemas.RecipeWithDetailedInfo, dict])
async def get_recipe(recipe_id: int, session: AsyncSession = Depends(get_db)) -> Union[models.Recipe, JSONResponse]:
    async with session.begin():
        res = await session.execute(select(models.Recipe)
                                    .where(models.Recipe.recipe_id == recipe_id))

        result = res.scalars().first()
        if result:
            return result
        raise HTTPException(status_code=404, detail='Recipe not found.')
