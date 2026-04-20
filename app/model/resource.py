##  Begin Standard Imports
import sys
from datetime import datetime
from configparser import ConfigParser
from pathlib import Path

CONST_ROOT_DIR:Path = Path.absolute(Path(sys.argv[0]).parent)
CONST_DATA_DIR:Path = Path.absolute(Path.joinpath(CONST_ROOT_DIR, r"data"))

# CONST_OUTPUT_DIR:Path = Path.absolute(Path.joinpath(CONST_ROOT_DIR, r"output"))
# CONST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def getDataFile(filename:str) -> Path:
    return Path.absolute(Path.joinpath(CONST_DATA_DIR, filename))

def generateTimestamp() -> str:
    result:str = datetime.now().strftime("%d%m%y-%H%M%S")
    return result