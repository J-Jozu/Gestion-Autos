"""
Vista principal de la aplicación
Contiene el sidebar de navegación y el contenedor principal
"""
import customtkinter as ctk
from view.auto_view import AutoView
from view.cliente_view import ClienteView
from view.venta_view import VentaView
from model.conexion import db

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainApplication(ctk.CTk):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("AutoGest - Sistema de Gestión de Venta de Autos")
        self.geometry("1400x800")
        self.minsize(1200, 700)
        
        # Conectar a la base de datos
        success, message = db.connect()
        if not success:
            self.show_error_and_exit(message)
            return
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear sidebar
        self.create_sidebar()
        
        self.main_container = ctk.CTkFrame(self, fg_color="#F5F7FA")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Vista actual
        self.current_view = None
        
        # Mostrar vista de autos por defecto
        self.show_autos_view()
    
    def create_sidebar(self):
        """Crea el sidebar de navegación"""
        self.sidebar = ctk.CTkFrame(
            self, 
            width=250, 
            corner_radius=0, 
            fg_color="#FFFFFF",
            border_width=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Logo y título
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="#6366F1", height=120, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        self.logo_label = ctk.CTkLabel(
            header_frame,
            text="AutoGest",
            font=ctk.CTkFont(family="Inter", size=28, weight="bold"),
            text_color="#FFFFFF"
        )
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Botones de navegación
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        
        self.btn_autos = ctk.CTkButton(
            nav_frame,
            text="🚗  Autos",
            command=self.show_autos_view,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            fg_color="transparent",
            hover_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            anchor="w",
            text_color="#374151"
        )
        self.btn_autos.pack(fill="x", padx=10, pady=5)
        
        self.btn_clientes = ctk.CTkButton(
            nav_frame,
            text="👥  Clientes",
            command=self.show_clientes_view,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            fg_color="transparent",
            hover_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            anchor="w",
            text_color="#374151"
        )
        self.btn_clientes.pack(fill="x", padx=10, pady=5)
        
        self.btn_ventas = ctk.CTkButton(
            nav_frame,
            text="💰  Ventas",
            command=self.show_ventas_view,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            fg_color="transparent",
            hover_color="#F3F4F6",
            border_width=0,
            corner_radius=8,
            anchor="w",
            text_color="#374151"
        )
        self.btn_ventas.pack(fill="x", padx=10, pady=5)
        
        # Botón de salir en la parte inferior
        self.btn_salir = ctk.CTkButton(
            self.sidebar,
            text="⬅️  Cerrar Sesión",
            command=self.quit_app,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            fg_color="transparent",
            hover_color="#FEE2E2",
            text_color="#DC2626",
            border_width=1,
            border_color="#DC2626",
            corner_radius=8
        )
        self.btn_salir.grid(row=3, column=0, padx=15, pady=20, sticky="ew")
    
    def clear_main_container(self):
        """Limpia el contenedor principal"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def show_autos_view(self):
        """Muestra la vista de autos"""
        self.clear_main_container()
        self.current_view = AutoView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_button(self.btn_autos)
    
    def show_clientes_view(self):
        """Muestra la vista de clientes"""
        self.clear_main_container()
        self.current_view = ClienteView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_button(self.btn_clientes)
    
    def show_ventas_view(self):
        """Muestra la vista de ventas"""
        self.clear_main_container()
        self.current_view = VentaView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.highlight_button(self.btn_ventas)
    
    def highlight_button(self, active_button):
        """Resalta el botón activo en el sidebar"""
        buttons = [self.btn_autos, self.btn_clientes, self.btn_ventas]
        for btn in buttons:
            if btn == active_button:
                btn.configure(fg_color="#6366F1", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color="#374151")
    
    def show_error_and_exit(self, message):
        """Muestra un error y cierra la aplicación"""
        error_label = ctk.CTkLabel(
            self,
            text=f"Error de conexión:\n{message}\n\nVerifique que MySQL esté instalado y en ejecución.",
            font=ctk.CTkFont(size=14),
            text_color="#DC2626"
        )
        error_label.pack(expand=True)
        
        close_btn = ctk.CTkButton(
            self,
            text="Cerrar",
            command=self.quit,
            fg_color="#DC2626"
        )
        close_btn.pack(pady=20)
    
    def quit_app(self):
        """Cierra la aplicación y desconecta la base de datos"""
        db.disconnect()
        self.quit()
