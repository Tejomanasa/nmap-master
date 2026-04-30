from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:  # pragma: no cover - optional dependency in local docs mode
    AsyncIOMotorClient = None

from .curriculum import BADGES_BY_LEVEL, MODULES


def _default_progress() -> dict[str, Any]:
    return {
        "user_id": "demo",
        "accepted_ethics": False,
        "completed_modules": [],
        "xp": 0,
        "badges": [],
        "level": 1,
        "scan_history": [],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@dataclass
class ProgressStore:
    mongo_uri: str | None = None
    db_name: str = "nmap_master"
    memory: dict[str, dict[str, Any]] = field(default_factory=dict)
    client: Any = None

    async def connect(self) -> None:
        self.mongo_uri = self.mongo_uri or os.getenv("MONGO_URI")
        if self.mongo_uri and AsyncIOMotorClient:
            self.client = AsyncIOMotorClient(self.mongo_uri)

    def _collection(self):
        if not self.client:
            return None
        return self.client[self.db_name]["progress"]

    async def get_progress(self, user_id: str = "demo") -> dict[str, Any]:
        collection = self._collection()
        if collection is not None:
            found = await collection.find_one({"user_id": user_id}, {"_id": 0})
            if found:
                return found
        progress = self.memory.get(user_id) or _default_progress()
        progress["user_id"] = user_id
        self.memory[user_id] = progress
        return progress

    async def save_progress(self, progress: dict[str, Any]) -> dict[str, Any]:
        progress["updated_at"] = datetime.now(timezone.utc).isoformat()
        collection = self._collection()
        if collection is not None:
            await collection.update_one({"user_id": progress["user_id"]}, {"$set": progress}, upsert=True)
        self.memory[progress["user_id"]] = progress
        return progress

    async def accept_ethics(self, user_id: str = "demo") -> dict[str, Any]:
        progress = await self.get_progress(user_id)
        progress["accepted_ethics"] = True
        return await self.save_progress(progress)

    async def add_scan(self, simulation: dict[str, Any], user_id: str = "demo") -> dict[str, Any]:
        progress = await self.get_progress(user_id)
        progress.setdefault("scan_history", []).insert(0, {
            "command": simulation["command"],
            "target": simulation["target"],
            "module_id": simulation["module_id"],
            "findings": simulation["findings"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        progress["scan_history"] = progress["scan_history"][:20]
        return await self.save_progress(progress)

    async def complete_module(self, module_id: int, flag: str, user_id: str = "demo") -> dict[str, Any]:
        progress = await self.get_progress(user_id)
        module = next((item for item in MODULES if item["id"] == module_id), None)
        if not module:
            raise ValueError("Unknown module.")
        expected_flags = set(module["challenge"]["answer_flags"])
        if flag.strip() not in expected_flags:
            raise ValueError("Incorrect flag for this challenge.")
        if module_id > 1 and module_id - 1 not in progress["completed_modules"]:
            raise ValueError("Complete the previous module first.")
        if module_id not in progress["completed_modules"]:
            progress["completed_modules"].append(module_id)
            progress["xp"] += module["challenge"]["xp"]
            badge = module["challenge"]["badge"]
            if badge not in progress["badges"]:
                progress["badges"].append(badge)
        progress["level"] = min(4, 1 + progress["xp"] // 500)
        level_badge = BADGES_BY_LEVEL.get(progress["level"])
        if level_badge and level_badge not in progress["badges"]:
            progress["badges"].append(level_badge)
        return await self.save_progress(progress)

    async def reset(self, user_id: str = "demo") -> dict[str, Any]:
        progress = _default_progress()
        progress["user_id"] = user_id
        return await self.save_progress(progress)
