"""Diálogo de Matching de Columnas - PyQt6"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFrame
from PyQt6.QtGui import QFont

class DialogoMatching(QDialog):
    def __init__(self, columnas_origen, columnas_destino, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matching de Columnas")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("🔗 Matching de Columnas")
        title.setFont(QFont("Montserrat", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        info = QLabel("Asocia las columnas del archivo origen con las columnas del sistema:")
        info.setFont(QFont("Montserrat", 10))
        layout.addWidget(info)
        
        # Área de matching
        for col_origen in columnas_origen[:5]:  # Primeras 5 columnas
            row_frame = QFrame()
            row_layout = QHBoxLayout(row_frame)
            
            origen_label = QLabel(col_origen)
            origen_label.setFixedWidth(200)
            row_layout.addWidget(origen_label)
            
            arrow_label = QLabel("→")
            row_layout.addWidget(arrow_label)
            
            destino_combo = QComboBox()
            destino_combo.addItems(columnas_destino)
            row_layout.addWidget(destino_combo)
            
            layout.addWidget(row_frame)
        
        layout.addStretch()
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        accept_btn = QPushButton("Aplicar Matching")
        accept_btn.clicked.connect(self.accept)
        btn_layout.addWidget(accept_btn)
        
        layout.addLayout(btn_layout)
