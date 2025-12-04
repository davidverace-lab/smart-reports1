"""
Motor de Templates HTML/NVD3.js INTERACTIVO MEJORADO
✨ CARACTERÍSTICAS AVANZADAS:
- Tooltips detallados con estadísticas
- Animación de "alzado" (hover effect) con elevación 3D
- Click para mostrar data source (base de datos, tabla, etc.)
- Transiciones suaves y animaciones fluidas
- Soporte para dark/light mode
"""

import json
from typing import Dict, List, Any, Optional
from smart_reports.config.themes import HUTCHISON_COLORS


class MotorTemplatesNVD3Interactive:
    """Motor mejorado para generar templates HTML con NVD3.js + interactividad completa"""

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
    def _generar_head_interactivo(titulo: str, tema: str = 'dark', data_source: Dict = None, chart_height: int = 500) -> str:
        """Generar <head> con estilos mejorados y data source embebido

        Args:
            titulo: Título del gráfico
            tema: 'dark' o 'light'
            data_source: Info de origen de datos
            chart_height: Altura del gráfico en píxeles (default: 500)
        """

        # Colores según tema - HUTCHISON PORTS THEME
        if tema == 'dark':
            bg_color = '#1a1a1a'  # Negro (Hutchison dark mode)
            card_bg = '#2d2d2d'   # Gris oscuro (Hutchison cards)
            text_color = '#ffffff'
            text_secondary = '#b0b0b0'
            hover_bg = '#383838'  # Hutchison hover dark
        else:
            bg_color = '#f5f5f5'  # Hutchison light background
            card_bg = '#ffffff'
            text_color = '#003087'  # Hutchison navy text
            text_secondary = '#4a5c8a'  # Navy más claro
            hover_bg = '#f0f0f0'  # Hutchison hover light

        # Data source por defecto
        if not data_source:
            from datetime import datetime
            data_source = {
                'database': 'MySQL - Instituto Hutchison Ports',
                'table': 'Data Visualization',
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'records_count': 0
            }

        data_source_json = json.dumps(data_source)

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
            transition: all 0.3s ease;
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
            margin-bottom: 20px;
        }}

        #chart {{
            height: {chart_height}px;
            position: relative;
            width: 100%;
        }}

        /* Asegurar que el SVG se renderice correctamente */
        #chart svg {{
            width: 100%;
            height: 100%;
        }}

        /* Estilos para el SVG en ambos temas */
        .nvd3 text {{
            fill: {text_color} !important;
            font-family: 'Montserrat', sans-serif !important;
        }}

        .nvd3 .nv-axis path,
        .nvd3 .nv-axis line {{
            stroke: {text_secondary} !important;
            stroke-opacity: 0.3;
        }}

        /* TOOLTIPS MEJORADOS */
        .nvd3 .nvtooltip {{
            background: rgba(0, 46, 109, 0.98) !important;
            border: 2px solid {HUTCHISON_COLORS['primary']} !important;
            border-radius: 12px !important;
            padding: 15px !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
            color: white !important;
            font-family: 'Montserrat', sans-serif !important;
            backdrop-filter: blur(10px);
            animation: tooltipFadeIn 0.2s ease-out;
        }}

        @keyframes tooltipFadeIn {{
            from {{ opacity: 0; transform: translateY(10px) scale(0.95); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .nvd3 .nvtooltip h3 {{
            font-size: 16px !important;
            font-weight: 700 !important;
            margin-bottom: 8px !important;
            color: {HUTCHISON_COLORS['aqua_green']} !important;
            border-bottom: 2px solid {HUTCHISON_COLORS['aqua_green']};
            padding-bottom: 8px;
        }}

        .nvd3 .nvtooltip p {{
            font-size: 14px !important;
            margin: 4px 0 !important;
            color: white !important;
        }}

        .tooltip-stat {{
            display: flex;
            justify-content: space-between;
            margin: 6px 0;
            padding: 4px 0;
        }}

        .tooltip-label {{
            font-weight: 600;
            color: {HUTCHISON_COLORS['aqua_green']};
        }}

        .tooltip-value {{
            font-weight: 700;
            color: white;
        }}

        /* HOVER EFFECT - ALZADO CON ELEVACIÓN 3D */
        .nvd3 .nv-bar:hover,
        .nvd3 .nv-slice:hover {{
            opacity: 1 !important;
            filter: brightness(1.2) drop-shadow(0 8px 16px rgba(0, 155, 222, 0.5));
            transform: translateY(-5px) scale(1.05);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            cursor: pointer;
        }}

        .nvd3 .nv-bar {{
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            cursor: pointer;
        }}

        .nvd3 .nv-bar:not(:hover) {{
            opacity: 0.85;
        }}

        /* CLICK EFFECT - PULSE */
        @keyframes pulseClick {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(0.95); }}
            100% {{ transform: scale(1); }}
        }}

        .bar-clicked {{
            animation: pulseClick 0.3s ease-out;
        }}

        /* DATA SOURCE INFO MODAL */
        .data-source-modal {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0.8);
            background: {card_bg};
            border: 3px solid {HUTCHISON_COLORS['primary']};
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            z-index: 10000;
            min-width: 400px;
            max-width: 600px;
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}

        .data-source-modal.show {{
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
            pointer-events: all;
        }}

        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 9999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            backdrop-filter: blur(5px);
        }}

        .modal-overlay.show {{
            opacity: 1;
            pointer-events: all;
        }}

        .modal-header {{
            font-size: 20px;
            font-weight: 700;
            color: {HUTCHISON_COLORS['primary']};
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .modal-close {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: {HUTCHISON_COLORS['danger']};
            color: white;
            border: none;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .modal-close:hover {{
            background: #d32f2f;
            transform: rotate(90deg) scale(1.1);
        }}

        .data-source-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px 15px;
            margin: 10px 0;
            background: {hover_bg};
            border-radius: 8px;
            border-left: 4px solid {HUTCHISON_COLORS['aqua_green']};
        }}

        .data-source-label {{
            font-weight: 600;
            color: {text_secondary};
        }}

        .data-source-value {{
            font-weight: 700;
            color: {text_color};
        }}

        /* Instrucción de interacción */
        .interaction-hint {{
            text-align: center;
            font-size: 12px;
            color: {text_secondary};
            margin-top: 15px;
            font-style: italic;
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

            .data-source-modal {{
                min-width: 90%;
                max-width: 90%;
            }}
        }}
    </style>

    <script>
        // Data source global
        window.DATA_SOURCE = {data_source_json};

        // Función para mostrar data source modal
        function showDataSourceModal(elementData) {{
            // Crear overlay si no existe
            let overlay = document.querySelector('.modal-overlay');
            if (!overlay) {{
                overlay = document.createElement('div');
                overlay.className = 'modal-overlay';
                overlay.onclick = hideDataSourceModal;
                document.body.appendChild(overlay);
            }}

            // Crear modal si no existe
            let modal = document.querySelector('.data-source-modal');
            if (!modal) {{
                modal = document.createElement('div');
                modal.className = 'data-source-modal';
                document.body.appendChild(modal);
            }}

            // Contenido del modal
            const ds = window.DATA_SOURCE;
            modal.innerHTML = `
                <button class="modal-close" onclick="hideDataSourceModal()">×</button>
                <div class="modal-header">
                    📊 Origen de Datos - ${{elementData ? elementData.x : 'Información General'}}
                </div>
                <div class="data-source-item">
                    <span class="data-source-label">🗄️ Base de Datos:</span>
                    <span class="data-source-value">${{ds.database}}</span>
                </div>
                <div class="data-source-item">
                    <span class="data-source-label">📋 Tabla:</span>
                    <span class="data-source-value">${{ds.table}}</span>
                </div>
                <div class="data-source-item">
                    <span class="data-source-label">🕐 Última Actualización:</span>
                    <span class="data-source-value">${{ds.last_update}}</span>
                </div>
                <div class="data-source-item">
                    <span class="data-source-label">📈 Total de Registros:</span>
                    <span class="data-source-value">${{ds.records_count.toLocaleString()}}</span>
                </div>
                ${{elementData ? `
                <div class="data-source-item">
                    <span class="data-source-label">📌 Elemento Seleccionado:</span>
                    <span class="data-source-value">${{elementData.x}}</span>
                </div>
                <div class="data-source-item">
                    <span class="data-source-label">💯 Valor:</span>
                    <span class="data-source-value">${{elementData.y.toLocaleString()}}</span>
                </div>
                ` : ''}}
            `;

            // Mostrar modal y overlay
            setTimeout(() => {{
                overlay.classList.add('show');
                modal.classList.add('show');
            }}, 10);
        }}

        function hideDataSourceModal() {{
            const overlay = document.querySelector('.modal-overlay');
            const modal = document.querySelector('.data-source-modal');
            if (overlay) overlay.classList.remove('show');
            if (modal) modal.classList.remove('show');
        }}

        // Cerrar con tecla ESC
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                hideDataSourceModal();
            }}
        }});
    </script>
