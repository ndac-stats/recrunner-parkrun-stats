import requests

from bs4 import BeautifulSoup
from loguru import logger

from config import AppConfig, WebsiteConfig
from parkrun_types import Parkrunner, ParkrunnerResultHistory
from parser import parse_results


def create_session(config: WebsiteConfig) -> requests.Session:
    """Create a configured HTTP session

    Args:
        config (WebsiteConfig): website configuration

    Returns:
        requests.Session: an active and configured requests session
    """
    session = requests.Session()
    session.headers.update(config.headers)

    return session

def fetch_athlete(session: requests.Session, athlete: Parkrunner, config: AppConfig) -> ParkrunnerResultHistory:
    """Requests the results page for a given athlete and extracts each result.

    Args:
        session (requests.Session): active requests session
        athlete (Parkrunner): athlete to retrieve results for
        config (AppConfig): app configuration

    Returns:
        results (ParkrunnerResultHistory): list of parkrun results for the athlete
    """
    url = f"{config.website.base_url}/{athlete.parkrun_id}/{config.website.results_path}"
    logger.debug(f"{athlete.display_name} URL: {url}")
    response = session.get(url, timeout=config.website.timeout)
    logger.debug(f"Got {response.status_code} response for ID {athlete.parkrun_id} ({athlete.display_name}) request")

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    return parse_results(soup, athlete.parkrun_id, config.parsing)
