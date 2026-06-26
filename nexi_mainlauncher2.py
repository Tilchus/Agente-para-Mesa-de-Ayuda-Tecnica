import time
import config_inicial2 
import gestor_datos_determinista2

def procesar_interaccion(nexi, consulta, es_reintento=False):
    # Agregamos la consulta al historial local del agente
    nexi.historial_bolsa.append(f"Usuario: {consulta}")
    
    try:
        if nexi.intentos < config_inicial2.MAX_INTENTOS:
            nexi.intentos += 1
            
            # --- CAMBIO DEFINITIVO: Usamos el método nativo del chat ---
            # Esto usa la configuración (temp 0.2, instructions) que ya tiene el agente
            response = nexi.chat.send_message(consulta)
            
            texto_nexi = response.text
            nexi.historial_bolsa.append(f"NEXI: {texto_nexi}")
            
            # --- Lógica de escalado (Manteniendo tu lógica original) ---
            if "ESCALAR" in texto_nexi.upper() or nexi.intentos >= config_inicial2.MAX_INTENTOS:
                reporte = gestor_datos_determinista2.ejecutar_escalado_determinista(nexi.historial_bolsa, nexi.client)
                
                # Reseteo del agente
                nexi.intentos = 0
                nexi.historial_bolsa = []
                nexi.resetear_chat() # Limpiamos el chat para la próxima sesión
                
                return f"Ticket escalado exitosamente.{reporte}"
            
            return texto_nexi
            
        else:
            # Caso de seguridad (Límite alcanzado)
            reporte = gestor_datos_determinista2.ejecutar_escalado_determinista(nexi.historial_bolsa, nexi.client)
            nexi.intentos = 0
            nexi.historial_bolsa = []
            nexi.resetear_chat()
            return f"[SISTEMA]: Límite alcanzado.{reporte}"
            
    except Exception as e:
        if "429" in str(e) or "503" in str(e):
            if not es_reintento:
                time.sleep(5)
                return procesar_interaccion(nexi, consulta, True)
            return "[SISTEMA]: Capacidad diaria alcanzada."
        return f"[Error técnico]: {str(e)}"

