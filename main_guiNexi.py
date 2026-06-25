import tkinter as tk
from tkinter import scrolledtext
import threading
import nexi_mainlauncher 
from agente_nexi import AgenteNexi
from PIL import Image, ImageTk  # Importación necesaria para redimensionar

class AppNexiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXI- Soporte IT")
        self.root.geometry("500x650") 
        
        # 1. Estilo 
        self.estilos = {
            "bg": "#1e1e1e",
            "fg": "#d4d4d4",
            "accent": "#007acc",
            "chat_bg": "#252526"
        }
        self.root.configure(bg=self.estilos["bg"])

        # Inicializamos el agente
        self.nexi = AgenteNexi()

        # 2. Carga y redimensionamiento de imagen con PIL
        ruta_logo = r"C:\Users\Sil_Tech\Desktop\Proyecto_AgenteNexi_Modularizado\logo.png"
        imagen_original = Image.open(ruta_logo)
        # Redimensionamos a 150x150 imagen
        imagen_redimensionada = imagen_original.resize((150, 150), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(imagen_redimensionada)
        
        self.lbl_logo = tk.Label(root, image=self.logo, bg=self.estilos["bg"])
        self.lbl_logo.pack(pady=10)

        # Título del sistema
        self.lbl_title = tk.Label(root, text="### NEXI ###", font=("Arial", 16, "bold"), 
                                  bg=self.estilos["bg"], fg="white")
        self.lbl_title.pack(pady=5)

        # 3. Área de chat
        self.chat_area = scrolledtext.ScrolledText(
            root, state='disabled', wrap='word', 
            font=("Consolas", 10),
            bg=self.estilos["chat_bg"],
            fg=self.estilos["fg"],
            insertbackground="white",
            relief="flat"
        )
        # expand=True permite que el chat ocupe el espacio sobrante
        self.chat_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # 4.Estilo consola
        self.input_field = tk.Entry(
            root, font=("Arial", 12),
            bg=self.estilos["chat_bg"],
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.input_field.pack(padx=20, pady=15, fill=tk.X)
        self.input_field.bind("<Return>", self.enviar_mensaje)
        self.input_field.focus_set()

        self.mostrar_bienvenida()

    def mostrar_bienvenida(self):
        self.actualizar_chat("=== MESA DE AYUDA TÉCNICA (Seguridad Activa) ===\n"
                             "Un agente de ayuda técnica lo atenderá a la brevedad.")
        self.root.after(3500, self.saludo_nexi)

    def saludo_nexi(self):
        mensaje = ("\n[NEXI]: Hola, soy NEXI, agente de soporte IT. ¿En qué puedo asistirte hoy?\n"
                   "(Realiza tu consulta o escribí 'finalizar' para terminar la atención.)")
        self.actualizar_chat(mensaje)

    def actualizar_chat(self, mensaje):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, mensaje + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def enviar_mensaje(self, event=None):
        consulta = self.input_field.get().strip()
        if not consulta: return

        if consulta.lower() in ['finalizar', 'salir', 'terminar']:
            self.actualizar_chat(f"[Usuario]: {consulta}")
            self.actualizar_chat("[SISTEMA]: Sesión finalizada.")
            self.input_field.config(state='disabled')
            return
        
        self.actualizar_chat(f"[Usuario]: {consulta}")
        self.input_field.delete(0, tk.END)
        threading.Thread(target=self.procesar_logica, args=(consulta,), daemon=True).start()

    def procesar_logica(self, consulta):
        respuesta = nexi_mainlauncher.procesar_interaccion(self.nexi, consulta)
        if respuesta:
            self.actualizar_chat(f"[NEXI]: {respuesta}")
            señales_fin = ["escalado", "límite alcanzado", "finalizada", "intente más tarde"]
            if any(señal in respuesta.lower() for señal in señales_fin):
                self.input_field.config(state='disabled')
                self.actualizar_chat("[SISTEMA]: La sesión ha sido cerrada por seguridad.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppNexiGUI(root)
    root.mainloop()
