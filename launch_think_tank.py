"""
GHST PhD Think Tank Launcher
===========================

Launch the complete PhD Think Tank system with all components.
"""

import os
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "core" / "src"))
sys.path.insert(0, str(project_root / "core" / "src" / "ai_collaboration"))


def launch_think_tank_demo():
    """Launch the think tank demo"""
    print("🧠 GHST PhD Think Tank System")
    print("=" * 40)
    print()

    # Test core think tank functionality
    try:
        print("🔍 Testing core think tank system...")
        import asyncio

        from ai_collaboration.phd_think_tank import main as think_tank_demo

        # Run demo
        asyncio.run(think_tank_demo())
        print("✅ Core think tank system working!")

    except Exception as e:
        print(f"❌ Core system error: {e}")
        print("Continuing with integration test...")

    print()

    # Test integration layer
    try:
        print("🔗 Testing think tank integration...")
        from ai_collaboration.think_tank_integration import demo_think_tank
        demo_think_tank()
        print("✅ Integration layer working!")

    except Exception as e:
        print(f"❌ Integration error: {e}")
        print("Continuing with GUI test...")

    print()


def launch_think_tank_gui():
    """Launch the VS Code-style GUI"""
    print("🎨 Launching GHST Think Tank GUI...")

    try:
        from ai_collaboration.think_tank_gui import main as gui_main
        gui_main()

    except ImportError as e:
        print(f"❌ GUI dependencies missing: {e}")
        print("💡 Please install PyQt5: pip install PyQt5")
        return False

    except Exception as e:
        print(f"❌ GUI error: {e}")
        return False

    return True


def main():
    """Main launcher"""
    print("🚀 GHST PhD Think Tank Launcher")
    print("=" * 50)
    print()
    print("Choose an option:")
    print("1. 🧠 Run Think Tank Demo (Console)")
    print("2. 🎨 Launch VS Code-Style GUI")
    print("3. 🔍 Test All Components")
    print("4. 📊 System Status")
    print("0. Exit")
    print()

    while True:
        try:
            choice = input("Enter choice (0-4): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break

            elif choice == "1":
                launch_think_tank_demo()

            elif choice == "2":
                launch_think_tank_gui()

            elif choice == "3":
                print("🧪 Testing all components...")
                launch_think_tank_demo()
                print("\n" + "=" * 50 + "\n")
                launch_think_tank_gui()

            elif choice == "4":
                print("📊 GHST Think Tank System Status")
                print("-" * 30)

                # Check core system
                try:
                    from ai_collaboration.phd_think_tank import think_tank
                    status = think_tank.get_system_status()

                    print(f"🎓 PhD Agents: {len(status['phd_agents'])}")
                    print(
                        f"📈 Total Debates: {
                            status['system_stats']['total_debates']}")
                    print(
                        f"✅ Successful Consensus: {
                            status['system_stats']['successful_consensus']}")
                    print(
                        f"⏱️  Average Consensus Time: {
                            status['system_stats']['average_consensus_time']:.1f}s")
                    print()
                    print("👨‍🎓 Available Experts:")
                    for name, field in status['phd_agents'].items():
                        print(f"   • {name}: PhD in {field}")

                except Exception as e:
                    print(f"❌ Core system unavailable: {e}")

                # Check GUI dependencies
                try:
                    import PyQt5
                    print(
                        f"\n🎨 GUI System: ✅ Ready (PyQt5 {
                            PyQt5.QtCore.QT_VERSION_STR})")
                except ImportError:
                    print("\n🎨 GUI System: ❌ PyQt5 not installed")

                print()

            else:
                print("❌ Invalid choice. Please enter 0-4.")

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
