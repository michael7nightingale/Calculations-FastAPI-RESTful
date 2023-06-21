from fastapi import APIRouter, Depends, Path

from app.api.dependencies import get_repository, get_result, get_formula_information
from app.db.repositories import ScienceRepository, CategoryRepository, FormulaRepository
from app.models.schemas import FormulaShow, CategoryShow


science_router = APIRouter(prefix='/science', tags=['Science'])


@science_router.get("/{science_slug}")
async def get_science(
        science_slug: str = Path(),
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository))
):
    science = science_repo.get(science_slug)
    return science.as_dict()


@science_router.get("/{science_slug}/categories", response_model=list[CategoryShow])
async def get_science(
        science_slug: str = Path(),
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):
    science = science_repo.get(science_slug)
    categories = category_repo.filter(science=science.title)
    return science.as_dict()


@science_router.get("/category/{category_slug}", response_model=CategoryShow)
async def get_category(
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):
    category = category_repo.get(slug=category_slug)
    return category.as_dict()


@science_router.get("/category/{category_slug}/formulas", response_model=list[FormulaShow])
async def get_category(
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
):
    category = category_repo.get(slug=category_slug)
    formulas = formula_repo.filter(category=category.title)
    return (f.as_dict() for f in formulas)


@science_router.get("/formula/{formula_slug}")
async def get_formula(formula: dict = Depends(get_formula_information)):
    return formula


@science_router.post("/count-formula")
async def count_formula(result: str = Depends(get_result)):
    return {"result": result}

