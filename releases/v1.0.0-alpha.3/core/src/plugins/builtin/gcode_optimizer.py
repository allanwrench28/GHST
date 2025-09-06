"""
G-code Optimizer Plugin

An experimental plugin that optimizes G-code for better print quality.
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

class GcodeOptimizerPlugin(BasePlugin):
    """Plugin for optimizing G-code output."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="G-code Optimizer",
            version="1.0.0",
            author="GHST Team",
            description="Experimental G-code optimizer for improved print quality and reduced print time",
            category="coding engine",
            requires_gui=False,
            experimental=True,
            safety_notes=[
                "EXPERIMENTAL: May modify G-code in unexpected ways",
                "Always verify G-code before printing",
                "Use at your own risk - may affect print quality",
                "Test on non-critical prints first"])

    def initialize(self) -> bool:
        """Initialize the plugin."""
        self.logger.warning(
            "⚠️ G-code Optimizer plugin initialized - EXPERIMENTAL!")
        self.optimization_count = 0
        return True

    def cleanup(self) -> bool:
        """Clean up plugin resources."""
        self.logger.info("G-code Optimizer plugin cleaned up")
        return True

    def process_gcode(self, gcode_lines: List[str]) -> List[str]:
        """Optimize G-code lines."""
        if not self.active:
            return gcode_lines

        self.logger.info("Optimizing G-code...")
        optimized_lines = []

        for line in gcode_lines:
            # Example optimizations (very basic)
            line = line.strip()

            # Skip empty lines and comments (except important ones)
            if not line or (line.startswith(';') and 'GHST' not in line):
                continue

            # Simple optimization: remove redundant moves
            if line.startswith(
                    'G1') and 'X' not in line and 'Y' not in line and 'Z' not in line:
                # Skip moves that only change extrusion without position
                continue

            optimized_lines.append(line)

        self.optimization_count += 1
        reduction = len(gcode_lines) - len(optimized_lines)

        self.logger.info(
            "G-code optimization complete: removed {reduction} lines ({
                reduction / len(gcode_lines) * 100:.1f}%)")

        # Add optimization header
        header = [
            "; GHST G-code Optimizer Plugin",
            "; Optimization #{self.optimization_count}",
            "; Removed {reduction} lines for efficiency",
            "; ⚠️ EXPERIMENTAL - verify before printing!",
            ""
        ]

        return header + optimized_lines

    def get_menu_actions(self) -> List[Dict[str, Any]]:
        """Return menu actions for this plugin."""
        return [
            {
                'name': 'Toggle G-code Optimization',
                'callback': self.toggle_optimization
            }
        ]

    def toggle_optimization(self):
        """Toggle optimization on/off."""
        self.active = not self.active
        status = "ENABLED" if self.active else "DISABLED"
        self.logger.warning("⚠️ G-code optimization {status}")
        print("G-code optimization {status}")

        if self.active:
            print("⚠️ WARNING: Experimental optimization enabled!")
            print("   - Always verify G-code before printing")
            print("   - Test on non-critical prints first")
