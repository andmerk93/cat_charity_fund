from datetime import datetime


def investment(
    target,
    sources
):
    list_modified = []
    if not target.invested_amount:
        target.invested_amount = 0
    for source in sources:
        to_invest = min(target.full_amount - target.invested_amount,
                        source.full_amount - source.invested_amount)
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
            list_modified.append(obj)
    return list_modified
