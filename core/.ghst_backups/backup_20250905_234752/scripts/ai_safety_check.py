#!/usr/bin/env python3
"""
FANTOM AI Safety Check Script
Automated safety validation for AI-related functionality.

⚠️ AI-generated analysis - verify before implementation
"""

import sys
import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Any, Set


class AISafetyChecker:
    """AI safety validation system."""
    
    def __init__(self):
        self.safety_violations = {
            'unsafe_ai_operations': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'__import__\s*\(',
                r'compile\s*\(',
                r'subprocess\..*shell\s*=\s*True',
                r'os\.system\s*\(',
            ],
            'unvalidated_inputs': [
                r'input\s*\([^)]*\)\s*[^.]*$',
                r'raw_input\s*\(',
                r'request\..*get\s*\([^)]*\)',
                r'\.read\s*\(\s*\)',
            ],
            'hardcoded_credentials': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
            ],
            'unsafe_file_operations': [
                r'open\s*\([^)]*["\']w["\'][^)]*\)',
                r'\.write\s*\(',
                r'\.remove\s*\(',
                r'\.unlink\s*\(',
                r'shutil\.rmtree',
            ],
            'ghost_safety_bypasses': [
                r'bypass.*safety',
                r'skip.*validation',
                r'ignore.*warning',
                r'force.*execute',
                r'emergency.*override',
            ]
        }
        
        self.ai_safety_requirements = [
            'human_approval_required',
            'safety_validation',
            'ethical_review',
            'liability_disclaimer',
            'error_handling'
        ]

    def check_file(self, filepath: str) -> Dict[str, Any]:
        """Check a single file for safety issues."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file': filepath,
                'error': str(e),
                'status': 'error'
            }
        
        violations = []
        warnings = []
        
        # Check for safety violations
        for category, patterns in self.safety_violations.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    violations.append({
                        'category': category,
                        'pattern': pattern,
                        'line': line_num,
                        'severity': 'high',
                        'match': match.group(0)
                    })
        
        # Check for missing safety requirements in AI-related code
        if self._is_ai_code(content):
            missing_requirements = self._check_safety_requirements(content)
            for req in missing_requirements:
                warnings.append({
                    'category': 'missing_safety_requirement',
                    'requirement': req,
                    'severity': 'medium'
                })
        
        # Parse AST for deeper analysis (if Python file)
        if filepath.endswith('.py'):
            ast_issues = self._analyze_ast(content, filepath)
            violations.extend(ast_issues)
        
        return {
            'file': filepath,
            'violations': violations,
            'warnings': warnings,
            'is_ai_code': self._is_ai_code(content),
            'status': 'checked',
            'safety_score': self._calculate_safety_score(violations, warnings)
        }

    def _is_ai_code(self, content: str) -> bool:
        """Check if code contains AI-related functionality."""
        ai_indicators = [
            'ghost', 'ai_', 'machine_learning', 'neural_network',
            'model.predict', 'tensorflow', 'pytorch', 'sklearn',
            'artificial_intelligence', 'automated_decision'
        ]
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in ai_indicators)

    def _check_safety_requirements(self, content: str) -> List[str]:
        """Check for missing AI safety requirements."""
        missing = []
        content_lower = content.lower()
        
        requirement_patterns = {
            'human_approval_required': [
                'human.*approval', 'user.*confirmation', 'manual.*review'
            ],
            'safety_validation': [
                'safety.*check', 'validate.*safety', 'safety.*validation'
            ],
            'ethical_review': [
                'ethical.*review', 'ethics.*check', 'bias.*detection'
            ],
            'liability_disclaimer': [
                'disclaimer', 'liability', 'no.*warranty', 'use.*at.*risk'
            ],
            'error_handling': [
                'try.*except', 'error.*handling', 'exception.*handling'
            ]
        }
        
        for requirement, patterns in requirement_patterns.items():
            if not any(re.search(pattern, content_lower) for pattern in patterns):
                missing.append(requirement)
        
        return missing

    def _analyze_ast(self, content: str, filepath: str) -> List[Dict[str, Any]]:
        """Analyze Python AST for security issues."""
        issues = []
        try:
            tree = ast.parse(content)
            
            class SecurityVisitor(ast.NodeVisitor):
                def visit_Call(self, node):
                    # Check for dangerous function calls
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'compile']:
                            issues.append({
                                'category': 'dangerous_function',
                                'function': node.func.id,
                                'line': node.lineno,
                                'severity': 'critical',
                                'message': f"Dangerous function {node.func.id} detected"
                            })
                    self.generic_visit(node)
                
                def visit_Import(self, node):
                    # Check for suspicious imports
                    for alias in node.names:
                        if alias.name in ['os', 'subprocess', 'sys']:
                            issues.append({
                                'category': 'suspicious_import',
                                'module': alias.name,
                                'line': node.lineno,
                                'severity': 'medium',
                                'message': f"Potentially unsafe module {alias.name} imported"
                            })
                    self.generic_visit(node)
            
            visitor = SecurityVisitor()
            visitor.visit(tree)
            
        except SyntaxError:
            # File has syntax errors, skip AST analysis
            pass
        except Exception as e:
            issues.append({
                'category': 'ast_analysis_error',
                'error': str(e),
                'line': 0,
                'severity': 'low',
                'message': f"AST analysis failed: {e}"
            })
        
        return issues

    def _calculate_safety_score(self, violations: List[Dict], warnings: List[Dict]) -> float:
        """Calculate safety score (0-100, higher is safer)."""
        critical_count = len([v for v in violations if v.get('severity') == 'critical'])
        high_count = len([v for v in violations if v.get('severity') == 'high'])
        medium_count = len([v for v in violations if v.get('severity') == 'medium']) + len(warnings)
        
        # Deduct points for violations
        score = 100.0
        score -= critical_count * 30
        score -= high_count * 15
        score -= medium_count * 5
        
        return max(0.0, score)

    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate safety report."""
        total_files = len(results)
        files_with_violations = len([r for r in results if r.get('violations')])
        ai_files = len([r for r in results if r.get('is_ai_code')])
        
        avg_safety_score = sum(r.get('safety_score', 0) for r in results) / max(1, total_files)
        
        report = f"""
🤖 AI SAFETY CHECK REPORT

📊 Summary:
- Total files checked: {total_files}
- Files with safety violations: {files_with_violations}
- AI-related files: {ai_files}
- Average safety score: {avg_safety_score:.1f}/100

"""
        
        if files_with_violations > 0:
            report += "🚨 SAFETY VIOLATIONS DETECTED:\n\n"
            for result in results:
                if result.get('violations'):
                    report += f"File: {result['file']} (Score: {result.get('safety_score', 0):.1f})\n"
                    for violation in result['violations']:
                        report += f"  ⚠️ {violation['category']}: {violation.get('message', violation.get('pattern', 'Unknown'))}\n"
                        if 'line' in violation:
                            report += f"     Line {violation['line']}: {violation.get('match', '')}\n"
                    report += "\n"
        
        report += "\n🛡️ SAFETY RECOMMENDATIONS:\n"
        if avg_safety_score < 70:
            report += "- CRITICAL: Safety score below threshold - immediate review required\n"
        if files_with_violations > 0:
            report += "- Address all identified safety violations\n"
            report += "- Add proper error handling and validation\n"
            report += "- Include safety disclaimers for AI functionality\n"
        if ai_files > 0:
            report += "- Ensure human oversight for AI-related operations\n"
            report += "- Implement ethical review processes\n"
        
        report += "\n✅ SAFETY FRAMEWORK COMPLIANCE:\n"
        report += f"- Safety score threshold: {'PASS' if avg_safety_score >= 70 else 'FAIL'}\n"
        report += f"- Human oversight: {'REQUIRED' if ai_files > 0 else 'RECOMMENDED'}\n"
        report += f"- Critical violations: {'NONE' if not any(v.get('severity') == 'critical' for r in results for v in r.get('violations', [])) else 'DETECTED'}\n"
        
        return report


def main():
    """Main safety check function."""
    if len(sys.argv) < 2:
        print("Usage: python ai_safety_check.py <file1> [file2] ...")
        sys.exit(1)
    
    checker = AISafetyChecker()
    results = []
    
    for filepath in sys.argv[1:]:
        if os.path.exists(filepath):
            result = checker.check_file(filepath)
            results.append(result)
    
    # Generate and display report
    report = checker.generate_report(results)
    print(report)
    
    # Exit with error code if critical issues found
    has_critical = any(
        v.get('severity') == 'critical' 
        for r in results 
        for v in r.get('violations', [])
    )
    avg_score = sum(r.get('safety_score', 0) for r in results) / max(1, len(results))
    
    if has_critical or avg_score < 70:
        print("\n🚨 Safety check failed - critical issues detected")
        sys.exit(1)
    elif any(r.get('violations') for r in results):
        print("\n⚠️ Safety warnings detected - review recommended")
        sys.exit(1)
    else:
        print("\n✅ Safety check passed - no critical issues detected")
        sys.exit(0)


if __name__ == '__main__':
    main()