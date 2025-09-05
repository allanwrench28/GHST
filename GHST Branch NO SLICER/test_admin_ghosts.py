#!/usr/bin/env python3
"""
Test ADMIN Ghost Collective - 24 Specialists with Full Access

This demonstrates our expanded team with internet access and admin privileges.
"""

import sys
import os
sys.path.append('src')

from ai_collaboration.ghost_manager import GhostManager

def test_admin_collective():
    """Test our 24-Ghost admin collective."""
    print("🚀 INITIALIZING ADMIN GHOST COLLECTIVE")
    print("=" * 50)
    
    gm = GhostManager()
    
    print(f"👻 Total Active Ghosts: {len(gm.active_ghosts)}")
    print(f"🌐 Internet Access: {gm.internet_enabled}")
    print(f"🔧 Admin Mode: {gm.admin_mode}")
    print(f"📝 Auto-Commit: {gm.auto_commit_enabled}")
    print()
    
    print("🎓 GHOST ROSTER:")
    print("-" * 30)
    
    # Organize by teams
    teams = {
        'Core Team': ['analysis', 'optimization', 'error', 'research'],
        'Engineering': ['physics', 'materials', 'mathematics', 'manufacturing', 'quality', 'innovation'],
        'UI/UX': ['colorscience', 'typography', 'uxdesign'],
        'Systems': ['efficiency', 'filesystem', 'git', 'chatbot'],
        'Specialists': ['security', 'performance', 'documentation', 'testing', 'deployment', 'ai', 'recruitment']
    }
    
    for team_name, ghost_prefixes in teams.items():
        print(f"\n📋 {team_name}:")
        for prefix in ghost_prefixes:
            ghost_key = f"{prefix}_ghost"
            if ghost_key in gm.active_ghosts:
                ghost = gm.active_ghosts[ghost_key]
                ghost_class = type(ghost).__name__
                print(f"  • Dr. {prefix.title()}: {ghost_class}")
    
    print(f"\n🎉 READY FOR AUTONOMOUS OPERATION!")
    print(f"   Full admin access with {len(gm.active_ghosts)} specialized Ghosts!")

if __name__ == "__main__":
    test_admin_collective()
