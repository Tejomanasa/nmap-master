from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .curriculum import DISCLAIMER, LAB_TARGETS, MODULES
from .simulator import SimulationError, explain_results, module_by_id, required_module_for_command, simulate_nmap
from .store import ProgressStore

app = FastAPI(
    title="NMAP MASTER - OSINT with Tejo Manasa",
    version="1.0.0",
    description="Safe Nmap learning simulator for authorized cybersecurity education.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = ProgressStore()


class ScanRequest(BaseModel):
    command: str = Field(min_length=4, max_length=300)
    user_id: str = "demo"


class CompleteModuleRequest(BaseModel):
    module_id: int
    flag: str
    user_id: str = "demo"


@app.on_event("startup")
async def startup() -> None:
    await store.connect()


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "disclaimer": DISCLAIMER}


@app.get("/api/modules")
async def modules(user_id: str = Query("demo")) -> dict:
    progress = await store.get_progress(user_id)
    completed = set(progress["completed_modules"])
    enriched = []
    for module in MODULES:
        unlocked = module["id"] == 1 or module["id"] - 1 in completed
        enriched.append({**module, "locked": not unlocked, "completed": module["id"] in completed})
    return {"modules": enriched, "progress": progress, "disclaimer": DISCLAIMER}


@app.get("/api/modules/{module_id}")
async def get_module(module_id: int, user_id: str = Query("demo")) -> dict:
    progress = await store.get_progress(user_id)
    module = module_by_id(module_id)
    locked = module_id != 1 and module_id - 1 not in progress["completed_modules"]
    if locked:
        raise HTTPException(status_code=423, detail="This module is locked. Complete the previous module first.")
    return {"module": {**module, "locked": False, "completed": module_id in progress["completed_modules"]}, "progress": progress}


@app.post("/api/ethics/accept")
async def accept_ethics(user_id: str = "demo") -> dict:
    return {"progress": await store.accept_ethics(user_id), "disclaimer": DISCLAIMER}


@app.post("/api/scan")
async def scan(request: ScanRequest) -> dict:
    progress = await store.get_progress(request.user_id)
    if not progress["accepted_ethics"]:
        raise HTTPException(status_code=403, detail="Accept the educational and legal disclaimer before scanning.")
    try:
        required_module = required_module_for_command(request.command)
        if required_module > 1 and required_module - 1 not in progress["completed_modules"]:
            raise HTTPException(status_code=423, detail=f"This command belongs to Module {required_module}. Complete earlier modules first.")
        simulation = simulate_nmap(request.command)
    except SimulationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    await store.add_scan(simulation, request.user_id)
    return {"simulation": simulation, "assistant": explain_results(simulation)}


@app.post("/api/modules/complete")
async def complete_module(request: CompleteModuleRequest) -> dict:
    try:
        progress = await store.complete_module(request.module_id, request.flag, request.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"progress": progress}


@app.get("/api/targets")
async def targets() -> dict:
    return {"targets": LAB_TARGETS}


@app.post("/api/report")
async def report(user_id: str = "demo") -> dict:
    progress = await store.get_progress(user_id)
    return {
        "title": "NMAP MASTER - Simulated Reconnaissance Report",
        "scope": list(LAB_TARGETS.keys()),
        "disclaimer": DISCLAIMER,
        "xp": progress["xp"],
        "badges": progress["badges"],
        "evidence": progress.get("scan_history", []),
        "recommendations": [
            "Keep all scans within authorized lab scope.",
            "Prioritize remediation for unnecessary open services.",
            "Use XML or JSON evidence for repeatable reporting workflows.",
        ],
    }
