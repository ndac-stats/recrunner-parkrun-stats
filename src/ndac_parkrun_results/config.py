
from dataclasses import dataclass, field
from pathlib import Path


# Project paths
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


@dataclass(frozen=True)
class WebsiteConfig:
    base_url: str = "https://www.parkrun.com.au/parkrunner"
    results_path: str = "all"
    timeout: int = 35

    headers: dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
    })


@dataclass(frozen=True)
class RequestConfig:
    min_delay: float = 12.0
    max_delay: float = 16.0


@dataclass(frozen=True)
class StorageConfig:
    athletes_file: Path = DATA_DIR / "athletes.json"
    results_file: Path = DATA_DIR / "results.json"
    json_indent: int = 4
    ensure_ascii: bool = False


@dataclass(frozen=True)
class ParsingConfig:
    date_format: str = "%d/%m/%Y"


@dataclass(frozen=True)
class AppConfig:
    website: WebsiteConfig = field(default_factory=WebsiteConfig)
    requests: RequestConfig = field(default_factory=RequestConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    parsing: ParsingConfig = field(default_factory=ParsingConfig)


# Default application configuration
CONFIG = AppConfig()
