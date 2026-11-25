from datetime import datetime

from bs4 import BeautifulSoup
from loguru import logger

from parkrun_types import ParkrunID, ParkrunResult, ParkrunnerResultHistory


def parse_results(soup: BeautifulSoup, athlete_id: ParkrunID) -> ParkrunnerResultHistory:
    """Extract the list of results from an athlete's results page

    Args:
        soup (BeautifulSoup): The BeautifulSoup representation of the athlete"s results page
        athlete_id (ParkrunID): the athlete parkrun ID for the results being parsed

    Returns:
        results (ParkrunnerResultHistory): list of athlete's results data
    """
    results = []

    result_columns = ["Event", "Run Date", "Run Number", "Pos", "Time", "Age Grade", "PB?"]

    table_data = extract_results_from_page(soup)

    for row in table_data:
        if len(row) != len(result_columns):
            logger.warning(f"Skipping malformed result row for athlete {athlete_id}: {row}")
            continue

        try:
            result = ParkrunResult(
                parkrun_id=athlete_id,
                event=row[0],
                run_date=datetime.strptime(row[1], "%d/%m/%Y").date(),
                run_number=int(row[2]),
                position=int(row[3]),
                time_seconds=time_to_seconds(row[4]),
                age_grade=float(row[5][:-1]) / 100,
                pb=True if "PB" in row[6] else False
            )
            results.append(result)
        except (ValueError, TypeError) as exc:
            logger.warning(f"Could not parse result for athlete {athlete_id}: {row}. {exc}")

    return results

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

def time_to_seconds(run_time: str) -> int:
    """Convert a result time to seconds

    Args:
        run_time (str): Athlete's time in mm:ss or hh:mm:ss format

    Raises:
        ValueError: Raised when format of `run_time` is not mm:ss or hh:mm:ss

    Returns:
        seconds: Athlete's time in seconds
    """
    parts = list(map(int, run_time.split(":")))

    if len(parts) == 2:  # mm:ss
        minutes, seconds = parts
        return minutes * 60 + seconds

    elif len(parts) == 3:  # hh:mm:ss
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds

    else:
        raise ValueError("Time must be in mm:ss or hh:mm:ss format")
