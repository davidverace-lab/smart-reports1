"""
Motor de Templates HTML/D3.js para Gráficos Interactivos
Sistema escalable y profesional para generación de visualizaciones
"""

import json
from typing import Dict, List, Any, Optional
from smart_reports.config.themes import HUTCHISON_COLORS


class MotorTemplatesD3:
    """Motor para generar templates HTML con D3.js embebido"""

    # Escala de azules desde navy (solicitado por usuario)
    PALETA_COLORES = [
        '#002E6D',  # Navy (Hutchison Ports - más oscuro)
        '#003D82',  # Navy blue
        '#004C97',  # Royal blue oscuro
        '#0066CC',  # Royal blue
        '#0080FF',  # Azure blue
        '#009BDE',  # Sky blue (Hutchison Ports)
        '#00B5E2',  # Horizon blue (Hutchison Ports)
        '#33C7F0',  # Light blue
        '#66D4F5',  # Lighter blue
        '#99E1FA',  # Very light blue
    ]

    @staticmethod
    def _generar_head(titulo: str, tema: str = 'dark') -> str:
        """Generar <head> con estilos y D3.js"""

        # Colores según tema
        if tema == 'dark':
            bg_color = '#1a1d2e'
            card_bg = '#2b2d42'
            text_color = '#ffffff'
            text_secondary = '#a0a0b0'
            border_color = '#3a3d5c'
        else:
            bg_color = '#f0f2f5'
            card_bg = '#ffffff'
            text_color = '#2b2d42'
            text_secondary = '#6c6c80'
            border_color = '#e0e0e0'

        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>

    <!-- D3.js v7 -->
    <script src="https://d3js.org/d3.v7.min.js"></script>

    <!-- Fuente Montserrat -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap" rel="stylesheet">

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Montserrat', sans-serif;
            background: {bg_color};
            color: {text_color};
            overflow-x: hidden;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .chart-card {{
            background: {card_bg};
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }}

        .chart-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            color: {text_color};
            text-align: center;
        }}

        .chart-subtitle {{
            font-size: 14px;
            font-weight: 400;
            color: {text_secondary};
            text-align: center;
            margin-bottom: 30px;
        }}

        #chart-container {{
            width: 100%;
            height: 600px;
            position: relative;
        }}

        /* Tooltips estilizados */
        .d3-tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            font-size: 13px;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
        }}

        .d3-tooltip.show {{
            opacity: 1;
        }}

        .d3-tooltip-title {{
            font-weight: 700;
            margin-bottom: 6px;
            font-size: 14px;
        }}

        .d3-tooltip-value {{
            font-size: 16px;
            color: #ffd93d;
        }}

        /* Ejes y etiquetas */
        .axis {{
            font-family: 'Montserrat', sans-serif;
            font-size: 12px;
            color: {text_secondary};
        }}

        .axis path,
        .axis line {{
            stroke: {border_color};
            stroke-width: 1.5px;
        }}

        .axis text {{
            fill: {text_secondary};
        }}

        .grid line {{
            stroke: {border_color};
            stroke-opacity: 0.3;
            shape-rendering: crispEdges;
        }}

        .grid path {{
            stroke-width: 0;
        }}

        /* Animaciones */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .chart-card {{
            animation: fadeIn 0.5s ease-out;
        }}

        /* Controles */
        .controls {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}

        .btn {{
            background: {HUTCHISON_COLORS['ports_sky_blue']};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 2px 8px rgba(0, 155, 222, 0.3);
        }}

        .btn:hover {{
            background: {HUTCHISON_COLORS['ports_horizon_blue']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 155, 222, 0.4);
        }}

        .btn:active {{
            transform: translateY(0);
        }}

        .btn-secondary {{
            background: #6c6c80;
        }}

        .btn-secondary:hover {{
            background: #7c7c90;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .chart-card {{
                padding: 20px;
            }}

            .chart-title {{
                font-size: 20px;
            }}

            #chart-container {{
                height: 400px;
            }}
        }}
    </style>
