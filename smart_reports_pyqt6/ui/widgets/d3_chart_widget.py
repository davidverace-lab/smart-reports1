"""
D3 Chart Widget - PyQt6 con QWebEngineView
Widget para renderizar gráficos D3.js/NVD3.js interactivos
"""

import os
import tempfile
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl


class D3ChartWidget(QWidget):
    """
    Widget para renderizar gráficos D3.js usando QWebEngineView

    Características:
    - Renderizado profesional con Chromium
    - Tooltips interactivos
    - Hover effects y animaciones
    - Click handlers personalizados
    - Templates HTML/JS/CSS externos
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.temp_file = None
        self.chart_type = None
        self.chart_data = None

        # Crear UI
        self._create_ui()

    def _create_ui(self):
        """Crear interfaz"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear QWebEngineView
        self.webview = QWebEngineView(self)

        # Configurar settings
        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, False)

        layout.addWidget(self.webview)

    def set_chart(self, chart_type: str, title: str, datos: dict, subtitle: str = "", tema: str = 'dark'):
        """
        Establecer gráfico D3.js

        Args:
            chart_type: 'bar', 'donut', 'line'
            title: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitle: Subtítulo opcional
            tema: 'dark' o 'light'
        """

        print(f"📊 Cargando gráfico {chart_type}: {title}")

        # Guardar datos
        self.chart_type = chart_type
        self.chart_data = datos

        # Generar HTML
        html = self._generate_html(chart_type, title, datos, subtitle, tema)

        # Cargar en webview
        self._load_html(html)

    def _generate_html(self, chart_type: str, title: str, datos: dict, subtitle: str, tema: str) -> str:
        """Generar HTML del gráfico"""

        # TODO: Aquí puedes usar templates externos o generar inline
        # Por ahora, vamos a generar inline simple pero funcional

        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Preparar datos para NVD3
        if chart_type == 'bar':
            chart_data = [{
                "key": "Valores",
                "values": [
                    {"x": str(labels[i]), "y": float(values[i])}
                    for i in range(len(labels))
                ]
            }]
        elif chart_type == 'donut':
            chart_data = [
                {"label": str(labels[i]), "value": float(values[i])}
                for i in range(len(labels))
            ]
        elif chart_type == 'line':
            chart_data = [{
                "key": "Tendencia",
                "values": [
                    {"x": i, "y": float(values[i]), "label": str(labels[i])}
                    for i in range(len(labels))
                ]
            }]
        else:
            chart_data = []

        import json
        chart_data_json = json.dumps(chart_data)
        labels_json = json.dumps(labels)

        # Colores
        hutchison_colors = [
            '#002E6D', '#003D82', '#004C97', '#0066CC', '#0080FF',
            '#009BDE', '#00B5E2', '#33C7F0', '#66D4F5', '#99E1FA'
        ]
        colors_json = json.dumps(hutchison_colors)

        # HTML completo
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>

    <!-- D3.js v3 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>

    <!-- NVD3.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
            background: {'#1a1a1a' if tema == 'dark' else '#f5f5f5'};
            color: {'#ffffff' if tema == 'dark' else '#003087'};
            padding: 20px;
        }}

        .chart-card {{
            background: {'#2d2d2d' if tema == 'dark' else '#ffffff'};
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}

        .chart-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }}

        #chart {{
            height: 400px;
            width: 100%;
        }}

        #chart svg {{
            width: 100%;
            height: 100%;
        }}

        .nvd3 text {{
            fill: {'#ffffff' if tema == 'dark' else '#003087'} !important;
            font-family: 'Montserrat', sans-serif !important;
        }}

        .nvd3 .nv-axis path,
        .nvd3 .nv-axis line {{
            stroke: {'#b0b0b0' if tema == 'dark' else '#4a5c8a'} !important;
            stroke-opacity: 0.3;
        }}

        .nvd3 .nvtooltip {{
            background: rgba(0, 46, 109, 0.98) !important;
            border: 2px solid #002E6D !important;
            border-radius: 12px !important;
            padding: 15px !important;
            color: white !important;
        }}

        .nvd3 .nv-bar:hover {{
            opacity: 1 !important;
            filter: brightness(1.2);
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="chart-card">
        <h1 class="chart-title">{title}</h1>
        {f'<p style="text-align: center; color: #888; margin-bottom: 20px;">{subtitle}</p>' if subtitle else ''}
        <svg id="chart"></svg>
    </div>

    <script>
        window.CHART_DATA = {chart_data_json};
        window.LABELS = {labels_json};
        window.COLORS = {colors_json};

        nv.addGraph(function() {{
            var chart;

            {'// Gráfico de barras' if chart_type == 'bar' else '// Gráfico donut' if chart_type == 'donut' else '// Gráfico de líneas'}

            {self._get_chart_script(chart_type)}

            d3.select('#chart')
                .datum(window.CHART_DATA)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""
        return html

    def _get_chart_script(self, chart_type: str) -> str:
        """Obtener script específico del tipo de gráfico"""

        if chart_type == 'bar':
            return """
            chart = nv.models.discreteBarChart()
                .x(function(d) { return d.x; })
                .y(function(d) { return d.y; })
                .staggerLabels(true)
                .showValues(true)
                .duration(350)
                .color(window.COLORS);

            chart.yAxis.tickFormat(d3.format(',.0f'));
            """

        elif chart_type == 'donut':
            return """
            chart = nv.models.pieChart()
                .x(function(d) { return d.label; })
                .y(function(d) { return d.value; })
                .showLabels(true)
                .labelType("percent")
                .donut(true)
                .donutRatio(0.35)
                .duration(350)
                .color(window.COLORS);
            """

        elif chart_type == 'line':
            return """
            chart = nv.models.lineChart()
                .useInteractiveGuideline(true)
                .duration(350)
                .showLegend(true)
                .color([window.COLORS[0]]);

            chart.xAxis.tickFormat(function(d) {
                return window.LABELS[d] || d;
            });

            chart.yAxis.tickFormat(d3.format(',.0f'));
            """

        return ""

    def _load_html(self, html: str):
        """Cargar HTML en el webview"""

        try:
            # Limpiar archivo temporal anterior
            if self.temp_file and os.path.exists(self.temp_file):
                os.unlink(self.temp_file)

            # Crear archivo temporal
            fd, self.temp_file = tempfile.mkstemp(suffix='.html', text=True)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(html)

            # Cargar desde archivo
            url = QUrl.fromLocalFile(self.temp_file)
            self.webview.load(url)

            print(f"✅ Gráfico D3.js cargado: {self.temp_file}")

        except Exception as e:
            print(f"❌ Error cargando HTML: {e}")
            import traceback
            traceback.print_exc()

    def clear(self):
        """Limpiar gráfico"""
        self.webview.setHtml("")

    def __del__(self):
        """Limpiar al destruir"""
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.unlink(self.temp_file)
            except:
                pass
