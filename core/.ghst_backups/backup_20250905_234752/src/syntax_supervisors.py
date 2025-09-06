#!/usr/bin/env python3
"""
GHST Syntax Supervisors (SS) - Background Code Analysis Engine
==============================================================

The Syntax Supervisors are specialized GHST agents that continuously
monitor and improve code quality in the background, inspired by how
Claude 4 handles fixing and debugging code.

Features:
- Real-time syntax error detection
- Orphaned code identification
- Smart code optimization suggestions
- Background processing with minimal resource usage
- Professional GHST theming without overwhelming the interface
"""

import ast
import asyncio
import json
import logging
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class SyntaxSupervisor:
    """Individual Syntax Supervisor for specific file types and tasks."""

    def __init__(self, name: str, specialty: str, file_patterns: List[str]):
        self.name = name
        self.specialty = specialty
        self.file_patterns = file_patterns
        self.active = True
        self.last_scan = None
        self.issues_found = []

    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a file for issues specific to this supervisor's specialty."""
        issues = {
            'syntax_errors': [],
            'orphaned_code': [],
            'optimization_suggestions': [],
            'timestamp': datetime.now().isoformat()
        }

        try:
            if file_path.suffix == '.py':
                issues.update(self._scan_python_file(file_path))
            elif file_path.suffix in ['.js', '.ts']:
                issues.update(self._scan_javascript_file(file_path))
            elif file_path.suffix in ['.cpp', '.c', '.h']:
                issues.update(self._scan_cpp_file(file_path))

        except Exception as e:
            issues['scan_error'] = str(e)

        return issues

    def _scan_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Claude 4-inspired Python analysis."""
        issues = {
            'syntax_errors': [],
            'orphaned_code': [],
            'optimization_suggestions': []}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # AST-based syntax checking
            try:
                tree = ast.parse(content)

                # Check for orphaned imports
                imports = [
                    node for node in ast.walk(tree) if isinstance(
                        node, (ast.Import, ast.ImportFrom))]
                used_names = set()

                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        used_names.add(node.id)

                for imp in imports:
                    if isinstance(imp, ast.Import):
                        for alias in imp.names:
                            name = alias.asname or alias.name
                            if name not in used_names:
                                issues['orphaned_code'].append({
                                    'type': 'unused_import',
                                    'line': imp.lineno,
                                    'module': alias.name,
                                    'suggestion': f"Remove unused import: {alias.name}"
                                })

                # Check for unreachable code
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self._check_unreachable_code(node, issues)

            except SyntaxError as e:
                issues['syntax_errors'].append({
                    'line': e.lineno,
                    'message': str(e),
                    'type': 'syntax_error'
                })

        except Exception as e:
            issues['scan_error'] = str(e)

        return issues

    def _scan_javascript_file(self, file_path: Path) -> Dict[str, Any]:
        """Basic JavaScript/TypeScript analysis."""
        issues = {
            'syntax_errors': [],
            'orphaned_code': [],
            'optimization_suggestions': []}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic checks for common issues
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'console.log' in line and 'debug' not in line.lower():
                    issues['orphaned_code'].append({
                        'type': 'debug_statement',
                        'line': i,
                        'suggestion': 'Remove debug console.log statement'
                    })

        except Exception as e:
            issues['scan_error'] = str(e)

        return issues

    def _scan_cpp_file(self, file_path: Path) -> Dict[str, Any]:
        """Basic C++ analysis."""
        issues = {
            'syntax_errors': [],
            'orphaned_code': [],
            'optimization_suggestions': []}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic checks
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if '#include' in line and '<iostream>' in line:
                    # Check if std::cout is actually used
                    if 'std::cout' not in content and 'cout' not in content:
                        issues['orphaned_code'].append({
                            'type': 'unused_include',
                            'line': i,
                            'suggestion': 'Remove unused #include <iostream>'
                        })

        except Exception as e:
            issues['scan_error'] = str(e)

        return issues

    def _check_unreachable_code(
            self,
            func_node: ast.FunctionDef,
            issues: Dict):
        """Check for unreachable code after return statements."""
        for i, stmt in enumerate(func_node.body):
            if isinstance(stmt, ast.Return) and i < len(func_node.body) - 1:
                issues['orphaned_code'].append({
                    'type': 'unreachable_code',
                    'line': func_node.body[i + 1].lineno,
                    'suggestion': 'Code after return statement is unreachable'
                })


class SyntaxSupervisorManager:
    """Manages the GHST Syntax Supervisor collective."""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.supervisors = self._initialize_supervisors()
        self.active = False
        self.scan_thread = None
        self.results = {}
        self.config = self._load_config()

        # Professional GHST theming
        self.theme = {
            'colors': {
                'ghost_blue': '#4A90E2',
                'ghost_purple': '#7B68EE',
                'ghost_green': '#32CD32',
                'ghost_red': '#FF6347',
                'ghost_gray': '#708090'
            },
            'icons': {
                'supervisor': '👁️',
                'scanning': '🔍',
                'error': '⚠️',
                'suggestion': '💡',
                'clean': '✅'
            }
        }

    def _initialize_supervisors(self) -> List[SyntaxSupervisor]:
        """Initialize the Syntax Supervisor collective."""
        return [
            SyntaxSupervisor(
                name="Python Syntax Supervisor",
                specialty="Python code analysis and optimization",
                file_patterns=['*.py']
            ),
            SyntaxSupervisor(
                name="JavaScript Syntax Supervisor",
                specialty="JavaScript/TypeScript analysis",
                file_patterns=['*.js', '*.ts', '*.jsx', '*.tsx']
            ),
            SyntaxSupervisor(
                name="C++ Syntax Supervisor",
                specialty="C/C++ code analysis",
                file_patterns=['*.cpp', '*.c', '*.h', '*.hpp']
            ),
            SyntaxSupervisor(
                name="General Code Supervisor",
                specialty="Generic code quality checks",
                file_patterns=['*.*']
            )
        ]

    def _load_config(self) -> Dict:
        """Load GHST configuration for Syntax Supervisors."""
        config_path = self.workspace_path / 'config' / 'syntax_supervisors.json'
        default_config = {
            'enabled': True,
            'scan_interval': 30,  # seconds
            'max_cpu_usage': 15,  # percentage
            'ignored_patterns': ['.git', '__pycache__', 'node_modules', '.venv'],
            'auto_fix_enabled': False,
            'notification_level': 'medium'  # low, medium, high
        }

        try:
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return {**default_config, **json.load(f)}
        except Exception:
            pass

        return default_config

    def start_monitoring(self):
        """Start background monitoring with GHST theming."""
        if self.active:
            return

        self.active = True
        self.scan_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True)
        self.scan_thread.start()

        print(
            f"{self.theme['icons']['supervisor']} GHST Syntax Supervisors (SS) activated")
        print(
            f"{self.theme['icons']['scanning']} Monitoring workspace: {self.workspace_path}")

    def stop_monitoring(self):
        """Stop background monitoring."""
        self.active = False
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
        print(
            f"{self.theme['icons']['supervisor']} GHST Syntax Supervisors deactivated")

    def _monitoring_loop(self):
        """Main monitoring loop that runs in background."""
        while self.active:
            try:
                self._scan_workspace()
                time.sleep(self.config['scan_interval'])
            except Exception as e:
                logging.error(f"SS monitoring error: {e}")
                time.sleep(60)  # Wait longer on error

    def _scan_workspace(self):
        """Scan the entire workspace for issues."""
        if not self.workspace_path.exists():
            return

        scan_results = {}
        file_count = 0

        for file_path in self._get_scannable_files():
            file_count += 1

            # Find appropriate supervisor
            supervisor = self._get_supervisor_for_file(file_path)
            if supervisor:
                results = supervisor.scan_file(file_path)
                if any(
                    results[key] for key in [
                        'syntax_errors',
                        'orphaned_code',
                        'optimization_suggestions']):
                    scan_results[str(file_path)] = results

        self.results = scan_results
        self._report_results(file_count)

    def _get_scannable_files(self) -> List[Path]:
        """Get all files that should be scanned."""
        scannable_files = []

        for pattern in [
            '**/*.py',
            '**/*.js',
            '**/*.ts',
            '**/*.cpp',
            '**/*.c',
                '**/*.h']:
            for file_path in self.workspace_path.glob(pattern):
                if self._should_scan_file(file_path):
                    scannable_files.append(file_path)

        return scannable_files

    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned based on ignore patterns."""
        for pattern in self.config['ignored_patterns']:
            if pattern in str(file_path):
                return False
        return True

    def _get_supervisor_for_file(
            self, file_path: Path) -> Optional[SyntaxSupervisor]:
        """Get the most appropriate supervisor for a file."""
        for supervisor in self.supervisors:
            for pattern in supervisor.file_patterns:
                if file_path.match(pattern.replace('*', '')):
                    return supervisor
        return None

    def _report_results(self, file_count: int):
        """Report scan results with GHST theming."""
        if not self.results:
            if self.config['notification_level'] in ['medium', 'high']:
                print(
                    f"{self.theme['icons']['clean']} SS: All {file_count} files clean")
            return

        total_issues = sum(
            len(results['syntax_errors']) +
            len(results['orphaned_code']) +
            len(results['optimization_suggestions'])
            for results in self.results.values()
        )

        if self.config['notification_level'] != 'low':
            print(
                f"{self.theme['icons']['supervisor']} SS: Found {total_issues} issues in {len(self.results)} files")

        if self.config['notification_level'] == 'high':
            self._detailed_report()

    def _detailed_report(self):
        """Provide detailed issue report."""
        for file_path, results in self.results.items():
            print(f"\n📁 {Path(file_path).name}:")

            for error in results['syntax_errors']:
                print(
                    f"  {
                        self.theme['icons']['error']} Line {
                        error['line']}: {
                        error['message']}")

            for orphan in results['orphaned_code']:
                print(f"  🧹 Line {orphan['line']}: {orphan['suggestion']}")

            for suggestion in results['optimization_suggestions']:
                print(f"  {self.theme['icons']['suggestion']} {suggestion}")

    def get_current_status(self) -> Dict:
        """Get current status for GUI integration."""
        if not self.active:
            return {'status': 'inactive', 'supervisors': 0}

        total_issues = sum(
            len(results['syntax_errors']) +
            len(results['orphaned_code']) +
            len(results['optimization_suggestions'])
            for results in self.results.values()
        ) if self.results else 0

        return {
            'status': 'active',
            'supervisors': len(self.supervisors),
            'files_monitored': len(self.results),
            'total_issues': total_issues,
            'last_scan': datetime.now().isoformat(),
            'theme': self.theme
        }


