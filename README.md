PyRomInfo
========

PyRomInfo is a convenient, unified way to get data about a file originating from a read-only memory chip, often from a video game cartridge, a computer's firmware, or from an arcade game's main board.

Requirements
------------
- Python 3.10 or higher
- uv package manager (recommended) or pip

Installation
------------
Using uv (recommended):
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install pyrominfo
uv pip install pyrominfo
```

Using pip:
```bash
pip install pyrominfo
```

Development Installation
----------------------
```bash
# Clone the repository
git clone https://github.com/yourusername/pyrominfo.git
cd pyrominfo

# Install development dependencies
uv pip install -r requirements.txt

# Install in editable mode
uv pip install -e .
```

Usage
-----
Basic usage in Python:
```python
# Import Gameboy support and parse a Gameboy ROM
from pyrominfo import RomInfo
from pyrominfo import gameboy
props = RomInfo.parse("Zelda.gb")
if props:
    print("Title:", props["title"])
    print("Publisher:", props["publisher"])

# Register all available ROM info parsers
from pyrominfo import *
props = RomInfo.parse("Super Smash Bros.n64")
props = RomInfo.parse("Super Mario Kart.smc")
```

Command-line Example
------------------
The package includes a command-line tool in the `examples` directory that demonstrates how to use the library:

```bash
# Make the script executable
chmod +x examples/parse_rom.py

# Parse a ROM file
./examples/parse_rom.py "path/to/your/rom.smc"
```

Example output:
```
ROM Information:
--------------------------------------------------
Cartridge Type: ROM+RAM+BATT
Memory Layout: LoROM
Platform: Super Nintendo
Publisher: Nintendo
Publisher Code: 0001
Region: USA/Canada
Rom Size: 4 Mbit
Rom Speed: SlowROM
Title: SUPER MARIOWORLD
Video Output: NTSC
Version: 00
--------------------------------------------------
```

Useful links
------------
* Enzyme: https://github.com/Diaoul/enzyme
* GuessIt: http://guessit.readthedocs.org
* Heimdall: https://github.com/topfs2/heimdall
* PyMediaInfo: https://github.com/paltman/pymediainfo
* Mutagen: https://code.google.com/p/mutagen
* Hachoir parser framework: https://pypi.python.org/pypi/hachoir-parser
* PS ISO Tool: https://github.com/CaptainCPS/PS_ISO_Tool/
