"""
Error Handler for GHST Agent System

Captures runtime errors, analyzes them with AI, and submits pull requests
for fixes with proper disclaimers and safety warnings.

All AI-generated fixes include no-liability disclaimers.
"""

import hashlib
import logging
import queue
import threading
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional


class ErrorHandler:
def normalize_user_input(raw_input: str) -> str:
    """
    Normalize and auto-correct user input for 'ape' typing and natural language brains.
    - Fix common syntax errors (missing colons, parentheses, etc.)
    - Auto-correct simple spelling mistakes
    - Standardize casing and whitespace
    - Make input more robust for downstream processing
    """
    import re
    # Example: Add colon after 'def' if missing
    raw_input = re.sub(r'(def\s+\w+\(.*\))\s*$', r'\1:', raw_input)
    # Example: Fix common Python keywords
    raw_input = re.sub(r'pritn', 'print', raw_input, flags=re.IGNORECASE)
    raw_input = re.sub(r'improt', 'import', raw_input, flags=re.IGNORECASE)
    # Example: Remove excessive whitespace
    raw_input = re.sub(r'\s+', ' ', raw_input)
    # Example: Lowercase keywords
    for kw in ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with', 'as', 'print']:
        raw_input = re.sub(rf'\b{kw}\b', kw, raw_input, flags=re.IGNORECASE)
    # More advanced corrections can be added here
    return raw_input.strip()
    """Captures and processes errors for GHST Agent analysis and fixing."""

    def __init__(self, ghst_manager=None, github_token: Optional[str] = None):
        self.ghst_manager = ghst_manager
        self.github_token = github_token
        self.error_queue = queue.Queue()
        self.error_history = []
        self.processing_thread = None
        self.running = False

        # Error classification patterns
        self.error_patterns = {
            'mesh_errors': ['mesh', 'vertices', 'faces', 'manifold', 'geometry'],
            'slicing_errors': ['slice', 'layer', 'gcode', 'path', 'toolpath'],
            'io_errors': ['file', 'load', 'save', 'read', 'write', 'permission'],
            'memory_errors': ['memory', 'allocation', 'out of memory', 'malloc'],
            'ai_errors': ['ghst', 'ai', 'model', 'prediction', 'analysis'],
            'config_errors': ['config', 'setting', 'parameter', 'yaml', 'validation']
        }

        # Setup logging
        self.setup_logging()

        # Start error processing
        self.start_processing()

    def setup_logging(self):
        """Setup error logging system."""
        self.logger = logging.getLogger('ErrorHandler')

        # Create error log file handler
        log_path = Path('logs')
        log_path.mkdir(exist_ok=True)

        error_log_path = log_path / 'coding enginegpt_errors.log'
        file_handler = logging.FileHandler(error_log_path)
        file_handler.setLevel(logging.ERROR)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
            'GHST Agent Analysis: %(ghst_analysis)s\n'
            'Disclaimer: ⚠️ AI-generated analysis - verify before implementation\n',
            defaults={
                'ghst_analysis': 'Pending'})
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def start_processing(self):
        """Start error processing thread."""
        if self.running:
            return

        self.running = True
        self.processing_thread = threading.Thread(
            target=self._process_errors, daemon=True)
        self.processing_thread.start()

        if self.ghst_manager:
            self.ghst_manager.log_activity(
                "🚨 Error handler started - GHST Agent analysis enabled")

    def stop_processing(self):
        """Stop error processing."""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)

    def capture_exception(self, exception: Exception, context: str = "",
                          function_name: str = "", file_path: str = ""):
        """Capture an exception for GHST Agent analysis."""
        try:
            error_data = {
                'timestamp': datetime.now().isoformat(),
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'traceback': traceback.format_exc(),
                'context': context,
                'function_name': function_name,
                'file_path': file_path,
                'error_id': self._generate_error_id(exception, context),
                'severity': self._assess_severity(exception),
                'category': self._classify_error(exception, context)
            }

            # Add to queue for processing
            self.error_queue.put(error_data)

            # Log immediately
            self.logger.error(
                f"Captured {
                    error_data['exception_type']}: {
                    error_data['exception_message']}", extra={
                    'ghst_analysis': 'Queued for analysis'})

            if self.ghst_manager:
                self.ghst_manager.log_activity(
                    "🚨 Error captured: {
                        error_data['exception_type']} - GHST Agent analysis queued")

        except Exception as e:
            # Fallback logging - don't let error handler crash
            print("Error handler failed to capture exception: {e}")

    def capture_custom_error(self,
                             error_code: str,
                             message: str,
                             context: str = "",
                             severity: str = "error",
                             data: Dict[str,
                                        Any] = None):
        """Capture a custom error condition for GHST Agent analysis."""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_code': error_code,
            'message': message,
            'context': context,
            'severity': severity,
            'category': self._classify_custom_error(error_code, message),
            'error_id': self._generate_custom_error_id(error_code, message),
            'custom_data': data or {}
        }

        self.error_queue.put(error_data)

        if self.ghst_manager:
            self.ghst_manager.log_activity(
                "🔍 Custom error logged: {error_code} - {message[:50]}..."
            )

    def _process_errors(self):
        """Main error processing loop."""
        while self.running:
            try:
                # Get error from queue with timeout
                error_data = self.error_queue.get(timeout=1)

                # Process with GHST Agent analysis
                self._analyze_with_ghosts(error_data)

                # Add to history
                self.error_history.append(error_data)

                # Keep history manageable
                if len(self.error_history) > 100:
                    self.error_history = self.error_history[-50:]

            except queue.Empty:
                continue
            except Exception as e:
                print("Error processing failed: {e}")

    def _analyze_with_ghosts(self, error_data: Dict[str, Any]):
        """Analyze error with GHST Agent collective."""
        if not self.ghst_manager:
            return

        try:
            # Prepare analysis context
            analysis_context = self._prepare_analysis_context(error_data)

            # Get GHST Agent analysis
            if hasattr(self.ghst_manager, 'analyze_with_ai'):
                analysis = self.ghst_manager.analyze_with_ai(
                    problem=error_data.get(
                        'exception_message', error_data.get(
                            'message', '')), context=analysis_context)

                error_data['ghst_analysis'] = analysis

                # Log analysis results
                self.ghst_manager.log_activity(
                    f"🧠 GHST Agent analysis complete for {
                        error_data.get(
                            'error_id', 'unknown')}")

                # Check if fix should be submitted
                if self._should_submit_fix(analysis):
                    self._submit_ghost_fix(error_data, analysis)

            else:
                # Fallback analysis
                error_data['ghst_analysis'] = {
                    'status': 'basic_analysis',
                    'category': error_data.get(
                        'category',
                        'unknown'),
                    'severity': error_data.get(
                        'severity',
                        'unknown'),
                    'disclaimer': '⚠️ Basic analysis only - GHST Agent AI unavailable'}

        except Exception as e:
            self.ghst_manager.log_activity(
                "❌ GHST Agent analysis failed: {e}")

    def _prepare_analysis_context(self, error_data: Dict[str, Any]) -> str:
        """Prepare context for GHST Agent analysis."""
        context_parts = [
            "Error Type: {
                error_data.get(
                    'exception_type', error_data.get(
                        'error_code', 'Unknown'))}", "Category: {
                    error_data.get(
                        'category', 'Unknown')}", "Severity: {
                            error_data.get(
                                'severity', 'Unknown')}", "Context: {
                                    error_data.get(
                                        'context', 'Not provided')}", ]

        if 'function_name' in error_data:
            context_parts.append("Function: {error_data['function_name']}")

        if 'file_path' in error_data:
            context_parts.append("File: {error_data['file_path']}")

        if 'traceback' in error_data:
            # Include last few lines of traceback
            traceback_lines = error_data['traceback'].split('\n')
            relevant_lines = traceback_lines[-5:] if len(
                traceback_lines) > 5 else traceback_lines
            context_parts.append(
                "Traceback excerpt: {
                    ' | '.join(relevant_lines)}")

        return '\n'.join(context_parts)

    def _should_submit_fix(self, analysis: Dict[str, Any]) -> bool:
        """Determine if GHST Agent should submit a fix PR."""
        if not analysis or 'confidence' not in analysis:
            return False

        # Only submit high-confidence fixes for non-critical errors
        confidence = analysis.get('confidence', 0)
        severity = analysis.get('severity', 'unknown')

        # Conservative approach - only submit for clear, non-dangerous issues
        if confidence > 0.8 and severity in ['warning', 'info']:
            return True

        return False

    def _submit_ghost_fix(
            self, error_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Submit a GHST Agent-generated fix as a pull request."""
        if not self.ghst_manager or not hasattr(
                self.ghst_manager, 'submit_ghost_pr'):
            return

        try:
            # Generate fix description with disclaimers
            fix_description = self._generate_fix_description(
                error_data, analysis)

            # Simulate code changes (in real implementation, would generate
            # actual fixes)
            code_changes = self._generate_code_changes(error_data, analysis)

            # Submit PR through GHST Agent manager
            success = self.ghst_manager.submit_ghost_pr(
                ghst_id="error_ghost",
                fix_description=fix_description,
                code_changes=code_changes,
                error_context=self._prepare_analysis_context(error_data)
            )

            if success:
                self.ghst_manager.log_activity(
                    "📝 GHST Agent fix submitted for {
                        error_data.get(
                            'error_id', 'unknown')}")
            else:
                self.ghst_manager.log_activity(
                    "❌ GHST Agent fix submission failed for {
                        error_data.get(
                            'error_id', 'unknown')}")

        except Exception as e:
            if self.ghst_manager:
                self.ghst_manager.log_activity(
                    "❌ GHST Agent fix submission error: {e}")

    def _generate_fix_description(self, error_data: Dict[str, Any],
                                  analysis: Dict[str, Any]) -> str:
        """Generate fix description with safety disclaimers."""
        error_type = error_data.get(
            'exception_type', error_data.get(
                'error_code', 'Unknown'))

        description = """
#  # 🤖 AI-Generated Fix for {error_type}

##  # Problem Description
{error_data.get('exception_message', error_data.get('message', 'No description'))}

##  # Context
{error_data.get('context', 'No context provided')}

##  # Analysis Results
- **Category**: {analysis.get('problem_type', 'Unknown')}
- **Severity**: {analysis.get('severity', 'Unknown')}
- **Confidence**: {analysis.get('confidence', 0):.2%}

##  # Proposed Solution
{analysis.get('suggested_solutions', ['No solution provided'])[0] if analysis.get('suggested_solutions') else 'AI analysis incomplete'}

##  # FOSS References
{len(analysis.get('foss_references', []))} relevant FOSS projects found for reference.

##  # ⚠️ CRITICAL SAFETY DISCLAIMER
This fix was generated by AI (GHST Agent in the Machine). **SlicerGPT assumes NO LIABILITY** for:
- Code correctness or functionality
- Printer damage or safety issues
- Data loss or corruption
- Any unexpected behavior

**REQUIRED HUMAN VERIFICATION:**
- [ ] Code review by experienced developer
- [ ] Test in safe environment before production use
- [ ] Verify no security vulnerabilities introduced
- [ ] Confirm compatibility with existing systems
- [ ] Test with sample prints before real projects

**USE AT YOUR OWN RISK** - This is experimental AI-generated code!
        """

        return description.strip()

    def _generate_code_changes(self, error_data: Dict[str, Any],
                               analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate code changes for the fix (placeholder implementation)."""
        # In real implementation, this would use AI to generate actual code
        # fixes

        error_data.get('exception_type', error_data.get('error_code', ''))

        # Simulated code fixes based on error type
        fixes = {
            'mesh_validation.py': self._generate_mesh_fix(error_data),
            'error_handling.py': self._generate_error_handling_fix(error_data),
            'safety_checks.py': self._generate_safety_check_fix(error_data)
        }

        return fixes

    def _generate_mesh_fix(self, error_data: Dict[str, Any]) -> str:
        """Generate mesh-related fix code."""
        return '''
# AI-Generated Mesh Fix
# ⚠️ WARNING: Verify this code before use - No liability assumed!

def validate_mesh_safely(mesh):
    """
    Validate mesh with comprehensive error handling.
    Generated by GHST Agent AI - USE AT YOUR OWN RISK!
    """
    try:
        if mesh is None:
            raise ValueError("Mesh cannot be None")

        if not hasattr(mesh, 'vertices') or len(mesh.vertices) == 0:
            raise ValueError("Mesh has no vertices")

        if not hasattr(mesh, 'faces') or len(mesh.faces) == 0:
            raise ValueError("Mesh has no faces")

        # Additional validation
        if not mesh.is_watertight:
            logging.warning("Mesh is not watertight - may cause slicing issues")

        return True

    except Exception as e:
        logging.error("Mesh validation failed: {e}")
        # ⚠️ GHST Agent-generated error handling - verify before use!
        return False
'''

    def _generate_error_handling_fix(self, error_data: Dict[str, Any]) -> str:
        """Generate error handling improvement."""
        return '''
# AI-Generated Error Handling Enhancement
# ⚠️ WARNING: GHST Agent-generated code - No liability for errors or issues!

def enhanced_error_handler(func):
    """
    Decorator for enhanced error handling.
    Generated by GHST Agent AI - VERIFY BEFORE PRODUCTION USE!
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log error with context
            logging.error("Function {func.__name__} failed: {e}")

            # ⚠️ AI-generated error recovery - may not be safe!
            # Human verification required before deployment

            # Attempt graceful degradation
            return None

    return wrapper

# ⚠️ DISCLAIMER: This code was generated by AI
# SlicerGPT assumes NO LIABILITY for any issues caused by this code
# ALWAYS VERIFY AND TEST before using in production!
'''

    def _generate_safety_check_fix(self, error_data: Dict[str, Any]) -> str:
        """Generate safety check enhancement."""
        return '''
# AI-Generated Safety Enhancement
# ⚠️ CRITICAL WARNING: AI-generated safety code - MUST be reviewed by humans!

class SafetyChecker:
    """
    Enhanced safety checking system.
    Generated by GHST Agent AI - NO LIABILITY ASSUMED!
    """

    @staticmethod
    def verify_temperature_settings(hotend_temp, bed_temp, material_type):
        """
        Verify temperature settings are safe.
        ⚠️ AI-GENERATED - Human verification required!
        """
        # ⚠️ Temperature limits generated by AI - verify against printer specs!
        safe_limits = {
            'PLA': {'hotend': (180, 220), 'bed': (0, 70)},
            'ABS': {'hotend': (220, 260), 'bed': (60, 100)},
            'PETG': {'hotend': (220, 250), 'bed': (70, 90)}
        }

        if material_type not in safe_limits:
            raise ValueError("Unknown material type: {material_type}")

        limits = safe_limits[material_type]

        if not (limits['hotend'][0] <= hotend_temp <= limits['hotend'][1]):
            raise ValueError("Unsafe hotend temperature for {material_type}: {hotend_temp}°C")

        if not (limits['bed'][0] <= bed_temp <= limits['bed'][1]):
            raise ValueError("Unsafe bed temperature for {material_type}: {bed_temp}°C")

        return True

# ⚠️ CRITICAL DISCLAIMER:
# This safety code was generated by AI and may contain errors!
# ALWAYS verify temperature limits against your printer specifications
# SlicerGPT assumes NO LIABILITY for printer damage or safety issues!
'''

    def _generate_error_id(self, exception: Exception, context: str) -> str:
        """Generate unique ID for error."""
        error_string = "{type(exception).__name__}:{str(exception)}:{context}"
        return hashlib.md5(error_string.encode()).hexdigest()[:8]

    def _generate_custom_error_id(self, error_code: str, message: str) -> str:
        """Generate unique ID for custom error."""
        error_string = "{error_code}:{message}"
        return hashlib.md5(error_string.encode()).hexdigest()[:8]

    def _assess_severity(self, exception: Exception) -> str:
        """Assess error severity."""
        if isinstance(exception, (MemoryError, SystemError)):
            return 'critical'
        elif isinstance(exception, (ValueError, TypeError, KeyError)):
            return 'error'
        elif isinstance(exception, (UserWarning, RuntimeWarning)):
            return 'warning'
        else:
            return 'error'

    def _classify_error(self, exception: Exception, context: str) -> str:
        """Classify error by type."""
        error_text = "{
            type(exception).__name__} {
            str(exception)} {context}".lower()

        for category, keywords in self.error_patterns.items():
            if any(keyword in error_text for keyword in keywords):
                return category

        return 'general'

    def _classify_custom_error(self, error_code: str, message: str) -> str:
        """Classify custom error by content."""
        error_text = "{error_code} {message}".lower()

        for category, keywords in self.error_patterns.items():
            if any(keyword in error_text for keyword in keywords):
                return category

        return 'custom'

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for GHST Agent analysis."""
        if not self.error_history:
            return {'total_errors': 0}

        total_errors = len(self.error_history)

        # Count by category
        categories = {}
        severities = {}

        for error in self.error_history:
            category = error.get('category', 'unknown')
            severity = error.get('severity', 'unknown')

            categories[category] = categories.get(category, 0) + 1
            severities[severity] = severities.get(severity, 0) + 1

        # Recent error rate
        recent_errors = [
            e for e in self.error_history if (
                datetime.now() -
                datetime.fromisoformat(
                    e['timestamp'])).seconds < 3600]

        return {
            'total_errors': total_errors,
            'categories': categories,
            'severities': severities,
            'recent_hourly_rate': len(recent_errors),
            'most_common_category': max(
                categories.items(),
                key=lambda x: x[1])[0] if categories else 'none',
            'ghst_analysis_available': bool(
                self.ghst_manager)}

# Decorator for automatic error capture
def capture_errors(error_handler: ErrorHandler, context: str = ""):
    """Decorator to automatically capture errors for GHST Agent analysis."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.capture_exception(
                    exception=e,
                    context=context,
                    function_name=func.__name__,
                    file_path=func.__code__.co_filename
                )
                raise  # Re-raise the exception
        return wrapper
    return decorator
