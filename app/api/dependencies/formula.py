from fastapi import Body, Depends, Path

from app.api.dependencies import get_current_user, get_repository
from app.db.repositories import HistoryRepository, FormulaRepository
from app.models.schemas import RequestSchema
from app.services.formulas import contextBuilder
from app.services.formulas.metadata import get_formula


async def get_result(data: RequestSchema = Body(),
                     user=Depends(get_current_user),
                     history_repo: HistoryRepository = Depends(get_repository(HistoryRepository))):
    data.user_id = user.id
    result = contextBuilder.build_template(request=data, history_repo=history_repo)
    return result


async def get_formula_information(
        formula_slug: str = Path(),
        formula_repo: FormulaRepository = Depends(get_repository(FormulaRepository))
) -> dict:
    return {
        "formula": formula_repo.get(slug=formula_slug).as_dict(),
        "info": get_formula(formula_slug).as_dict()
    }
