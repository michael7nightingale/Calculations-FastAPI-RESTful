from fastapi import APIRouter, Depends, Path, Request
from starlette.exceptions import HTTPException

from app.api.dependencies import (
    get_repository, get_result, get_formula_information,
    get_plot_path
)
from app.db.repositories import ScienceRepository, CategoryRepository, FormulaRepository
from app.models.schemas import FormulaShow, CategoryShow
from app.resources.responses import (
    SCIENCE_NOT_FOUND, CATEGORY_NOT_FOUND, SPECIAL_CATEGORY,

)
from app.services.formulas.mathem_extra_counter import equation_system


# initializing router
science_router = APIRouter(prefix='/science', tags=['Science'])


@science_router.get("/{science_slug}")
async def get_science(
        science_slug: str = Path(),
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository))
):
    """
    Get single science data.
    """
    science = science_repo.get(science_slug)
    if science is None:
        raise HTTPException(status_code=404, detail=SCIENCE_NOT_FOUND)
    return science.as_dict()


@science_router.get("/{science_slug}/categories", response_model=list[CategoryShow])
async def get_science_categories(
        science_slug: str = Path(),
        science_repo: ScienceRepository = Depends(get_repository(ScienceRepository)),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):
    """
    Get all categories` data on some science.
    """
    science = science_repo.get(science_slug)
    if science is None:
        raise HTTPException(status_code=404, detail=SCIENCE_NOT_FOUND)
    categories = category_repo.filter(science=science.title)
    return (c.as_dict() for c in categories)


@science_router.get("/category/{category_slug}", response_model=CategoryShow)
async def get_category(
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository))
):
    """
    Get single category data.
    """
    category = category_repo.get(slug=category_slug)
    if category is None:
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    return category.as_dict()


async def count_plot(plot_path: str = Depends(get_plot_path)):
    """
    Get plot image path on functions and settings.
    """
    return {"plot": plot_path}


async def count_equations(request: Request):
    """
    Count equation or several ones.
    """
    data = request.form()
    equations = []
    for i in range(1, 10):
        equation = data.get(f"equation{i}")
        if equation is not None:
            equations.append(equation)

    solution = equation_system(equations)
    return {"solution": solution}


SPECIAL_CATEGORIES = {
    "plots": count_plot,
    "equations": count_equations,

}


@science_router.get("/category/{category_slug}/formulas", response_model=list[FormulaShow])
async def get_category_formulas(
        category_slug: str = Path(),
        category_repo: CategoryRepository = Depends(get_repository(CategoryRepository)),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
):
    """
    Get formulas on some category.
    """
    if category_repo in SPECIAL_CATEGORIES:  # special category does not have formulas
        raise HTTPException(status_code=400, detail=SPECIAL_CATEGORY)
    category = category_repo.get(slug=category_slug)
    if category is None:    # scalar is None
        raise HTTPException(status_code=404, detail=CATEGORY_NOT_FOUND)
    formulas = formula_repo.filter(category=category.title)
    return (f.as_dict() for f in formulas)


@science_router.get("/formula/{formula_slug}")
async def get_formula(formula: dict = Depends(get_formula_information)):
    """
    Get formulas data.
    :return - dict, where:
     - "formula": information from the database
     - "info": information of Python objects to count formula (literals, SI, etc.).
    """
    return formula


@science_router.post("/count-formula")
async def count_formula(result: str = Depends(get_result)):
    """
    Count formula strictly according to request schema. All information data is from `get_formula`.
    """
    return {"result": result}


@science_router.post("/special-category/{category_slug}")
async def count_special_category(request: Request, category_slug: str = Path(), *args, **kwargs):
    """
    Return function of a special category
    """
    return await SPECIAL_CATEGORY[category_slug](*args, **kwargs)
