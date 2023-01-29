import openai
openai.api_key = "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"


def resposta_chat_gpt(pergunta: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=pergunta,
        max_tokens=1024
    )
    resultado = response["choices"][0]["text"].replace("\n", " ")
    return resultado
