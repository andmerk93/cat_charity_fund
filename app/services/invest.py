from datetime import datetime
from typing import List

from app.models.charity_basemodel import CharityBaseModel


def investment(
    target: CharityBaseModel,
    sources: List[CharityBaseModel]
) -> List[CharityBaseModel]:
    modified = []
    if not target.invested_amount and target.invested_amount != 0:
        target.invested_amount = 0
    for source in sources:
        to_invest = target.full_amount - target.invested_amount
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        modified.append(source)
        if target.fully_invested:
            break
    return modified
