import json
import os
from pathlib import Path
from typing import Any

from loguru import logger

from config import StorageConfig
from parkrun_types import ParkrunID, Parkrunner, ParkrunnerResultHistory


def read_athletes(config: StorageConfig) -> list[Parkrunner]:
    """Read and return list of athletes

    Args:
        config (StorageConfig): storage configuration

    Raises:
        SystemExit: Raised when no athlete IDs are found

    Returns:
        athletes (list[Parkrunner]): list of athlete data
    """
    athletes = []
    athletes_file = config.athletes_file

    with athletes_file.open(mode="r", encoding="utf-8") as athlete_fp:
        data = json.load(athlete_fp)
        for record in data["runners"]:
            athlete = Parkrunner.from_dict(record)
            athletes.append(athlete)

    if not athletes:
        raise SystemExit(f"No athlete IDs found in {athletes_file}")

    return athletes

def update_athlete_results(new_results: dict[ParkrunID, ParkrunnerResultHistory], config: StorageConfig) -> None:
    """Updates the results file with the provided, new results

    Args:
        new_results (dict[ParkrunID, ParkrunnerResultHistory]): dictionary of parkrun ID to parkrun results
        config (StorageConfig): storage configuration
    """
    existing_results: dict[ParkrunID, list[Any]]
    results_file = config.results_file

    if results_file.exists():
        with results_file.open(mode="r", encoding="utf-8") as results_fp:
            existing_results = json.load(results_fp)
    else:
        existing_results = {}

    # Update only athletes returned by the latest scrape
    for athlete_id, results in new_results.items():
        existing_results[athlete_id] = []
        for result in results:
            existing_results[athlete_id].append(result.to_dict())

    # Save merged results
    write_json_atomic(existing_results, results_file)

    logger.success(f"Athlete results successfully written to {results_file}")

def write_json_atomic(data: dict, filepath: Path) -> None:
    """Write JSON safely without risking the existing file.

    Args:
        data (dict): data to be written to file
        filepath (Path): file to write the data to
    """
    temp_file = filepath.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)

    os.replace(temp_file, filepath)
