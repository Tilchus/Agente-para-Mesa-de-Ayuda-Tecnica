import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
ARCHIVO_TICKETS = r"C:\Users\Sil_Tech\Desktop\Proyecto_AgenteNexi_Modularizado\historial_tickets.json"
MAX_INTENTOS = 3

