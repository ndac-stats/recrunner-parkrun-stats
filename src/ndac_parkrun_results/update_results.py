"""Fetch public parkrun athlete histories and publish a small JSON snapshot.
"""
from datetime import date
import json
from pathlib import Path
import random
import time
from typing import Any

from bs4 import BeautifulSoup
from loguru import logger
import requests

from parkrun_types import Parkrunner, ParkrunResult

ROOT = Path(__file__).resolve().parents[2]
ATHLETES_FILE = ROOT / "data" / "athletes.json"
RESULTS_FILE = ROOT / "data" / "results.json"
BASE_URL = "https://www.parkrun.com.au/parkrunner"
BASE_URL_SUFFIX = "all"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
}

def read_athletes() -> list[Parkrunner]:
    """Read and return list of athletes

    Returns:
        athletes (list[Parkrunner]): list of athlete data
    """
    athletes = []

    with ATHLETES_FILE.open(mode="r", encoding="utf-8") as athlete_fp:
        data = json.load(athlete_fp)
        for record in data["runners"]:
            athlete = Parkrunner.from_dict(record)
            athletes.append(athlete)

    return athletes

def extract_results_from_page(soup: BeautifulSoup) -> list[list[str]]:
    """Find the results table and extract the list of results

    Args:
        soup (BeautifulSoup): The athlete's results page

    Returns:
        results (list[list[str]]): rows of athlete results
    """
    results = []
    
    # find all tables on the page
    tables = soup.find_all("table")
    if not len(tables):
        logger.warning("Did not find any <table> tags")

    for table in tables:
        # find tables which have a caption tag
        caption = table.find("caption")
        # only inspect those captions which contain the word 'result' (case insensitive)
        if caption and "result" in caption.text.lower():
            # iterate over each row of the table
            for row in table.find_all("tr"):
                # iterate over each cell within the row
                cells = row.find_all("td")

                if cells:
                    results.append([cell.get_text(" ", strip=True) for cell in cells])

    return results

def parse_results(soup: BeautifulSoup) -> list[ParkrunResult]:
    """Extract the list of results from an athlete's results page

    Args:
        soup (BeautifulSoup): The BeautifulSoup representation of the athlete"s results page

    Returns:
        results (list[ParkrunResult]): list of athlete's results data
    """
    results = []

    result_columns = ["Event", "Run Date", "Run Number", "Pos", "Time", "Age Grade", "PB?"]

    table_data = extract_results_from_page(soup)

    for row in table_data:
        result = ParkrunResult(
            parkrun_id="123", # TODO: test if it can be left blank and populated later
            event=row[result_columns.index("Event")],
            run_date=date(2026, 12, 1),#row[result_columns.index("Run Date")], # TODO: convert to date
            run_number=row[result_columns.index("Run Number")], # TODO: convert to int
            position=row[result_columns.index("Pos")],  # TODO: convert to int
            time_seconds=row[result_columns.index("Time")], # TODO: interpret time and convert to seconds
            age_grade=row[result_columns.index("Age Grade")],   # TODO: convert to float
            pb=row[result_columns.index("PB?")] # TODO: cast to boolean
        )
        results.append(result)

    return results

def fetch_athlete(session: requests.Session, athlete: Parkrunner) -> list[ParkrunResult]:
    """Requests the results page for a given athlete and extracts each result.

    Args:
        session (requests.Session): active requests session
        athlete (Parkrunner): athlete to retrieve results for

    Returns:
        results (list[ParkrunResult]): list of parkrun results for the athlete
    """
    url = f"{BASE_URL}/{athlete.parkrun_id}/{BASE_URL_SUFFIX}"
    logger.debug(f"{athlete.display_name} URL: {url}")
    response = session.get(url, timeout=35)
    logger.debug(f"Got {response.status_code} response for ID {athlete.parkrun_id} ({athlete.display_name}) request")

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    return parse_results(soup)

def update_athlete_results(new_results: dict[str, list[ParkrunResult]]) -> None:
    """Updates the results file with the provided, new results

    Args:
        new_results (dict[str, list[ParkrunResult]]): dictionary of parkrun ID to parkrun results
    """
    existing_results: dict[str, list[Any]]
    if RESULTS_FILE.exists():
        with RESULTS_FILE.open(mode="r", encoding="utf-8") as results_fp:
            existing_results = json.load(results_fp)
    else:
        existing_results = {}

    # Update only athletes returned by the latest scrape
    for athlete_id, results in new_results.items():
        existing_results[athlete_id] = []
        for result in results:
            existing_results[athlete_id].append(result.to_dict())

    # Save merged results
    with RESULTS_FILE.open(mode="w", encoding="utf-8") as results_fp:
        json.dump(existing_results, results_fp, indent=4, ensure_ascii=False)

    logger.success("Athlete results successfully updated.")

def main():
    athletes = read_athletes()
    if not athletes:
        raise SystemExit(f"No athlete IDs found in {ATHLETES_FILE}")

    session = requests.Session()
    session.headers.update(HEADERS)

    new_results: dict[str, list[ParkrunResult]] = {}
    failures: dict[str, str] = {}

    for index, athlete in enumerate(athletes):
        if not athlete.active:
            logger.info(f"Skipping {athlete.display_name} (inactive)")
            continue
        try:
            results = fetch_athlete(session, athlete)
            new_results[athlete.parkrun_id] = results
            logger.success(f"Fetched {athlete.parkrun_id} ({athlete.display_name}): {len(results)} results")

        except Exception as exc:
            failures[athlete.parkrun_id] = f"{athlete.parkrun_id}: {exc}"
            logger.exception(f"Failed to fetch athlete data for {athlete.parkrun_id} ({athlete.display_name}): {exc}")

        # A deliberate pause between requests to avoid hammering the site.
        if index < len(athletes) - 1:
            human_like_delay = 10 + random.randrange(2, 6) + random.random()
            logger.debug(f"Sleeping for {human_like_delay:.2f} seconds")
            time.sleep(human_like_delay)

    # Do not overwrite a previously good snapshot if every request failed.
    if not new_results:
        raise SystemExit("Every athlete request failed; existing data was left untouched.")

    update_athlete_results(new_results)

    logger.info("Results update complete")
    logger.info(f"Successfully updated {len(new_results)} results")
    if len(failures):
        logger.warning(f"Failed to update {len(failures)} results")
        logger.info("Summary of failures")
        for athlete_id, failure_reason in failures.items():
            logger.warning(f"ID {athlete_id}: {failure_reason}")


if __name__ == "__main__":
    main()