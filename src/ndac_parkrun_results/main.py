"""Fetch public parkrun athlete histories and publish a small JSON snapshot.
"""
import random
import time

from loguru import logger

from parkrun_types import ParkrunResult
from scraper import create_session, fetch_athlete
from storage import read_athletes, update_athlete_results

def main():
    athletes = read_athletes()
    session = create_session()

    active_athletes = []
    for athlete in athletes:
        if athlete.active:
            active_athletes.append(athlete)
        else:
            logger.info(f"Skipping {athlete.display_name} (inactive)")

    new_results: dict[str, list[ParkrunResult]] = {}
    failures: dict[str, str] = {}

    try:
        for index, athlete in enumerate(active_athletes):
            try:
                results = fetch_athlete(session, athlete)
                new_results[athlete.parkrun_id] = results
                logger.success(f"Fetched {athlete.parkrun_id} ({athlete.display_name}): {len(results)} results")

            except Exception as exc:
                failures[athlete.parkrun_id] = f"{athlete.parkrun_id}: {exc}"
                logger.exception(f"Failed to fetch athlete data for {athlete.parkrun_id} ({athlete.display_name}): {exc}")

            # A deliberate pause between requests to avoid hammering the site.
            if index < len(active_athletes) - 1:
                human_like_delay = 10 + random.randrange(2, 6) + random.random()
                logger.debug(f"Sleeping for {human_like_delay:.2f} seconds")
                time.sleep(human_like_delay)
    finally:
        session.close()

    # Do not overwrite a previously good snapshot if every request failed.
    if not new_results:
        raise SystemExit("Every athlete request failed; existing data was left untouched.")

    update_athlete_results(new_results)

    logger.info("Results update complete")
    logger.info(f"Successfully updated results for {len(new_results)} athlete(s)")
    if failures:
        logger.warning(f"Failed to update results for {len(failures)} athlete(s)")
        logger.info("Summary of failures")
        for athlete_id, failure_reason in failures.items():
            logger.warning(f"ID {athlete_id}: {failure_reason}")


if __name__ == "__main__":
    main()