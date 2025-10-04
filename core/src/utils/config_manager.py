"""
Configuration Manager for GHST

Manages YAML-based configuration system inspired by Klipper:
- Printer profiles
- Material settings
- Slicing parameters
- AI GHST Agent preferences

All configs include safety disclaimers and experimental feature warnings.
"""

import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Import plugin system
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from plugins.plugin_manager import PluginManager
    PLUGINS_AVAILABLE = True
except ImportError:
    PLUGINS_AVAILABLE = False


@dataclass
class PrinterConfig:
    """Printer configuration data structure."""
    name: str
    bed_size_x: float
    bed_size_y: float
    bed_size_z: float
    nozzle_diameter: float
    max_temp_hotend: int
    max_temp_bed: int
    max_feedrate_x: int
    max_feedrate_y: int
    max_feedrate_z: int
    firmware_type: str = "marlin"
    supports_nonplanar: bool = False
    experimental_features: List[str] = None

    def __post_init__(self):
        if self.experimental_features is None:
            self.experimental_features = []


@dataclass
class MaterialConfig:
    """Material configuration data structure."""
    name: str
    type: str  # PLA, ABS, PETG, etc.
    temp_hotend: int
    temp_bed: int
    fan_speed: int
    retraction_distance: float
    retraction_speed: int
    linear_advance: float = 0.0
    ai_optimized: bool = False
    safety_notes: List[str] = None

    def __post_init__(self):
        if self.safety_notes is None:
            self.safety_notes = []


@dataclass
class SlicingConfig:
    """Slicing configuration data structure."""
    layer_height: float
    first_layer_height: float
    infill_percentage: int
    infill_pattern: str
    perimeters: int
    top_solid_layers: int
    bottom_solid_layers: int
    support_enabled: bool
    support_threshold: float
    ai_optimization: bool = True
    experimental_features: Dict[str, bool] = None

    def __post_init__(self):
        if self.experimental_features is None:
            self.experimental_features = {
                "nonplanar_slicing": False,
                "ai_generated_supports": True,
                "adaptive_infill": True,
                "ghst_optimization": True
            }


