import logging


logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


class Classifier:
    def __init__(self, gpt_client):
        self.gpt_client = gpt_client

    def classify_html_content(self, html_content: str) -> str:
        if not html_content:
            return "Не удалось получить контент"

        prompt = (
            "Определи, к какому типу относится сайт на основе полного HTML:\n"
            "1) Сайт-агрегатор\n"
            "2) Коммерческий сайт компании\n"
            "3) Информационный сайт\n\n"
            "HTML:\n"
            f"{html_content}\n\n"
            "Ответь одной фразой, без лишних объяснений. "
            "Должен быть один из вариантов: "
            "Сайт-агрегатор, Коммерческий сайт компании, или Информационный сайт."
        )

        response = self.gpt_client.get_response(prompt)
        if response is None:
            return "Ошибка при классификации"

        return response.strip()
