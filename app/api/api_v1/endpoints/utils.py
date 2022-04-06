from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.services import user_services
from app.core.celery_app import celery_app
from app.utils import send_test_email

router = APIRouter()


# @router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
# def test_celery(
#     msg: schemas.Msg,
#     current_user: models.User = Depends(user_services.get_current_user),
# ) -> Any:
#     """
#     Test Celery worker.
#     """
#     celery_app.send_task("app.worker.test_celery", args=[msg.msg])
#     return {"msg": "Word received"}


# @router.post("/test-email/", response_model=schemas.Msg, status_code=201)
# def test_email(
#     email_to: EmailStr,
#     current_user: models.User = Depends(user_services.get_current_user),
# ) -> Any:
#     """
#     Test emails.
#     """
#     send_test_email(email_to=email_to)
#     return {"msg": "Test email sent"}
