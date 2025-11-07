"""
Gráficos D3.js Avanzados
Tipos especializados y personalizados
"""

import json
from nucleo.configuracion.ajustes import HUTCHISON_COLORS


class GraficosD3Avanzados:
    """Gráficos D3.js avanzados y especializados"""

    PALETA_COLORES = [
        HUTCHISON_COLORS['ports_sky_blue'],
        HUTCHISON_COLORS['ports_horizon_blue'],
        HUTCHISON_COLORS['success'],
        HUTCHISON_COLORS['warning'],
        HUTCHISON_COLORS['danger'],
        '#8B4CFA', '#FF8C42', '#4ECDC4', '#A78BFA', '#FB923C',
    ]

    @staticmethod
    def generar_gauge_chart(
        titulo: str,
        valor: float,
        maximo: float = 100,
        subtitulo: str = "",
        tema: str = 'dark'
    ) -> str:
        """
        Gráfico de gauge/velocímetro

        Args:
            titulo: Título
            valor: Valor actual
            maximo: Valor máximo
            subtitulo: Subtítulo
            tema: 'dark' o 'light'
        """

        porcentaje = (valor / maximo) * 100

        bg_color = '#1a1d2e' if tema == 'dark' else '#f0f2f5'
        card_bg = '#2b2d42' if tema == 'dark' else '#ffffff'
        text_color = '#ffffff' if tema == 'dark' else '#2b2d42'

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Montserrat', sans-serif;
            background: {bg_color};
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: {text_color};
        }}
        .gauge-container {{
            background: {card_bg};
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            text-align: center;
        }}
        .gauge-title {{
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 10px;
        }}
        .gauge-subtitle {{
            font-size: 14px;
            color: #a0a0b0;
            margin-bottom: 30px;
        }}
        .gauge-value {{
            font-size: 64px;
            font-weight: 800;
            color: {HUTCHISON_COLORS['ports_sky_blue']};
            margin: 20px 0;
        }}
        .gauge-label {{
            font-size: 16px;
            color: #a0a0b0;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="gauge-container">
        <div class="gauge-title">{titulo}</div>
        <div class="gauge-subtitle">{subtitulo}</div>
        <svg id="gauge"></svg>
        <div class="gauge-value" id="value">0</div>
        <div class="gauge-label">de {maximo}</div>
    </div>

    <script>
        const valor = {valor};
        const maximo = {maximo};
        const porcentaje = {porcentaje};

        const width = 400;
        const height = 300;
        const margin = 20;

        const svg = d3.select("#gauge")
            .attr("width", width)
            .attr("height", height);

        const g = svg.append("g")
            .attr("transform", `translate(${{width/2}}, ${{height - margin}})`);

        // Escala de arco
        const arcScale = d3.scaleLinear()
            .domain([0, 100])
            .range([-Math.PI/2, Math.PI/2]);

        // Arco fondo
        const arcBackground = d3.arc()
            .innerRadius(100)
            .outerRadius(130)
            .startAngle(-Math.PI/2)
            .endAngle(Math.PI/2);

        g.append("path")
            .attr("d", arcBackground)
            .attr("fill", "#2b2d42");

        // Arco de progreso
        const arcProgress = d3.arc()
            .innerRadius(100)
            .outerRadius(130)
            .startAngle(-Math.PI/2);

        const path = g.append("path")
            .datum({{endAngle: -Math.PI/2}})
            .attr("fill", "{HUTCHISON_COLORS['ports_sky_blue']}")
            .attr("d", arcProgress);

        // Animación
        path.transition()
            .duration(2000)
            .ease(d3.easeElastic)
            .attrTween("d", function(d) {{
                const interpolate = d3.interpolate(d.endAngle, arcScale(porcentaje));
                return function(t) {{
                    d.endAngle = interpolate(t);
                    return arcProgress(d);
                }};
            }});

        // Animar valor
        d3.select("#value")
            .transition()
            .duration(2000)
            .tween("text", function() {{
                const interpolate = d3.interpolateNumber(0, valor);
                return function(t) {{
                    this.textContent = Math.round(interpolate(t));
                }};
            }});

        // Marcas
        [0, 25, 50, 75, 100].forEach(tick => {{
            const angle = arcScale(tick);
            const x1 = Math.cos(angle) * 95;
            const y1 = Math.sin(angle) * 95;
            const x2 = Math.cos(angle) * 85;
            const y2 = Math.sin(angle) * 85;

            g.append("line")
                .attr("x1", x1)
                .attr("y1", y1)
                .attr("x2", x2)
                .attr("y2", y2)
                .attr("stroke", "#6c6c80")
                .attr("stroke-width", 2);

            if (tick % 25 === 0) {{
                const x3 = Math.cos(angle) * 75;
                const y3 = Math.sin(angle) * 75;

                g.append("text")
                    .attr("x", x3)
                    .attr("y", y3)
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "middle")
                    .attr("fill", "#a0a0b0")
                    .attr("font-size", "14px")
                    .attr("font-weight", "600")
                    .text(tick);
            }}
        }});
    </script>
</body>
</html>
"""

        return html

    @staticmethod
    def generar_heatmap(
        titulo: str,
        datos: dict,
        subtitulo: str = "",
        tema: str = 'dark'
    ) -> str:
        """
        Mapa de calor con D3.js

        Args:
            titulo: Título
            datos: {
                'rows': ['Fila 1', 'Fila 2', ...],
                'cols': ['Col 1', 'Col 2', ...],
                'values': [[val11, val12, ...], [val21, val22, ...], ...]
            }
            subtitulo: Subtítulo
            tema: 'dark' o 'light'
        """

        rows_json = json.dumps(datos['rows'])
        cols_json = json.dumps(datos['cols'])
        values_json = json.dumps(datos['values'])

        bg_color = '#1a1d2e' if tema == 'dark' else '#f0f2f5'
        card_bg = '#2b2d42' if tema == 'dark' else '#ffffff'
        text_color = '#ffffff' if tema == 'dark' else '#2b2d42'

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Montserrat', sans-serif;
            background: {bg_color};
            padding: 40px;
            color: {text_color};
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {card_bg};
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
        .title {{
            font-size: 28px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            font-size: 14px;
            color: #a0a0b0;
            text-align: center;
            margin-bottom: 40px;
        }}
        .d3-tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 12px;
            border-radius: 8px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            font-size: 13px;
        }}
        .d3-tooltip.show {{ opacity: 1; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">{titulo}</div>
        <div class="subtitle">{subtitulo}</div>
        <div id="heatmap"></div>
    </div>

    <script>
        const rows = {rows_json};
        const cols = {cols_json};
        const values = {values_json};

        const margin = {{top: 80, right: 40, bottom: 100, left: 120}};
        const width = 1000 - margin.left - margin.right;
        const height = 600 - margin.top - margin.bottom;

        const svg = d3.select("#heatmap")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

        // Escalas
        const x = d3.scaleBand()
            .domain(cols)
            .range([0, width])
            .padding(0.05);

        const y = d3.scaleBand()
            .domain(rows)
            .range([0, height])
            .padding(0.05);

        const allValues = values.flat();
        const colorScale = d3.scaleSequential()
            .domain([d3.min(allValues), d3.max(allValues)])
            .interpolator(d3.interpolateBlues);

        // Tooltip
        const tooltip = d3.select("body")
            .append("div")
            .attr("class", "d3-tooltip");

        // Crear celdas
        rows.forEach((row, i) => {{
            cols.forEach((col, j) => {{
                svg.append("rect")
                    .attr("x", x(col))
                    .attr("y", y(row))
                    .attr("width", x.bandwidth())
                    .attr("height", y.bandwidth())
                    .attr("fill", colorScale(values[i][j]))
                    .attr("stroke", "{bg_color}")
                    .attr("stroke-width", 2)
                    .attr("rx", 4)
                    .style("opacity", 0)
                    .on("mouseover", function(event) {{
                        d3.select(this).style("opacity", 0.7);
                        tooltip.html(`
                            <b>${{row}} - ${{col}}</b><br/>
                            Valor: ${{values[i][j]}}
                        `)
                        .style("left", (event.pageX + 15) + "px")
                        .style("top", (event.pageY - 28) + "px")
                        .classed("show", true);
                    }})
                    .on("mouseout", function() {{
                        d3.select(this).style("opacity", 1);
                        tooltip.classed("show", false);
                    }})
                    .transition()
                    .delay((i * cols.length + j) * 20)
                    .duration(300)
                    .style("opacity", 1);

                // Texto
                svg.append("text")
                    .attr("x", x(col) + x.bandwidth() / 2)
                    .attr("y", y(row) + y.bandwidth() / 2)
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "middle")
                    .attr("fill", values[i][j] > (d3.max(allValues) / 2) ? "white" : "black")
                    .attr("font-size", "12px")
                    .attr("font-weight", "600")
                    .style("opacity", 0)
                    .text(values[i][j])
                    .transition()
                    .delay((i * cols.length + j) * 20 + 300)
                    .duration(300)
                    .style("opacity", 1);
            }});
        }});

        // Ejes
        svg.append("g")
            .attr("transform", `translate(0, ${{height}})`)
            .call(d3.axisBottom(x))
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-45)")
            .style("fill", "{text_color}");

        svg.append("g")
            .call(d3.axisLeft(y))
            .selectAll("text")
            .style("fill", "{text_color}");
    </script>
</body>
</html>
"""

        return html
