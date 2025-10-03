#!/usr/bin/env python3
"""
Mixture of Experts (MoE) System Demo

This script demonstrates how to use the MoE system for dynamic expert selection
and query routing in the GHST framework.
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core' / 'src'))

from ai_collaboration.expert_metadata import (
    ExpertMetadata,
    ExpertDomain,
    ExpertRegistry,
    create_default_registry
)
from ai_collaboration.moe_router import MoERouter


def demo_basic_routing():
    """Demonstrate basic query routing."""
    print("=" * 70)
    print("DEMO 1: Basic Query Routing")
    print("=" * 70)
    
    # Create registry and router
    registry = create_default_registry()
    router = MoERouter(registry, max_experts=3)
    
    # Example queries
    queries = [
        "How can I improve the color scheme of my user interface?",
        "I need to optimize mesh processing for 3D printing",
        "Help me find and fix security vulnerabilities in my code",
        "Optimize the performance of my slicing algorithm"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        print("-" * 70)
        
        selections = router.route_query(query)
        
        if not selections:
            print("❌ No relevant experts found")
            continue
        
        for i, selection in enumerate(selections, 1):
            print(f"\n{i}. {selection.metadata.name}")
            print(f"   Expert ID: {selection.expert_id}")
            print(f"   Domain: {selection.metadata.domain.value}")
            print(f"   Relevance: {selection.relevance_score:.2f}")
            print(f"   Reasoning: {selection.reasoning}")
            print(f"   Expertise: {selection.metadata.expertise}")


def demo_domain_experts():
    """Demonstrate getting experts by domain."""
    print("\n" + "=" * 70)
    print("DEMO 2: Domain-Specific Experts")
    print("=" * 70)
    
    registry = create_default_registry()
    router = MoERouter(registry)
    
    domains_to_check = [
        ExpertDomain.CORE,
        ExpertDomain.UI_UX_DESIGN,
        ExpertDomain.ENGINEERING
    ]
    
    for domain in domains_to_check:
        print(f"\n🎯 Domain: {domain.value}")
        print("-" * 70)
        
        selections = router.get_expert_by_domain(domain)
        
        if not selections:
            print("   No experts in this domain")
            continue
        
        for selection in selections:
            print(f"   • {selection.metadata.name}")
            print(f"     Specialization: {selection.metadata.specialization}")


def demo_expert_search():
    """Demonstrate searching for experts."""
    print("\n" + "=" * 70)
    print("DEMO 3: Expert Search")
    print("=" * 70)
    
    registry = create_default_registry()
    
    search_terms = [
        "color design",
        "optimization performance",
        "security vulnerability"
    ]
    
    for term in search_terms:
        print(f"\n🔍 Searching for: {term}")
        print("-" * 70)
        
        results = registry.search_experts(term, threshold=0.1)
        
        if not results:
            print("   No experts found")
            continue
        
        for expert, score in results[:3]:  # Top 3 results
            print(f"   • {expert.name} (Score: {score:.2f})")
            print(f"     Keywords: {', '.join(expert.keywords[:5])}")


def demo_statistics():
    """Demonstrate router statistics."""
    print("\n" + "=" * 70)
    print("DEMO 4: Router Statistics")
    print("=" * 70)
    
    registry = create_default_registry()
    router = MoERouter(registry)
    
    # Make some queries to generate statistics
    test_queries = [
        "optimize code",
        "fix errors",
        "analyze mesh",
        "improve UI design",
        "optimize performance"
    ]
    
    print("\n📊 Running test queries...")
    for query in test_queries:
        router.route_query(query)
        print(f"   ✓ {query}")
    
    # Get statistics
    stats = router.get_statistics()
    
    print("\n📈 Statistics:")
    print("-" * 70)
    print(f"Total Queries: {stats['total_queries']}")
    print(f"Total Registered Experts: {stats['total_registered_experts']}")
    print(f"Enabled Experts: {stats['enabled_experts']}")
    print(f"Average Experts per Query: {stats['average_experts_per_query']}")
    
    print("\n🏆 Most Used Experts:")
    for expert in stats['most_used_experts'][:5]:
        print(f"   • {expert['expert_id']}: {expert['count']} queries")


def demo_all_domains():
    """List all available domains."""
    print("\n" + "=" * 70)
    print("DEMO 5: Available Domains")
    print("=" * 70)
    
    registry = create_default_registry()
    
    print("\n🌐 All Available Domains:")
    print("-" * 70)
    
    for domain in ExpertDomain:
        experts = registry.get_by_domain(domain)
        print(f"\n{domain.value.replace('_', ' ').title()}")
        print(f"  Experts: {len(experts)}")
        if experts:
            for expert in experts:
                print(f"    • {expert.name}")


def demo_context_modifiers():
    """Demonstrate context-based expert selection."""
    print("\n" + "=" * 70)
    print("DEMO 6: Context-Based Selection")
    print("=" * 70)
    
    registry = create_default_registry()
    router = MoERouter(registry)
    
    query = "optimize code performance"
    
    # Query without context
    print(f"\n📝 Query: {query}")
    print("\n1️⃣ Without context:")
    print("-" * 70)
    
    selections1 = router.route_query(query)
    for selection in selections1[:3]:
        print(f"   • {selection.expert_id}: {selection.relevance_score:.2f}")
    
    # Query with preferred expert
    print("\n2️⃣ With preferred expert (optimization_ghost):")
    print("-" * 70)
    
    context = {'preferred_experts': ['optimization_ghost']}
    selections2 = router.route_query(query, context)
    for selection in selections2[:3]:
        print(f"   • {selection.expert_id}: {selection.relevance_score:.2f}")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("🎭 GHST Mixture of Experts (MoE) System Demo")
    print("=" * 70)
    
    try:
        demo_basic_routing()
        demo_domain_experts()
        demo_expert_search()
        demo_all_domains()
        demo_statistics()
        demo_context_modifiers()
        
        print("\n" + "=" * 70)
        print("✅ Demo completed successfully!")
        print("=" * 70)
        print("\nTo learn more:")
        print("  • See docs/MOE_README.md for usage guide")
        print("  • See docs/MOE_ARCHITECTURE.md for architecture details")
        print("  • See docs/EXPERT_TEMPLATE.md for creating experts")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
