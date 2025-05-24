# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from typing import Dict, Any, List, Type
import os

class RomInfoParser:
    _parsers: List[Type['RomInfoParser']] = []

    @classmethod
    def register_parser(cls, parser: 'RomInfoParser') -> None:
        cls._parsers.append(parser)

    @classmethod
    def get_parsers(cls) -> List['RomInfoParser']:
        return cls._parsers

    def get_valid_extensions(self) -> List[str]:
        return []

    def is_valid_extension(self, ext: str) -> bool:
        return ext.lower() in self.get_valid_extensions()

    def is_valid_data(self, data: bytes) -> bool:
        return False

    def parse(self, filename: str) -> Dict[str, Any]:
        return {}

    def parse_buffer(self, data: bytes) -> Dict[str, Any]:
        return {}

    def _get_extension(self, filename: str) -> str:
        return os.path.splitext(filename)[1].lower().lstrip('.')

class RomInfo(object):
    @staticmethod
    def parse(filename: str) -> Dict[str, Any]:
        ext = None
        for parser in RomInfoParser.get_parsers():
            if not ext:
                ext = parser._get_extension(filename)
            if parser.is_valid_extension(ext):
                props = parser.parse(filename)
                if props and any(props):
                    return props
        return {}

    @staticmethod
    def parse_buffer(data: bytes) -> Dict[str, Any]:
        for parser in RomInfoParser.get_parsers():
            if parser.is_valid_data(data):
                props = parser.parse_buffer(data)
                if props and any(props):
                    return props
        return {}

# Import all parsers
from pyrominfo.gameboy import GameboyParser
from pyrominfo.gba import GBAParser
from pyrominfo.genesis import GenesisParser
from pyrominfo.mastersystem import MasterSystemParser
from pyrominfo.nes import NESParser
from pyrominfo.nintendo64 import Nintendo64Parser
from pyrominfo.snes import SNESParser
from pyrominfo.dreamcast import DreamcastParser

__all__ = [
    "RomInfo",
    "RomInfoParser",
    "gameboy",
    "gba",
    "genesis",
    "mastersystem",
    "nes",
    "nintendo64",
    "snes",
    "dreamcast",
]
