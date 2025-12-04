"""Exportador de Logs - PyQt6"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt6.QtGui import QFont

class ExportadorLogs(QDialog):
    def __init__(self, logs_text, parent=None):
        super().__init__(parent)
        self.logs_text = logs_text
        self.setWindowTitle("Exportar Logs")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("📋 Exportar Logs de Importación")
        title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Vista previa de logs
        self.logs_preview = QTextEdit()
        self.logs_preview.setReadOnly(True)
        self.logs_preview.setPlainText(logs_text)
        layout.addWidget(self.logs_preview)
        
        # Botones
        export_btn = QPushButton("💾 Exportar a TXT")
        export_btn.clicked.connect(self._export_txt)
        layout.addWidget(export_btn)
        
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _export_txt(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Logs",
            "logs_importacion.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.logs_text)
            print(f"✅ Logs exportados a: {file_name}")
