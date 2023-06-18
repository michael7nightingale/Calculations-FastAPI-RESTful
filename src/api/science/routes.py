from fastapi import APIRouter, Depends, Path

from ..auth.dependencies import get_current_user
from infrastructure.db.dependencies import get_repository
from .db.repository import ScienceRepository, CategoryRepository, FormulaRepository
from .schemas import ScienceEnum
from .dependencies import get_result


science_router = APIRouter(prefix='/science')


@science_router.get("/{science_slug}")
async def get_science(
        science_slug: ScienceEnum,
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository))
):
    science = await science_repo.get(science_slug.value)
    return science.as_dict()


@science_router.get("/{science_slug}/category/{category_slug}")
async def get_category(
        science: dict = Depends(get_science),
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):
    category = await category_repo.get(slug=category_slug)
    return category.as_dict()


@science_router.get("/{science_slug}/formula/{formula_slug}")
async def get_formula(
        science: dict = Depends(get_science),
        formula_slug: str = Path(),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
):
    formula = await formula_repo.get(slug=formula_slug)
    return formula.as_dict()


@science_router.post("/count-formula")
async def count_formula(result: float = Depends(get_result),
                        user = Depends(get_current_user)):
    return {"result": result}
