"""
Motor de Templates HTML/NVD3.js para Gráficos Interactivos
NVD3 es una librería de componentes reutilizables construida sobre D3.js
"""

import json
from typing import Dict, List, Any, Optional
from smart_reports.config.themes import HUTCHISON_COLORS


class MotorTemplatesNVD3:
    """Motor para generar templates HTML con NVD3.js embebido"""

    # Escala de azules Hutchison
    PALETA_COLORES = [
        '#002E6D',  # Navy
        '#003D82',  # Navy blue
        '#004C97',  # Royal blue oscuro
        '#0066CC',  # Royal blue
        '#0080FF',  # Azure blue
        '#009BDE',  # Sky blue
        '#00B5E2',  # Horizon blue
        '#33C7F0',  # Light blue
        '#66D4F5',  # Lighter blue
        '#99E1FA',  # Very light blue
    ]

    @staticmethod
    def _generar_head(titulo: str, tema: str = 'dark') -> str:
        """Generar <head> con estilos y NVD3.js + D3.js"""

        # Colores según tema
        if tema == 'dark':
            bg_color = '#1a1d2e'
            card_bg = '#2b2d42'
            text_color = '#ffffff'
            text_secondary = '#a0a0b0'
        else:
            bg_color = '#f0f2f5'
            card_bg = '#ffffff'
            text_color = '#2b2d42'
            text_secondary = '#6c6c80'

        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>

    <!-- D3.js v3 (NVD3 requiere D3 v3.x) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>

    <!-- NVD3.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.6/nv.d3.min.css">

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

        #chart {{
            width: 100%;
            height: 600px;
        }}

        /* Personalización de NVD3 */
        .nvd3 text {{
            font-family: 'Montserrat', sans-serif;
            fill: {text_secondary};
        }}

        .nvd3 .nv-axis path,
        .nvd3 .nv-axis line {{
            stroke: {text_secondary};
        }}

        .nvtooltip {{
            background: rgba(0, 0, 0, 0.9) !important;
            border: none !important;
            border-radius: 8px !important;
            font-family: 'Montserrat', sans-serif !important;
            padding: 12px 16px !important;
        }}

        .nvtooltip h3 {{
            color: white !important;
            font-weight: 700 !important;
        }}

        .nvtooltip p {{
            color: #ffd93d !important;
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
            background: {HUTCHISON_COLORS['primary']};
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
            background: {HUTCHISON_COLORS['info']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 155, 222, 0.4);
        }}

        .btn:active {{
            transform: translateY(0);
        }}

        /* Animaciones */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .chart-card {{
            animation: fadeIn 0.5s ease-out;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .chart-card {{
                padding: 20px;
            }}

            .chart-title {{
                font-size: 20px;
            }}

            #chart {{
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
        tema: str = 'dark'
    ) -> str:
        """
        Generar gráfico de barras con NVD3.js

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            tema: 'dark' o 'light'
        """

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        # DEBUG: Imprimir datos recibidos
        print(f"🔍 [DEBUG] generar_grafico_barras - Título: {titulo}")
        print(f"🔍 [DEBUG] Labels: {labels}")
        print(f"🔍 [DEBUG] Values: {values}")

        # VALIDACIÓN: Verificar que haya datos
        if not labels or not values:
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico de barras")
            # Retornar HTML con mensaje de error
            html = MotorTemplatesNVD3._generar_head(titulo, tema)
            html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            <div style="text-align: center; padding: 100px; color: #ff6b6b;">
                <h2>⚠️ No hay datos disponibles</h2>
                <p>No se encontraron datos para mostrar en este gráfico.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html

        # VALIDACIÓN: Verificar que ambas listas tengan la misma longitud
        min_len = min(len(labels), len(values))
        if len(labels) != len(values):
            print(f"⚠️ [WARNING] Labels y values tienen longitudes diferentes. Usando {min_len} elementos.")
            labels = labels[:min_len]
            values = values[:min_len]

        # NVD3 usa formato [{ x: label, y: value}, ...]
        chart_data = [{"x": str(labels[i]), "y": float(values[i])} for i in range(len(labels))]
        chart_data_json = json.dumps([{"key": "Valores", "values": chart_data}])
        colors_json = json.dumps(MotorTemplatesNVD3.PALETA_COLORES)

        print(f"✅ [DEBUG] Datos transformados correctamente: {len(chart_data)} puntos")

        html = MotorTemplatesNVD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>
        </div>
    </div>

    <script>
        nv.addGraph(function() {{
            var chart = nv.models.discreteBarChart()
                .x(function(d) {{ return d.x; }})
                .y(function(d) {{ return d.y; }})
                .staggerLabels(true)
                .showValues(true)
                .duration(350)
                .color({colors_json});

            chart.tooltip.contentGenerator(function(obj) {{
                return '<h3>' + obj.data.x + '</h3>' +
                       '<p>' + obj.data.y.toLocaleString() + '</p>';
            }});

            chart.yAxis
                .tickFormat(d3.format(',.0f'));

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
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
        """Generar gráfico de dona con NVD3.js"""

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        # DEBUG: Imprimir datos recibidos
        print(f"🔍 [DEBUG] generar_grafico_donut - Título: {titulo}")
        print(f"🔍 [DEBUG] Labels: {labels}")
        print(f"🔍 [DEBUG] Values: {values}")

        # VALIDACIÓN: Verificar que haya datos
        if not labels or not values:
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico de dona")
            html = MotorTemplatesNVD3._generar_head(titulo, tema)
            html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            <div style="text-align: center; padding: 100px; color: #ff6b6b;">
                <h2>⚠️ No hay datos disponibles</h2>
                <p>No se encontraron datos para mostrar en este gráfico.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html

        # VALIDACIÓN: Verificar que ambas listas tengan la misma longitud
        min_len = min(len(labels), len(values))
        if len(labels) != len(values):
            print(f"⚠️ [WARNING] Labels y values tienen longitudes diferentes. Usando {min_len} elementos.")
            labels = labels[:min_len]
            values = values[:min_len]

        # NVD3 pie chart formato
        chart_data = [{"label": str(labels[i]), "value": float(values[i])} for i in range(len(labels))]
        chart_data_json = json.dumps(chart_data)
        colors_json = json.dumps(MotorTemplatesNVD3.PALETA_COLORES)

        print(f"✅ [DEBUG] Datos transformados correctamente: {len(chart_data)} puntos")

        html = MotorTemplatesNVD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>
        </div>
    </div>

    <script>
        nv.addGraph(function() {{
            var chart = nv.models.pieChart()
                .x(function(d) {{ return d.label; }})
                .y(function(d) {{ return d.value; }})
                .showLabels(true)
                .labelThreshold(.05)
                .labelType("percent")
                .donut(true)
                .donutRatio(0.35)
                .duration(350)
                .color({colors_json});

            chart.tooltip.contentGenerator(function(obj) {{
                var total = d3.sum({chart_data_json}, function(d) {{ return d.value; }});
                var percent = ((obj.data.value / total) * 100).toFixed(1);
                return '<h3>' + obj.data.label + '</h3>' +
                       '<p>' + obj.data.value.toLocaleString() + ' (' + percent + '%)</p>';
            }});

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        }});
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
        """Generar gráfico de líneas con NVD3.js"""

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])
        series = datos.get('series', [{'name': 'Serie 1', 'values': values}]) if values else []

        # DEBUG: Imprimir datos recibidos
        print(f"🔍 [DEBUG] generar_grafico_lineas - Título: {titulo}")
        print(f"🔍 [DEBUG] Labels: {labels}")
        print(f"🔍 [DEBUG] Values/Series: {values if not series else 'multiple series'}")

        # VALIDACIÓN: Verificar que haya datos
        if not labels or (not values and not series):
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico de líneas")
            html = MotorTemplatesNVD3._generar_head(titulo, tema)
            html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            <div style="text-align: center; padding: 100px; color: #ff6b6b;">
                <h2>⚠️ No hay datos disponibles</h2>
                <p>No se encontraron datos para mostrar en este gráfico.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html

        # Convertir a formato NVD3
        nvd3_data = []
        for serie in series:
            serie_name = serie.get('name', 'Serie')
            serie_values = serie.get('values', [])
            if serie_values:  # Solo agregar si tiene valores
                nvd3_data.append({
                    "key": serie_name,
                    "values": [{"x": i, "y": float(serie_values[i])} for i in range(len(serie_values))]
                })

        print(f"✅ [DEBUG] Datos transformados correctamente: {len(nvd3_data)} series")

        chart_data_json = json.dumps(nvd3_data)
        labels_json = json.dumps(labels)
        colors_json = json.dumps(MotorTemplatesNVD3.PALETA_COLORES)

        html = MotorTemplatesNVD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>
        </div>
    </div>

    <script>
        var labels = {labels_json};

        nv.addGraph(function() {{
            var chart = nv.models.lineChart()
                .options({{
                    duration: 300,
                    useInteractiveGuideline: true
                }})
                .color({colors_json});

            chart.xAxis
                .tickFormat(function(d) {{
                    return labels[d] || d;
                }});

            chart.yAxis
                .tickFormat(d3.format(',.0f'));

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""

        return html

    @staticmethod
    def generar_grafico_area(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark'
    ) -> str:
        """Generar gráfico de área apilada con NVD3.js"""

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])
        series = datos.get('series', [{'name': 'Serie 1', 'values': values}])

        # Convertir a formato NVD3
        nvd3_data = []
        for serie in series:
            serie_name = serie.get('name', 'Serie')
            serie_values = serie.get('values', [])
            nvd3_data.append({
                "key": serie_name,
                "values": [{"x": i, "y": serie_values[i]} for i in range(len(serie_values))]
            })

        chart_data_json = json.dumps(nvd3_data)
        labels_json = json.dumps(labels)
        colors_json = json.dumps(MotorTemplatesNVD3.PALETA_COLORES)

        html = MotorTemplatesNVD3._generar_head(titulo, tema)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <div class="controls">
                <button class="btn" onclick="chart.style('stack');">📊 Apilado</button>
                <button class="btn" onclick="chart.style('stream');">🌊 Stream</button>
                <button class="btn" onclick="chart.style('expand');">📈 Expandido</button>
            </div>

            <svg id="chart"></svg>
        </div>
    </div>

    <script>
        var labels = {labels_json};
        var chart;

        nv.addGraph(function() {{
            chart = nv.models.stackedAreaChart()
                .x(function(d) {{ return d.x; }})
                .y(function(d) {{ return d.y; }})
                .clipEdge(true)
                .duration(300)
                .useInteractiveGuideline(true)
                .color({colors_json});

            chart.xAxis
                .tickFormat(function(d) {{
                    return labels[d] || d;
                }});

            chart.yAxis
                .tickFormat(d3.format(',.0f'));

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""

        return html
