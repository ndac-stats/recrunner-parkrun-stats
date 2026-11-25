# Future Work

## To do
* improve HTTP error handling
* GitHub Actions for site deployment
* website interface
    * display of monthly report for newsletter
    * display of stats
    * UI for adding/removing active members
* parkrun regions (country, state)
* yellow top tracking
* transfer of existing stats

## Improve HTTP Error Handling
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)

    retry_strategy = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session

session = create_session()
```