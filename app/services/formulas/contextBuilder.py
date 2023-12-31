import numpy as np
import logging

from numpy import pi, e, cos, sin    # type: ignore # noqa: F401  # for eval()

from app.db.repositories import HistoryRepository
from .metadata import storage
from app.models.schemas import RequestSchema, HistoryIn

# логирование
logger = logging.getLogger(__name__)


def build_template(request: RequestSchema,
                   history_repo: HistoryRepository):
    # получение параметров
    formula_obj = storage[request.formula_slug]
    params = formula_obj.literals
    args = formula_obj.args
    find_mark = args[0]
    result = ''
    message = ""
    try:
        # переменные, которые могут поменяться если будет POST метод
        # параметры для шаблона
        find_mark = request.find_mark
        # параметры для вычисления
        nums_comma = int(request.nums_comma)
        nums = np.array([], dtype='float16')
        si = np.array([], dtype='float16')

        find_args = tuple(filter(lambda x: x != find_mark, formula_obj.args))
        for arg in find_args:
            nums = np.append(nums, eval(request.data[arg]))
            si = np.append(si, float(params[arg].si[request.data[f"{arg}si"]]))
        # считать результат
        result = formula_obj.match(
            **dict(zip(find_args, nums * si))
        )[0]
        result = str(round(result, nums_comma))
        history_repo.create(HistoryIn(
            formula=formula_obj.formula,
            result=result,
            user=request.user_id
        ))

    except (SyntaxError, NameError):
        message = "Невалидные данные."
    except TypeError:
        message = "Ожидаются рациональные числа."
    except ZeroDivisionError:
        message = "На ноль делить нет смысла."
    except ArithmeticError:
        message = "Вычислительно невозможное выражение"

    return result if result else message
