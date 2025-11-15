"""
Generador de PDFs para reportes e impresión
Utiliza reportlab para crear documentos PDF
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from pathlib import Path
from utils.paths import path_manager
import os
import platform
import subprocess

class PDFGenerator:
    """Generador de documentos PDF para la aplicación"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Crea estilos personalizados para el PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#3B82F6'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        ))
    
    def generate_auto_report(self, auto_data, output_filename):
        """
        Genera un reporte PDF de un auto
        
        Args:
            auto_data: Diccionario con los datos del auto
            output_filename: Nombre del archivo de salida
        """
        output_path = path_manager.get_output_path(output_filename)
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Título
        title = Paragraph("FICHA TÉCNICA DEL VEHÍCULO", self.styles['CustomTitle'])
        story.append(title)
        
        # Subtítulo con sistema
        subtitle = Paragraph("AutoGest - Sistema de Gestión de Venta de Autos", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 0.3*inch))
        
        # Imagen del auto si existe
        if auto_data.get('imagen'):
            image_path = path_manager.get_image_path(auto_data['imagen'])
            if Path(image_path).exists():
                img = Image(image_path, width=4.5*inch, height=3*inch)
                story.append(img)
                story.append(Spacer(1, 0.3*inch))
        
        # Datos del auto
        heading = Paragraph("Información del Vehículo", self.styles['CustomHeading'])
        story.append(heading)
        
        data = [
            ['Marca:', auto_data.get('marca', 'N/A')],
            ['Modelo:', auto_data.get('modelo', 'N/A')],
            ['Año:', str(auto_data.get('anio', 'N/A'))],
            ['Color:', auto_data.get('color', 'N/A')],
            ['Transmisión:', auto_data.get('transmision', 'N/A')],
            ['Combustible:', auto_data.get('combustible', 'N/A')],
            ['Precio:', f"${auto_data.get('precio', 0):,.2f}"],
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1F2937')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')])
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.5*inch))
        
        # Fecha de generación
        fecha = Paragraph(
            f"<i>Documento generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</i>",
            self.styles['Normal']
        )
        story.append(fecha)
        
        doc.build(story)
        return output_path
    
    def generate_venta_report(self, venta_data, output_filename):
        """
        Genera un reporte PDF de una venta
        
        Args:
            venta_data: Diccionario con los datos de la venta
            output_filename: Nombre del archivo de salida
        """
        output_path = path_manager.get_output_path(output_filename)
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Título
        title = Paragraph("COMPROBANTE DE VENTA", self.styles['CustomTitle'])
        story.append(title)
        
        # Subtítulo
        subtitle = Paragraph("AutoGest - Sistema de Gestión de Venta de Autos", self.styles['CustomSubtitle'])
        story.append(subtitle)
        story.append(Spacer(1, 0.3*inch))
        
        # Información de la venta
        heading = Paragraph("Datos de la Venta", self.styles['CustomHeading'])
        story.append(heading)
        
        venta_info = [
            ['ID Venta:', str(venta_data.get('id_venta', 'N/A'))],
            ['Fecha:', venta_data.get('fecha_venta', 'N/A')],
            ['Método de Pago:', venta_data.get('metodo_pago', 'N/A')],
        ]
        
        table1 = Table(venta_info, colWidths=[2*inch, 4.5*inch])
        table1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
        ]))
        story.append(table1)
        story.append(Spacer(1, 0.2*inch))
        
        # Información del cliente
        heading2 = Paragraph("Datos del Cliente", self.styles['CustomHeading'])
        story.append(heading2)
        
        cliente_info = [
            ['Nombre:', venta_data.get('cliente_nombre', 'N/A')],
            ['Teléfono:', venta_data.get('cliente_telefono', 'N/A')],
            ['Correo:', venta_data.get('cliente_correo', 'N/A')],
            ['Dirección:', venta_data.get('cliente_direccion', 'N/A')],
        ]
        
        table2 = Table(cliente_info, colWidths=[2*inch, 4.5*inch])
        table2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
        ]))
        story.append(table2)
        story.append(Spacer(1, 0.2*inch))
        
        # Información del vehículo
        heading3 = Paragraph("Datos del Vehículo", self.styles['CustomHeading'])
        story.append(heading3)
        
        # Imagen del auto si existe
        if venta_data.get('auto_imagen'):
            image_path = path_manager.get_image_path(venta_data['auto_imagen'])
            if Path(image_path).exists():
                img = Image(image_path, width=3.5*inch, height=2.5*inch)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
        
        auto_info = [
            ['Marca:', venta_data.get('auto_marca', 'N/A')],
            ['Modelo:', venta_data.get('auto_modelo', 'N/A')],
            ['Año:', str(venta_data.get('auto_anio', 'N/A'))],
            ['Color:', venta_data.get('auto_color', 'N/A')],
        ]
        
        table3 = Table(auto_info, colWidths=[2*inch, 4.5*inch])
        table3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
        ]))
        story.append(table3)
        story.append(Spacer(1, 0.3*inch))
        
        # Monto total
        monto_data = [['MONTO TOTAL:', f"${venta_data.get('monto', 0):,.2f}"]]
        table4 = Table(monto_data, colWidths=[2*inch, 4.5*inch])
        table4.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
        ]))
        story.append(table4)
        story.append(Spacer(1, 0.3*inch))
        
        # Fecha de generación
        fecha = Paragraph(
            f"<i>Documento generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</i>",
            self.styles['Normal']
        )
        story.append(fecha)
        
        doc.build(story)
        return output_path
    
    def open_pdf(self, pdf_path):
        """
        Abre el PDF generado con el visor predeterminado del sistema
        
        Args:
            pdf_path: Ruta del archivo PDF a abrir
        """
        try:
            system = platform.system()
            
            if system == 'Windows':
                os.startfile(pdf_path)
            elif system == 'Darwin':  # macOS
                subprocess.run(['open', pdf_path])
            else:  # Linux y otros Unix
                subprocess.run(['xdg-open', pdf_path])
        except Exception as e:
            print(f"No se pudo abrir el PDF automáticamente: {str(e)}")

# Instancia global del generador de PDFs
pdf_generator = PDFGenerator()
