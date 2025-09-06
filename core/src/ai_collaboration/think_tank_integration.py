"""
GHST Think Tank Integration
==========================

Integrates the PhD Think Tank system with the main GHST interface,
providing seamless access to collaborative AI problem-solving.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from phd_think_tank import PHDThinkTankSystem, think_tank

# Add the core modules to path
sys.path.append(str(Path(__file__).parent))


class GHSTThinkTankInterface:
    """Interface between GHST main system and PhD Think Tank"""

    def __init__(self):
        self.think_tank = think_tank
        self.active_sessions = {}

    async def solve_coding_problem(
            self, problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Solve a coding problem using the PhD think tank"""
        if context is None:
            context = {}

        # Add GHST-specific context
        context.update({
            'system': 'GHST',
            'framework': 'open_source_ai_collaboration',
            'goal': 'optimal_coding_solution'
        })

        consensus = await self.think_tank.solve_problem(problem, context)

        # Format response for GHST interface
        return {
            'solution': consensus.solution,
            'confidence': consensus.confidence_score,
            'phd_experts': {
                'supporting': consensus.supporting_agents,
                'dissenting': consensus.dissenting_agents
            },
            'evidence_quality': consensus.evidence_quality,
            'implementation_plan': consensus.implementation_plan,
            'consensus_time': consensus.time_to_consensus,
            'think_tank_stats': self.think_tank.get_system_status()
        }

    def get_available_experts(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available PhD experts"""
        status = self.think_tank.get_system_status()
        return status['agent_expertise']

    def get_think_tank_stats(self) -> Dict[str, Any]:
        """Get think tank performance statistics"""
        return self.think_tank.get_system_status()


# Global interface instance
ghst_think_tank = GHSTThinkTankInterface()


def demo_think_tank():
    """Demo the integrated think tank system"""
    print("🧠 GHST Integrated Think Tank Demo")
    print("=" * 40)

    async def run_demo():
        # Example coding problems
        problems = [{'problem': """
                Our GHST installer needs to handle large file downloads (500MB+)
                with progress tracking, resume capability, and error recovery.
                Current implementation is blocking the UI and has no error handling.
                """,
                     'context': {'language': 'Python',
                                 'framework': 'PyQt5',
                                 'file_size': '500MB+',
                                 'requirements': ['progress_tracking',
                                                  'resume',
                                                  'error_recovery']}},
                    {'problem': """
                Need to optimize GHST's AI agent communication system for real-time
                collaboration between 32+ agents without message queue bottlenecks.
                """,
                     'context': {'language': 'Python',
                                 'agents': 32,
                                 'communication_type': 'real_time',
                                 'bottleneck': 'message_queue'}}]

        for i, prob in enumerate(problems, 1):
            print(f"\n🎯 Problem {i}: {prob['problem'].strip()[:80]}...")

            result = await ghst_think_tank.solve_coding_problem(
                prob['problem'],
                prob['context']
            )

            print(f"✅ Solution: {result['solution'][:100]}...")
            print(f"📊 Confidence: {result['confidence']:.2f}")
            print(
                f"👨‍🎓 Supporting Experts: {
                    ', '.join(
                        result['phd_experts']['supporting'])}")
            print(f"⏱️  Consensus Time: {result['consensus_time']:.1f}s")
            print(f"🔬 Evidence Quality: {result['evidence_quality']:.2f}")

        # Show expert capabilities
        print(f"\n👨‍🎓 Available PhD Experts:")
        experts = ghst_think_tank.get_available_experts()
        for name, info in experts.items():
            print(
                f"   {name}: PhD in {info['field']} - {info['specialization']}")

    # Run the demo
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n👋 Think tank demo interrupted")


if __name__ == "__main__":
    demo_think_tank()
