from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Data:
    name: str


@dataclass
class Config:
    tg_bot: TgBot
    database: Data


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN')),
                  database=Data(
        name=env('DATABASE_NAME'))
    )
