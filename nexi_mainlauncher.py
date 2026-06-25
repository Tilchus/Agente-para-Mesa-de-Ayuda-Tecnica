import time
import config_inicial 
import gestor_datos_determinista

def procesar_interaccion(nexi, consulta, es_reintento=False):
    nexi.historial_bolsa.append(f"Usuario: {consulta}")
    contexto_actual = "\n".join(nexi.historial_bolsa)
    
    try:
        if nexi.intentos < config_inicial.MAX_INTENTOS:
            nexi.intentos += 1
            
            response = nexi.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contexto_actual,
                config={"system_instruction": (
                    "Sos NEXI, Soporte IT. Respondé breve (máx 20 palabras). "
                    "Si no se resuelve tras 3 intentos, decí 'ESCALAR'."
                )}
            )
            
            texto_nexi = response.text
            nexi.historial_bolsa.append(f"NEXI: {texto_nexi}")
            
            # --- Lógica de escalado con reporte ---
            if "ESCALAR" in texto_nexi.upper() or nexi.intentos >= config_inicial.MAX_INTENTOS:
                # Capturamos el string que devuelve tu nueva función
                reporte = gestor_datos_determinista.ejecutar_escalado_determinista(nexi.historial_bolsa, nexi.client)
                
                # Reseteo
                nexi.intentos = 0
                nexi.historial_bolsa = []
                
                # Retornamos el mensaje compuesto para que la GUI lo muestre en el chat
                return f"Ticket escalado exitosamente.{reporte}"
            
            return texto_nexi
            
        else:
            # Caso de seguridad
            reporte = gestor_datos_determinista.ejecutar_escalado_determinista(nexi.historial_bolsa, nexi.client)
            nexi.intentos = 0
            nexi.historial_bolsa = []
            return f"[SISTEMA]: Límite alcanzado.{reporte}"
            
    except Exception as e:
        if "429" in str(e) or "503" in str(e):
            if not es_reintento:
                time.sleep(5)
                return procesar_interaccion(nexi, consulta, True)
            return "[SISTEMA]: Capacidad diaria alcanzada."
        return f"[Error técnico]: {str(e)}"
