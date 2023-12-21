from __future__ import annotations

from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseSettings:
    """Настройки базы данных."""
    url: str

@dataclass
class TgBot:
    token: str   # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    database: DatabaseSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('BOT_TOKEN')),
        database=DatabaseSettings(url=env('DB_URL'))
    )