</head>
"""

    @staticmethod
    def generar_grafico_barras_interactivo(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark',
        data_source: Dict = None,
        chart_height: int = 400
    ) -> str:
        """
        Generar gráfico de barras INTERACTIVO con NVD3.js

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            tema: 'dark' o 'light'
            data_source: {'database': str, 'table': str, 'last_update': str, 'records_count': int}
            chart_height: Altura del gráfico en píxeles (default: 400)
        """

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        # DEBUG: Imprimir datos recibidos
        print(f"🔍 [DEBUG] generar_grafico_barras_interactivo - Título: {titulo}")
        print(f"🔍 [DEBUG] Labels: {labels}")
        print(f"🔍 [DEBUG] Values: {values}")

        # VALIDACIÓN: Verificar que haya datos
        if not labels or not values:
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico de barras")
            html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)
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

        # Actualizar data_source con records_count real
        if not data_source:
            from datetime import datetime
            data_source = {}
        data_source['records_count'] = len(labels)

        # Calcular estadísticas para tooltips
        total = sum(values)
        max_val = max(values)
        min_val = min(values)
        avg_val = total / len(values)

        # NVD3 usa formato [{ x: label, y: value}, ...]
        chart_data = [{"x": str(labels[i]), "y": float(values[i])} for i in range(len(labels))]
        chart_data_json = json.dumps([{"key": "Valores", "values": chart_data}])
        colors_json = json.dumps(MotorTemplatesNVD3Interactive.PALETA_COLORES)

        print(f"✅ [DEBUG] Datos transformados correctamente: {len(chart_data)} puntos")

        html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>

            <p class="interaction-hint">
                💡 Pasa el mouse sobre las barras para ver detalles • Haz clic para ver el origen de datos
            </p>
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

            // TOOLTIP MEJORADO con estadísticas
            chart.tooltip.contentGenerator(function(obj) {{
                const percentage = (obj.data.y / {total}) * 100;
                const ranking = {json.dumps(sorted([(v, l) for l, v in zip(labels, values)], reverse=True))};
                const position = ranking.findIndex(r => r[1] === obj.data.x) + 1;

                return '<h3>📊 ' + obj.data.x + '</h3>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Valor:</span>' +
                       '  <span class="tooltip-value">' + obj.data.y.toLocaleString() + '</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Porcentaje:</span>' +
                       '  <span class="tooltip-value">' + percentage.toFixed(1) + '%</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Ranking:</span>' +
                       '  <span class="tooltip-value">#' + position + ' de {len(labels)}</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Promedio:</span>' +
                       '  <span class="tooltip-value">' + {avg_val:.0f}.toLocaleString() + '</span>' +
                       '</div>' +
                       '<p style="margin-top: 10px; font-size: 11px; opacity: 0.8;">🖱️ Haz clic para ver origen de datos</p>';
            }});

            chart.yAxis
                .tickFormat(d3.format(',.0f'));

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            // CLICK HANDLER - Mostrar data source
            d3.selectAll('.nv-bar').on('click', function(d) {{
                // Agregar clase de animación
                d3.select(this).classed('bar-clicked', true);
                setTimeout(() => {{
                    d3.select(this).classed('bar-clicked', false);
                }}, 300);

                // Mostrar modal con data source
                showDataSourceModal(d);
            }});

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""
        return html


    @staticmethod
    def generar_grafico_donut_interactivo(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark',
        data_source: Dict = None,
        chart_height: int = 400
    ) -> str:
        """
        Generar gráfico donut INTERACTIVO con NVD3.js

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            tema: 'dark' o 'light'
            data_source: {'database': str, 'table': str, 'last_update': str, 'records_count': int}
        """

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        print(f"🔍 [DEBUG] generar_grafico_donut_interactivo - Título: {titulo}")

        if not labels or not values:
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico donut")
            html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)
            html += """
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">""" + titulo + """</h1>
            <div style="text-align: center; padding: 100px; color: #ff6b6b;">
                <h2>⚠️ No hay datos disponibles</h2>
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html

        min_len = min(len(labels), len(values))
        if len(labels) != len(values):
            labels = labels[:min_len]
            values = values[:min_len]

        if not data_source:
            data_source = {}
        data_source['records_count'] = len(labels)

        total = sum(values)

        # NVD3 pie chart formato
        chart_data = [{"label": str(labels[i]), "value": float(values[i])} for i in range(len(labels))]
        chart_data_json = json.dumps(chart_data)
        colors_json = json.dumps(MotorTemplatesNVD3Interactive.PALETA_COLORES)

        html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>

            <p class="interaction-hint">
                💡 Pasa el mouse sobre las secciones para ver detalles • Haz clic para ver el origen de datos
            </p>
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

            // TOOLTIP MEJORADO
            chart.tooltip.contentGenerator(function(obj) {{
                const percentage = (obj.data.value / {total}) * 100;

                return '<h3>📊 ' + obj.data.label + '</h3>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Valor:</span>' +
                       '  <span class="tooltip-value">' + obj.data.value.toLocaleString() + '</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Porcentaje:</span>' +
                       '  <span class="tooltip-value">' + percentage.toFixed(1) + '%</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Total:</span>' +
                       '  <span class="tooltip-value">' + {total}.toLocaleString() + '</span>' +
                       '</div>' +
                       '<p style="margin-top: 10px; font-size: 11px; opacity: 0.8;">🖱️ Haz clic para ver origen de datos</p>';
            }});

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            // CLICK HANDLER
            d3.selectAll('.nv-slice').on('click', function(d) {{
                d3.select(this).classed('bar-clicked', true);
                setTimeout(() => {{
                    d3.select(this).classed('bar-clicked', false);
                }}, 300);

                showDataSourceModal({{x: d.data.label, y: d.data.value}});
            }});

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""
        return html

    @staticmethod
    def generar_grafico_lineas_interactivo(
        titulo: str,
        datos: Dict[str, Any],
        subtitulo: str = "",
        tema: str = 'dark',
        data_source: Dict = None,
        chart_height: int = 400
    ) -> str:
        """
        Generar gráfico de líneas INTERACTIVO con NVD3.js

        Args:
            titulo: Título del gráfico
            datos: {'labels': [...], 'values': [...]}
            subtitulo: Subtítulo opcional
            tema: 'dark' o 'light'
            data_source: {'database': str, 'table': str, 'last_update': str, 'records_count': int}
        """

        labels = datos.get('labels') or datos.get('categorias', [])
        values = datos.get('values') or datos.get('valores', [])

        print(f"🔍 [DEBUG] generar_grafico_lineas_interactivo - Título: {titulo}")

        if not labels or not values:
            print(f"⚠️ [WARNING] No hay datos para generar el gráfico de líneas")
            html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)
            html += """
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">""" + titulo + """</h1>
            <div style="text-align: center; padding: 100px; color: #ff6b6b;">
                <h2>⚠️ No hay datos disponibles</h2>
            </div>
        </div>
    </div>
</body>
</html>
"""
            return html

        min_len = min(len(labels), len(values))
        if len(labels) != len(values):
            labels = labels[:min_len]
            values = values[:min_len]

        if not data_source:
            data_source = {}
        data_source['records_count'] = len(labels)

        total = sum(values)
        avg_val = total / len(values)
        max_val = max(values)
        min_val = min(values)

        # NVD3 line chart formato: [{key: "Series", values: [{x:0, y:val}, ...]}]
        chart_data = [{"x": i, "y": float(values[i]), "label": str(labels[i])} for i in range(len(labels))]
        chart_data_json = json.dumps([{"key": "Tendencia", "values": chart_data}])
        colors_json = json.dumps([HUTCHISON_COLORS['primary']])

        html = MotorTemplatesNVD3Interactive._generar_head_interactivo(titulo, tema, data_source, chart_height)

        html += f"""
<body>
    <div class="container">
        <div class="chart-card">
            <h1 class="chart-title">{titulo}</h1>
            {f'<p class="chart-subtitle">{subtitulo}</p>' if subtitulo else ''}

            <svg id="chart"></svg>

            <p class="interaction-hint">
                💡 Pasa el mouse sobre los puntos para ver detalles • Haz clic para ver el origen de datos
            </p>
        </div>
    </div>

    <script>
        nv.addGraph(function() {{
            var chart = nv.models.lineChart()
                .useInteractiveGuideline(true)
                .duration(350)
                .showLegend(true)
                .showYAxis(true)
                .showXAxis(true)
                .color({colors_json});

            // TOOLTIP MEJORADO
            chart.tooltip.contentGenerator(function(obj) {{
                const point = obj.point || obj.series[0];
                const percentage = (point.y / {total}) * 100;

                return '<h3>📈 ' + point.label + '</h3>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Valor:</span>' +
                       '  <span class="tooltip-value">' + point.y.toLocaleString() + '</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Porcentaje:</span>' +
                       '  <span class="tooltip-value">' + percentage.toFixed(1) + '%</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Promedio:</span>' +
                       '  <span class="tooltip-value">' + {avg_val:.0f}.toLocaleString() + '</span>' +
                       '</div>' +
                       '<div class="tooltip-stat">' +
                       '  <span class="tooltip-label">Máximo:</span>' +
                       '  <span class="tooltip-value">' + {max_val}.toLocaleString() + '</span>' +
                       '</div>' +
                       '<p style="margin-top: 10px; font-size: 11px; opacity: 0.8;">🖱️ Haz clic para ver origen de datos</p>';
            }});

            chart.xAxis
                .tickFormat(function(d) {{
                    var labels = {json.dumps(labels)};
                    return labels[d] || d;
                }});

            chart.yAxis
                .tickFormat(d3.format(',.0f'));

            d3.select('#chart')
                .datum({chart_data_json})
                .call(chart);

            // CLICK HANDLER en puntos
            d3.selectAll('.nv-point').on('click', function(d) {{
                d3.select(this).classed('bar-clicked', true);
                setTimeout(() => {{
                    d3.select(this).classed('bar-clicked', false);
                }}, 300);

                showDataSourceModal({{x: d.label, y: d.y}});
            }});

            nv.utils.windowResize(chart.update);

            return chart;
        }});
    </script>
</body>
</html>
"""
        return html


# Alias para compatibilidad
generar_grafico_barras = MotorTemplatesNVD3Interactive.generar_grafico_barras_interactivo
generar_grafico_donut = MotorTemplatesNVD3Interactive.generar_grafico_donut_interactivo
generar_grafico_lineas = MotorTemplatesNVD3Interactive.generar_grafico_lineas_interactivo
