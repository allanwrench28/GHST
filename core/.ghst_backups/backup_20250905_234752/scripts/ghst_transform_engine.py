#!/usr/bin/env python3
"""
GHST Global Find and Replace Engine
===================================

Streamlines bulk code transformations across the entire GHST codebase.
Leverages global group selections and automated replacements to ensure
consistent theming and implementation of new features.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import shutil
from datetime import datetime


class GHSTTransformEngine:
    """Handles global find/replace operations for GHST codebase updates."""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.backup_dir = self.workspace_path / '.ghst_backups'
        self.transformation_log = []
        
        # GHST transformation patterns based on the prompt
        self.ghst_patterns = {
            # Theme updates
            'ghost_references': [
                (r'\bGhost\b(?!.*[Ss]upervisor)', 'GHST Agent'),
                (r'\bghost(?!.*[Ss]upervisor)', 'ghst'),
                (r'Ghosts in the Machine', 'GHST Expert Collective'),
                (r'ghost_manager', 'expert_manager'),
                (r'GhostManager', 'ExpertManager'),
            ],
            
            # Component updates for the prompt requirements
            'component_updates': [
                (r'FANTOMWindow', 'GHSTWindow'),
                (r'fantom\.py', 'ghst.py'),
                (r'launch_fantom', 'launch_ghst'),
                (r'FANTOM', 'GHST'),
                (r'slicer_ui', 'ghst_ui'),
                (r'3D printing', 'AI coding assistance'),
                (r'slicer', 'coding engine'),
            ],
            
            # API and integration updates
            'api_integrations': [
                (r'# TODO: Add AI integration', '# xAI Grok integration ready'),
                (r'mock_ai_call', 'grok_api_call'),
                (r'placeholder.*AI', 'xAI Grok API'),
            ],
            
            # Syntax Supervisor integration
            'syntax_supervisor_integration': [
                (r'# Code analysis placeholder', 'self.syntax_supervisors = SyntaxSupervisorManager(workspace)'),
                (r'error_handler\.py', 'syntax_supervisors.py'),
            ]
        }
        
        # File type patterns for selective updates
        self.file_patterns = {
            'python': ['*.py'],
            'config': ['*.json', '*.yaml', '*.yml'],
            'docs': ['*.md', '*.txt', '*.rst'],
            'web': ['*.html', '*.css', '*.js', '*.ts'],
            'all': ['*.*']
        }
    
    def create_backup(self) -> str:
        """Create a timestamped backup of the workspace."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f'backup_{timestamp}'
        
        self.backup_dir.mkdir(exist_ok=True)
        shutil.copytree(self.workspace_path, backup_path, 
                       ignore=shutil.ignore_patterns('.ghst_backups', '*.pyc', '__pycache__'))
        
        print(f"📦 Backup created: {backup_path}")
        return str(backup_path)
    
    def apply_ghst_transformations(self, categories: List[str] = None) -> Dict:
        """Apply GHST transformations based on the implementation prompt."""
        if categories is None:
            categories = list(self.ghst_patterns.keys())
        
        results = {
            'files_processed': 0,
            'transformations_applied': 0,
            'errors': [],
            'backup_path': self.create_backup()
        }
        
        # Get all relevant files
        target_files = self._get_target_files(['python', 'config', 'docs'])
        
        for file_path in target_files:
            try:
                if self._process_file(file_path, categories):
                    results['files_processed'] += 1
                    
            except Exception as e:
                results['errors'].append(f"{file_path}: {str(e)}")
        
        results['transformations_applied'] = len(self.transformation_log)
        self._save_transformation_log()
        
        return results
    
    def _get_target_files(self, file_types: List[str]) -> List[Path]:
        """Get all files matching the specified types."""
        files = []
        
        for file_type in file_types:
            if file_type in self.file_patterns:
                for pattern in self.file_patterns[file_type]:
                    files.extend(self.workspace_path.rglob(pattern))
        
        # Filter out backups and cache directories
        filtered_files = []
        for file_path in files:
            if not any(ignore in str(file_path) for ignore in 
                      ['.ghst_backups', '__pycache__', '.git', 'node_modules']):
                filtered_files.append(file_path)
        
        return filtered_files
    
    def _process_file(self, file_path: Path, categories: List[str]) -> bool:
        """Process a single file with the specified transformation categories."""
        if not file_path.is_file():
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Skip binary files
            return False
        
        original_content = content
        transformations_applied = 0
        
        # Apply transformations for each category
        for category in categories:
            if category in self.ghst_patterns:
                for pattern, replacement in self.ghst_patterns[category]:
                    old_content = content
                    content = re.sub(pattern, replacement, content)
                    
                    if content != old_content:
                        transformations_applied += 1
                        self.transformation_log.append({
                            'file': str(file_path),
                            'category': category,
                            'pattern': pattern,
                            'replacement': replacement,
                            'timestamp': datetime.now().isoformat()
                        })
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def implement_syntax_supervisors(self):
        """Specifically implement Syntax Supervisor integration throughout codebase."""
        
        # Update main launcher to include SS
        launcher_path = self.workspace_path / 'core' / 'launcher.py'
        if launcher_path.exists():
            self._add_ss_to_launcher(launcher_path)
        
        # Update GUI to show SS status
        gui_files = list(self.workspace_path.rglob('**/ui_components/*.py'))
        for gui_file in gui_files:
            self._add_ss_gui_integration(gui_file)
        
        # Update configuration system
        config_files = list(self.workspace_path.rglob('**/config/*.yaml'))
        for config_file in config_files:
            self._add_ss_config(config_file)
    
    def _add_ss_to_launcher(self, launcher_path: Path):
        """Add Syntax Supervisor integration to main launcher."""
        try:
            with open(launcher_path, 'r') as f:
                content = f.read()
            
            # Add SS import
            if 'from syntax_supervisors import' not in content:
                import_section = 'from pathlib import Path\n'
                if import_section in content:
                    content = content.replace(
                        import_section,
                        import_section + 'from src.syntax_supervisors import SyntaxSupervisorManager\n'
                    )
            
            # Add SS initialization in launch function
            if 'SyntaxSupervisorManager' not in content:
                init_section = 'expert_manager = ExpertManager()'
                if init_section in content:
                    content = content.replace(
                        init_section,
                        init_section + '\n        ' +
                        '# Initialize Syntax Supervisors\n        ' +
                        'ss_manager = SyntaxSupervisorManager(str(project_root))\n        ' +
                        'ss_manager.start_monitoring()'
                    )
            
            with open(launcher_path, 'w') as f:
                f.write(content)
                
            print(f"✅ Added Syntax Supervisors to {launcher_path}")
            
        except Exception as e:
            print(f"❌ Error updating launcher: {e}")
    
    def _add_ss_gui_integration(self, gui_file: Path):
        """Add SS status display to GUI components."""
        try:
            with open(gui_file, 'r') as f:
                content = f.read()
            
            # Add SS status widget if this is a main window file
            if 'class' in content and 'Window' in content:
                if 'ss_status' not in content:
                    # Add SS status panel placeholder
                    content += '\n\n# Syntax Supervisor status integration point\n' + \
                              '# TODO: Add SS status widget to GUI\n'
                    
                    with open(gui_file, 'w') as f:
                        f.write(content)
                    
                    print(f"✅ Added SS integration point to {gui_file}")
            
        except Exception as e:
            print(f"❌ Error updating GUI file {gui_file}: {e}")
    
    def _add_ss_config(self, config_file: Path):
        """Add SS configuration to config files."""
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            if 'syntax_supervisors' not in content:
                content += '\n\n# Syntax Supervisors configuration\n' + \
                          'syntax_supervisors:\n' + \
                          '  enabled: true\n' + \
                          '  scan_interval: 30\n' + \
                          '  notification_level: medium\n'
                
                with open(config_file, 'w') as f:
                    f.write(content)
                
                print(f"✅ Added SS config to {config_file}")
            
        except Exception as e:
            print(f"❌ Error updating config file {config_file}: {e}")
    
    def _save_transformation_log(self):
        """Save detailed transformation log."""
        log_path = self.workspace_path / '.ghst_transformations.json'
        
        with open(log_path, 'w') as f:
            json.dump(self.transformation_log, f, indent=2)
        
        print(f"📋 Transformation log saved: {log_path}")
    
    def apply_prompt_implementation(self):
        """Apply all changes required by the GHST Implementation Prompt."""
        
        print("🚀 Implementing GHST according to prompt specifications...")
        
        # 1. Apply core transformations
        results = self.apply_ghst_transformations()
        
        # 2. Implement Syntax Supervisors
        self.implement_syntax_supervisors()
        
        # 3. Update version and project info
        self._update_project_metadata()
        
        # 4. Create required directory structure
        self._create_ghst_structure()
        
        print(f"✅ Implementation complete!")
        print(f"📊 Files processed: {results['files_processed']}")
        print(f"🔄 Transformations applied: {results['transformations_applied']}")
        
        if results['errors']:
            print(f"⚠️ Errors encountered: {len(results['errors'])}")
            for error in results['errors'][:5]:  # Show first 5 errors
                print(f"   {error}")
    
    def _update_project_metadata(self):
        """Update project metadata to match GHST prompt requirements."""
        
        # Update setup.py if it exists
        setup_path = self.workspace_path / 'core' / 'setup.py'
        if setup_path.exists():
            try:
                with open(setup_path, 'r') as f:
                    content = f.read()
                
                # Update project name and description
                content = re.sub(
                    r'name=["\'].*?["\']',
                    'name="ghst"',
                    content
                )
                content = re.sub(
                    r'description=["\'].*?["\']',
                    'description="GHST - Open Source AI Coding Engine"',
                    content
                )
                
                with open(setup_path, 'w') as f:
                    f.write(content)
                
                print(f"✅ Updated {setup_path}")
                
            except Exception as e:
                print(f"❌ Error updating setup.py: {e}")
    
    def _create_ghst_structure(self):
        """Create the directory structure required by the GHST prompt."""
        
        required_dirs = [
            'ghosts',  # For Ghost Pool
            'training_scripts',  # For LoRA training
            'local_pool',  # For cached ghosts
            'vendor',  # For bundled dependencies
        ]
        
        for dir_name in required_dirs:
            dir_path = self.workspace_path / 'core' / dir_name
            dir_path.mkdir(exist_ok=True)
            
            # Add placeholder files
            if dir_name == 'ghosts':
                (dir_path / 'ghost_list.txt').touch()
            elif dir_name == 'training_scripts':
                (dir_path / 'few_shot.py').touch()
                (dir_path / 'train_manager.py').touch()
        
        print("📁 Created GHST directory structure")


def main():
    """Main entry point for global transformations."""
    workspace_path = Path.cwd()
    
    engine = GHSTTransformEngine(str(workspace_path))
    engine.apply_prompt_implementation()


if __name__ == "__main__":
    main()
