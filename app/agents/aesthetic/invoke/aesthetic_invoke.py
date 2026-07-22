# from langfuse import observe
from datetime import datetime, timezone
import time
from typing import Any

from app.agents.aesthetic.graph.aesthetic_graph import aesthetic_graph_app
from app.agents.aesthetic.state.aesthic_state import AestheticState


# @observe(name="aesthetic_agent")
async def AestheticInvoke(
    payload: AestheticState,
) -> dict[str, Any]:

    start_time = time.time()

    try:
        final_state = await aesthetic_graph_app.ainvoke(payload)

        return {
            "data": final_state,
            "_meta": {
                "status": "success",
                "duration_sec": round(
                    time.time() - start_time,
                    3,
                ),
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
        }

    except Exception as exc:
        return {
            "error": str(exc),
            "_meta": {
                "status": "failed",
                "duration_sec": round(
                    time.time() - start_time,
                    3,
                ),
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
        }