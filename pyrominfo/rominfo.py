#
#     Copyright (C) 2013 Garrett Brown
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
# The Software may include Python modules derived from other works using
# different licensing terms. In such cases, the Python module is considered to
# be a separate work and is subject to the licensing terms declared at the
# beginning of that module.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List, Dict, Any

class RomInfoParser(object):
    """
    Base class for ROM info parsers. When an info parser subclasses this
    object, it can register itself with register_parser(), and
    pyrominfo.parse() will automatically include it when trying to parse a ROM
    file.
    """

    __parsers: List['RomInfoParser'] = []

    @staticmethod
    def register_parser(rom_info_parser: 'RomInfoParser') -> None:
        RomInfoParser.__parsers.append(rom_info_parser)

    @staticmethod
    def get_parsers() -> List['RomInfoParser']:
        return RomInfoParser.__parsers

    def __init__(self) -> None:
        pass

    def get_valid_extensions(self) -> List[str]:
        return []

    def is_valid_extension(self, ext: str) -> bool:
        return ext in self.get_valid_extensions()

    def parse(self, filename: str) -> Dict[str, Any]:
        return {}

    def is_valid_data(self, data: bytes) -> bool:
        return False

    def parse_buffer(self, data: bytes) -> Dict[str, Any]:
        return {}

    def _get_extension(self, uri: str) -> str:
        return uri[uri.rindex(".") + 1:].lower() if "." in uri else ""

    def _sanitize(self, title: bytes) -> str:
        """
        Turn all non-ASCII characters into spaces (tab, CR and LF line breaks
        are OK to preserve formatting), and then return a stripped string.
        """
        return ''.join(chr(b) if b in [ord('\t'), ord('\n'), ord('\r')] or \
                       0x20 <= b and b <= 0x7E else ' ' for b in title).strip()

    def _all_ascii(self, data: bytes) -> bool:
        return all(0x20 <= b and b <= 0x7E for b in data)
