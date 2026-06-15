from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail

        message = detail.get("message") if isinstance(detail, dict) else str(detail)

        payload = {
            "error": {
                "status_code": exc.status_code,
                "message": message,
            }
        }

        return JSONResponse(
            status_code=exc.status_code,
            content=payload,
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        if exc.status_code == 404:
            payload = {
                "error": {
                    "status_code": 404,
                    "message": "Not Found",
                }
            }
            return JSONResponse(status_code=404, content=payload)

        payload = {
            "error": {
                "status_code": exc.status_code,
                "message": str(exc.detail),
            }
        }

        return JSONResponse(status_code=exc.status_code, content=payload)

    # -------------------------------------------------
    # Validation Errors (422)
    # -------------------------------------------------
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        first_error = exc.errors()[0]

        payload = {
            "error": {
                "status_code": 422,
                "message": first_error.get("msg", "Validation error"),
            }
        }

        return JSONResponse(status_code=422, content=payload)

    # -------------------------------------------------
    # Unhandled Errors (500)
    # -------------------------------------------------
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        payload = {
            "error": {
                "status_code": 500,
                "message": "Internal server error",
            }
        }

        return JSONResponse(status_code=500, content=payload)
