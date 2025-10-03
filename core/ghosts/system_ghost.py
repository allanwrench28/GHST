"""
System Ghost - System Management and Monitoring

The system ghost manages GHST infrastructure, monitors system health,
and handles plugin management operations.
"""

import logging
from typing import Dict, Optional, Any
from .base_ghost import BaseGhost


class SystemGhost(BaseGhost):
    """System management ghost for GHST."""
    
    def __init__(self):
        """Initialize the system ghost."""
        super().__init__(
            ghost_id="system_ghost",
            name="System Manager",
            specialization="System Management & Monitoring"
        )
        self.system_metrics = {}
        
    def process_query(self, query: str, context: Optional[Dict] = None) -> str:
        """Process system-related queries.
        
        Args:
            query: User query
            context: Additional context
            
        Returns:
            System response
        """
        query_lower = query.lower()
        
        if "status" in query_lower or "health" in query_lower:
            return self._get_system_status(context)
        elif "plugin" in query_lower or "expertise" in query_lower:
            return self._get_plugin_status(context)
        elif "memory" in query_lower or "cache" in query_lower:
            return self._get_memory_status(context)
        else:
            return "System Ghost: I can help with system status, plugin management, and resource monitoring."
            
    def _get_system_status(self, context: Optional[Dict] = None) -> str:
        """Get system status report.
        
        Args:
            context: System context
            
        Returns:
            Status report
        """
        report = ["🔧 GHST System Status Report\n"]
        report.append("=" * 40)
        
        if context:
            if 'ghost_count' in context:
                report.append(f"👻 Active Ghosts: {context['ghost_count']}")
            if 'plugin_count' in context:
                report.append(f"🔌 Loaded Plugins: {context['plugin_count']}")
            if 'memory_usage' in context:
                report.append(f"🧠 Memory Usage: {context['memory_usage']}")
        else:
            report.append("✅ System operational")
            report.append("⚙️  All core components initialized")
            
        return "\n".join(report)
        
    def _get_plugin_status(self, context: Optional[Dict] = None) -> str:
        """Get plugin status report.
        
        Args:
            context: Plugin context
            
        Returns:
            Plugin status
        """
        if context and 'loaded_plugins' in context:
            plugins = context['loaded_plugins']
            report = [f"🔌 Loaded Expertise Plugins ({len(plugins)}):\n"]
            for plugin in plugins:
                report.append(f"  ✓ {plugin}")
            return "\n".join(report)
        return "No expertise plugins currently loaded."
        
    def _get_memory_status(self, context: Optional[Dict] = None) -> str:
        """Get memory/cache status.
        
        Args:
            context: Memory context
            
        Returns:
            Memory status
        """
        if context and 'memory_stats' in context:
            stats = context['memory_stats']
            return f"🧠 Memory: {stats.get('fragments', 0)} fragments, {stats.get('size_mb', 0):.2f} MB"
        return "Memory system operational"
        
    def get_capabilities(self) -> Dict[str, Any]:
        """Get system ghost capabilities.
        
        Returns:
            Capabilities dictionary
        """
        return {
            "type": "system",
            "specialization": self.specialization,
            "capabilities": [
                "System health monitoring",
                "Plugin management",
                "Resource tracking",
                "Error reporting"
            ],
            "features": {
                "real_time_monitoring": True,
                "auto_diagnostics": True,
                "plugin_lifecycle": True
            }
        }
        
    def log_metric(self, metric_name: str, value: Any):
        """Log a system metric.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
        """
        self.system_metrics[metric_name] = {
            "value": value,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        self.logger.debug(f"Logged metric: {metric_name} = {value}")