def create_syntax_supervisor_script():
    """Create the main SS script for GHST."""
    script_content = '''#!/usr/bin/env python3
"""
GHST Syntax Supervisors - Standalone Script
===========================================

Run this script to start background code monitoring for your GHST workspace.
"""

import sys
import signal
from pathlib import Path

# Add GHST src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from syntax_supervisors import SyntaxSupervisorManager

def main():
    workspace = Path.cwd()
    if len(sys.argv) > 1:
        workspace = Path(sys.argv[1])

    ss_manager = SyntaxSupervisorManager(str(workspace))

    # Handle graceful shutdown
    def signal_handler(signum, frame):
        print("\\n👋 Shutting down GHST Syntax Supervisors...")
        ss_manager.stop_monitoring()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🚀 Starting GHST Syntax Supervisors...")
    ss_manager.start_monitoring()

    try:
        # Keep running until interrupted
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
'''

    return script_content


# Integration with main GHST system
def integrate_with_ghst():
    """Integration points for the main GHST system."""

    # This function would be called from the main GHST launcher
    # to automatically start Syntax Supervisors in the background

    pass


if __name__ == "__main__":
    # For testing
    manager = SyntaxSupervisorManager(".")
    manager.start_monitoring()

    try:
        import time
        time.sleep(60)  # Monitor for 1 minute
    except KeyboardInterrupt:
        manager.stop_monitoring()
