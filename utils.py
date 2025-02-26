import logging
import httpx
from urllib.parse import urlparse


def read_from_file(input_file: str) -> list[str]:
    sites = []
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                url = line.strip()
                if url:
                    sites.append(validation_url(url))
    except Exception as ex:
        logging.error(f"Error reading file {input_file}: {ex}")

    return sites


def fetch_html(url: str, client: httpx.Client) -> str:
    try:
        response = client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.text
    except Exception as ex:
        logging.error(f"Error fetching {url}: {ex}")
        return ""


def save_results_to_file(result: list, output_file: str):
    with open(output_file, "w", encoding="utf-8") as file:
        for site, classification in result:
            file.write(f"{site},{classification}\n")


def validation_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        return "http://" + url
    return url
