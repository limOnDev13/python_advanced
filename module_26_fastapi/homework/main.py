from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import select
from typing import List, Union

import models
import schemas
from database import engine, session


# deprecated
# @app.on_event('startup')
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     await session.close()
#     await engine.dispose()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # shutdown
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post('/recipes', response_model=schemas.RecipeWithDetailedInfo)
async def add_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())

    async with session.begin():
        session.add(new_recipe)

    return new_recipe


@app.get('/recipes', response_model=List[schemas.RecipeFromTop])
async def get_list_recipes() -> List[models.Recipe]:
    async with session.begin():
        res = await session.execute(select(models.Recipe.title, models.Recipe.views, models.Recipe.cooking_time)
                                    .order_by(models.Recipe.views.desc()).order_by(models.Recipe.cooking_time))
        return res.all()


@app.get('/recipes/{recipe_id}', response_model=Union[schemas.RecipeWithDetailedInfo, dict])
async def get_recipe(recipe_id: int) -> Union[models.Recipe, JSONResponse]:
    async with session.begin():
        res = await session.execute(select(models.Recipe)
                                    .where(models.Recipe.recipe_id == recipe_id))

        result = res.scalars().first()
        if result:
            return result
        return JSONResponse(content={'message': "Recipe not found"}, status_code=404)
