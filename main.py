import logging
import httpx

from openai import OpenAI
from dotenv import dotenv_values

from gpts import GPT
from classification import Classifier
from utils import read_from_file, fetch_html, save_results_to_file


config = dotenv_values(".env")


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    """
    Основная точка входа в программу:
    1) Считывает список сайтов из txt-файла (sites.txt).
    2) Получает HTML-страницы.
    3) Классифицирует каждую страницу через GPT.
    4) Сохраняет результат в results.txt.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Допустим, ключ OpenAI API берем из переменной окружения
    openai_api_key = config["OPENAI_API_KEY"]
    client_openai = OpenAI(api_key=openai_api_key)

    # Инициализация GPT-клиента
    gpt_client = GPT(model="gpt-3.5-turbo", client=client_openai)

    # Инициализация классификатора
    classifier = Classifier(gpt_client)

    # Пути к входному и выходному файлам
    input_file = "files/sites.txt"
    output_file = "files/results.txt"

    # Считываем URL-ы
    sites = read_from_file(input_file)
    results = []

    # Один httpx.Client для всех запросов
    with httpx.Client() as httpx_client:
        for site in sites:
            html_content = fetch_html("https://r.jina.ai/" + site, httpx_client)
            classification = classifier.classify_html_content(html_content)
            results.append((site, classification))
            logging.info(f"Сайт: {site} -> {classification}")

    # Сохраняем результаты
    save_results_to_file(results, output_file)


if __name__ == "__main__":
    main()
