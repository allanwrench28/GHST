#!/usr/bin/env python3
"""
GHST Intelligent Codebase Cleanup Daemon
========================================

Smart daemon that:
1. Identifies obsolete/unused files and scripts
2. Preserves innovative code patterns for ML enhancement
3. Archives old code instead of deleting (safety first)
4. Suggests ML integration opportunities
5. Maintains clean, focused codebase
"""

import os
import sys
import ast
import time
import json
import shutil
import logging
import io
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict

# Configure logging (UTF-8 safe handlers)
_stdout_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
file_handler = logging.FileHandler('codebase_cleanup_daemon.log', encoding='utf-8')
stream_handler = logging.StreamHandler(_stdout_stream)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyzes code for patterns, dependencies, and innovation potential"""
    
    def __init__(self):
        self.ml_keywords = {
            'machine_learning', 'neural', 'model', 'train', 'predict', 'algorithm',
            'optimization', 'heuristic', 'pattern', 'classification', 'regression',
            'clustering', 'ai', 'intelligence', 'learning', 'adaptive', 'genetic',
            'evolution', 'swarm', 'bayesian', 'markov', 'monte_carlo'
        }
        
        self.innovation_patterns = {
            'async_patterns': ['async', 'await', 'asyncio', 'concurrent'],
            'design_patterns': ['factory', 'singleton', 'observer', 'strategy'],
            'optimization': ['cache', 'memoize', 'lazy', 'efficient', 'optimized'],
            'ai_collaboration': ['agent', 'consensus', 'debate', 'collective'],
            'automation': ['auto', 'daemon', 'monitor', 'schedule'],
            'api_integration': ['rest', 'graphql', 'webhook', 'api'],
            'data_processing': ['pipeline', 'stream', 'batch', 'transform']
        }
        
    def analyze_python_file(self, filepath: Path) -> Dict:
        """Analyze Python file for complexity, dependencies, and patterns"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            analysis = {
                'filepath': str(filepath),
                'size_lines': len(content.split('\n')),
                'size_bytes': len(content.encode('utf-8')),
                'functions': [],
                'classes': [],
                'imports': [],
                'ml_potential': 0,
                'innovation_score': 0,
                'complexity_score': 0,
                'last_modified': filepath.stat().st_mtime,
                'patterns_found': []
            }
            
            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)
            
            # Calculate scores
            analysis['ml_potential'] = self._calculate_ml_potential(content, analysis)
            analysis['innovation_score'] = self._calculate_innovation_score(content)
            analysis['complexity_score'] = self._calculate_complexity_score(analysis)
            
            return analysis
            
        except Exception as e:
            logger.warning(f"⚠️ Could not analyze {filepath}: {e}")
            return {'filepath': str(filepath), 'error': str(e)}
    
    def _calculate_ml_potential(self, content: str, analysis: Dict) -> float:
        """Calculate potential for ML integration"""
        content_lower = content.lower()
        score = 0
        
        # Check for ML-related keywords
        ml_matches = sum(1 for keyword in self.ml_keywords if keyword in content_lower)
        score += ml_matches * 10
        
        # Check for data processing patterns
        if any(term in content_lower for term in ['data', 'process', 'analyze', 'pattern']):
            score += 20
        
        # Check for mathematical operations
        if any(term in content_lower for term in ['math', 'numpy', 'scipy', 'statistics']):
            score += 15
        
        # Complex algorithms indicate ML potential
        if analysis.get('complexity_score', 0) > 50:
            score += 25
        
        return min(score, 100)  # Cap at 100
    
    def _calculate_innovation_score(self, content: str) -> float:
        """Calculate innovation/uniqueness score"""
        content_lower = content.lower()
        score = 0
        patterns_found = []
        
        for pattern_type, keywords in self.innovation_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in content_lower)
            if matches > 0:
                score += matches * 5
                patterns_found.append(pattern_type)
        
        # Bonus for unique combinations
        if len(patterns_found) > 2:
            score += 20
        
        return min(score, 100)
    
    def _calculate_complexity_score(self, analysis: Dict) -> float:
        """Calculate complexity score"""
        score = 0
        
        # Function count
        score += len(analysis.get('functions', [])) * 2
        
        # Class count (higher weight)
        score += len(analysis.get('classes', [])) * 5
        
        # Import diversity
        score += len(set(analysis.get('imports', []))) * 1
        
        # File size factor
        lines = analysis.get('size_lines', 0)
        if lines > 100:
            score += (lines / 100) * 10
        
        return min(score, 100)


