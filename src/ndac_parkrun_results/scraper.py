import requests

from bs4 import BeautifulSoup
from loguru import logger

from parkrun_types import Parkrunner, ParkrunnerResultHistory
from parser import parse_results

BASE_URL = "https://www.parkrun.com.au/parkrunner"
BASE_URL_SUFFIX = "all"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"
}

def create_session() -> requests.Session:
    """Create a configured HTTP session

    Returns:
        requests.Session: an active and configured requests session
    """
    session = requests.Session()
    session.headers.update(HEADERS)

    return session

def fetch_athlete(session: requests.Session, athlete: Parkrunner) -> ParkrunnerResultHistory:
    """Requests the results page for a given athlete and extracts each result.

    Args:
        session (requests.Session): active requests session
        athlete (Parkrunner): athlete to retrieve results for

    Returns:
        results (ParkrunnerResultHistory): list of parkrun results for the athlete
    """
    url = f"{BASE_URL}/{athlete.parkrun_id}/{BASE_URL_SUFFIX}"
    logger.debug(f"{athlete.display_name} URL: {url}")
    response = session.get(url, timeout=35)
    logger.debug(f"Got {response.status_code} response for ID {athlete.parkrun_id} ({athlete.display_name}) request")

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    return parse_results(soup, athlete.parkrun_id)
