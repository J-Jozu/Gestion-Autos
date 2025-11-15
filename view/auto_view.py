"""
Vista para la gestión de autos
Incluye tabla, formularios y operaciones CRUD
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.auto_controller import AutoController
from utils.paths import path_manager
from utils.printer import pdf_generator
from PIL import Image, ImageTk
from pathlib import Path
import os

class AutoView(ctk.CTkFrame):
    """Vista de gestión de autos"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F5F7FA")
        
        self.selected_auto = None
        self.selected_image_path = None
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear componentes
        self.create_header()
        self.create_table()
        self.create_buttons()
        
        # Cargar datos
        self.load_autos()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(2, weight=1)
        
        # Contenido del header con padding
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", padx=20, pady=15)
        content_frame.grid_columnconfigure(2, weight=1)
        
        # Configuración del grid para el content_frame
        content_frame.grid_columnconfigure(1, weight=1)  # La columna del medio se expande
        
        # Barra de búsqueda
        self.search_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Buscar auto...",
            width=300,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_autos)
        
        # Frame para los botones (alineados a la derecha)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, sticky="e")
        
        btn_nuevo = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo Auto",
            command=self.show_form_nuevo,
            width=130,
            height=40,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=8
        )
        btn_nuevo.pack(side="left", padx=(0, 10))
        
        btn_imprimir = ctk.CTkButton(
            buttons_frame,
            text="🖨️ Imprimir",
            command=self.generar_pdf,
            width=130,
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8
        )
        btn_imprimir.pack(side="left", padx=(0, 10))
    
    def create_table(self):
        """Crea la tabla de autos"""
        table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#F9FAFB", corner_radius=0, height=45)
        headers_frame.grid(row=0, column=0, sticky="ew")
        headers_frame.grid_propagate(False)
        
        headers = ["Imagen", "ID", "Marca", "Modelo", "Año", "Color", "Transmisión", "Precio", "Acciones"]
        weights = [2, 1, 2, 2, 1, 2, 2, 2, 1]
        
        # Configurar columnas del header
        for i in range(len(headers)):
            headers_frame.grid_columnconfigure(i, weight=weights[i])
        
        for i, (header, weight) in enumerate(zip(headers, weights)):
            headers_frame.grid_columnconfigure(i, weight=weight)
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color="#1F2937"
            )
            label.grid(row=0, column=i, padx=10, pady=12)
            label.configure(anchor="center", justify="center")
        
        # Contenedor con scroll
        self.table_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="#FFFFFF")
        self.table_scroll.grid(row=1, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        # Los botones ahora están en el encabezado
        pass
    
    def load_autos(self):
        """Carga los autos en la tabla"""
        # Limpiar tabla
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Obtener autos
        success, result = AutoController.obtener_todos()
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        # Mostrar autos
        for i, auto in enumerate(result):
            row_frame = ctk.CTkFrame(
                self.table_scroll,
                fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                corner_radius=0,
                height=70
            )
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure(0, weight=1)
            
            # Contenedor principal de la fila
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            weights = [2, 1, 2, 2, 1, 2, 2, 2, 1, 2]
            
            # Imagen del auto
            img_frame = ctk.CTkFrame(data_frame, fg_color="#F3F4F6", width=60, height=60, corner_radius=8)
            img_frame.grid(row=0, column=0, padx=5)
            img_frame.grid_propagate(False)
            
            if auto.get('imagen_path'):
                try:
                    img = Image.open(auto['imagen_path'])
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = ctk.CTkLabel(img_frame, image=photo, text="")
                    img_label.image = photo
                    img_label.place(relx=0.5, rely=0.5, anchor="center")
                except:
                    img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                    img_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                img_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Configurar columnas del data_frame
            for i, weight in enumerate(weights):
                data_frame.grid_columnconfigure(i, weight=weight)
            
            # Imagen del auto
            img_frame = ctk.CTkFrame(data_frame, fg_color="#F3F4F6", width=60, height=60, corner_radius=8)
            img_frame.grid(row=0, column=0, padx=5)
            img_frame.grid_propagate(False)
            
            if auto.get('imagen_path') and Path(auto['imagen_path']).exists():
                try:
                    img = Image.open(auto['imagen_path'])
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    img_label = ctk.CTkLabel(img_frame, image=photo, text="")
                    img_label.image = photo
                    img_label.place(relx=0.5, rely=0.5, anchor="center")
                except Exception:
                    img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                    img_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                img_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Resto de datos
            values = [
                auto['id_auto'],
                auto['marca'],
                auto['modelo'],
                auto['anio'],
                auto['color'],
                auto['transmision'],
                f"${auto['precio']:,.2f}"
            ]
            
            # Configurar columnas para los datos
            for j, value in enumerate(values):
                cell_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=35)
                cell_frame.grid(row=0, column=j+1, sticky="nsew", padx=5)
                cell_frame.grid_propagate(False)
                
                label = ctk.CTkLabel(
                    cell_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#374151",
                    anchor="center"
                )
                label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Frame para botones de acción
            actions_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=35)
            actions_frame.grid(row=0, column=len(values)+1, sticky="nsew", padx=5)
            actions_frame.grid_propagate(False)
            
            buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
            buttons_container.place(relx=0.5, rely=0.5, anchor="center")
            
            btn_editar = ctk.CTkButton(
                buttons_container,
                text="✏️",
                width=30,
                height=30,
                fg_color="#6366F1",
                hover_color="#4F46E5",
                corner_radius=8,
                command=lambda a=auto: self.show_form(mode="editar", auto=a)
            )
            btn_editar.pack(side="left", padx=2)
            
            btn_eliminar = ctk.CTkButton(
                buttons_container,
                text="🗑️",
                width=30,
                height=30,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                corner_radius=8,
                command=lambda a=auto: self.eliminar_auto(a)
            )
            btn_eliminar.pack(side="left", padx=2)
            
            for j, (value, weight) in enumerate(zip(values, weights)):
                data_frame.grid_columnconfigure(j, weight=weight)
                label = ctk.CTkLabel(
                    data_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#1F2937"
                )
                label.grid(row=0, column=j, padx=10, sticky="w")
                label.bind("<Button-1>", lambda e, a=auto: self.select_auto(a))
    
    def select_auto(self, auto):
        """Selecciona un auto de la tabla"""
        self.selected_auto = auto
    
    def search_autos(self, event=None):
        """Busca autos por criterio"""
        criterio = self.search_entry.get().strip()
        
        if not criterio:
            self.load_autos()
            return
        
        # Limpiar tabla
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Buscar autos
        success, result = AutoController.buscar_autos(criterio)
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        # Mostrar resultados
        for i, auto in enumerate(result):
            row_frame = ctk.CTkFrame(
                self.table_scroll,
                fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                corner_radius=0
            )
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_columnconfigure(0, weight=1)
            
            row_frame.bind("<Button-1>", lambda e, a=auto: self.select_auto(a))
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#DBEAFE"))
            row_frame.bind("<Leave>", lambda e, rf=row_frame, idx=i: rf.configure(
                fg_color="#FFFFFF" if idx % 2 == 0 else "#F9FAFB"
            ))
            
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="x", padx=5, pady=8)
            
            weights = [1, 2, 2, 1, 2, 2, 2, 2]
            values = [
                auto['id_auto'],
                auto['modelo'],
                auto['anio'],
                auto['color'],
                auto['transmision'],
                auto['combustible'],
                f"${auto['precio']:,.2f}"
            ]
            
            for j, (value, weight) in enumerate(zip(values, weights)):
                data_frame.grid_columnconfigure(j, weight=weight)
                label = ctk.CTkLabel(
                    data_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#1F2937"
                )
                label.grid(row=0, column=j, padx=10, sticky="w")
                label.bind("<Button-1>", lambda e, a=auto: self.select_auto(a))
    
    def show_form_nuevo(self):
        """Muestra el formulario para crear un nuevo auto"""
        self.show_form(mode="nuevo")
    
    def show_form_editar(self):
        """Muestra el formulario para editar un auto"""
        if not self.selected_auto:
            messagebox.showwarning("Advertencia", "Debe seleccionar un auto para editar")
            return
        
        self.show_form(mode="editar", auto=self.selected_auto)
    
    def show_form(self, mode="nuevo", auto=None):
        """Muestra el formulario de auto"""
        form_window = ctk.CTkToplevel(self)
        form_window.title("Nuevo Auto" if mode == "nuevo" else "Editar Auto")
        form_window.geometry("650x750")
        form_window.resizable(False, False)
        
        if mode == "editar" and auto and auto.get('imagen_path'):
            self.selected_image_path = auto['imagen_path']
            if os.path.exists(self.selected_image_path):
                # Cargar la imagen existente después de que se cree el formulario
                form_window.after(100, lambda: self.update_image_preview(self.selected_image_path))
        
        # Centrar ventana
        form_window.transient(self)
        form_window.grab_set()
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(form_window, fg_color="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Nuevo Auto" if mode == "nuevo" else "Editar Auto",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#1F2937"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True)
        
        # Scroll para el formulario
        scroll_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos
        fields = [
            ("Marca:", "marca"),
            ("Modelo:", "modelo"),
            ("Año:", "anio"),
            ("Precio:", "precio"),
            ("Color:", "color"),
        ]
        
        entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = ctk.CTkLabel(
                scroll_frame,
                text=label_text,
                font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
                text_color="#6B7280",
                anchor="w"
            )
            label.pack(anchor="w", pady=(15 if i == 0 else 10, 5))
            
            entry = ctk.CTkEntry(
                scroll_frame,
                height=40,
                border_width=1,
                border_color="#E5E7EB",
                fg_color="#F9FAFB",
                corner_radius=8,
                font=ctk.CTkFont(family="Inter", size=13)
            )
            entry.pack(fill="x")
            entries[field_name] = entry
            
            # Prellenar si es edición
            if mode == "editar" and auto:
                entry.insert(0, str(auto[field_name]))
            
            # Enfoque automático en el primer campo
            if i == 0:
                entry.focus()
        
        # Transmisión
        label_trans = ctk.CTkLabel(
            scroll_frame,
            text="Transmisión:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_trans.pack(anchor="w", pady=(10, 5))
        
        transmision_var = ctk.StringVar(value="Manual" if mode == "nuevo" else auto['transmision'])
        transmision_combo = ctk.CTkComboBox(
            scroll_frame,
            values=["Manual", "Automática"],
            variable=transmision_var,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        transmision_combo.pack(fill="x")
        
        # Combustible
        label_comb = ctk.CTkLabel(
            scroll_frame,
            text="Combustible:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_comb.pack(anchor="w", pady=(10, 5))
        
        combustible_var = ctk.StringVar(value="Gasolina" if mode == "nuevo" else auto['combustible'])
        combustible_combo = ctk.CTkComboBox(
            scroll_frame,
            values=["Gasolina", "Diésel", "Eléctrico", "Híbrido"],
            variable=combustible_var,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        combustible_combo.pack(fill="x")
        
        # Imagen
        image_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        image_frame.pack(fill="x", pady=(20, 10))
        
        # Preview de imagen
        self.preview_frame = ctk.CTkFrame(
            image_frame, 
            fg_color="#F3F4F6",
            width=200,
            height=200,
            corner_radius=10
        )
        self.preview_frame.pack(side="left", padx=10)
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Vista previa\nde imagen",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#9CA3AF"
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controles de imagen
        controls_frame = ctk.CTkFrame(image_frame, fg_color="transparent")
        controls_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        label_img = ctk.CTkLabel(
            controls_frame,
            text="Imagen del Vehículo:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_img.pack(anchor="w", pady=(0, 10))
        
        self.selected_image_path = None
        
        btn_imagen = ctk.CTkButton(
            controls_frame,
            text="📸 Seleccionar Imagen",
            command=lambda: self.select_image(form_window),
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        btn_imagen.pack(fill="x")
        
        # Botones
        buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="  Guardar",
            command=lambda: self.save_auto(mode, entries, transmision_var, combustible_var, form_window, auto),
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            height=45,
            width=140,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=10
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            buttons_frame,
            text="  Cancelar",
            command=form_window.destroy,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            width=140,
            fg_color="#6B7280",
            hover_color="#4B5563",
            corner_radius=10
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def select_image(self, parent):
        """Abre el diálogo para seleccionar una imagen"""
        filetypes = (
            ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("Todos los archivos", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            parent=parent,
            title="Seleccionar imagen del auto",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_image_path = filename
            self.update_image_preview(filename)
    
    def update_image_preview(self, image_path):
        """Actualiza la vista previa de la imagen"""
        try:
            # Limpiar preview anterior
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
                
            # Cargar y mostrar nueva imagen
            img = Image.open(image_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            preview = ctk.CTkLabel(self.preview_frame, image=photo, text="")
            preview.image = photo
            preview.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
            self.selected_image_path = None
    
    def save_auto(self, mode, entries, transmision_var, combustible_var, window, auto=None):
        """Guarda el auto (crear o actualizar)"""
        # Obtener valores
        marca = entries['marca'].get().strip()
        modelo = entries['modelo'].get().strip()
        anio = entries['anio'].get().strip()
        precio = entries['precio'].get().strip()
        color = entries['color'].get().strip()
        transmision = transmision_var.get()
        combustible = combustible_var.get()
        
        if mode == "nuevo":
            success, result = AutoController.crear_auto(
                marca, modelo, anio, precio, color, transmision, combustible, self.selected_image_path
            )
        else:
            success, result = AutoController.actualizar_auto(
                auto['id_auto'], marca, modelo, anio, precio, color, transmision, combustible, self.selected_image_path
            )
        
        if success:
            messagebox.showinfo("Éxito", "Auto guardado correctamente")
            window.destroy()
            self.load_autos()
        else:
            messagebox.showerror("Error", result)
    
    def eliminar_auto(self, auto):
        """Elimina el auto seleccionado"""
        
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el auto {self.selected_auto['marca']} {self.selected_auto['modelo']}?"
        )
        
        if not confirm:
            return
        
        success, result = AutoController.eliminar_auto(self.selected_auto['id_auto'])
        
        if success:
            messagebox.showinfo("Éxito", "Auto eliminado correctamente")
            self.selected_auto = None
            self.load_autos()
        else:
            messagebox.showerror("Error", result)
    
    def generar_pdf(self):
        """Genera un PDF del auto seleccionado"""
        if not self.selected_auto:
            messagebox.showwarning("Advertencia", "Debe seleccionar un auto para generar el PDF")
            return
        
        try:
            filename = f"auto_{self.selected_auto['id_auto']}_{self.selected_auto['marca']}_{self.selected_auto['modelo']}.pdf"
            output_path = pdf_generator.generate_auto_report(self.selected_auto, filename)
            
            # Preguntar si desea abrir el PDF
            open_pdf = messagebox.askyesno(
                "PDF Generado",
                f"PDF generado correctamente en:\n{output_path}\n\n¿Desea abrir el archivo?"
            )
            
            if open_pdf:
                pdf_generator.open_pdf(output_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
