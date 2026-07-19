from openai import AsyncOpenAI

class OpenAICorrector:
    def __init__(self, base_url: str, api_key: str, system_prompt: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        self.model = model

    async def correct_text(self, text: str):
        response = await self.client.responses.create(
            model=self.model,
            instructions=self.system_prompt,
            input=text,
            reasoning={"effort": "none"},
            text={"verbosity": "low"},
            store=False
        )

        return response.output_text
