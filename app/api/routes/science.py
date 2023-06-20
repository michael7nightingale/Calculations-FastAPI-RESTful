from fastapi import APIRouter, Depends, Path

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.formula import get_result
from app.db.repositories import ScienceRepository, CategoryRepository, FormulaRepository
from app.models.schemas.science import ScienceEnum, RequestSchema


science_router = APIRouter(prefix='/science', tags=['Science'])


@science_router.post("/count-formula")
async def count_formula(result: str = Depends(get_result)):
    return {"result": result}


@science_router.get("/{science_slug}")
async def get_science(
        science_slug: ScienceEnum,
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository))
):
    science = science_repo.get(science_slug.value)
    return science.as_dict()


@science_router.get("/category/{category_slug}")
async def get_category(
        # science: dict = Depends(get_science),
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):

    category = category_repo.get(slug=category_slug)
    return category.as_dict()


@science_router.get("/category/{category_slug}/formulas")
async def get_category(
        # science: dict = Depends(get_science),
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
):
    category = category_repo.get(slug=category_slug)
    formulas = formula_repo.filter(category=category.title)
    return [f.as_dict() for f in formulas]


@science_router.get("/formula/{formula_slug}")
async def get_formula(
        # science: dict = Depends(get_science),
        formula_slug: str = Path(),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
):
    formula = formula_repo.get(slug=formula_slug)
    return formula.as_dict()

