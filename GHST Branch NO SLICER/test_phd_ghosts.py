#!/usr/bin/env python3
"""
Test Script for PhD-Level Ghost Collective

This script demonstrates our expanded team of 10 specialized PhD-level Ghosts,
each with unique expertise in different aspects of 3D printing and engineering.

⚠️ DISCLAIMER: AI-generated recommendations. Always verify before use.
"""

import sys
import os
sys.path.append('src')

from ai_collaboration.ghost_manager import GhostManager
import time

def test_phd_ghost_collective():
    """Test our expanded PhD-level Ghost collective."""
    print("🎓 Initializing PhD-Level Ghost Collective...")
    print("=" * 60)
    
    # Initialize Ghost Manager
    ghost_manager = GhostManager()
    
    print(f"✨ Active Ghosts: {len(ghost_manager.active_ghosts)} specialists")
    print()
    
    # Display each Ghost's expertise
    ghost_descriptions = {
        'analysis_ghost': "Computer Science PhD - Code analysis & optimization",
        'optimization_ghost': "Applied Mathematics PhD - Performance improvements", 
        'error_ghost': "Systems Engineering PhD - Bug detection & troubleshooting",
        'research_ghost': "Materials Science PhD - FOSS research & innovation",
        'physics_ghost': "Mechanical Engineering PhD - Fluid dynamics & thermodynamics",
        'materials_ghost': "Chemistry PhD - Polymer science & material behavior",
        'mathematics_ghost': "Applied Math PhD - Computational geometry & algorithms", 
        'manufacturing_ghost': "Industrial Engineering PhD - Process optimization",
        'quality_ghost': "Metrology PhD - Precision measurement & quality control",
        'innovation_ghost': "Design Engineering PhD - Creative problem solving"
    }
    
    print("👻 Meet Your PhD-Level Ghost Team:")
    print("-" * 40)
    for ghost_id, description in ghost_descriptions.items():
        if ghost_id in ghost_manager.active_ghosts:
            ghost_class = type(ghost_manager.active_ghosts[ghost_id]).__name__
            print(f"🎓 Dr. {ghost_class}: {description}")
    
    print()
    print("🧪 Testing Ghost Monitoring Capabilities...")
    print("-" * 40)
    
    # Test a few monitoring cycles
    for i in range(3):
        print(f"\n📊 Monitoring Cycle {i+1}:")
        for ghost_id, ghost in ghost_manager.active_ghosts.items():
            try:
                ghost.monitor_cycle()
            except Exception as e:
                print(f"  ⚠️ {ghost_id}: {e}")
        
        # Display recent activities
        if hasattr(ghost_manager, 'activity_log') and ghost_manager.activity_log:
            latest = ghost_manager.activity_log[-3:]  # Last 3 activities
            for activity in latest:
                print(f"  {activity}")
        
        time.sleep(1)  # Brief pause between cycles
    
    print()
    print("🎉 PhD-Level Ghost Collective Test Complete!")
    print("   Ready to tackle complex 3D printing challenges!")

if __name__ == "__main__":
    test_phd_ghost_collective()
