#!/usr/bin/env python3
"""
GHST Main Launcher

Launches the GHST modular offline LLM system with core engine
and expertise plugin support.
"""

import sys
import logging
from pathlib import Path

# Add core to path
core_path = Path(__file__).parent / "core"
sys.path.insert(0, str(core_path))

from llm_engine.ghost_core import GhostCore
from llm_engine.context_manager import ContextManager
from llm_engine.memory_system import MemorySystem
from llm_engine.plugin_loader import PluginLoader
from ghosts.core_ghost import CoreGhost
from ghosts.system_ghost import SystemGhost


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/ghst.log')
        ]
    )


def print_banner():
    """Print GHST startup banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║    👻  GHST - Ghost in the Shell                     ║
    ║    Modular Offline LLM System                        ║
    ║                                                       ║
    ║    Version: 0.1.0-alpha                              ║
    ║    Architecture: Modular Plugin-based                ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for GHST."""
    # Setup
    Path("logs").mkdir(exist_ok=True)
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print_banner()
    
    try:
        # Initialize core components
        print("🚀 Initializing GHST Core Engine...")
        
        print("  ⚙️  Loading LLM orchestrator...")
        core_engine = GhostCore()
        
        print("  📚 Initializing context manager...")
        context_mgr = ContextManager()
        
        print("  🧠 Setting up memory system...")
        memory = MemorySystem()
        
        print("  🔌 Loading plugin loader...")
        plugin_loader = PluginLoader()
        
        print("\n👻 Activating Core Ghosts...")
        print("  ✨ Core Assistant Ghost...")
        core_ghost = CoreGhost()
        
        print("  ✨ System Manager Ghost...")
        system_ghost = SystemGhost()
        
        print("\n🔍 Scanning for expertise branches...")
        # Import branch scanner
        sys.path.insert(0, str(core_path / "src"))
        from utils.branch_scanner import BranchScanner
        
        scanner = BranchScanner()
        available_branches = scanner.scan_branches()
        
        if available_branches:
            print(f"  📊 Found {len(available_branches)} expertise branches:")
            for branch in available_branches:
                status = "✅" if branch.get('valid') else "⚠️"
                print(f"    {status} {branch['name']}: {branch['description']}")
        else:
            print("  ℹ️  No expertise branches found (this is normal for fresh installations)")
            
        print("\n✅ GHST Core initialized successfully!")
        print("\n" + "="*60)
        print("GHST is ready to assist you!")
        print("="*60)
        
        # Demo interaction
        print("\n📝 Demo: Testing core ghost...")
        test_query = "Hello, what can you help me with?"
        print(f"\nUser: {test_query}")
        response = core_ghost.process_query(test_query, context={
            'loaded_expertise': available_branches[:3] if available_branches else []
        })
        print(f"\n{response}")
        
        print("\n📝 Demo: Testing system ghost...")
        test_query = "What's the system status?"
        print(f"\nUser: {test_query}")
        response = system_ghost.process_query(test_query, context={
            'ghost_count': 2,
            'plugin_count': len(available_branches),
            'loaded_plugins': [b['name'] for b in available_branches[:3]] if available_branches else []
        })
        print(f"\n{response}")
        
        print("\n" + "="*60)
        print("💡 Next Steps:")
        print("  1. Create expertise branches for your domains")
        print("  2. Use the template in examples/expertise_branch_template/")
        print("  3. See ARCHITECTURE.md for complete documentation")
        print("  4. Configure settings in core/config/")
        print("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to start GHST: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("See logs/ghst.log for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())
