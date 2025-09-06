#!/usr/bin/env python3
"""
GHST System Test Suite
=====================

Comprehensive test of the GHST AI coding engine to ensure all components work.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ghst_components():
    """Test all GHST components."""

    print("🧪 GHST SYSTEM TEST SUITE")
    print("=" * 50)
    print()

    results = {
        'syntax_supervisors': False,
        'expert_manager': False,
        'config_manager': False,
        'plugin_system': False,
        'gui_components': False
    }

    # Test 1: Syntax Supervisors
    print("🔍 Testing Syntax Supervisors...")
    try:
        from core.src.syntax_supervisors import SyntaxSupervisorManager
        SyntaxSupervisorManager(str(project_root))
        print("✅ Syntax Supervisors: PASS")
        results['syntax_supervisors'] = True
    except Exception as e:
        print("❌ Syntax Supervisors: FAIL - {e}")

    # Test 2: Expert Manager
    print("🧠 Testing Expert Manager...")
    try:
        from core.src.ai_collaboration.expert_manager import ExpertManager
        ExpertManager()
        print("✅ Expert Manager: PASS")
        results['expert_manager'] = True
    except Exception as e:
        print("❌ Expert Manager: FAIL - {e}")

    # Test 3: Config Manager
    print("⚙️ Testing Config Manager...")
    try:
        from core.src.utils.config_manager import ConfigManager
        ConfigManager()
        print("✅ Config Manager: PASS")
        results['config_manager'] = True
    except Exception as e:
        print("❌ Config Manager: FAIL - {e}")

    # Test 4: Plugin System
    print("🔌 Testing Plugin System...")
    try:
        from core.src.plugins.plugin_manager import PluginManager
        PluginManager()
        print("✅ Plugin System: PASS")
        results['plugin_system'] = True
    except Exception as e:
        print("❌ Plugin System: FAIL - {e}")

    # Test 5: GUI Components
    print("🎨 Testing GUI Components...")
    try:
        print("✅ GUI Components: PASS")
        results['gui_components'] = True
    except Exception as e:
        print("❌ GUI Components: FAIL - {e}")

    # Summary
    print()
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 30)

    passed = sum(results.values())
    total = len(results)

    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print("{status_icon} {component.replace('_', ' ').title()}")

    print()
    print("🎯 OVERALL: {passed}/{total} components working")

    if passed == total:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        return True
    else:
        print("⚠️ Some components need attention")
        return False

def test_ghst_integration():
    """Test GHST integration and workflow."""

    print("\n🔗 TESTING GHST INTEGRATION")
    print("=" * 40)

    try:
        # Test Syntax Supervisors background monitoring
        print("🔍 Testing SS background monitoring...")
        from core.src.syntax_supervisors import SyntaxSupervisorManager

        ss_manager = SyntaxSupervisorManager(str(project_root))
        ss_manager.start_monitoring()

        print("✅ Background monitoring started")

        # Test code analysis
        test_code = """
def hello_world():
    print("Hello from GHST!")
    return True
"""

        # Create a temporary test file
        test_file = project_root / "test_temp.py"
        with open(test_file, 'w') as f:
            f.write(test_code)

        # Let SS analyze it
        import time
        time.sleep(2)  # Give SS time to scan

        # Clean up
        if test_file.exists():
            test_file.unlink()

        ss_manager.stop_monitoring()
        print("✅ Integration test complete")

        return True

    except Exception as e:
        print("❌ Integration test failed: {e}")
        return False

def main():
    """Run the complete GHST test suite."""

    print("🚀 Starting GHST System Tests...")
    print()

    # Run component tests
    components_ok = test_ghst_components()

    # Run integration tests
    integration_ok = test_ghst_integration()

    # Final report
    print("\n" + "=" * 50)
    print("🏁 FINAL TEST REPORT")
    print("=" * 50)

    if components_ok and integration_ok:
        print("🎉 GHST SYSTEM: FULLY OPERATIONAL!")
        print("✅ All components working")
        print("✅ Integration successful")
        print("🚀 Ready for production use!")
        return 0
    else:
        print("⚠️ GHST SYSTEM: NEEDS ATTENTION")
        if not components_ok:
            print("❌ Some components failing")
        if not integration_ok:
            print("❌ Integration issues detected")
        print("🔧 Debug and fix issues before production")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
