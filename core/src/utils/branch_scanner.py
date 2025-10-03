"""
Branch Scanner for GHST Expertise Branches

Scans the repository for expertise branches and identifies available
specialized knowledge modules.
"""

import logging
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any


class BranchScanner:
    """Scanner for discovering expertise branches in the repository."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize branch scanner.
        
        Args:
            repo_path: Path to the repository (defaults to current)
        """
        self.repo_path = repo_path or Path.cwd()
        self.logger = logging.getLogger(__name__)
        
    def scan_branches(self) -> List[Dict[str, Any]]:
        """Scan repository for expertise branches.
        
        Returns:
            List of branch information dictionaries
        """
        branches = []
        
        try:
            # Get all branches
            result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Remove branch prefix markers
                    branch_name = line.replace('* ', '').replace('remotes/origin/', '')
                    
                    # Skip special branches
                    if branch_name in ['main', 'master', 'HEAD']:
                        continue
                        
                    # Check if it's an expertise branch
                    if self._is_expertise_branch(branch_name):
                        branch_info = self._get_branch_info(branch_name)
                        if branch_info:
                            branches.append(branch_info)
                            
        except Exception as e:
            self.logger.error(f"Failed to scan branches: {e}")
            
        self.logger.info(f"Found {len(branches)} expertise branches")
        return branches
        
    def _is_expertise_branch(self, branch_name: str) -> bool:
        """Check if a branch is an expertise branch.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            True if it's an expertise branch
        """
        # Look for common expertise branch patterns
        expertise_patterns = [
            '-branch',
            '-expertise',
            '-plugin',
            'slicer',
            'web-dev',
            'devops',
            'security'
        ]
        
        branch_lower = branch_name.lower()
        return any(pattern in branch_lower for pattern in expertise_patterns)
        
    def _get_branch_info(self, branch_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a branch.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            Branch information dictionary or None
        """
        try:
            # Check if branch has a manifest file
            result = subprocess.run(
                ["git", "ls-tree", "-r", branch_name, "--name-only"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                files = result.stdout.split('\n')
                has_manifest = any('manifest.yaml' in f for f in files)
                has_expertise = any('expertise/' in f for f in files)
                
                return {
                    "name": branch_name,
                    "has_manifest": has_manifest,
                    "has_expertise_dir": has_expertise,
                    "valid": has_manifest and has_expertise,
                    "description": self._infer_description(branch_name)
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get branch info for {branch_name}: {e}")
            
        return None
        
    def _infer_description(self, branch_name: str) -> str:
        """Infer a description from the branch name.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            Inferred description
        """
        # Simple description inference
        name_lower = branch_name.lower()
        
        if 'slicer' in name_lower or '3d' in name_lower:
            return "3D Printing & Slicing Expertise"
        elif 'web' in name_lower:
            return "Web Development Expertise"
        elif 'devops' in name_lower or 'cicd' in name_lower:
            return "DevOps & CI/CD Expertise"
        elif 'security' in name_lower:
            return "Security & Vulnerability Expertise"
        else:
            return f"Expertise: {branch_name}"
            
    def get_available_expertise(self) -> List[str]:
        """Get list of available expertise domains.
        
        Returns:
            List of expertise domain names
        """
        branches = self.scan_branches()
        return [b['name'] for b in branches if b.get('valid', False)]
