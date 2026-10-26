def business_case(benefit, upfront, run, years, rate):
    return {"npv": 0.0, "payback_years": None, "roi": 0.0}


def recommendation(case):
    return "revise"


case = business_case(benefit=420_000, upfront=600_000, run=80_000, years=3, rate=0.10)
print(case, recommendation(case))
