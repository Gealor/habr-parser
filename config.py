from pathlib import Path
from urllib.parse import urljoin
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env"],
        case_sensitive=False,
    )

    URL_HABR_BASE: str = "https://habr.com/ru/"

    URL_ARTICLES_TOP_DAILY: str = "articles/top/daily/"

    FILEPATH: Path = Path(__file__).parent / "articles.json"

    @property
    def URL_HABR(self):
        return urljoin(self.URL_HABR_BASE, self.URL_ARTICLES_TOP_DAILY)

settings = Settings()