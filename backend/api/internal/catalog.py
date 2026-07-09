from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/internal/catalog", tags=["catalog"])

@router.get("/countries")
async def api_get_countries():
    from services.esim_provider import AVAILABLE_COUNTRIES, COUNTRY_NAMES
    return {"countries": AVAILABLE_COUNTRIES, "names": COUNTRY_NAMES}

@router.get("/plans/{country_code}")
async def api_get_plans_by_country(country_code: str):
    from services.esim_provider import get_plans_by_country
    return get_plans_by_country(country_code)

@router.get("/plan/{plan_id}")
async def api_get_plan(plan_id: str):
    from services.esim_provider import get_plan_by_id
    plan = get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan
