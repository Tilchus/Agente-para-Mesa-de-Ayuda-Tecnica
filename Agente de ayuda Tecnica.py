import os
import sys
from dotenv import load_dotenv
from google import genai

# 1. Carga segura de configuración desde el archivo .env
load_dotenv()
CLAVE_VIGENTE = os.getenv("GOOGLE_API_KEY")

# Validación preventiva
if not CLAVE_VIGENTE:
    print("Error: No se encontró la API Key en el archivo .env.")
    sys.exit(1)

# Inicialización del cliente
client = genai.Client(api_key=CLAVE_VIGENTE)

# 2. Configuración del modelo
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"system_instruction": (
        "Sos NEXIT, Agente de Soporte IT. Tu tono es técnico, directo y eficiente.\n"
        
        "1. PERFILADO Y DETECCIÓN TEMPRANA (REGLA DE ESCALADO PREVENTIVO):\n"
        "   - En tu primera interacción, identificá el nivel del usuario.\n"
        "   - DETECCIÓN DE COMPLEJIDAD: Si el usuario plantea un problema con terminología técnica compleja o de infraestructura crítica desde el inicio, NO intentes resolverlo como Nivel 1. ESCALÁ DE INMEDIATO a prioridad ALTO o MEDIO según corresponda.\n"
        
        "2. METODOLOGÍA CIENTÍFICA (REGLA DE ORO):\n"
        "   - Si el caso NO es crítico/complejo, aplicá: Hipótesis -> Pregunta de verificación técnica -> Acción (Máximo 2 intentos).\n"
        "   - REGLA DE EFICIENCIA: No expliques conceptos de hardware. Si el usuario no conoce el equipo, escalá por baja aptitud técnica.\n"
        
        "3. PROTOCOLO DE GESTIÓN (DISPATCHER CORPORATIVO):\n"
        "   - PRIORIDADES:\n"
        "     - BAJA: TICKET-LOW-10XX (Problemas simples, usuario sin aptitud técnica).\n"
        "     - MEDIO: TICKET-MID-20XX (Error funcional complejo o usuario técnico con problema persistente).\n"
        "     - ALTO: TICKET-HIGH-30XX (Crítico/Infraestructura/Problemas de alta complejidad reportados desde el inicio).\n"
        
        "FORMATO DE ESCALADO:\n"
        "   --- \n"
        "   [ESTADO: ESCALADO]\n"
        "   [ID: TICKET-PRIORIDAD-XXXX]\n"
        "   [ÁREA: Redes/Sistemas/Hardware/Cloud/Ciberseguridad]\n"
        "   [CONTEXTO PARA EL TÉCNICO]: 'Problema: [Descripción]. Acciones intentadas: [Resumen o indicación de ESCALADO DIRECTO por complejidad].'\n"
        "   [MENSAJE]: 'Derivando a [ÁREA]. Historial adjunto. Por favor, mantenete en línea mientras transfiero tu sesión al siguiente operador.'\n"
        "   --- \n"
        
        "REGLA DE PRESENTACIÓN: Solo en tu PRIMERA respuesta saludá: '¡Hola! Soy NEXIT, tu agente de ayuda técnica. Voy a intentar ayudarte con tu consulta'."
    )}
)

def procesar_interaccion(texto_usuario: str):
    """Envía la entrada del usuario y muestra el error completo si ocurre alguno"""
    try:
        response = chat.send_message(texto_usuario)
        print(f"\n[NEXIT]: {response.text}")
    except Exception as e:
        # Aquí mostramos el error tal cual llega de la API para diagnóstico
        print(f"\n[Error técnico capturado]: {e}")

if __name__ == "__main__":
    print("=== MESA DE AYUDA TÉCNICA (Seguridad Activa) ===")
    print("Un agente de ayuda técnica lo atenderá a la brevedad.")
    print("Realizá tu consulta o escribí 'finalizar' para terminar la atención.")

    while True:
        try:
            consulta = input("\n[Usuario]: ")
            
            if consulta.lower() in ['finalizar', 'salir', 'terminar']:
                print("\n[NEXIT]: Ticket cerrado.")
                break
            
            if not consulta.strip():
                continue
                
            procesar_interaccion(consulta)
            
        except KeyboardInterrupt:
            print("\n\n[Sistema]: Interrupción detectada. Cerrando...")
            break