from pydantic import Field
from pydantic_settings import BaseSettings


class DataBaseSettings(BaseSettings):
    # дефолтные значения для кредов указываю в рамках допущения, что это тестовая задача)
    # в идеале их не должно быть в коде ни в каком виде
    user: str = Field(validation_alias="DB_USER", default="admin")
    password: str = Field(validation_alias="DB_PASS", default="admin")
    host: str = Field(validation_alias="DB_HOST", default="localhost")
    name: str = Field(validation_alias="DB_NAME", default="gpn")
    port: int = Field(validation_alias="DB_PORT", default=8503)
    echo: bool = Field(validation_alias="DB_ECHO", default=False)

    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )
