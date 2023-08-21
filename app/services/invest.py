from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation

MODEL_TYPES = Union[CharityProject, Donation]


def investment(
    target: MODEL_TYPES,
    sources: List[MODEL_TYPES]
) -> List[MODEL_TYPES]:
    list_modified = []
    if not target.invested_amount and target.invested_amount != 0:
        target.invested_amount = 0
    for source in sources:
        to_invest = target.full_amount - target.invested_amount
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        list_modified.append(source)
    return list_modified