</head>
"""

    @staticmethod
    def generar_grafico_barras(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark',
        interactivo: bool = True
    ) -> str:
        """
        Generar gráfico de barras con D3.js

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            tema: 'dark' o 'light'
            interactivo: Si es True, agrega hover y animaciones
        """

        # Aceptar tanto 'labels'/'values' como 'categorias'/'valores'
        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        labels_json = json.dumps(labels)
        values_json = json.dumps(values)
        colores_json = json.dumps(MotorTemplatesD3.PALETA_COLORES)

        html = MotorTemplatesD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <div class="controls">
                <button class="btn" onclick="sortAscending()">📈 Ordenar Ascendente</button>
                <button class="btn" onclick="sortDescending()">📉 Ordenar Descendente</button>
                <button class="btn btn-secondary" onclick="resetOrder()">🔄 Restablecer</button>
            </div>

            <div id="chart-container"></div>
        </div>
    </div>

    <script>
        // Datos
        const rawData = {{
            labels: {labels_json},
            values: {values_json}
        }};

        const colors = {colores_json};

        // Crear datos con índice original
        let data = rawData.labels.map((label, i) => ({{
            label: label,
            value: rawData.values[i],
            originalIndex: i
        }}));

        // Configuración
        const margin = {{top: 40, right: 40, bottom: 100, left: 80}};
        const container = document.getElementById('chart-container');
        const width = container.clientWidth - margin.left - margin.right;
        const height = container.clientHeight - margin.top - margin.bottom;

        // Crear SVG
        const svg = d3.select("#chart-container")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

        // Escalas
        const x = d3.scaleBand()
            .range([0, width])
            .padding(0.2);

        const y = d3.scaleLinear()
            .range([height, 0]);

        // Tooltip
        const tooltip = d3.select("body")
            .append("div")
            .attr("class", "d3-tooltip");

        // Función para dibujar gráfico
        function drawChart(animationDuration = 1000) {{
            // Actualizar escalas
            x.domain(data.map(d => d.label));
            y.domain([0, d3.max(data, d => d.value) * 1.1]);

            // Grid lines
            svg.selectAll(".grid").remove();
            svg.append("g")
                .attr("class", "grid")
                .call(d3.axisLeft(y)
                    .tickSize(-width)
                    .tickFormat("")
                );

            // Ejes
            svg.selectAll(".axis").remove();

            // Eje X
            svg.append("g")
                .attr("class", "axis")
                .attr("transform", `translate(0,${{height}})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("dy", ".15em")
                .attr("transform", "rotate(-45)");

            // Eje Y
            svg.append("g")
                .attr("class", "axis")
                .call(d3.axisLeft(y));

            // Barras
            const bars = svg.selectAll(".bar")
                .data(data, d => d.label);

            // Exit
            bars.exit()
                .transition()
                .duration(animationDuration / 2)
                .attr("height", 0)
                .attr("y", height)
                .remove();

            // Update + Enter
            const barsEnter = bars.enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => x(d.label))
                .attr("width", x.bandwidth())
                .attr("y", height)
                .attr("height", 0)
                .attr("fill", (d, i) => colors[i % colors.length])
                .attr("rx", 6)
                .attr("ry", 6);

            // Merge y animación
            bars.merge(barsEnter)
                .on("mouseover", function(event, d) {{
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("opacity", 0.7);

                    tooltip.html(`
                        <div class="d3-tooltip-title">${{d.label}}</div>
                        <div class="d3-tooltip-value">${{d.value.toLocaleString()}}</div>
                    `)
                    .style("left", (event.pageX + 15) + "px")
                    .style("top", (event.pageY - 28) + "px")
                    .classed("show", true);
                }})
                .on("mouseout", function() {{
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("opacity", 1);

                    tooltip.classed("show", false);
                }})
                .transition()
                .duration(animationDuration)
                .attr("x", d => x(d.label))
                .attr("y", d => y(d.value))
                .attr("height", d => height - y(d.value))
                .attr("fill", (d, i) => colors[d.originalIndex % colors.length]);

            // Etiquetas de valor
            const labels = svg.selectAll(".value-label")
                .data(data, d => d.label);

            labels.exit().remove();

            const labelsEnter = labels.enter()
                .append("text")
                .attr("class", "value-label")
                .attr("text-anchor", "middle")
                .attr("fill", "{HUTCHISON_COLORS['ports_sky_blue']}")
                .attr("font-weight", "600")
                .attr("font-size", "13px")
                .attr("y", height);

            labels.merge(labelsEnter)
                .transition()
                .duration(animationDuration)
                .attr("x", d => x(d.label) + x.bandwidth() / 2)
                .attr("y", d => y(d.value) - 8)
                .text(d => d.value.toLocaleString());
        }}

        // Funciones de ordenamiento
        function sortAscending() {{
            data.sort((a, b) => a.value - b.value);
            drawChart(800);
        }}

        function sortDescending() {{
            data.sort((a, b) => b.value - a.value);
            drawChart(800);
        }}

        function resetOrder() {{
            data.sort((a, b) => a.originalIndex - b.originalIndex);
            drawChart(800);
        }}

        // Dibujar inicialmente
        drawChart();

        // Responsive
        window.addEventListener('resize', () => {{
            d3.select("#chart-container svg").remove();
            drawChart(0);
        }});
    </script>
</body>
</html>
"""

        return html

    @staticmethod
    def generar_grafico_donut(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark'
    ) -> str:
        """Generar gráfico de donut con D3.js"""

        # Aceptar tanto 'labels'/'values' como 'categorias'/'valores'
        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        labels_json = json.dumps(labels)
        values_json = json.dumps(values)
        colores_json = json.dumps(MotorTemplatesD3.PALETA_COLORES)

        html = MotorTemplatesD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}
            <div id="chart-container"></div>
        </div>
    </div>

    <script>
        // Datos
        const labels = {labels_json};
        const values = {values_json};
        const colors = {colores_json};

        const data = labels.map((label, i) => ({{
            label: label,
            value: values[i]
        }}));

        // Configuración
        const container = document.getElementById('chart-container');
        const width = Math.min(container.clientWidth, 700);
        const height = Math.min(container.clientHeight, 600);
        const radius = Math.min(width, height) / 2 - 40;

        // Crear SVG
        const svg = d3.select("#chart-container")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${{width / 2}},${{height / 2}})`);

        // Pie layout
        const pie = d3.pie()
            .value(d => d.value)
            .sort(null);

        // Arc generator
        const arc = d3.arc()
            .innerRadius(radius * 0.6)
            .outerRadius(radius);

        const arcHover = d3.arc()
            .innerRadius(radius * 0.6)
            .outerRadius(radius * 1.08);

        // Tooltip
        const tooltip = d3.select("body")
            .append("div")
            .attr("class", "d3-tooltip");

        // Crear arcos
        const arcs = svg.selectAll(".arc")
            .data(pie(data))
            .enter()
            .append("g")
            .attr("class", "arc");

        // Paths con animación
        arcs.append("path")
            .attr("fill", (d, i) => colors[i % colors.length])
            .attr("stroke", "white")
            .attr("stroke-width", 3)
            .on("mouseover", function(event, d) {{
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("d", arcHover);

                const percentage = (d.data.value / d3.sum(values) * 100).toFixed(1);
                tooltip.html(`
                    <div class="d3-tooltip-title">${{d.data.label}}</div>
                    <div class="d3-tooltip-value">${{d.data.value.toLocaleString()}} (${{percentage}}%)</div>
                `)
                .style("left", (event.pageX + 15) + "px")
                .style("top", (event.pageY - 28) + "px")
                .classed("show", true);
            }})
            .on("mouseout", function() {{
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("d", arc);

                tooltip.classed("show", false);
            }})
            .transition()
            .duration(1000)
            .attrTween("d", function(d) {{
                const i = d3.interpolate({{startAngle: 0, endAngle: 0}}, d);
                return function(t) {{
                    return arc(i(t));
                }};
            }});

        // Etiquetas
        arcs.append("text")
            .attr("transform", d => `translate(${{arc.centroid(d)}})`)
            .attr("text-anchor", "middle")
            .attr("font-size", "14px")
            .attr("font-weight", "700")
            .attr("fill", "white")
            .style("opacity", 0)
            .text(d => {{
                const percentage = (d.data.value / d3.sum(values) * 100).toFixed(0);
                return percentage > 5 ? `${{percentage}}%` : '';
            }})
            .transition()
            .delay(1000)
            .duration(500)
            .style("opacity", 1);

        // Total en el centro
        svg.append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", "32px")
            .attr("font-weight", "800")
            .attr("fill", "{HUTCHISON_COLORS['ports_sky_blue']}")
            .attr("y", -10)
            .style("opacity", 0)
            .text(d3.sum(values).toLocaleString())
            .transition()
            .delay(1200)
            .duration(500)
            .style("opacity", 1);

        svg.append("text")
            .attr("text-anchor", "middle")
            .attr("font-size", "14px")
            .attr("font-weight", "500")
            .attr("fill", "#a0a0b0")
            .attr("y", 15)
            .style("opacity", 0)
            .text("TOTAL")
            .transition()
            .delay(1200)
            .duration(500)
            .style("opacity", 1);
    </script>
</body>
</html>
"""

        return html

    @staticmethod
    def generar_grafico_lineas(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark'
    ) -> str:
        """Generar gráfico de líneas con D3.js (múltiples series)"""

        # Aceptar tanto 'labels'/'values' como 'categorias'/'valores'
        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        # datos = {'labels': [...], 'series': [{'name': '...', 'values': [...]}, ...]}
        labels_json = json.dumps(labels)
        series_json = json.dumps(datos.get('series', [{'name': 'Serie 1', 'values': values}]))
        colores_json = json.dumps(MotorTemplatesD3.PALETA_COLORES)

        html = MotorTemplatesD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}
            <div id="chart-container"></div>
        </div>
    </div>

    <script>
        // Datos
        const labels = {labels_json};
        const series = {series_json};
        const colors = {colores_json};

        // Configuración
        const margin = {{top: 40, right: 120, bottom: 60, left: 80}};
        const container = document.getElementById('chart-container');
        const width = container.clientWidth - margin.left - margin.right;
        const height = container.clientHeight - margin.top - margin.bottom;

        // Crear SVG
        const svg = d3.select("#chart-container")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

        // Escalas
        const x = d3.scalePoint()
            .domain(labels)
            .range([0, width]);

        const allValues = series.flatMap(s => s.values);
        const y = d3.scaleLinear()
            .domain([0, d3.max(allValues) * 1.1])
            .range([height, 0]);

        // Grid
        svg.append("g")
            .attr("class", "grid")
            .call(d3.axisLeft(y)
                .tickSize(-width)
                .tickFormat("")
            );

        // Ejes
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", `translate(0,${{height}})`)
            .call(d3.axisBottom(x));

        svg.append("g")
            .attr("class", "axis")
            .call(d3.axisLeft(y));

        // Línea generator
        const line = d3.line()
            .x((d, i) => x(labels[i]))
            .y(d => y(d))
            .curve(d3.curveMonotoneX);

        // Dibujar líneas
        series.forEach((serie, serieIndex) => {{
            const path = svg.append("path")
                .datum(serie.values)
                .attr("fill", "none")
                .attr("stroke", colors[serieIndex % colors.length])
                .attr("stroke-width", 3)
                .attr("d", line);

            // Animación
            const totalLength = path.node().getTotalLength();
            path.attr("stroke-dasharray", totalLength + " " + totalLength)
                .attr("stroke-dashoffset", totalLength)
                .transition()
                .duration(1500)
                .ease(d3.easeLinear)
                .attr("stroke-dashoffset", 0);

            // Puntos
            svg.selectAll(`.dot-${{serieIndex}}`)
                .data(serie.values)
                .enter()
                .append("circle")
                .attr("class", `dot-${{serieIndex}}`)
                .attr("cx", (d, i) => x(labels[i]))
                .attr("cy", d => y(d))
                .attr("r", 0)
                .attr("fill", colors[serieIndex % colors.length])
                .attr("stroke", "white")
                .attr("stroke-width", 2)
                .on("mouseover", function(event, d) {{
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("r", 8);
                }})
                .on("mouseout", function() {{
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .attr("r", 5);
                }})
                .transition()
                .delay((d, i) => i * 100 + 1500)
                .duration(300)
                .attr("r", 5);
        }});

        // Leyenda
        const legend = svg.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${{width + 20}}, 0)`);

        series.forEach((serie, i) => {{
            const legendRow = legend.append("g")
                .attr("transform", `translate(0, ${{i * 30}})`);

            legendRow.append("rect")
                .attr("width", 20)
                .attr("height", 20)
                .attr("rx", 4)
                .attr("fill", colors[i % colors.length]);

            legendRow.append("text")
                .attr("x", 30)
                .attr("y", 15)
                .attr("font-size", "13px")
                .attr("fill", "{'#ffffff' if tema == 'dark' else '#2b2d42'}")
                .text(serie.name);
        }});
    </script>
</body>
</html>
"""

        return html

