from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.services.user_services import InvalidToken,  UserNotFound, UserAlreadyExists

def apply_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidToken)
    def invalid_token_handler(request: Request, e: InvalidToken):
        return JSONResponse(
            status_code=401,
            content={"message": "Token provided is invalid"}
        )

    @app.exception_handler(UserNotFound)
    def user_not_found_handler(request: Request, e: UserNotFound):
        return JSONResponse(
            status_code=404,
            content={"message": f"User {e.user} does not exist"}
        )

    @app.exception_handler(UserAlreadyExists)
    def user_already_exists_handler(request: Request, e: UserAlreadyExists):
        return JSONResponse(
            status_code=401,
            content={"message": f"User {e.user_name} already exists"}
        )
