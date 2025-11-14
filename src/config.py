import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_config(config_path: str = "config.json") -> dict:
    """
    Carga config.json si existe, si no, cae en config_example.json.
    """
    cfg_file = BASE_DIR / config_path
    if not cfg_file.exists():
        cfg_file = BASE_DIR / "config_example.json"

    with cfg_file.open("r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()

DATA_DIR = BASE_DIR / CONFIG["data_dir"]
DATOS_ALMACEN_PATH = DATA_DIR / CONFIG["datos_almacen_file"]
PREVISION_PATH = DATA_DIR / CONFIG["prevision_file"]
CLIENTES_PATH = DATA_DIR / CONFIG["clientes_file"]
TALLERES_PATH = DATA_DIR / CONFIG["talleres_file"]
EXPORT_DIR = BASE_DIR / CONFIG["export_dir"]
