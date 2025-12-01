"""D3 Interactive Chart Card - PyQt6"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtGui import QFont
from smart_reports_pyqt6.ui.widgets.d3_chart_widget import D3ChartWidget

class D3InteractiveChartCard(QFrame):
    def __init__(self, titulo, chart_type, datos, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        title = QLabel(titulo)
        title.setFont(QFont("Montserrat", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        chart = D3ChartWidget(self)
        chart.set_chart(chart_type, titulo, datos)
        layout.addWidget(chart)
