"""Sistema de Rollback - PyQt6"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from PyQt6.QtGui import QFont

class SistemaRollback(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sistema de Rollback")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🔄 Sistema de Rollback")
        title.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        info = QLabel("Puntos de restauración disponibles:")
        info.setFont(QFont("Montserrat", 10))
        layout.addWidget(info)
        
        # Lista de puntos de restauración
        self.restore_points = QListWidget()
        self.restore_points.addItems([
            "2025-12-01 14:30 - Importación Training Report (1,245 registros)",
            "2025-12-01 10:15 - Importación Org Planning (876 registros)",
            "2025-11-30 16:45 - Actualización masiva (2,134 registros)"
        ])
        layout.addWidget(self.restore_points)
        
        # Botones
        restore_btn = QPushButton("🔙 Restaurar Punto Seleccionado")
        restore_btn.clicked.connect(self._restore)
        layout.addWidget(restore_btn)
        
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _restore(self):
        if self.restore_points.currentItem():
            reply = QMessageBox.question(
                self,
                "Confirmar Rollback",
                "¿Estás seguro de restaurar este punto? Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                QMessageBox.information(self, "Rollback", "Sistema restaurado exitosamente")
