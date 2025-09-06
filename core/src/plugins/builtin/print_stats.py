"""
Print Statistics Plugin

A simple example plugin that calculates and displays print statistics.
"""

from typing import Dict, Any, List

# Simple approach - try to import BasePlugin from different possible locations
BasePlugin = None
PluginMetadata = None

# Try different import paths
for import_path in [
    "base_plugin",
    "plugins.base_plugin",
    "src.plugins.base_plugin"
]:
    try:
        module = __import__(
            import_path, fromlist=[
                'BasePlugin', 'PluginMetadata'])
        BasePlugin = getattr(module, 'BasePlugin', None)
        PluginMetadata = getattr(module, 'PluginMetadata', None)
        if BasePlugin and PluginMetadata:
            break
    except ImportError:
        continue

# If we still don't have BasePlugin, we can't proceed
if not BasePlugin or not PluginMetadata:
    raise ImportError("Could not import BasePlugin and PluginMetadata")

class PrintStatsPlugin(BasePlugin):
    """Plugin for calculating print statistics."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Print Statistics",
            version="1.0.0",
            author="GHST Team",
            description="Calculates detailed print statistics including time, material usage, and cost estimates",
            category="analysis",
            requires_gui=True,
            experimental=False,
            safety_notes=[
                "Statistics are estimates only",
                "Actual print times may vary",
                "Cost calculations require manual price input"])

    def initialize(self) -> bool:
        """Initialize the plugin."""
        self.logger.info("Print Statistics plugin initialized")
        self.stats = {}
        return True

    def cleanup(self) -> bool:
        """Clean up plugin resources."""
        self.logger.info("Print Statistics plugin cleaned up")
        return True

    def get_menu_actions(self) -> List[Dict[str, Any]]:
        """Return menu actions for this plugin."""
        return [
            {
                'name': 'Show Print Statistics',
                'callback': self.show_statistics,
                'shortcut': 'Ctrl+Shift+S'
            }
        ]

    def on_slicing_completed(
            self, gcode_lines: List[str], stats: Dict[str, Any]):
        """Calculate statistics when slicing completes."""
        try:
            self.stats = self._calculate_stats(gcode_lines, stats)
            self.logger.info("Calculated print statistics: {self.stats}")
        except Exception as e:
            self.logger.error("Failed to calculate statistics: {e}")

    def _calculate_stats(self,
                         gcode_lines: List[str],
                         basic_stats: Dict[str,
                                           Any]) -> Dict[str,
                                                         Any]:
        """Calculate detailed statistics from G-code."""
        stats = {
            'total_lines': len(gcode_lines),
            'estimated_time_minutes': basic_stats.get(
                'estimated_print_time',
                0),
            'layer_count': basic_stats.get(
                'layers',
                0),
            'estimated_filament_length': 0,
            'estimated_filament_weight': 0,
            'estimated_cost': 0}

        # Simple filament calculation (mock implementation)
        extrusion_moves = sum(
            1 for line in gcode_lines if line.startswith('G1') and 'E' in line)
        stats['estimated_filament_length'] = extrusion_moves * 0.5  # mm
        # grams
        stats['estimated_filament_weight'] = stats['estimated_filament_length'] * 0.00125
        stats['estimated_cost'] = stats['estimated_filament_weight'] * \
            0.02  # $0.02/gram

        return stats

    def show_statistics(self):
        """Show statistics dialog."""
        if not self.stats:
            self.logger.warning(
                "No statistics available - slice a model first")
            return

        # In a real implementation, this would show a GUI dialog
        print("\n" + "=" * 50)
        print("PRINT STATISTICS")
        print("=" * 50)
        print("Total G-code lines: {self.stats['total_lines']}")
        print(
            "Estimated print time: {
                self.stats['estimated_time_minutes']:.1f} minutes")
        print("Layer count: {self.stats['layer_count']}")
        print(
            "Estimated filament: {
                self.stats['estimated_filament_length']:.1f} mm")
        print(
            "Estimated weight: {
                self.stats['estimated_filament_weight']:.2f} g")
        print("Estimated cost: ${self.stats['estimated_cost']:.2f}")
        print("=" * 50)

        self.logger.info("Displayed print statistics")
