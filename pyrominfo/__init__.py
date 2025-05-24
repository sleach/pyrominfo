# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from typing import Dict, Any
from rominfo import RomInfoParser

__all__ = [
    "RomInfo",
    "gameboy",
    "gba",
    "genesis",
    "mastersystem",
    "nes",
    "nintendo64",
    "snes",
]

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
