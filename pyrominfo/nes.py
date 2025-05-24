# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from rominfo import RomInfoParser

class NESParser(RomInfoParser):
    """
    Parse a NES image. Valid extensions are nes, unf.
    NES file format documentation and related source code:
    * http://nesdev.com/neshdr20.txt
    * http://wiki.nesdev.com/w/index.php/INES
    * http://codef00.com/unif_cur.txt
    * nes_slot.c of the MAME project:
    * http://git.redump.net/mame/tree/src/mess/machine/nes_slot.c
    """

    def get_valid_extensions(self):
        return ["nes", "unf"]

    def parse(self, filename):
        props = {}
        with open(filename, "rb") as f:
            data = bytearray(f.read())
            if self.is_valid_data(data):
                props = self.parse_buffer(data)
        return props

    def is_valid_data(self, data):
        if len(data) >= 16:
            if data[0:4] == b"NES\x1a":
                return True
            if data[0:4] == b"UNIF":
                return True
        return False

    def parse_buffer(self, data):
        props = {}
        if data[0:4] == b"NES\x1a":
            # NES format
            props["header"] = "NES"
            props["trainer"] = "yes" if data[6] & 0x04 else ""
            props["battery"] = "yes" if data[6] & 0x02 else ""
            props["four_screen_vram"] = "yes" if data[6] & 0x08 else ""
            props["video_output"] = "PAL" if data[9] & 0x01 else "NTSC"
            props["title"] = self._sanitize(data[0x0a:0x0a + 16])
        elif data[0:4] == b"UNIF":
            # UNIF format
            props["header"] = "UNIF"
            props["trainer"] = ""
            props["battery"] = ""
            props["four_screen_vram"] = ""
            props["video_output"] = ""
            props["title"] = self._sanitize(data[0x0a:0x0a + 16])
        return props

RomInfoParser.registerParser(NESParser())
