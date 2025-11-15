"""
Vista para reportes y estadísticas
"""
import customtkinter as ctk
from tkinter import messagebox
from controller.venta_controller import VentaController

class ReportView(ctk.CTkFrame):
    """Vista de reportes y estadísticas"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F4F6F7")
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear componentes
        self.create_header()
        self.create_stats_cards()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", padx=20, pady=15)
        
        title = ctk.CTkLabel(
            content_frame,
            text="Reportes y Estadísticas",
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color="#1F2937"
        )
        title.pack(side="left")
    
    def create_stats_cards(self):
        """Crea las tarjetas de estadísticas"""
        success, stats = VentaController.obtener_estadisticas()
        
        if not success:
            messagebox.showerror("Error", stats)
            return
        
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        card1 = self.create_stat_card(
            cards_frame,
            "Total de Ventas",
            str(stats['total_ventas'] or 0),
            "#10B981"
        )
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        card2 = self.create_stat_card(
            cards_frame,
            "Monto Total",
            f"${stats['monto_total'] or 0:,.2f}",
            "#3B82F6"
        )
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        card3 = self.create_stat_card(
            cards_frame,
            "Venta Promedio",
            f"${stats['monto_promedio'] or 0:,.2f}",
            "#8B5CF6"
        )
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        card4 = self.create_stat_card(
            cards_frame,
            "Venta Mayor",
            f"${stats['venta_mayor'] or 0:,.2f}",
            "#F59E0B"
        )
        card4.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        card5 = self.create_stat_card(
            cards_frame,
            "Venta Menor",
            f"${stats['venta_menor'] or 0:,.2f}",
            "#EF4444"
        )
        card5.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    def create_stat_card(self, parent, title, value, color):
        """Crea una tarjeta de estadística"""
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=10)
        
        color_bar = ctk.CTkFrame(card, fg_color=color, height=6, corner_radius=0)
        color_bar.pack(fill="x")
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=ctk.CTkFont(family="Inter", size=13),
            text_color="#6B7280"
        )
        title_label.pack(pady=(0, 12))
        
        value_label = ctk.CTkLabel(
            content_frame,
            text=value,
            font=ctk.CTkFont(family="Inter", size=36, weight="bold"),
            text_color="#1F2937"
        )
        value_label.pack()
        
        return card
