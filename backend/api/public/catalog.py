from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/catalog", tags=["catalog"])

@router.get("/countries")
async def api_get_countries():
    from services.esim_provider import get_celitech_destinations, get_esimaccess_destinations, AVAILABLE_COUNTRIES, COUNTRY_NAMES
    from config import config
    
    if config.ESIM_PROVIDER == "celitech":
        destinations = await get_celitech_destinations()
        names = {d: d for d in destinations}
        return {"countries": destinations, "names": names}
    elif config.ESIM_PROVIDER == "esimaccess":
        destinations = await get_esimaccess_destinations()
        names = {d: d for d in destinations}
        return {"countries": destinations, "names": names}
        
    return {"countries": AVAILABLE_COUNTRIES, "names": COUNTRY_NAMES}

@router.get("/plans/{country_code}")
async def api_get_plans_by_country(country_code: str):
    from services.esim_provider import get_plans_by_country
    return await get_plans_by_country(country_code)

@router.get("/plan/{plan_id}")
async def api_get_plan(plan_id: str):
    from services.esim_provider import get_plan_by_id
    plan = await get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan
