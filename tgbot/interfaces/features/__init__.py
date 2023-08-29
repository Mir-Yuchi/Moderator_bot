from dataclasses import dataclass


@dataclass
class BotFeatureInfo:
    id: int
    name: str
    title: str


@dataclass
class FeatureSettings:
    on: bool
