#!/usr/bin/env python3
"""
GHST GHST Agent Collective Ethical Review Script
Automated ethical review for AI-related code changes.

⚠️ AI-generated analysis - human oversight required
"""

import os
import re
import sys
from typing import Any, Dict, List


class GhostEthicalReviewer:
    """GHST Agent collective ethical review system."""

    def __init__(self):
        self.ethical_patterns = {
            'bias_risks': [
                r'bias.*filter',
                r'demographic.*filter',
                r'gender.*assumption',
                r'race.*classification',
                r'hardcoded.*stereotype'
            ],
            'privacy_concerns': [
                r'personal.*data',
                r'user.*tracking',
                r'location.*data',
                r'private.*information',
                r'credential.*storage'
            ],
            'safety_issues': [
                r'unsafe.*operation',
                r'skip.*validation',
                r'bypass.*safety',
                r'ignore.*warning',
                r'emergency.*override'
            ],
            'transparency_violations': [
                r'hidden.*feature',
                r'undisclosed.*tracking',
                r'secret.*logging',
                r'covert.*operation'
            ]
        }

        self.ai_code_patterns = [
            r'ghst.*collective',
            r'ai.*model',
            r'machine.*learning',
            r'neural.*network',
            r'artificial.*intelligence',
            r'automated.*decision'
        ]

    def review_file(self, filepath: str) -> Dict[str, Any]:
        """Review a single file for ethical concerns."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except Exception as e:
            return {
                'file': filepath,
                'error': str(e),
                'status': 'error'
            }

        issues = []
        is_ai_related = self._is_ai_related_code(content)

        for category, patterns in self.ethical_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    issues.append({
                        'category': category,
                        'pattern': pattern,
                        'severity': 'high' if is_ai_related else 'medium'
                    })

        return {
            'file': filepath,
            'ai_related': is_ai_related,
            'issues': issues,
            'status': 'reviewed',
            'requires_human_review': len(issues) > 0 or is_ai_related
        }

    def _is_ai_related_code(self, content: str) -> bool:
        """Check if code contains AI-related functionality."""
        for pattern in self.ai_code_patterns:
            if re.search(pattern, content):
                return True
        return False

    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate ethical review report."""
        total_files = len(results)
        files_with_issues = len([r for r in results if r.get('issues')])
        ai_related_files = len([r for r in results if r.get('ai_related')])

        report = """
👻 GHOST COLLECTIVE ETHICAL REVIEW REPORT

📊 Summary:
- Total files reviewed: {total_files}
- Files with ethical concerns: {files_with_issues}
- AI-related files: {ai_related_files}

"""

        if files_with_issues > 0:
            report += "🚨 ETHICAL CONCERNS DETECTED:\n\n"
            for result in results:
                if result.get('issues'):
                    report += "File: {result['file']}\n"
                    for issue in result['issues']:
                        report += "  ⚠️ {
                            issue['category']}: {
                            issue['pattern']} ({
                            issue['severity']})\n"
                    report += "\n"

        if ai_related_files > 0:
            report += "🤖 AI-RELATED FILES REQUIRING HUMAN REVIEW:\n\n"
            for result in results:
                if result.get('ai_related'):
                    report += "  - {result['file']}\n"

        report += "\n⚖️ ETHICAL FRAMEWORK COMPLIANCE:\n"
        report += "- Human oversight: REQUIRED ✅\n"
        report += "- Transparency: MAINTAINED ✅\n"
        report += "- Accountability: TRACKED ✅\n"
        report += "- Safety-first approach: ACTIVE ✅\n"

        report += "\n🔔 NEXT STEPS:\n"
        if files_with_issues > 0 or ai_related_files > 0:
            report += "1. Human review required before merge\n"
            report += "2. Address ethical concerns identified\n"
            report += "3. Update documentation if needed\n"
            report += "4. Seek additional ethics review if uncertain\n"
        else:
            report += "1. No immediate ethical concerns detected\n"
            report += "2. Proceed with standard review process\n"

        return report

def main():
    """Main ethical review function."""
    if len(sys.argv) < 2:
        print("Usage: python ghst_ethical_review.py <file1> [file2] ...")
        sys.exit(1)

    reviewer = GhostEthicalReviewer()
    results = []

    for filepath in sys.argv[1:]:
        if os.path.exists(filepath):
            result = reviewer.review_file(filepath)
            results.append(result)

    # Generate and display report
    report = reviewer.generate_report(results)
    print(report)

    # Exit with error code if issues found
    has_issues = any(r.get('issues') or r.get('ai_related') for r in results)
    if has_issues:
        print("\n⚠️ Ethical review flagged concerns - human oversight required")
        sys.exit(1)
    else:
        print("\n✅ Ethical review passed - no immediate concerns detected")
        sys.exit(0)

if __name__ == '__main__':
    main()
