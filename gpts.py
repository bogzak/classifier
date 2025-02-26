import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class GPT:
    def __init__(self, model: str, client) -> None:
        self.model = model
        self.client = client

    def get_response(self, message: str) -> str | None:
        try:
            completion = self.client.chat.completion.create(
                model=self.model,
                message=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as ex:
            logging.error(f"Error getting response: {ex}")
            return None

    def bulk_response(self, message_temp: str, prompt_parts: list) -> tuple:
        message = message_temp.format(*prompt_parts)
        try:
            response = self.get_response(message)
            return prompt_parts, response
        except Exception as ex:
            logging.error(f"Error in bulk_response: {ex}")
            return prompt_parts, None
