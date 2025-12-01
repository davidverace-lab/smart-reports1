"""Configurador de Columnas - PyQt6"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ConfiguradorColumnas(QDialog):
    def __init__(self, columnas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Columnas")
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("⚙️ Configurar Columnas Visibles")
        title.setFont(QFont("Montserrat", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        info = QLabel("Selecciona las columnas que deseas mostrar:")
        info.setFont(QFont("Montserrat", 10))
        layout.addWidget(info)
        
        # Lista de columnas
        self.columnas_list = QListWidget()
        for col in columnas:
            item = QListWidgetItem(col)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.columnas_list.addItem(item)
        
        layout.addWidget(self.columnas_list)
        
        # Botones
        btn_layout = QVBoxLayout()
        
        select_all_btn = QPushButton("Seleccionar Todas")
        select_all_btn.clicked.connect(self._select_all)
        btn_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deseleccionar Todas")
        deselect_all_btn.clicked.connect(self._deselect_all)
        btn_layout.addWidget(deselect_all_btn)
        
        layout.addLayout(btn_layout)
        
        # Botones finales
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _select_all(self):
        for i in range(self.columnas_list.count()):
            self.columnas_list.item(i).setCheckState(Qt.CheckState.Checked)
    
    def _deselect_all(self):
        for i in range(self.columnas_list.count()):
            self.columnas_list.item(i).setCheckState(Qt.CheckState.Unchecked)
