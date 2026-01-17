import random
import os
from urllib.parse import quote

from locust import HttpUser, task, between, events

from config import (
    BASE_URL,
    SEARCH_PATH,
    DEFAULT_HEADERS,
    MIN_WAIT_TIME,
    MAX_WAIT_TIME,
    INVALID_SEARCH_TERMS,
)


def load_search_terms() -> list[str]:
    csv_path = os.path.join(os.path.dirname(__file__), "search_terms.csv")
    search_terms = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            term = line.strip()
            if term:
                search_terms.append(term)
    return search_terms


SEARCH_TERMS = load_search_terms()
search_term_index = 0


def get_next_search_term() -> str:
    global search_term_index
    term = SEARCH_TERMS[search_term_index % len(SEARCH_TERMS)]
    search_term_index += 1
    return term


@events.quitting.add_listener
def on_quitting(environment, **kwargs):
    if environment.stats.total.fail_ratio > 0.01:
        environment.process_exit_code = 1


class N11SearchUser(HttpUser):
    host = BASE_URL
    wait_time = between(MIN_WAIT_TIME, MAX_WAIT_TIME)

    def on_start(self):
        self.client.get("/", headers=DEFAULT_HEADERS, name="Homepage")

    @task(5)
    def search_product(self):
        search_term = get_next_search_term()
        encoded_term = quote(search_term)

        with self.client.get(
            f"{SEARCH_PATH}?q={encoded_term}",
            headers=DEFAULT_HEADERS,
            catch_response=True,
            name="Search - Basic",
        ) as response:
            self._validate_search_response(response, search_term)

    @task(2)
    def search_with_pagination(self):
        search_term = get_next_search_term()
        encoded_term = quote(search_term)

        with self.client.get(
            f"{SEARCH_PATH}?q={encoded_term}",
            headers=DEFAULT_HEADERS,
            catch_response=True,
            name="Search - Page 1",
        ) as response:
            if not self._validate_search_response(response, search_term):
                return

        with self.client.get(
            f"{SEARCH_PATH}?q={encoded_term}&pg=2",
            headers=DEFAULT_HEADERS,
            catch_response=True,
            name="Search - Page 2 (Pagination)",
        ) as response:
            self._validate_search_response(response, search_term, page=2)

    @task(1)
    def search_invalid_term(self):
        invalid_term = random.choice(INVALID_SEARCH_TERMS)
        encoded_term = quote(invalid_term)

        with self.client.get(
            f"{SEARCH_PATH}?q={encoded_term}",
            headers=DEFAULT_HEADERS,
            catch_response=True,
            name="Search - Invalid Term",
        ) as response:
            if response.status_code >= 500:
                response.failure(f"Server error: {response.status_code}")
            else:
                response.success()

    def _validate_search_response(
        self, response, search_term: str, page: int = 1
    ) -> bool:
        if response.status_code != 200:
            response.failure(f"Status {response.status_code} for: {search_term}")
            return False

        if not response.text:
            response.failure(f"Empty response for: {search_term}")
            return False

        if "q=" not in response.url:
            response.failure(f"Missing search param in URL: {response.url}")
            return False

        content_indicators = [
            "columnContent",
            "searchResultList",
            "productItem",
            "resultCount",
        ]

        has_content = any(ind in response.text for ind in content_indicators)

        if has_content:
            response.success()
        else:
            response.failure(f"No search results found for: {search_term}")
            return False

        return True
