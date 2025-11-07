"""
UnitSelector - Selector elegante de unidad de negocio con dropdown
"""
import customtkinter as ctk
from nucleo.configuracion.ajustes import HUTCHISON_COLORS


class UnitSelector(ctk.CTkFrame):
    """Selector elegante de unidad de negocio con diseño mejorado"""

    def __init__(self, parent, units, default_unit=None, command=None, **kwargs):
        """
        Args:
            parent: Widget padre
            units: Lista de unidades disponibles
            default_unit: Unidad seleccionada por defecto
            command: Función a ejecutar cuando cambia la selección
        """
        super().__init__(
            parent,
            fg_color='#2b2d42',
            corner_radius=15,
            border_width=2,
            border_color=HUTCHISON_COLORS['ports_sky_blue'],
            **kwargs
        )

        self.units = units
        self.selected_unit = default_unit or (units[0] if units else None)
        self.command = command

        # Container con padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=20, pady=15)

        # Label
        label = ctk.CTkLabel(
            container,
            text="📍 Seleccionar Unidad de Negocio:",
            font=('Montserrat', 16, 'bold'),
            text_color='#ffffff',
            anchor='w'
        )
        label.pack(side='left', padx=(0, 20))

        # ComboBox mejorado
        self.combo = ctk.CTkOptionMenu(
            container,
            values=units,
            font=('Montserrat', 14),
            fg_color=HUTCHISON_COLORS['ports_sky_blue'],
            button_color=HUTCHISON_COLORS['ports_sea_blue'],
            button_hover_color=HUTCHISON_COLORS['ports_horizon_blue'],
            dropdown_fg_color='#2b2d42',
            dropdown_hover_color=HUTCHISON_COLORS['ports_sky_blue'],
            dropdown_text_color='#ffffff',
            text_color='#ffffff',
            corner_radius=10,
            height=45,
            width=280,
            anchor='center',
            command=self._on_selection_change
        )
        self.combo.pack(side='left')

        # Establecer valor inicial
        if self.selected_unit:
            self.combo.set(self.selected_unit)

    def _on_selection_change(self, choice):
        """Callback interno cuando cambia la selección"""
        self.selected_unit = choice
        if self.command:
            self.command(choice)

    def get(self):
        """Obtener unidad seleccionada"""
        return self.selected_unit

    def set(self, unit):
        """Establecer unidad seleccionada"""
        if unit in self.units:
            self.selected_unit = unit
            self.combo.set(unit)
