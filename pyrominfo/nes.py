# Copyright (C) 2013 Garrett Brown
# See Copyright Notice in rominfo.py

from pyrominfo import RomInfoParser


class NESParser(RomInfoParser):
    """
    Parse a NES image. Valid extensions are nes, fds, nsf, nsfe, unif, unif.
    NES file format documentation and related source code:
    * http://nesdev.com/neshdr20.txt
    * http://wiki.nesdev.com/w/index.php/INES
    * http://codef00.com/unif_cur.txt
    * nes_slot.c of the MAME project:
    * http://git.redump.net/mame/tree/src/mess/machine/nes_slot.c
    """

    def get_valid_extensions(self):
        return ["nes", "fds", "nsf", "nsfe", "unif", "unif"]

    def parse(self, filename):
        props = {}
        with open(filename, "rb") as f:
            data = bytearray(f.read())
            if len(data):
                props = self.parse_buffer(data)
        return props

    def is_valid_data(self, data):
        if len(data):
            if data[0:4] == b"NES\x1a":
                return True
            # TODO: Need more conclusive tests
            return False
        return False

    def parse_buffer(self, romdata):
        props = {}
        if romdata[0:4] == b"NES\x1a":
            # NES 2.0 format
            if (romdata[7] & 0x0C) == 0x08:
                props["mapper"] = (
                    ((romdata[6] >> 4) & 0x0F)
                    | (romdata[7] & 0xF0)
                    | ((romdata[8] & 0x0F) << 8)
                )
                props["submapper"] = (romdata[8] >> 4) & 0x0F
                props["prg_rom_size"] = (
                    romdata[4] | ((romdata[9] & 0x0F) << 8)
                ) * 16384
                props["chr_rom_size"] = (romdata[5] | ((romdata[9] & 0xF0) << 4)) * 8192
                props["prg_ram_size"] = (
                    (64 << (romdata[10] & 0x0F)) if (romdata[10] & 0x0F) else 0
                )
                props["chr_ram_size"] = (
                    (64 << (romdata[10] >> 4)) if (romdata[10] >> 4) else 0
                )
                props["tv_system"] = "PAL" if (romdata[12] & 0x01) else "NTSC"
                props["vs_ppu"] = (
                    "RP2C03B"
                    if (romdata[13] == 0x01)
                    else (
                        "RP2C03G"
                        if (romdata[13] == 0x02)
                        else (
                            "RP2C04-0001"
                            if (romdata[13] == 0x03)
                            else (
                                "RP2C04-0002"
                                if (romdata[13] == 0x04)
                                else (
                                    "RP2C04-0003"
                                    if (romdata[13] == 0x05)
                                    else (
                                        "RP2C04-0004"
                                        if (romdata[13] == 0x06)
                                        else (
                                            "RC2C03B"
                                            if (romdata[13] == 0x07)
                                            else (
                                                "RC2C03C"
                                                if (romdata[13] == 0x08)
                                                else (
                                                    "RC2C05-01"
                                                    if (romdata[13] == 0x09)
                                                    else (
                                                        "RC2C05-02"
                                                        if (romdata[13] == 0x0A)
                                                        else (
                                                            "RC2C05-03"
                                                            if (romdata[13] == 0x0B)
                                                            else (
                                                                "RC2C05-04"
                                                                if (romdata[13] == 0x0C)
                                                                else (
                                                                    "RC2C05-05"
                                                                    if (
                                                                        romdata[13]
                                                                        == 0x0D
                                                                    )
                                                                    else ""
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
                props["vs_hardware"] = (
                    "VS Unisystem"
                    if (romdata[13] & 0x01)
                    else "VS DualSystem"
                    if (romdata[13] & 0x02)
                    else ""
                )
                props["extended_console_type"] = (
                    "VS System"
                    if (romdata[7] & 0x01)
                    else (
                        "Playchoice 10"
                        if (romdata[7] & 0x02)
                        else (
                            "Extended Console Type"
                            if (romdata[7] & 0x03)
                            else "Regular NES/Famicom/Dendy"
                        )
                    )
                )
                props["misc_roms"] = romdata[11] & 0x03
                props["default_expansion_device"] = romdata[11] & 0x3C
            # iNES format
            else:
                props["mapper"] = (romdata[6] >> 4) | (romdata[7] & 0xF0)
                props["prg_rom_size"] = romdata[4] * 16384
                props["chr_rom_size"] = romdata[5] * 8192
                props["prg_ram_size"] = 8192 if (romdata[6] & 0x02) else 0
                props["tv_system"] = "PAL" if (romdata[9] & 0x01) else "NTSC"
                props["vs_ppu"] = (
                    "RP2C03B"
                    if (romdata[7] & 0x01)
                    else (
                        "RP2C03G"
                        if (romdata[7] & 0x02)
                        else (
                            "RP2C04-0001"
                            if (romdata[7] & 0x03)
                            else (
                                "RP2C04-0002"
                                if (romdata[7] & 0x04)
                                else (
                                    "RP2C04-0003"
                                    if (romdata[7] & 0x05)
                                    else (
                                        "RP2C04-0004"
                                        if (romdata[7] & 0x06)
                                        else (
                                            "RC2C03B"
                                            if (romdata[7] & 0x07)
                                            else (
                                                "RC2C03C"
                                                if (romdata[7] & 0x08)
                                                else (
                                                    "RC2C05-01"
                                                    if (romdata[7] & 0x09)
                                                    else (
                                                        "RC2C05-02"
                                                        if (romdata[7] & 0x0A)
                                                        else (
                                                            "RC2C05-03"
                                                            if (romdata[7] & 0x0B)
                                                            else (
                                                                "RC2C05-04"
                                                                if (romdata[7] & 0x0C)
                                                                else (
                                                                    "RC2C05-05"
                                                                    if (
                                                                        romdata[7]
                                                                        & 0x0D
                                                                    )
                                                                    else ""
                                                                )
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
                props["vs_hardware"] = (
                    "VS Unisystem"
                    if (romdata[7] & 0x01)
                    else "VS DualSystem"
                    if (romdata[7] & 0x02)
                    else ""
                )
                props["extended_console_type"] = (
                    "VS System"
                    if (romdata[7] & 0x01)
                    else (
                        "Playchoice 10"
                        if (romdata[7] & 0x02)
                        else (
                            "Extended Console Type"
                            if (romdata[7] & 0x03)
                            else "Regular NES/Famicom/Dendy"
                        )
                    )
                )
                props["misc_roms"] = 0
                props["default_expansion_device"] = 0
            props["mirroring"] = "Vertical" if (romdata[6] & 0x01) else "Horizontal"
            props["battery"] = "Yes" if (romdata[6] & 0x02) else "No"
            props["trainer"] = "Yes" if (romdata[6] & 0x04) else "No"
            props["four_screen"] = "Yes" if (romdata[6] & 0x08) else "No"
            props["region"] = "PAL" if (romdata[9] & 0x01) else "NTSC"
            props["vs_ppu"] = (
                "RP2C03B"
                if (romdata[7] & 0x01)
                else (
                    "RP2C03G"
                    if (romdata[7] & 0x02)
                    else (
                        "RP2C04-0001"
                        if (romdata[7] & 0x03)
                        else (
                            "RP2C04-0002"
                            if (romdata[7] & 0x04)
                            else (
                                "RP2C04-0003"
                                if (romdata[7] & 0x05)
                                else (
                                    "RP2C04-0004"
                                    if (romdata[7] & 0x06)
                                    else (
                                        "RC2C03B"
                                        if (romdata[7] & 0x07)
                                        else (
                                            "RC2C03C"
                                            if (romdata[7] & 0x08)
                                            else (
                                                "RC2C05-01"
                                                if (romdata[7] & 0x09)
                                                else (
                                                    "RC2C05-02"
                                                    if (romdata[7] & 0x0A)
                                                    else (
                                                        "RC2C05-03"
                                                        if (romdata[7] & 0x0B)
                                                        else (
                                                            "RC2C05-04"
                                                            if (romdata[7] & 0x0C)
                                                            else (
                                                                "RC2C05-05"
                                                                if (romdata[7] & 0x0D)
                                                                else ""
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
            props["vs_hardware"] = (
                "VS Unisystem"
                if (romdata[7] & 0x01)
                else "VS DualSystem"
                if (romdata[7] & 0x02)
                else ""
            )
            props["extended_console_type"] = (
                "VS System"
                if (romdata[7] & 0x01)
                else (
                    "Playchoice 10"
                    if (romdata[7] & 0x02)
                    else (
                        "Extended Console Type"
                        if (romdata[7] & 0x03)
                        else "Regular NES/Famicom/Dendy"
                    )
                )
            )
            props["misc_roms"] = 0
            props["default_expansion_device"] = 0
        return props


RomInfoParser.register_parser(NESParser())
