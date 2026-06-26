import json, os, config_inicial2, random
from datetime import datetime

def generar_resumen_tecnico(historial, client):
    """Genera un resumen técnico usando el modelo."""
    prompt = "Resumí en 2 líneas este incidente técnico: " + " ".join(historial)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

def guardar_ticket_json(historial, area, prioridad, resumen):
    """Guarda el ticket en el archivo JSON especificado."""
    nuevo_ticket = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "area": area,
        "prioridad": prioridad,
        "resumen_tecnico": resumen,
        "transcripcion": historial
    }
    datos = []
    if os.path.exists(config_inicial2.ARCHIVO_TICKETS):
        with open(config_inicial2.ARCHIVO_TICKETS, "r", encoding="utf-8") as f:
            try: datos = json.load(f)
            except: datos = []
            
    datos.append(nuevo_ticket)
    
    with open(config_inicial2.ARCHIVO_TICKETS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def clasificar_area(texto_total):
    if any(k in texto_total for k in ["internet", "red", "conexión", "wifi"]):
        return "Redes y Conectividad"
    if any(k in texto_total for k in ["servidor", "cobros", "sistema"]):
        return "Sistemas Críticos"
    return "Microinformática"

def clasificar_prioridad(texto_total):
    if any(k in texto_total for k in ["urgente", "caído", "error 500", "no funciona"]):
        return "ALTA"
    if any(k in texto_total for k in ["consulta", "duda", "ayuda", "lento"]):
        return "BAJA"
    return "MEDIA"

def ejecutar_escalado_determinista(historial, client):
    texto_total = " ".join(historial).lower()
    
    # Clasificación
    area = clasificar_area(texto_total)
    prioridad = clasificar_prioridad(texto_total)
    
    # 1. Generamos el número de ticket aleatorio
    nro_ticket = f"NEXI-{random.randint(1000, 9999)}"
    
    # 2. Generación y guardado
    resumen = generar_resumen_tecnico(historial, client)
    guardar_ticket_json(historial, area, prioridad, resumen)
    
    # 3. Reporte visual con Prioridad y Nro de Ticket
    reporte = (
        f"\n{'='*50}\n"
        f"--- [ESTADO: TICKET ESCALADO] ---\n"
        f"Número de Ticket: {nro_ticket}\n"
        f"Area: {area}\n"
        f"Prioridad: {prioridad}\n"
        f"[CONTEXTO PARA EL TÉCNICO]\n"
        f"Problema: {resumen}\n"
        f"{'-' * 50}\n"
        f"MENSAJE: Derivando a soporte especializado. Historial adjunto.\n"
        f"Por favor, mantenerse en línea mientras transfiero su sesión.\n"
        f"{'=' * 50}\n"
    )
    return reporte
