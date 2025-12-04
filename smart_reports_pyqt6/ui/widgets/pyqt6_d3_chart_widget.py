"""
D3 Chart Widget - PyQt6 con QWebEngineView
Widget para renderizar gráficos D3.js v7 interactivos (sin NVD3)
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
    Widget para renderizar gráficos D3.js v7 usando QWebEngineView

    Características:
    - Renderizado profesional con Chromium
    - D3.js v7 (última versión)
    - Tooltips interactivos
    - Hover effects y animaciones suaves
    - Responsive design
    - Colores corporativos Hutchison Ports
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
        Establecer gráfico D3.js v7

        Args:
            chart_type: 'bar', 'donut', 'line', 'area', 'scatter'
            title: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitle: Subtítulo opcional
            tema: 'dark' o 'light'
        """

        print(f"📊 Cargando gráfico D3.js v7 - {chart_type}: {title}")

        # Guardar datos
        self.chart_type = chart_type
        self.chart_data = datos

        # CRÍTICO: Limpiar webview antes de cargar nuevo contenido
        self.webview.setHtml("")

        # Generar HTML
        html = self._generate_html(chart_type, title, datos, subtitle, tema)

        # Cargar en webview con delay para asegurar renderizado
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(50, lambda: self._load_html(html))

    def _generate_html(self, chart_type: str, title: str, datos: dict, subtitle: str, tema: str) -> str:
        """Generar HTML del gráfico usando D3.js v7"""

        labels = datos.get('labels', [])
        values = datos.get('values', [])

        # Preparar datos para D3.js v7
        chart_data = [
            {"label": str(labels[i]), "value": float(values[i])}
            for i in range(len(labels))
        ]

        import json
        chart_data_json = json.dumps(chart_data)

        # Colores Hutchison Ports
        hutchison_colors = [
            '#002E6D', '#003D82', '#004C97', '#0066CC', '#0080FF',
            '#009BDE', '#00B5E2', '#33C7F0', '#66D4F5', '#99E1FA'
        ]
        colors_json = json.dumps(hutchison_colors)

        # Colores de fondo según tema
        bg_color = '#1a1a1a' if tema == 'dark' else '#f5f5f5'
        card_bg = '#2d2d2d' if tema == 'dark' else '#ffffff'
        text_color = '#ffffff' if tema == 'dark' else '#003087'
        axis_color = '#b0b0b0' if tema == 'dark' else '#4a5c8a'

        # HTML completo con D3.js v7
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>

    <!-- D3.js v7 (última versión) -->
    <script src="https://d3js.org/d3.v7.min.js"></script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
            background: {bg_color};
            color: {text_color};
            padding: 20px;
            overflow: hidden;
        }}

        .chart-container {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        .chart-card {{
            background: {card_bg};
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            width: 95%;
            max-width: 1200px;
        }}

        .chart-title {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 15px;
            text-align: center;
            color: {text_color};
        }}

        .chart-subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 20px;
            font-size: 14px;
        }}

        #chart {{
            width: 100%;
            height: 450px;
        }}

        /* Estilos de ejes */
        .axis text {{
            fill: {text_color};
            font-family: 'Montserrat', sans-serif;
            font-size: 11px;
        }}

        .axis line,
        .axis path {{
            stroke: {axis_color};
            stroke-opacity: 0.3;
        }}

        .grid line {{
            stroke: {axis_color};
            stroke-opacity: 0.1;
        }}

        /* Estilos de tooltip */
        .tooltip {{
            position: absolute;
            padding: 12px 16px;
            background: rgba(0, 46, 109, 0.98);
            border: 2px solid #002E6D;
            border-radius: 12px;
            color: white;
            font-size: 13px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .tooltip.show {{
            opacity: 1;
        }}

        .tooltip-label {{
            font-weight: 700;
            margin-bottom: 6px;
            font-size: 14px;
        }}

        .tooltip-value {{
            font-size: 16px;
            color: #00D4AA;
        }}

        /* Estilos específicos por tipo de gráfico */
        .bar {{
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .bar:hover {{
            opacity: 0.8;
            filter: brightness(1.2);
        }}

        .line {{
            fill: none;
            stroke-width: 3;
        }}

        .dot {{
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .dot:hover {{
            r: 8;
        }}

        .arc {{
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .arc:hover {{
            opacity: 0.8;
            filter: brightness(1.1);
        }}

        .legend {{
            font-size: 12px;
            fill: {text_color};
        }}

        .legend-item {{
            cursor: pointer;
        }}

        .legend-item:hover {{
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-card">
            <h1 class="chart-title">{title}</h1>
            {f'<p class="chart-subtitle">{subtitle}</p>' if subtitle else ''}
            <div id="chart"></div>
        </div>
    </div>

    <script>
        // Datos del gráfico
        const data = {chart_data_json};
        const colors = {colors_json};

        // Tipo de gráfico
        const chartType = '{chart_type}';

        // Tooltip
        const tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip');

        // Funciones de tooltip
        function showTooltip(event, d) {{
            tooltip
                .html(`
                    <div class="tooltip-label">${{d.label}}</div>
                    <div class="tooltip-value">${{d.value.toLocaleString()}}</div>
                `)
                .style('left', (event.pageX + 15) + 'px')
                .style('top', (event.pageY - 15) + 'px')
                .classed('show', true);
        }}

        function hideTooltip() {{
            tooltip.classed('show', false);
        }}

        // Renderizar según tipo
        {self._get_d3v7_chart_script(chart_type)}
    </script>
</body>
</html>
"""
        return html

    def _get_d3v7_chart_script(self, chart_type: str) -> str:
        """Obtener script D3.js v7 específico del tipo de gráfico"""

        if chart_type == 'bar':
            return """
        // ===== GRÁFICO DE BARRAS D3.js v7 =====
        const container = d3.select('#chart');
        const containerNode = container.node();
        const width = containerNode.clientWidth;
        const height = containerNode.clientHeight;
        const margin = {top: 40, right: 30, bottom: 80, left: 60};
        const chartWidth = width - margin.left - margin.right;
        const chartHeight = height - margin.top - margin.bottom;

        const svg = container.append('svg')
            .attr('width', width)
            .attr('height', height);

        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Escalas
        const x = d3.scaleBand()
            .domain(data.map(d => d.label))
            .range([0, chartWidth])
            .padding(0.3);

        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value) * 1.1])
            .range([chartHeight, 0]);

        // Escala de colores
        const colorScale = d3.scaleOrdinal()
            .domain(data.map(d => d.label))
            .range(colors);

        // Grid
        g.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(y)
                .tickSize(-chartWidth)
                .tickFormat('')
            );

        // Barras
        g.selectAll('.bar')
            .data(data)
            .join('rect')
            .attr('class', 'bar')
            .attr('x', d => x(d.label))
            .attr('y', chartHeight)
            .attr('width', x.bandwidth())
            .attr('height', 0)
            .attr('fill', d => colorScale(d.label))
            .on('mouseover', showTooltip)
            .on('mousemove', showTooltip)
            .on('mouseout', hideTooltip)
            .transition()
            .duration(800)
            .ease(d3.easeCubicOut)
            .attr('y', d => y(d.value))
            .attr('height', d => chartHeight - y(d.value));

        // Etiquetas de valores
        g.selectAll('.label')
            .data(data)
            .join('text')
            .attr('class', 'label')
            .attr('x', d => x(d.label) + x.bandwidth() / 2)
            .attr('y', d => y(d.value) - 5)
            .attr('text-anchor', 'middle')
            .attr('fill', '{text_color}')
            .attr('font-size', '12px')
            .attr('font-weight', '600')
            .attr('opacity', 0)
            .text(d => d.value.toLocaleString())
            .transition()
            .delay(800)
            .duration(300)
            .attr('opacity', 1);

        // Ejes
        g.append('g')
            .attr('class', 'axis')
            .attr('transform', `translate(0,${chartHeight})`)
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .attr('dx', '-0.5em')
            .attr('dy', '0.5em');

        g.append('g')
            .attr('class', 'axis')
            .call(d3.axisLeft(y).tickFormat(d => d.toLocaleString()));

        // Responsive
        window.addEventListener('resize', () => {
            location.reload();
        });
            """

        elif chart_type == 'donut':
            return """
        // ===== GRÁFICO DONUT D3.js v7 =====
        const container = d3.select('#chart');
        const containerNode = container.node();
        const width = containerNode.clientWidth;
        const height = containerNode.clientHeight;
        const radius = Math.min(width, height) / 2 - 40;

        const svg = container.append('svg')
            .attr('width', width)
            .attr('height', height);

        const g = svg.append('g')
            .attr('transform', `translate(${width/2},${height/2})`);

        // Escala de colores
        const colorScale = d3.scaleOrdinal()
            .domain(data.map(d => d.label))
            .range(colors);

        // Generador de arcos
        const arc = d3.arc()
            .innerRadius(radius * 0.6)
            .outerRadius(radius);

        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);

        // Dibujar arcos
        const arcs = g.selectAll('.arc')
            .data(pie(data))
            .join('g')
            .attr('class', 'arc');

        arcs.append('path')
            .attr('d', arc)
            .attr('fill', d => colorScale(d.data.label))
            .attr('stroke', '{card_bg}')
            .attr('stroke-width', 3)
            .style('opacity', 0)
            .on('mouseover', function(event, d) {
                d3.select(this).transition().duration(200)
                    .attr('d', d3.arc()
                        .innerRadius(radius * 0.6)
                        .outerRadius(radius + 10)
                    );
                showTooltip(event, d.data);
            })
            .on('mousemove', (event, d) => showTooltip(event, d.data))
            .on('mouseout', function() {
                d3.select(this).transition().duration(200)
                    .attr('d', arc);
                hideTooltip();
            })
            .transition()
            .duration(800)
            .style('opacity', 1)
            .attrTween('d', function(d) {
                const i = d3.interpolate(d.startAngle, d.endAngle);
                return function(t) {
                    d.endAngle = i(t);
                    return arc(d);
                };
            });

        // Etiquetas
        arcs.append('text')
            .attr('transform', d => `translate(${arc.centroid(d)})`)
            .attr('text-anchor', 'middle')
            .attr('font-size', '13px')
            .attr('font-weight', '600')
            .attr('fill', 'white')
            .attr('opacity', 0)
            .text(d => {
                const percent = (d.data.value / d3.sum(data, d => d.value) * 100).toFixed(1);
                return percent > 5 ? percent + '%' : '';
            })
            .transition()
            .delay(800)
            .duration(300)
            .attr('opacity', 1);

        // Leyenda
        const legend = svg.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(20, 20)`);

        const legendItems = legend.selectAll('.legend-item')
            .data(data)
            .join('g')
            .attr('class', 'legend-item')
            .attr('transform', (d, i) => `translate(0, ${i * 25})`);

        legendItems.append('rect')
            .attr('width', 18)
            .attr('height', 18)
            .attr('fill', d => colorScale(d.label))
            .attr('rx', 3);

        legendItems.append('text')
            .attr('x', 25)
            .attr('y', 13)
            .attr('fill', '{text_color}')
            .attr('font-size', '12px')
            .text(d => d.label);

        // Responsive
        window.addEventListener('resize', () => {
            location.reload();
        });
            """

        elif chart_type == 'line':
            return """
        // ===== GRÁFICO DE LÍNEAS D3.js v7 =====
        const container = d3.select('#chart');
        const containerNode = container.node();
        const width = containerNode.clientWidth;
        const height = containerNode.clientHeight;
        const margin = {top: 40, right: 30, bottom: 80, left: 60};
        const chartWidth = width - margin.left - margin.right;
        const chartHeight = height - margin.top - margin.bottom;

        const svg = container.append('svg')
            .attr('width', width)
            .attr('height', height);

        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Escalas
        const x = d3.scalePoint()
            .domain(data.map(d => d.label))
            .range([0, chartWidth])
            .padding(0.5);

        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value) * 1.1])
            .range([chartHeight, 0]);

        // Grid
        g.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(y)
                .tickSize(-chartWidth)
                .tickFormat('')
            );

        // Generador de línea
        const line = d3.line()
            .x(d => x(d.label))
            .y(d => y(d.value))
            .curve(d3.curveMonotoneX);

        // Área bajo la línea
        const area = d3.area()
            .x(d => x(d.label))
            .y0(chartHeight)
            .y1(d => y(d.value))
            .curve(d3.curveMonotoneX);

        // Dibujar área
        g.append('path')
            .datum(data)
            .attr('fill', colors[0])
            .attr('fill-opacity', 0.2)
            .attr('d', area);

        // Dibujar línea
        const path = g.append('path')
            .datum(data)
            .attr('class', 'line')
            .attr('stroke', colors[0])
            .attr('d', line);

        // Animación de la línea
        const pathLength = path.node().getTotalLength();
        path
            .attr('stroke-dasharray', pathLength)
            .attr('stroke-dashoffset', pathLength)
            .transition()
            .duration(1500)
            .ease(d3.easeCubicOut)
            .attr('stroke-dashoffset', 0);

        // Puntos
        g.selectAll('.dot')
            .data(data)
            .join('circle')
            .attr('class', 'dot')
            .attr('cx', d => x(d.label))
            .attr('cy', d => y(d.value))
            .attr('r', 0)
            .attr('fill', colors[0])
            .attr('stroke', 'white')
            .attr('stroke-width', 2)
            .on('mouseover', showTooltip)
            .on('mousemove', showTooltip)
            .on('mouseout', hideTooltip)
            .transition()
            .delay((d, i) => i * 100 + 1500)
            .duration(300)
            .attr('r', 5);

        // Ejes
        g.append('g')
            .attr('class', 'axis')
            .attr('transform', `translate(0,${chartHeight})`)
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('transform', 'rotate(-45)')
            .style('text-anchor', 'end')
            .attr('dx', '-0.5em')
            .attr('dy', '0.5em');

        g.append('g')
            .attr('class', 'axis')
            .call(d3.axisLeft(y).tickFormat(d => d.toLocaleString()));

        // Responsive
        window.addEventListener('resize', () => {
            location.reload();
        });
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

            print(f"✅ Gráfico D3.js v7 cargado: {self.temp_file}")

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
