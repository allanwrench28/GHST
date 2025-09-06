# GHST Studio - AI-Driven 3D Printing Development Environment
# Setup script for development environment
# ⚠️ Run at your own risk - verify all operations

import os
import subprocess
import sys
from pathlib import Path

# ⚠️ DISCLAIMER: This setup script is provided without warranty
print("=" * 60)
print("⚠️  GHST Studio Setup - NO WARRANTY")
print("=" * 60)
print("This script will set up GHST Studio development environment.")
print("GHST Studio assumes NO LIABILITY for any issues that may occur.")
print("User assumes ALL RISK when running this setup.")
print("By continuing, you acknowledge and accept these terms.")
print("=" * 60)

response = input("Do you accept these terms and wish to continue? (yes/no): ")
if response.lower() != 'yes':
    print("Setup cancelled by user.")
    sys.exit(0)


def run_command(cmd, description):
    """Run a command with error handling and user notification."""
    print("\n🔧 {description}")
    print("Command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, check=True,
                                capture_output=True, text=True)
        print("✅ Success: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed: {description}")
        print("Error: {e.stderr}")
        return False


def main():
    """Main setup routine."""
    print("\n🚀 Starting GHST Studio setup...")

    # Verify we're in the right directory
    if not Path("src").exists():
        print("❌ Error: Not in GHST Studio root directory")
        print("Please run this script from the GHST Studio project root.")
        sys.exit(1)

    # Create virtual environment
    print("\n📦 Setting up Python virtual environment...")
    if not run_command("python -m venv fantom_studio_env",
                       "Creating virtual environment"):
        print("⚠️ Virtual environment creation failed.")
        print("Please install Python 3.8+ and try again.")
        return False

    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "fantom_studio_env\\Scripts\\activate && "
    else:  # Unix/Linux/macOS
        activate_cmd = "source fantom_studio_env/bin/activate && "

    install_cmd = "{activate_cmd}pip install -r requirements.txt"
    if not run_command(install_cmd, "Installing Python dependencies"):
        print("⚠️ Dependency installation failed.")
        print("Check requirements.txt and try manual installation.")
        return False

    # Create additional directories
    dirs_to_create = [
        "logs",
        "backups",
        "temp",
        "exports",
        "plugins"
    ]

    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
        print("📁 Created directory: {dir_name}")

    # Copy default config if needed
    config_path = Path("config/user.yaml")
    if not config_path.exists():
        import shutil
        shutil.copy("config/default.yaml", config_path)
        print("📄 Created user configuration file")

    print("\n✅ GHST Studio setup complete!")
    print("\n🎉 Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':
        print("   fantom_studio_env\\Scripts\\activate")
    else:
        print("   source fantom_studio_env/bin/activate")
    print("2. Run the studio demo:")
    print("   python demo.py")
    print("3. Or run the plugin system demo:")
    print("   python demo_plugin_system.py")
    print("\n⚠️ Remember: Always review AI-generated code before use!")
    print("⚠️ GHST Studio assumes no liability for any issues.")
    print("⚠️ This version excludes coding engine functionality.")

    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Setup failed with error: {e}")
        print("⚠️ SlicerGPT assumes no liability for setup issues.")
        sys.exit(1)
