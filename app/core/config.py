import logging
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class MariaDBDsn(AnyHttpUrl):
    allowed_schemes = {"mariadb+pymysql"}
    user_required = True
    host_required = True


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # TODO: validate this baseed on EMAILS_ENABLED or replace it with SMTP_HOST
    SERVER_HOST: Optional[AnyHttpUrl]
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "backend-boilerplate"
    SENTRY_DSN: Optional[HttpUrl] = None

    # TODO
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    # TODO: why can't these just work???
    # MARIADB_SERVER: str
    # MARIADB_USER: str
    # MARIADB_PASSWORD: str
    # MARIADB_DB: str

    SQLALCHEMY_DATABASE_URI: MariaDBDsn

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(
    #     cls, v: Optional[str], values: Dict[str, Any]
    # ) -> Any:
    #     logger.info("v is %s", v)
    #     logger.info("values  is %s", values)
    #     if isinstance(v, str):
    #         return v
    #     a = MariaDBDsn.build(
    #         scheme="mariad+pymysql",
    #         user=values.get("MARIADB_USER"),
    #         password=values.get("MARIADB_PASSWORD"),
    #         host=values.get("MARIADB_SERVER"),
    #         path=f"/{values.get('MARIADB_DB') or ''}",
    #     )
    #     logger.info("dsn is %s", a)
    #     return a

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, _: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings(_env_file="/vault/secrets/env")  # type: ignore
