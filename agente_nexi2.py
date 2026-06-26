from google import genai
import config_inicial2


class AgenteNexi:
    def __init__(self):
        self.client = genai.Client(api_key=config_inicial2.API_KEY)
        self.resetear_chat()
        self.historial_bolsa = []
        self.intentos = 0

    def resetear_chat(self):
        """Limpia el historial en la nube de Google completamente."""
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": (
                "Sos NEXI, Soporte IT. 1. Máximo 20 palabras. 2. Técnica y directa. "
                "3. Una pregunta por vez. 4. Si tras 3 intentos no se resuelve, decí 'ESCALAR'."
                "3. Si detectas una consulta de Nivel 2 o usuario avanzado (ej. configuración avanzada de servidores, "
                "   código, o infraestructura compleja), respondé estrictamente 'ESCALAR' para omitir los intentos. "
                ),
            "temperature": 0.2  # Valor bajo (cerca de 0) hace al modelo más determinista
            }
        )
        self.historial_bolsa = []
        self.intentos = 0



