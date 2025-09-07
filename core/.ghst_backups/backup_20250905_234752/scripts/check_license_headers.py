#!/usr/bin/env python3
"""
License Header Check Script
Ensures all source files have proper license headers.

⚠️ Part of FANTOM repository ruleset
"""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


class LicenseChecker:
    """License header validation system."""

    def __init__(self):
        self.license_templates = {
            'python': {
                'header': '''"""
FANTOM: AI-Driven 3D Printing Platform
Copyright (c) 2024 FANTOM Development Team

This file is part of FANTOM.

FANTOM is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

⚠️ AI-generated content - verify before use
FANTOM assumes no liability for AI-generated code or suggestions.
"""''',
                'pattern': r'("""|\'\'\').*?FANTOM.*?MIT.*?("""|\'\'\')',
                'extensions': ['.py']
            },
            'javascript': {
                'header': '''/*
 * FANTOM: AI-Driven 3D Printing Platform
 * Copyright (c) 2024 FANTOM Development Team
 *
 * This file is part of FANTOM.
 *
 * FANTOM is free software: you can redistribute it and/or modify
 * it under the terms of the MIT License.
 *
 * ⚠️ AI-generated content - verify before use
 * FANTOM assumes no liability for AI-generated code or suggestions.
 */''',
                'pattern': r'/\*.*?FANTOM.*?MIT.*?\*/',
                'extensions': ['.js', '.ts']
            },
            'cpp': {
                'header': '''/*
 * FANTOM: AI-Driven 3D Printing Platform
 * Copyright (c) 2024 FANTOM Development Team
 *
 * This file is part of FANTOM.
 *
 * FANTOM is free software: you can redistribute it and/or modify
 * it under the terms of the MIT License.
 *
 * ⚠️ AI-generated content - verify before use
 * FANTOM assumes no liability for AI-generated code or suggestions.
 */''',
                'pattern': r'/\*.*?FANTOM.*?MIT.*?\*/',
                'extensions': ['.cpp', '.cc', '.cxx', '.h', '.hpp']
            }
        }

        self.excluded_files = {
            '__init__.py',
            'setup.py',
            'conftest.py',
        }

        self.excluded_dirs = {
            '__pycache__',
            '.git',
            '.venv',
            'venv',
            'node_modules',
            'build',
            'dist',
            'logs'
        }

    def check_file(self, filepath: str) -> Dict[str, Any]:
        """Check if file has proper license header."""
        file_path = Path(filepath)

        # Skip excluded files and directories
        if file_path.name in self.excluded_files:
            return {
                'file': filepath,
                'status': 'skipped',
                'reason': 'excluded_file'}

        if any(part in self.excluded_dirs for part in file_path.parts):
            return {
                'file': filepath,
                'status': 'skipped',
                'reason': 'excluded_directory'}

        # Determine file type
        file_type = self._get_file_type(file_path)
        if not file_type:
            return {
                'file': filepath,
                'status': 'skipped',
                'reason': 'unsupported_type'}

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {'file': filepath, 'status': 'error', 'error': str(e)}

        # Check for license header
        template = self.license_templates[file_type]
        has_license = bool(
            re.search(
                template['pattern'],
                content,
                re.DOTALL | re.IGNORECASE))

        result = {
            'file': filepath,
            'file_type': file_type,
            'has_license': has_license,
            'status': 'checked'
        }

        if not has_license:
            result['missing_license'] = True
            result['suggested_header'] = template['header']

        return result

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type based on extension."""
        extension = file_path.suffix.lower()

        for file_type, template in self.license_templates.items():
            if extension in template['extensions']:
                return file_type

        return None

    def fix_license_header(self, filepath: str, file_type: str) -> bool:
        """Add license header to file if missing."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            template = self.license_templates[file_type]
            header = template['header']

            # Add header at the beginning of the file
            if file_type == 'python':
                # Handle shebang for Python files
                lines = content.split('\n')
                if lines and lines[0].startswith('#!'):
                    new_content = lines[0] + '\n' + \
                        header + '\n' + '\n'.join(lines[1:])
                else:
                    new_content = header + '\n' + content
            else:
                new_content = header + '\n' + content

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True

        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
            return False

    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate license check report."""
        total_files = len([r for r in results if r['status'] == 'checked'])
        files_missing_license = len(
            [r for r in results if r.get('missing_license')])
        skipped_files = len([r for r in results if r['status'] == 'skipped'])
        error_files = len([r for r in results if r['status'] == 'error'])

        report = f"""
⚖️ LICENSE HEADER CHECK REPORT

📊 Summary:
- Total files checked: {total_files}
- Files missing license: {files_missing_license}
- Files skipped: {skipped_files}
- Files with errors: {error_files}

"""

        if files_missing_license > 0:
            report += "📝 FILES MISSING LICENSE HEADERS:\n\n"
            for result in results:
                if result.get('missing_license'):
                    report += f"  ❌ {result['file']} ({result['file_type']})\n"
            report += "\n"

        if error_files > 0:
            report += "⚠️ FILES WITH ERRORS:\n\n"
            for result in results:
                if result['status'] == 'error':
                    report += f"  ❌ {
                        result['file']}: {
                        result.get(
                            'error',
                            'Unknown error')}\n"
            report += "\n"

        report += "📋 LICENSE COMPLIANCE:\n"
        if files_missing_license == 0:
            report += "✅ All files have proper license headers\n"
        else:
            report += f"❌ {files_missing_license} files missing license headers\n"
            report += "   Use --fix to automatically add headers\n"

        report += "\n🔍 FILE TYPE BREAKDOWN:\n"
        file_types = {}
        for result in results:
            if result['status'] == 'checked':
                ft = result.get('file_type', 'unknown')
                if ft not in file_types:
                    file_types[ft] = {'total': 0, 'missing': 0}
                file_types[ft]['total'] += 1
                if result.get('missing_license'):
                    file_types[ft]['missing'] += 1

        for ft, counts in file_types.items():
            report += f"  {ft}: {
                counts['total']} files, {
                counts['missing']} missing license\n"

        return report


def main():
    """Main license check function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Check and fix license headers')
    parser.add_argument('files', nargs='+', help='Files to check')
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Fix missing license headers')
    args = parser.parse_args()

    checker = LicenseChecker()
    results = []

    for filepath in args.files:
        if os.path.exists(filepath):
            result = checker.check_file(filepath)
            results.append(result)

            # Fix license if requested and missing
            if args.fix and result.get('missing_license'):
                file_type = result.get('file_type')
                if file_type:
                    success = checker.fix_license_header(filepath, file_type)
                    if success:
                        result['fixed'] = True
                        print(f"✅ Added license header to {filepath}")
                    else:
                        result['fix_failed'] = True
                        print(f"❌ Failed to add license header to {filepath}")

    # Generate and display report
    report = checker.generate_report(results)
    print(report)

    # Exit with error code if files missing license (and not fixed)
    missing_license = any(
        r.get('missing_license') and not r.get('fixed')
        for r in results
    )

    if missing_license:
        print("\n❌ License check failed - files missing license headers")
        sys.exit(1)
    else:
        print("\n✅ License check passed - all files have proper headers")
        sys.exit(0)


if __name__ == '__main__':
    main()