class ConfigManager:
    """Manages all SlicerGPT configuration files and settings."""

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

        # Initialize logging
        self.logger = logging.getLogger('ConfigManager')

        # Default configurations
        self.current_printer: Optional[PrinterConfig] = None
        self.current_material: Optional[MaterialConfig] = None
        self.current_slicing: Optional[SlicingConfig] = None

        # Initialize plugin manager if available
        self.plugin_manager = None
        if PLUGINS_AVAILABLE:
            try:
                self.plugin_manager = PluginManager()
                self.plugin_manager.load_all_plugins()
                self.logger.info(
                    "Plugin system enabled with {len(self.plugin_manager.loaded_plugins)} plugins loaded")
            except Exception as e:
                self.logger.warning(
                    "Failed to initialize plugin manager: {e}")
        else:
            self.logger.warning("Plugin system not available")

        # Load or create default configs
        self.ensure_default_configs()

    def ensure_default_configs(self):
        """Ensure default configuration files exist."""

        # Create default printer config (Bambu Lab P1S)
        bambu_config_path = self.config_dir / "bambu_p1s.yaml"
        if not bambu_config_path.exists():
            self.create_bambu_p1s_config()

        # Create default PLA material config
        pla_config_path = self.config_dir / "pla_basic.yaml"
        if not pla_config_path.exists():
            self.create_pla_material_config()

        # Create default slicing config
        slicing_config_path = self.config_dir / "default_slicing.yaml"
        if not slicing_config_path.exists():
            self.create_default_slicing_config()

        # Load defaults
        self.load_printer_config("bambu_p1s")
        self.load_material_config("pla_basic")
        self.load_slicing_config("default_slicing")

    def create_bambu_p1s_config(self):
        """Create Bambu Lab P1S printer configuration."""
        config = PrinterConfig(
            name="Bambu Lab P1S",
            bed_size_x=256.0,
            bed_size_y=256.0,
            bed_size_z=256.0,
            nozzle_diameter=0.4,
            max_temp_hotend=300,
            max_temp_bed=120,
            max_feedrate_x=20000,
            max_feedrate_y=20000,
            max_feedrate_z=1000,
            firmware_type="bambu",
            supports_nonplanar=True,  # Experimental!
            experimental_features=["nonplanar_slicing", "ai_optimization"]
        )

        # Add safety disclaimer to config
        config_data = asdict(config)
        config_data['_disclaimer'] = {
            'warning': 'SlicerGPT assumes NO LIABILITY for printer damage or injury',
            'experimental_notice': 'Non-planar slicing is EXPERIMENTAL - use at your own risk',
            'verification_required': 'Always verify G-code before printing',
            'liability': 'Use of this configuration is at your own risk'}

        self.save_yaml_config(config_data, "bambu_p1s.yaml")

    def create_pla_material_config(self):
        """Create basic PLA material configuration."""
        config = MaterialConfig(
            name="PLA Basic",
            type="PLA",
            temp_hotend=210,
            temp_bed=60,
            fan_speed=100,
            retraction_distance=0.8,
            retraction_speed=35,
            linear_advance=0.05,
            ai_optimized=True,
            safety_notes=[
                "Ensure adequate ventilation",
                "Monitor first layer adhesion",
                "Verify temperatures before printing"
            ]
        )

        config_data = asdict(config)
        config_data['_disclaimer'] = {
            'warning': 'Material settings generated by AI - verify before use',
            'temperature_safety': 'Incorrect temperatures may damage printer or cause injury',
            'liability': 'SlicerGPT assumes no liability for material-related issues'}

        self.save_yaml_config(config_data, "pla_basic.yaml")

    def create_default_slicing_config(self):
        """Create default slicing configuration."""
        config = SlicingConfig(
            layer_height=0.2,
            first_layer_height=0.25,
            infill_percentage=20,
            infill_pattern="gyroid",
            perimeters=2,
            top_solid_layers=4,
            bottom_solid_layers=3,
            support_enabled=True,
            support_threshold=45.0,
            ai_optimization=True,
            experimental_features={
                "nonplanar_slicing": False,
                "ai_generated_supports": True,
                "adaptive_infill": True,
                "ghst_optimization": True
            }
        )

        config_data = asdict(config)
        config_data['_disclaimer'] = {
            'warning': 'AI-optimized slicing settings - use at your own risk',
            'experimental_notice': 'Experimental features may cause print failures or damage',
            'verification': 'Always preview and verify sliced output before printing',
            'liability': 'SlicerGPT assumes no liability for print quality or failures'}

        config_data['_safety_notes'] = [
            "Enable developer mode for experimental features",
            "Non-planar slicing requires compatible printer",
            "AI optimizations may produce unexpected results",
            "Always verify G-code output before printing",
            "Monitor first layer and initial print progress"
        ]

        self.save_yaml_config(config_data, "default_slicing.yaml")

    def save_yaml_config(self, config_data: Dict[str, Any], filename: str):
        """Save configuration data to YAML file."""
        file_path = self.config_dir / filename

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # Add header comment with disclaimer
                f.write("  # GHST Configuration File\n")
                f.write("  # WARNING: Use at your own risk - No liability assumed\n")
                f.write("  # Generated by AI - Verify all settings before use\n\n")

                yaml.dump(config_data, f, default_flow_style=False, indent=2)

            self.logger.info("Saved configuration: {filename}")

        except Exception as e:
            self.logger.error("Failed to save config {filename}: {e}")
            raise

    def load_yaml_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration data from YAML file."""
        file_path = self.config_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {filename}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)

            # Ensure we return a dictionary even if file is empty
            if config_data is None:
                config_data = {}

            self.logger.info("Loaded configuration: {filename}")
            return config_data

        except Exception as e:
            self.logger.error("Failed to load config {filename}: {e}")
            raise

    def load_printer_config(self, config_name: str) -> PrinterConfig:
        """Load printer configuration."""
        try:
            config_data = self.load_yaml_config("{config_name}.yaml")
        except FileNotFoundError:
            # Create default config if file doesn't exist
            self.logger.warning(
                "Printer config {config_name}.yaml not found, using defaults")
            config_data = self._get_default_printer_config()

        if config_data is None:
            config_data = self._get_default_printer_config()

        # Remove disclaimer and metadata
        config_data.pop('_disclaimer', None)
        config_data.pop('_safety_notes', None)

        # Ensure all required fields are present
        default_config = self._get_default_printer_config()
        for key, value in default_config.items():
            if key not in config_data:
                config_data[key] = value

        self.current_printer = PrinterConfig(**config_data)
        return self.current_printer

    def load_material_config(self, config_name: str) -> MaterialConfig:
        """Load material configuration."""
        try:
            config_data = self.load_yaml_config("{config_name}.yaml")
        except FileNotFoundError:
            self.logger.warning(
                "Material config {config_name}.yaml not found, using defaults")
            config_data = self._get_default_material_config()

        if config_data is None:
            config_data = self._get_default_material_config()

        # Remove disclaimer and metadata
        config_data.pop('_disclaimer', None)
        config_data.pop('_safety_notes', None)

        # Ensure all required fields are present
        default_config = self._get_default_material_config()
        for key, value in default_config.items():
            if key not in config_data:
                config_data[key] = value

        self.current_material = MaterialConfig(**config_data)
        return self.current_material

    def load_slicing_config(self, config_name: str) -> SlicingConfig:
        """Load slicing configuration."""
        try:
            config_data = self.load_yaml_config("{config_name}.yaml")
        except FileNotFoundError:
            self.logger.warning(
                "Slicing config {config_name}.yaml not found, using defaults")
            config_data = self._get_default_slicing_config()

        if config_data is None:
            config_data = self._get_default_slicing_config()

        # Remove disclaimer and metadata
        config_data.pop('_disclaimer', None)
        config_data.pop('_safety_notes', None)

        # Ensure all required fields are present
        default_config = self._get_default_slicing_config()
        for key, value in default_config.items():
            if key not in config_data:
                config_data[key] = value

        self.current_slicing = SlicingConfig(**config_data)
        return self.current_slicing

    def list_configs(self, config_type: str = "all") -> List[str]:
        """List available configuration files."""
        configs = []

        for file_path in self.config_dir.glob("*.yaml"):
            name = file_path.stem

            if config_type == "all":
                configs.append(name)
            elif config_type == "printer" and any(printer in name.lower()
                                                  for printer in ["bambu", "ender", "prusa", "printer"]):
                configs.append(name)
            elif config_type == "material" and any(material in name.lower()
                                                   for material in ["pla", "abs", "petg", "material"]):
                configs.append(name)
            elif config_type == "slicing" and "slicing" in name.lower():
                configs.append(name)

        return sorted(configs)

    def _get_default_printer_config(self) -> Dict[str, Any]:
        """Get default printer configuration."""
        return {
            'name': 'Generic Printer',
            'bed_size_x': 220.0,
            'bed_size_y': 220.0,
            'bed_size_z': 250.0,
            'nozzle_diameter': 0.4,
            'max_temp_hotend': 250,
            'max_temp_bed': 80,
            'max_feedrate_x': 150,
            'max_feedrate_y': 150,
            'max_feedrate_z': 10,
            'firmware_type': 'marlin',
            'supports_nonplanar': False,
            'experimental_features': []
        }

    def _get_default_material_config(self) -> Dict[str, Any]:
        """Get default material configuration."""
        return {
            'name': 'Generic PLA',
            'type': 'PLA',
            'temp_hotend': 200,
            'temp_bed': 60,
            'fan_speed': 100,
            'retraction_distance': 1.0,
            'retraction_speed': 40,
            'linear_advance': 0.0,
            'ai_optimized': False,
            'safety_notes': []
        }

    def _get_default_slicing_config(self) -> Dict[str, Any]:
        """Get default slicing configuration."""
        return {
            'layer_height': 0.2,
            'first_layer_height': 0.3,
            'infill_percentage': 20,
            'infill_pattern': 'honeycomb',
            'perimeters': 3,
            'top_solid_layers': 3,
            'bottom_solid_layers': 3,
            'support_enabled': True,
            'support_threshold': 45.0,
            'ai_optimization': True,
            'experimental_features': {
                "nonplanar_slicing": False,
                "ai_generated_supports": True,
                "adaptive_infill": True,
                "ghst_optimization": True
            }
        }

    def get_experimental_features(self) -> Dict[str, bool]:
        """Get current experimental feature settings."""
        if not self.current_slicing:
            return {}

        return self.current_slicing.experimental_features.copy()

    def enable_experimental_feature(self, feature: str, enabled: bool = True):
        """Enable/disable experimental feature with safety check."""
        if not self.current_slicing:
            raise ValueError("No slicing configuration loaded")

        if feature not in self.current_slicing.experimental_features:
            raise ValueError("Unknown experimental feature: {feature}")

        self.current_slicing.experimental_features[feature] = enabled

        # Log safety warning
        if enabled:
            self.logger.warning(
                "⚠️  Experimental feature '{feature}' ENABLED - Use at your own risk!")
        else:
            self.logger.info("Experimental feature '{feature}' disabled")

    # Plugin Management Methods
    def get_plugin_manager(self):
        """Get the plugin manager instance."""
        return self.plugin_manager

    def get_available_plugins(self) -> Dict[str, Any]:
        """Get information about all available plugins."""
        if not self.plugin_manager:
            return {}
        return self.plugin_manager.get_plugin_status()

    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a specific plugin."""
        if not self.plugin_manager:
            self.logger.warning("Plugin system not available")
            return False

        result = self.plugin_manager.enable_plugin(plugin_name)
        if result:
            self.logger.warning(
                "⚠️ Plugin '{plugin_name}' ENABLED - Use at your own risk!")
        return result

    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a specific plugin."""
        if not self.plugin_manager:
            return False

        result = self.plugin_manager.disable_plugin(plugin_name)
        if result:
            self.logger.info("Plugin '{plugin_name}' disabled")
        return result

    def get_plugin_menu_actions(self) -> List[Dict[str, Any]]:
        """Get menu actions from all enabled plugins."""
        if not self.plugin_manager:
            return []
        return self.plugin_manager.get_all_menu_actions()

    def call_plugin_hook(self, hook_name: str, *args, **kwargs):
        """Call a plugin hook on all enabled plugins."""
        if self.plugin_manager:
            self.plugin_manager.call_plugin_hook(hook_name, *args, **kwargs)

    def process_mesh_with_plugins(self, mesh_data: Any) -> Any:
        """Process mesh data through enabled plugins."""
        if self.plugin_manager:
            return self.plugin_manager.process_mesh_through_plugins(mesh_data)
        return mesh_data

    def process_gcode_with_plugins(self, gcode_lines: List[str]) -> List[str]:
        """Process G-code through enabled plugins."""
        if self.plugin_manager:
            return self.plugin_manager.process_gcode_through_plugins(
                gcode_lines)
        return gcode_lines

    def validate_config_safety(self) -> List[str]:
        """Validate current configuration for safety issues."""
        warnings = []

        if self.current_printer:
            # Check for dangerous temperature settings
            if hasattr(self.current_material, 'temp_hotend'):
                if self.current_material.temp_hotend > self.current_printer.max_temp_hotend:
                    warnings.append(
                        f"⚠️  Material hotend temp ({self.current_material.temp_hotend}°C) exceeds printer max ({self.current_printer.max_temp_hotend}°C)")

            if hasattr(self.current_material, 'temp_bed'):
                if self.current_material.temp_bed > self.current_printer.max_temp_bed:
                    warnings.append(
                        f"⚠️  Material bed temp ({self.current_material.temp_bed}°C) exceeds printer max ({self.current_printer.max_temp_bed}°C)")

        if self.current_slicing:
            # Check for experimental features
            enabled_experimental = [
                feature for feature,
                enabled in self.current_slicing.experimental_features.items() if enabled]

            if enabled_experimental:
                features_list = ', '.join(enabled_experimental)
                warnings.append(
                    f"⚠️  Experimental features enabled: {features_list}")

            # Check for non-planar slicing
            if self.current_slicing.experimental_features.get(
                    "nonplanar_slicing", False):
                if not self.current_printer or not self.current_printer.supports_nonplanar:
                    warnings.append(
                        "🚨 Non-planar slicing enabled but printer may not support it!")

        return warnings

    def export_config_bundle(self, output_path: str):
        """Export all current configurations as a bundle."""
        bundle = {
            'version': '1.0.0',
            'generated_by': 'SlicerGPT',
            'timestamp': str(
                Path().cwd()),
            'disclaimer': {
                'warning': 'SlicerGPT assumes NO LIABILITY for any damage or injury',
                'experimental': 'Configuration contains experimental features - use at own risk',
                'verification': 'Verify all settings before printing'},
            'printer': asdict(
                self.current_printer) if self.current_printer else None,
            'material': asdict(
                self.current_material) if self.current_material else None,
            'slicing': asdict(
                self.current_slicing) if self.current_slicing else None}

        with open(output_path, 'w') as f:
            yaml.dump(bundle, f, default_flow_style=False, indent=2)

        self.logger.info("Exported configuration bundle: {output_path}")

    def get_config_summary(self) -> str:
        """Get a human-readable summary of current configuration."""
        summary = ["📊 Current SlicerGPT Configuration:\n"]

        if self.current_printer:
            summary.append(f"🖨️  Printer: {self.current_printer.name}")
            bed_info = f"{self.current_printer.bed_size_x}×{self.current_printer.bed_size_y}×{self.current_printer.bed_size_z}mm"
            summary.append(f"   Bed: {bed_info}")
            summary.append(
                f"   Nozzle: {self.current_printer.nozzle_diameter}mm\n")

        if self.current_material:
            summary.append(
                f"🧱 Material: {self.current_material.name} ({self.current_material.type})")
            summary.append(
                f"   Hotend: {self.current_material.temp_hotend}°C, Bed: {self.current_material.temp_bed}°C\n")

        if self.current_slicing:
            summary.append(
                f"⚡ Slicing: {self.current_slicing.layer_height}mm layers, {self.current_slicing.infill_percentage}% infill")

            enabled_experimental = [
                feature for feature,
                enabled in self.current_slicing.experimental_features.items() if enabled]
            if enabled_experimental:
                features_str = ', '.join(enabled_experimental)
                summary.append(
                    f"🧪 Experimental: {features_str}")

        # Add safety warnings
        warnings = self.validate_config_safety()
        if warnings:
            summary.append("\n⚠️  Safety Warnings:")
            summary.extend(["   {warning}" for warning in warnings])

        summary.append(
            "\n💡 Remember: SlicerGPT assumes no liability - verify all settings!")

        return "\n".join(summary)
