from dataclasses import dataclass


@dataclass
class BotFeatureInfo:
    name: str
    title: str


@dataclass
class FeatureSettings:
    on: bool
