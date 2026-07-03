import requests

from app.config.settings import (
    LLM_SERVER_PATH
)


class LLMService:

    def generate(
            self,
            prompt: str,
            n_predict: int = 512
    ) -> str:

        response = requests.post(
            f"{LLM_SERVER_PATH}/completion",
            json={
                "prompt": prompt,
                "temperature": 0.2,
                "n_predict": n_predict
            }
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        data = response.json()

        return self._clean_output(
            data["content"]
        )

    def _clean_output(
            self,
            content: str
    ) -> str:
        cleaned = content.strip()

        for prefix in [
            "Answer:",
            "Summary:"
        ]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[
                    len(prefix):
                ].strip()

        for marker in [
            "END OF ANSWER",
            "<|endoftext|>"
        ]:
            if marker in cleaned:
                cleaned = cleaned.split(
                    marker,
                    1
                )[0].strip()

        return cleaned