class CodebaseCleanupDaemon:
    """Intelligent codebase cleanup daemon"""
    
    def __init__(self, config_file='cleanup_daemon_config.json'):
        self.config = self.load_config(config_file)
        self.repo_path = Path(self.config.get('repo_path', '.'))
        self.archive_path = Path(self.config.get('archive_path', './archived_code'))
        self.check_interval = self.config.get('check_interval_hours', 24) * 3600
        self.analyzer = CodeAnalyzer()
        self.running = False
        
        # Thresholds
        self.obsolete_threshold_days = self.config.get('obsolete_threshold_days', 30)
        self.min_innovation_score = self.config.get('min_innovation_score', 30)
        self.min_ml_potential = self.config.get('min_ml_potential', 25)
        
        # Create archive directory
        self.archive_path.mkdir(exist_ok=True)
        
    def load_config(self, config_file):
        """Load configuration"""
        default_config = {
            'repo_path': '.',
            'archive_path': './archived_code',
            'check_interval_hours': 24,
            'obsolete_threshold_days': 30,
            'min_innovation_score': 30,
            'min_ml_potential': 25,
            'preserve_patterns': [
                'ai_collaboration',
                'machine_learning', 
                'optimization',
                'automation',
                'innovative_algorithms'
            ],
            'cleanup_extensions': ['.py', '.js', '.ts', '.java', '.cpp'],
            'exclude_directories': [
                '.git', '__pycache__', 'node_modules', 'dist', 'build',
                'venv', '.vscode', '.idea', 'archived_code'
            ],
            'never_delete': [
                'main.py', 'app.py', 'server.py', '__init__.py',
                'config.py', 'settings.py', 'requirements.txt'
            ]
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"⚠️ Could not load config: {e}")
        else:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"📝 Created default config: {config_file}")
        
        return default_config
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files in repository"""
        files = []
        exclude_dirs = set(self.config['exclude_directories'])
        
        for root, dirs, filenames in os.walk(self.repo_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for filename in filenames:
                if filename.endswith(tuple(self.config['cleanup_extensions'])):
                    filepath = Path(root) / filename
                    files.append(filepath)
        
        return files
    
    def analyze_codebase(self) -> Dict:
        """Analyze entire codebase"""
        logger.info("🔍 Analyzing codebase for cleanup opportunities...")
        
        files = self.find_python_files()
        analysis_results = {
            'total_files': len(files),
            'file_analyses': [],
            'obsolete_candidates': [],
            'ml_opportunities': [],
            'innovation_preserves': [],
            'cleanup_recommendations': []
        }
        
        for filepath in files:
            file_analysis = self.analyzer.analyze_python_file(filepath)
            if 'error' not in file_analysis:
                analysis_results['file_analyses'].append(file_analysis)
                
                # Categorize files
                self._categorize_file(file_analysis, analysis_results)
        
        return analysis_results
    
    def _categorize_file(self, analysis: Dict, results: Dict):
        """Categorize file based on analysis"""
        filepath = analysis['filepath']
        filename = Path(filepath).name
        
        # Never delete critical files
        if filename in self.config['never_delete']:
            return
        
        # Check if file is old and potentially obsolete
        days_old = (time.time() - analysis['last_modified']) / (24 * 3600)
        
        # ML Opportunities
        if analysis['ml_potential'] >= self.min_ml_potential:
            results['ml_opportunities'].append({
                'file': filepath,
                'ml_potential': analysis['ml_potential'],
                'innovation_score': analysis['innovation_score'],
                'recommendation': self._generate_ml_recommendation(analysis)
            })
        
        # Innovation Preservation
        elif analysis['innovation_score'] >= self.min_innovation_score:
            results['innovation_preserves'].append({
                'file': filepath,
                'innovation_score': analysis['innovation_score'],
                'patterns': analysis.get('patterns_found', []),
                'recommendation': 'Preserve for innovation patterns'
            })
        
        # Obsolete Candidates
        elif (days_old > self.obsolete_threshold_days and 
              analysis['complexity_score'] < 20 and
              analysis['innovation_score'] < 15):
            results['obsolete_candidates'].append({
                'file': filepath,
                'days_old': int(days_old),
                'size_lines': analysis['size_lines'],
                'complexity_score': analysis['complexity_score'],
                'recommendation': 'Archive (low value, old)'
            })
    
    def _generate_ml_recommendation(self, analysis: Dict) -> str:
        """Generate ML integration recommendation"""
        recommendations = []
        
        if analysis['ml_potential'] > 70:
            recommendations.append("High ML potential - integrate into think tank system")
        elif analysis['ml_potential'] > 50:
            recommendations.append("Good ML candidate - extract algorithms")
        else:
            recommendations.append("ML patterns detected - review for enhancement")
        
        if analysis['innovation_score'] > 60:
            recommendations.append("Contains innovative patterns worth preserving")
        
        return "; ".join(recommendations)
    
    def archive_obsolete_files(self, obsolete_files: List[Dict]) -> int:
        """Archive obsolete files instead of deleting"""
        archived_count = 0
        
        for file_info in obsolete_files:
            filepath = Path(file_info['file'])
            
            if not filepath.exists():
                continue
            
            # Create archive structure
            relative_path = filepath.relative_to(self.repo_path)
            archive_dest = self.archive_path / relative_path
            archive_dest.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                # Copy to archive
                shutil.copy2(filepath, archive_dest)
                
                # Create metadata
                metadata = {
                    'archived_date': datetime.now().isoformat(),
                    'original_path': str(filepath),
                    'reason': file_info['recommendation'],
                    'file_info': file_info
                }
                
                metadata_file = archive_dest.with_suffix('.meta.json')
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                # Remove original
                filepath.unlink()
                
                logger.info(f"📦 Archived: {relative_path}")
                archived_count += 1
                
            except Exception as e:
                logger.error(f"❌ Failed to archive {filepath}: {e}")
        
        return archived_count
    
    def generate_ml_integration_report(self, ml_opportunities: List[Dict]):
        """Generate report for ML integration opportunities"""
        report_path = self.repo_path / 'ML_INTEGRATION_OPPORTUNITIES.md'
        
        with open(report_path, 'w') as f:
            f.write("# 🤖 ML Integration Opportunities\n\n")
            f.write("Files with potential for machine learning enhancement:\n\n")
            
            for opportunity in sorted(ml_opportunities, 
                                    key=lambda x: x['ml_potential'], reverse=True):
                f.write(f"## {Path(opportunity['file']).name}\n\n")
                f.write(f"- **File**: `{opportunity['file']}`\n")
                f.write(f"- **ML Potential**: {opportunity['ml_potential']}/100\n")
                f.write(f"- **Innovation Score**: {opportunity['innovation_score']}/100\n")
                f.write(f"- **Recommendation**: {opportunity['recommendation']}\n\n")
        
        logger.info(f"📊 Generated ML integration report: {report_path}")
    
    def run_cleanup_cycle(self):
        """Run one cleanup cycle"""
        logger.info("🧹 Starting intelligent codebase cleanup cycle")
        
        analysis = self.analyze_codebase()
        
        logger.info(f"📁 Analyzed {analysis['total_files']} files")
        logger.info(f"🤖 Found {len(analysis['ml_opportunities'])} ML opportunities")
        logger.info(f"💡 Found {len(analysis['innovation_preserves'])} innovative files")
        logger.info(f"🗑️ Found {len(analysis['obsolete_candidates'])} obsolete candidates")
        
        # Archive obsolete files
        if analysis['obsolete_candidates']:
            archived = self.archive_obsolete_files(analysis['obsolete_candidates'])
            logger.info(f"📦 Archived {archived} obsolete files")
        
        # Generate ML opportunities report
        if analysis['ml_opportunities']:
            self.generate_ml_integration_report(analysis['ml_opportunities'])
        
        # Generate summary report
        self._generate_summary_report(analysis)
        
        logger.info("✅ Cleanup cycle completed")
    
    def _generate_summary_report(self, analysis: Dict):
        """Generate cleanup summary report"""
        report_path = self.repo_path / 'CODEBASE_CLEANUP_REPORT.md'
        
        with open(report_path, 'w') as f:
            f.write("# 🧹 Codebase Cleanup Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Files Analyzed**: {analysis['total_files']}\n")
            f.write(f"- **ML Opportunities**: {len(analysis['ml_opportunities'])}\n")
            f.write(f"- **Innovation Preserves**: {len(analysis['innovation_preserves'])}\n")
            f.write(f"- **Files Archived**: {len(analysis['obsolete_candidates'])}\n\n")
            
            if analysis['ml_opportunities']:
                f.write("## 🤖 Top ML Integration Opportunities\n\n")
                for opp in analysis['ml_opportunities'][:5]:
                    f.write(f"- `{Path(opp['file']).name}` (ML: {opp['ml_potential']}/100)\n")
                f.write("\n")
            
            if analysis['innovation_preserves']:
                f.write("## 💡 Preserved Innovation Files\n\n")
                for preserve in analysis['innovation_preserves'][:5]:
                    f.write(f"- `{Path(preserve['file']).name}` (Innovation: {preserve['innovation_score']}/100)\n")
        
        logger.info(f"📋 Generated summary report: {report_path}")
    
    def run_daemon(self):
        """Run cleanup daemon continuously"""
        logger.info("🚀 Starting GHST Intelligent Cleanup Daemon")
        logger.info(f"📁 Repository: {self.repo_path.absolute()}")
        logger.info(f"📦 Archive path: {self.archive_path.absolute()}")
        logger.info(f"⏱️ Check interval: {self.check_interval/3600:.1f} hours")
        
        self.running = True
        
        try:
            while self.running:
                try:
                    self.run_cleanup_cycle()
                    
                    logger.info(f"😴 Sleeping for {self.check_interval/3600:.1f} hours")
                    time.sleep(self.check_interval)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"❌ Cleanup cycle error: {e}")
                    time.sleep(3600)  # Wait 1 hour before retry
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            logger.info("👋 Cleanup daemon stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GHST Intelligent Cleanup Daemon')
    parser.add_argument('--config', default='cleanup_daemon_config.json')
    parser.add_argument('--once', action='store_true',
                       help='Run cleanup once instead of as daemon')
    parser.add_argument('--dry-run', action='store_true',
                       help='Analyze only, don\'t archive files')
    
    args = parser.parse_args()
    
    daemon = CodebaseCleanupDaemon(args.config)
    
    if args.once:
        if args.dry_run:
            logger.info("🔍 Running analysis only (dry run)")
            analysis = daemon.analyze_codebase()
            daemon._generate_summary_report(analysis)
            if analysis['ml_opportunities']:
                daemon.generate_ml_integration_report(analysis['ml_opportunities'])
        else:
            daemon.run_cleanup_cycle()
    else:
        daemon.run_daemon()


if __name__ == '__main__':
    main()
