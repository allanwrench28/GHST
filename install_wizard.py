#!/usr/bin/env python3
"""
GHST Installation Wizard
========================

Comprehensive installation wizard for GHST - AI Coding Engine
Handles prerequisites, dependencies, configuration, and setup.

This wizard provides both interactive and automated installation modes.
"""

import sys
import os
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InstallWizard:
    """Main installation wizard class."""
    
    def __init__(self):
        self.install_dir = Path.cwd()
        self.python_version = sys.version_info
        self.system = platform.system()
        self.config = {}
        
    def print_header(self, text: str):
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")
    
    def print_error(self, text: str):
        """Print an error message."""
        print(f"{Colors.RED}❌ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")
    
    def check_prerequisites(self) -> bool:
        """Check system prerequisites."""
        self.print_header("Checking Prerequisites")
        
        all_ok = True
        
        # Check Python version
        if self.python_version >= (3, 8):
            self.print_success(f"Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        else:
            self.print_error(f"Python 3.8+ required (found {self.python_version.major}.{self.python_version.minor})")
            all_ok = False
        
        # Check pip
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         capture_output=True, check=True)
            self.print_success("pip is installed")
        except subprocess.CalledProcessError:
            self.print_error("pip is not available")
            all_ok = False
        
        # Check git
        try:
            subprocess.run(['git', '--version'], 
                         capture_output=True, check=True)
            self.print_success("git is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_warning("git not found (optional but recommended)")
        
        # Check disk space
        stat = shutil.disk_usage(self.install_dir)
        free_gb = stat.free / (1024**3)
        if free_gb > 1:
            self.print_success(f"Disk space: {free_gb:.1f} GB available")
        else:
            self.print_warning(f"Low disk space: {free_gb:.1f} GB available")
        
        return all_ok
    
    def get_user_input(self, prompt: str, default: str = "") -> str:
        """Get user input with a default value."""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    
    def get_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Get yes/no input from user."""
        default_str = "Y/n" if default else "y/N"
        while True:
            response = input(f"{prompt} [{default_str}]: ").strip().lower()
            if not response:
                return default
            if response in ['y', 'yes']:
                return True
            if response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")
    
    def configure_installation(self):
        """Interactive configuration."""
        self.print_header("Installation Configuration")
        
        # Installation type
        print("\nSelect installation type:")
        print("1. Full Installation (Recommended)")
        print("2. Core Only (Minimal)")
        print("3. Development Mode (Full + Dev Tools)")
        
        while True:
            choice = self.get_user_input("Enter choice", "1")
            if choice in ['1', '2', '3']:
                break
            print("Please enter 1, 2, or 3")
        
        self.config['install_type'] = {
            '1': 'full',
            '2': 'minimal',
            '3': 'development'
        }[choice]
        
        # Components
        self.config['install_syntax_supervisors'] = self.get_yes_no(
            "\nInstall Syntax Supervisors (background monitoring)", True)
        self.config['install_expert_system'] = self.get_yes_no(
            "Install AI Expert System", True)
        self.config['install_plugins'] = self.get_yes_no(
            "Install Plugin System", True)
        
        # Virtual environment
        self.config['use_venv'] = self.get_yes_no(
            "\nCreate virtual environment (recommended)", True)
        
        # Theme
        print("\nSelect theme:")
        print("1. Ghost Dark (Default)")
        print("2. Ghost Light")
        print("3. Professional")
        theme_choice = self.get_user_input("Enter choice", "1")
        self.config['theme'] = {
            '1': 'ghost_dark',
            '2': 'ghost_light',
            '3': 'professional'
        }.get(theme_choice, 'ghost_dark')
        
        # Summary
        self.print_header("Configuration Summary")
        print(f"Installation Type: {self.config['install_type']}")
        print(f"Syntax Supervisors: {'Yes' if self.config['install_syntax_supervisors'] else 'No'}")
        print(f"Expert System: {'Yes' if self.config['install_expert_system'] else 'No'}")
        print(f"Plugin System: {'Yes' if self.config['install_plugins'] else 'No'}")
        print(f"Virtual Environment: {'Yes' if self.config['use_venv'] else 'No'}")
        print(f"Theme: {self.config['theme']}")
        
        if not self.get_yes_no("\nProceed with installation?", True):
            self.print_info("Installation cancelled by user")
            sys.exit(0)
    
    def create_directories(self):
        """Create necessary directory structure."""
        self.print_header("Creating Directory Structure")
        
        directories = [
            'logs',
            'exports',
            'backups',
            'config/user',
            'plugins/custom',
            'experts/custom',
        ]
        
        for directory in directories:
            dir_path = self.install_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.print_success(f"Created: {directory}")
    
    def setup_virtual_environment(self):
        """Set up Python virtual environment."""
        if not self.config.get('use_venv', True):
            return
        
        self.print_header("Setting Up Virtual Environment")
        
        venv_path = self.install_dir / 'venv'
        
        if venv_path.exists():
            self.print_warning("Virtual environment already exists")
            return
        
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)],
                         check=True)
            self.print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            raise
    
    def install_dependencies(self):
        """Install Python dependencies."""
        self.print_header("Installing Dependencies")
        
        # Determine which requirements file to use
        req_file = self.install_dir / 'core' / 'requirements.txt'
        if not req_file.exists():
            req_file = self.install_dir / 'requirements.txt'
        
        if not req_file.exists():
            self.print_warning("No requirements.txt found, skipping dependency installation")
            return
        
        self.print_info(f"Installing from: {req_file}")
        
        try:
            # Use pip to install requirements
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                '--upgrade', 'pip'
            ], check=True, capture_output=True)
            self.print_success("Updated pip")
            
            subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                '-r', str(req_file)
            ], check=True)
            self.print_success("Dependencies installed")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e}")
            self.print_info("You may need to install dependencies manually:")
            self.print_info(f"  pip install -r {req_file}")
    
    def create_configuration(self):
        """Create default configuration files."""
        self.print_header("Creating Configuration")
        
        config_dir = self.install_dir / 'config' / 'user'
        config_file = config_dir / 'settings.yaml'
        
        config_content = f"""# GHST User Configuration
# Generated by install wizard

app:
  name: "GHST - AI Coding Engine"
  version: "1.0.0"
  theme: "{self.config.get('theme', 'ghost_dark')}"
  auto_save: true

expert_system:
  enabled: {str(self.config.get('install_expert_system', True)).lower()}
  max_concurrent_experts: 8
  response_timeout: 30

syntax_supervisors:
  enabled: {str(self.config.get('install_syntax_supervisors', True)).lower()}
  scan_interval: 30
  notification_level: "medium"

plugins:
  enabled: {str(self.config.get('install_plugins', True)).lower()}
  auto_load: true
  custom_plugin_dirs:
    - "plugins/custom"

experts:
  custom_expert_dirs:
    - "experts/custom"
  auto_discover: true

interface:
  window_size: [1400, 900]
  show_tips: true
  confirm_actions: true

logging:
  level: "INFO"
  file: "logs/ghst.log"
  max_size_mb: 10
  backup_count: 5

# Safety and Ethics
safety:
  require_human_approval: true
  experimental_features_warning: true
  validate_ai_output: true
"""
        
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        self.print_success(f"Configuration created: {config_file}")
    
    def create_readme(self):
        """Create a getting started README."""
        self.print_header("Creating Documentation")
        
        readme_content = """# GHST Installation

## Installation Complete! 🎉

Your GHST AI Coding Engine has been successfully installed.

## Quick Start

### Activate Virtual Environment

"""
        
        if self.config.get('use_venv', True):
            if self.system == "Windows":
                readme_content += """On Windows:
```
venv\\Scripts\\activate
```

"""
            else:
                readme_content += """On Linux/Mac:
```
source venv/bin/activate
```

"""
        
        readme_content += """### Run GHST

```bash
# Launch the main application
python core/launch_gui.py

# Or use the launcher
python core/launcher.py
```

## Configuration

Your configuration is located at: `config/user/settings.yaml`

Edit this file to customize GHST to your preferences.

## Directory Structure

- `logs/` - Application logs
- `exports/` - Exported files and outputs
- `backups/` - Backup files
- `config/user/` - Your configuration files
- `plugins/custom/` - Custom plugins
- `experts/custom/` - Custom expert modules

## Getting Help

- Documentation: `docs/`
- Issues: https://github.com/allanwrench28/GHST/issues
- Contributing: See CONTRIBUTING.md

## Next Steps

1. Review the configuration in `config/user/settings.yaml`
2. Read the documentation in `docs/`
3. Try running the application
4. Check out the examples in `examples/`

Happy coding with GHST! 👻
"""
        
        readme_file = self.install_dir / 'INSTALL_README.md'
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        self.print_success(f"Getting started guide created: {readme_file}")
    
    def validate_installation(self):
        """Validate the installation."""
        self.print_header("Validating Installation")
        
        # Check directories
        required_dirs = ['logs', 'exports', 'config/user']
        for directory in required_dirs:
            dir_path = self.install_dir / directory
            if dir_path.exists():
                self.print_success(f"Directory exists: {directory}")
            else:
                self.print_warning(f"Directory missing: {directory}")
        
        # Check configuration
        config_file = self.install_dir / 'config' / 'user' / 'settings.yaml'
        if config_file.exists():
            self.print_success("Configuration file created")
        else:
            self.print_warning("Configuration file not found")
        
        # Test Python imports (optional)
        self.print_info("\nTesting core imports...")
        test_modules = [
            ('yaml', 'PyYAML'),
            ('pathlib', 'Built-in'),
        ]
        
        for module, package in test_modules:
            try:
                __import__(module)
                self.print_success(f"{package} available")
            except ImportError:
                self.print_warning(f"{package} not available (may need: pip install {package.lower()})")
    
    def show_completion_message(self):
        """Show installation completion message."""
        self.print_header("Installation Complete!")
        
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("   _____ _    _  _____ _______ ")
        print("  / ____| |  | |/ ____|__   __|")
        print(" | |  __| |__| | (___    | |   ")
        print(" | | |_ |  __  |\\___ \\   | |   ")
        print(" | |__| | |  | |____) |  | |   ")
        print("  \\_____|_|  |_|_____/   |_|   ")
        print(f"{Colors.ENDC}\n")
        
        print("GHST AI Coding Engine has been successfully installed!\n")
        
        print(f"{Colors.CYAN}Next Steps:{Colors.ENDC}")
        print("1. Read INSTALL_README.md for getting started guide")
        print("2. Review configuration in config/user/settings.yaml")
        
        if self.config.get('use_venv', True):
            print("\n3. Activate virtual environment:")
            if self.system == "Windows":
                print(f"   {Colors.YELLOW}venv\\Scripts\\activate{Colors.ENDC}")
            else:
                print(f"   {Colors.YELLOW}source venv/bin/activate{Colors.ENDC}")
        
        print("\n4. Launch GHST:")
        print(f"   {Colors.YELLOW}python core/launch_gui.py{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Happy coding with GHST! 👻{Colors.ENDC}\n")
    
    def run(self, interactive: bool = True):
        """Run the installation wizard."""
        try:
            # Welcome message
            self.print_header("GHST Installation Wizard")
            print("Welcome to the GHST AI Coding Engine Installation Wizard!")
            print("This wizard will guide you through the installation process.\n")
            
            # Check prerequisites
            if not self.check_prerequisites():
                self.print_error("Prerequisites check failed")
                self.print_info("Please install required prerequisites and try again")
                return False
            
            # Configuration
            if interactive:
                self.configure_installation()
            else:
                # Use defaults for non-interactive
                self.config = {
                    'install_type': 'full',
                    'install_syntax_supervisors': True,
                    'install_expert_system': True,
                    'install_plugins': True,
                    'use_venv': True,
                    'theme': 'ghost_dark'
                }
            
            # Installation steps
            self.create_directories()
            
            if self.config.get('use_venv', True):
                self.setup_virtual_environment()
            
            self.install_dependencies()
            self.create_configuration()
            self.create_readme()
            self.validate_installation()
            
            # Completion
            self.show_completion_message()
            
            return True
            
        except KeyboardInterrupt:
            self.print_warning("\n\nInstallation cancelled by user")
            return False
        except Exception as e:
            self.print_error(f"\n\nInstallation failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="GHST Installation Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install_wizard.py              # Interactive installation
  python install_wizard.py --auto       # Automated with defaults
  python install_wizard.py --help       # Show this help
        """
    )
    
    parser.add_argument(
        '--auto', '--non-interactive',
        action='store_true',
        help='Run installation with default settings (non-interactive)'
    )
    
    args = parser.parse_args()
    
    wizard = InstallWizard()
    success = wizard.run(interactive=not args.auto)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
