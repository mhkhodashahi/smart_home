import openai


class chat:

    def __init__(self):
        self.openai = openai
        self.openai.api_key = "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"

        self._model_engine = "text-davinci-003"

    def chat(self, prompt):
        try:
        # Generate a response
            completion = openai.Completion.create(
                engine=self._model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )

            response = completion.choices[0].text
            print(response)
        except Exception as err:
            print(err)
