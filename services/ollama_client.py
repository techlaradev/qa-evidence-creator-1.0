import requests

def ollama_generate(prompt: str, model: str = "mistral:7b-instruct-instruct", timeout: int = 300) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )

        data = response.json()

        if "response" in data:
            return data["response"]
        elif "error" in data:
            return f"Erro do Ollama: {data['error']}"
        else:
            return str(data)

    except Exception as e:
        return f"Erro ao conectar com Ollama: {e}"
