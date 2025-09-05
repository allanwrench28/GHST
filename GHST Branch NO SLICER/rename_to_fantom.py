#!/usr/bin/env python3
"""
FANTOM Global Rename Script
Renames all instances of FANTOM/fantom to FANTOM/fantom throughout the project

The Ghost Collective's official rebrand operation!
👻 29 Ghosts working together to transform our digital home
"""

import os
import re
import shutil
from pathlib import Path

class FantomRename:
    """Global rename utility for the FANTOM rebrand"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.replacements = {
            # Case variations
            'FANTOM': 'FANTOM',
            'fantom': 'fantom',
            'FANTOM': 'FANTOM',
            'FANTOM': 'FANTOM',
            'FANTOM2': 'FANTOM',
            
            # File/folder specific
            'launch_fantom.py': 'launch_fantom.py',
            'test_fantom.py': 'test_fantom.py',
        }
        
        # Files to process
        self.file_patterns = [
            '*.py', '*.md', '*.txt', '*.json', '*.yaml', '*.yml', 
            '*.cfg', '*.ini', '*.toml', '*.requirements'
        ]
        
        # Files/folders to skip
        self.skip_patterns = [
            '.git/', '__pycache__/', '.venv/', '*.pyc',
            '.github/workflows/', 'node_modules/'
        ]
        
    def should_skip_file(self, file_path):
        """Check if file should be skipped"""
        file_str = str(file_path)
        for pattern in self.skip_patterns:
            if pattern in file_str:
                return True
        return False
        
    def rename_file_contents(self, file_path):
        """Rename FANTOM to FANTOM in file contents"""
        if self.should_skip_file(file_path):
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Apply all replacements
            for old, new in self.replacements.items():
                content = content.replace(old, new)
                
            # Special case: update repository URLs
            content = re.sub(
                r'github\.com/allanwrench28/FANTOM',
                'github.com/allanwrench28/FANTOM',
                content
            )
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Updated: {file_path}")
                return True
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            
        return False
        
    def rename_files_and_folders(self):
        """Rename files and folders containing 'fantom'"""
        renamed_items = []
        
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            
            # Skip certain directories
            if self.should_skip_file(root_path):
                continue
                
            # Rename files
            for file in files:
                old_path = root_path / file
                new_name = file
                
                for old, new in self.replacements.items():
                    if old.lower() in file.lower():
                        new_name = file.replace(old, new)
                        break
                        
                if new_name != file:
                    new_path = root_path / new_name
                    try:
                        shutil.move(str(old_path), str(new_path))
                        renamed_items.append((str(old_path), str(new_path)))
                        print(f"📁 Renamed file: {file} → {new_name}")
                    except Exception as e:
                        print(f"❌ Error renaming {old_path}: {e}")
                        
        return renamed_items
        
    def process_all_files(self):
        """Process all files for content replacement"""
        updated_files = []
        
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            
            if self.should_skip_file(root_path):
                continue
                
            for file in files:
                file_path = root_path / file
                
                # Check if file matches our patterns
                if any(file_path.match(pattern) for pattern in self.file_patterns):
                    if self.rename_file_contents(file_path):
                        updated_files.append(str(file_path))
                        
        return updated_files
        
    def execute_rebrand(self):
        """Execute the complete FANTOM rebrand"""
        print("🚀 FANTOM REBRAND OPERATION STARTING!")
        print("👻 29 Ghosts working together...")
        print()
        
        # Step 1: Update file contents
        print("📝 Step 1: Updating file contents...")
        updated_files = self.process_all_files()
        print(f"✅ Updated {len(updated_files)} files")
        print()
        
        # Step 2: Rename files and folders
        print("📁 Step 2: Renaming files and folders...")
        renamed_items = self.rename_files_and_folders()
        print(f"✅ Renamed {len(renamed_items)} items")
        print()
        
        print("🎉 FANTOM REBRAND COMPLETE!")
        print("👻 Welcome to the FANTOM Ghost Collective!")
        
        return {
            'updated_files': updated_files,
            'renamed_items': renamed_items
        }

if __name__ == "__main__":
    # Run from project root
    project_root = Path(__file__).parent
    renamer = FantomRename(project_root)
    
    print("🔍 FANTOM Rebrand Script")
    print("👻 Created by the 29-Ghost Collective")
    print()
    
    confirm = input("Proceed with FANTOM rebrand? (y/N): ")
    if confirm.lower() == 'y':
        results = renamer.execute_rebrand()
        print(f"\n📊 Summary:")
        print(f"   Files updated: {len(results['updated_files'])}")
        print(f"   Items renamed: {len(results['renamed_items'])}")
    else:
        print("❌ Rebrand cancelled")
