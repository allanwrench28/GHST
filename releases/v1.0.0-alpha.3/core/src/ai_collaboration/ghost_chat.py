"""
GHST Agent Chat Interface - Conversational AI for GHST

This module provides a chat interface allowing users to directly communicate
with the GHST Agent collective for assistance with slicing, troubleshooting,
theme customization, and AI coding assistance guidance.

Features:
- Direct chat with PhD-level GHST Agent specialists
- Auto-slicing recommendations
- Theme randomization and customization
- Real-time troubleshooting assistance
- Educational AI coding assistance guidance

⚠️ DISCLAIMER: AI-generated recommendations. Always verify before use.
"""

import re
import json
import time
import random
from typing import Dict, List, Optional, Any
from datetime import datetime


class GhostChatInterface:
    """Conversational interface for interacting with the GHST Agent collective."""
    
    def __init__(self, ghst_manager):
        self.ghst_manager = ghst_manager
        self.chat_history = []
        self.user_preferences = {}
        self.available_themes = {
            'material_dark': 'Material Design Dark Theme',
            'cyberpunk': 'Cyberpunk Neon Theme', 
            'forest': 'Forest Green Theme',
            'ocean': 'Ocean Blue Theme',
            'sunset': 'Warm Sunset Theme',
            'monochrome': 'Elegant Monochrome Theme',
            'retro': 'Retro 80s Theme',
            'professional': 'Professional Corporate Theme'
        }
        
    def process_user_message(self, message: str) -> str:
        """Process user message and route to appropriate GHST Agent specialist."""
        message_lower = message.lower()
        
        # Store message in history
        self.chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': message,
            'response': None
        })
        
        # Check for idea capture keywords first
        if any(word in message_lower for word in ['idea:', 'feature:', 'what if', 'could we', 'suggestion:']):
            response = self._handle_idea_capture(message)
        # Route message to appropriate GHST Agent based on keywords
        elif any(word in message_lower for word in ['theme', 'color', 'appearance', 'visual']):
            response = self._handle_visual_query(message)
        elif any(word in message_lower for word in ['slice', 'print', 'gcode', 'settings']):
            response = self._handle_slicing_query(message)
        elif any(word in message_lower for word in ['error', 'problem', 'issue', 'bug']):
            response = self._handle_error_query(message)
        elif any(word in message_lower for word in ['optimize', 'improve', 'better', 'faster']):
            response = self._handle_optimization_query(message)
        elif any(word in message_lower for word in ['material', 'filament', 'temperature']):
            response = self._handle_materials_query(message)
        elif any(word in message_lower for word in ['random', 'surprise', 'choose']):
            response = self._handle_randomization_query(message)
        elif any(word in message_lower for word in ['tasks', 'ideas', 'background', 'todo']):
            response = self._handle_task_management_query(message)
        else:
            response = self._handle_general_query(message)
            
        # Update chat history with response
        self.chat_history[-1]['response'] = response
        return response
    
    def _handle_visual_query(self, message: str) -> str:
        """Handle visual/theme related queries."""
        if 'random' in message.lower() or 'surprise' in message.lower():
            theme = random.choice(list(self.available_themes.keys()))
            return f"🎨 **Dr. ColorScience & Dr. UXDesign**: I've randomly selected the '{self.available_themes[theme]}' for you! This theme offers excellent visual balance and modern aesthetics. Would you like me to apply it?"
        
        return f"🎨 **Dr. ColorScience**: I can help with visual customization! Available themes: {', '.join(self.available_themes.values())}. I also optimize color contrast ratios and ensure accessibility compliance. What specific visual aspect would you like to improve?"
    
    def _handle_slicing_query(self, message: str) -> str:
        """Handle slicing and AI coding assistance queries."""
        responses = [
            "⚙️ **Dr. Manufacturing & Dr. Physics**: For optimal slicing, I recommend analyzing your model's geometry first. What's your nozzle diameter and material type?",
            "🔬 **Dr. Materials & Dr. Quality**: I can optimize print settings based on your specific filament. PLA, PETG, or ABS? Each requires different temperature and speed profiles.",
            "📐 **Dr. Mathematics**: I'll calculate optimal layer heights and infill patterns for your model. What's the intended use - prototype, functional part, or display piece?"
        ]
        return random.choice(responses)
    
    def _handle_error_query(self, message: str) -> str:
        """Handle error and troubleshooting queries."""
        return f"🚨 **Dr. Error & Dr. FileSystem**: I'm analyzing your issue. Common problems include: file path issues, configuration errors, or dependency conflicts. Can you share the specific error message? I'll cross-reference with our knowledge base."
    
    def _handle_optimization_query(self, message: str) -> str:
        """Handle optimization and performance queries."""
        return f"⚡ **Dr. Efficiency & Dr. Optimization**: I'll analyze performance bottlenecks and suggest improvements. Are you looking to optimize print time, quality, material usage, or software performance?"
    
    def _handle_materials_query(self, message: str) -> str:
        """Handle material science queries."""
        return f"🧪 **Dr. Materials**: I can provide detailed material guidance! Each polymer has unique thermal properties, crystallization behavior, and optimal processing parameters. What material are you working with?"
    
    def _handle_randomization_query(self, message: str) -> str:
        """Handle randomization requests."""
        if 'theme' in message.lower():
            theme = random.choice(list(self.available_themes.keys()))
            return f"🎲 **Dr. Innovation**: Surprise! I've selected '{self.available_themes[theme]}' - it'll give your interface a fresh new look!"
        else:
            return f"🎲 **Dr. Innovation**: I love creative randomization! I can randomize themes, suggest experimental print settings, or generate novel infill patterns. What would you like me to surprise you with?"
    
    def _handle_general_query(self, message: str) -> str:
        """Handle general queries and provide helpful guidance."""
        return ("👻 **GHST Agent Collective**: Hello! Our 25 PhD-level specialists "
                "are here to help, with Dr. Ethics GHST Agent ensuring responsible "
                "AI behavior. We cover everything from color science to "
                "manufacturing optimization. Try asking about 'slicing "
                "settings', 'theme customization', 'error troubleshooting', "
                "or 'material guidance'!")
    
    def _handle_ethical_query(self, message: str) -> str:
        """Handle ethics and safety related queries."""
        return ("⚖️ **Dr. Ethics**: I ensure all AI recommendations "
                "prioritize human safety and agency. Remember: you maintain "
                "ultimate authority over all decisions. All AI-generated "
                "content requires your validation before use. How can I "
                "help you use GHST responsibly?")
    
    def request_human_approval(self, action_type: str, details: str) -> bool:
        """Request human approval for critical actions."""
        approval_request = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'details': details,
            'status': 'pending_approval'
        }
        
        # Store request for GUI display
        if not hasattr(self, 'pending_approvals'):
            self.pending_approvals = []
        self.pending_approvals.append(approval_request)
        
        # Log the request
        self.chat_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': 'SYSTEM_REQUEST',
            'response': (f"⚖️ **APPROVAL NEEDED**: {action_type}\n{details}\n"
                         "Please review and approve/deny this action.")
        })
        
        return False  # Default to requiring approval
    
    def get_available_commands(self) -> List[str]:
        """Get list of available chat commands."""
        return [
            "randomize theme - Apply a random color theme",
            "optimize settings - Get slicing optimization suggestions",
            "troubleshoot error - Get help with technical issues",
            "material advice - Get material-specific guidance",
            "visual customization - Customize interface appearance",
            "auto slice - Get automated slicing recommendations"
        ]
    
    def get_chat_history(self, limit: int = 10) -> List[Dict]:
        """Get recent chat history."""
        return self.chat_history[-limit:] if self.chat_history else []
    
    def clear_chat_history(self):
        """Clear chat history."""
        self.chat_history = []
        
    def export_chat_log(self, filename: str = None) -> str:
        """Export chat history to file."""
        if not filename:
            filename = f"ghst_chat_log_{int(time.time())}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, indent=2, ensure_ascii=False)
        
        return filename
