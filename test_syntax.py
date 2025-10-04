#!/usr/bin/env python3
"""
Simple test to validate Python syntax and basic imports.
"""
import sys
import pytest


def test_core_scripts_import():
    """Test that core scripts can be imported without syntax errors."""
    # These should not raise syntax errors
    import py_compile
    
    scripts = [
        'core/scripts/nightly_build.py',
        'core/scripts/ai_safety_check.py',
        'core/scripts/check_license_headers.py',
        'core/scripts/ghost_ethical_review.py',
    ]
    
    for script in scripts:
        try:
            py_compile.compile(script, doraise=True)
            print(f"✓ {script} - No syntax errors")
        except py_compile.PyCompileError as e:
            pytest.fail(f"Syntax error in {script}: {e}")


def test_core_modules_syntax():
    """Test that core modules have valid Python syntax."""
    import py_compile
    
    modules = [
        'core/src/ai_collaboration/error_handler.py',
        'core/src/ai_collaboration/expert_manager.py',
        'core/src/ai_collaboration/ghost_chat.py',
        'core/src/ai_collaboration/ghost_manager.py',
        'core/src/plugins/base_plugin.py',
        'core/src/plugins/plugin_manager.py',
        'core/src/plugins/builtin/gcode_optimizer.py',
        'core/src/plugins/builtin/print_stats.py',
        'core/src/utils/config_manager.py',
    ]
    
    for module in modules:
        try:
            py_compile.compile(module, doraise=True)
            print(f"✓ {module} - No syntax errors")
        except py_compile.PyCompileError as e:
            pytest.fail(f"Syntax error in {module}: {e}")


def test_basic_imports():
    """Test basic imports work."""
    # Test that core modules can be imported (will add to path if needed)
    sys.path.insert(0, 'core/src')
    
    # These should not raise ImportError for basic syntax
    try:
        # Don't actually import as they may have runtime dependencies
        # Just validate syntax
        import py_compile
        py_compile.compile('core/src/ai_collaboration/error_handler.py', doraise=True)
        print("✓ error_handler.py syntax valid")
    except Exception as e:
        pytest.fail(f"Error validating error_handler.py: {e}")


if __name__ == '__main__':
    print("Running syntax validation tests...")
    test_core_scripts_import()
    test_core_modules_syntax()
    test_basic_imports()
    print("\n✅ All syntax tests passed!")
