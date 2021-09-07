import json
from datetime import date, datetime
from typing import Any

import ujson
from starlette.responses import JSONResponse

__all__ = ["ExtendedJSONResponse"]


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()

        return ujson.dumps(o)


class ExtendedJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=CustomEncoder,
        ).encode("utf-8")
