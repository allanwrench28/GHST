"""
GHST Think Tank VS Code-Style GUI
================================

A beautiful VS Code-inspired interface for the PhD Think Tank system.
"""

import sys
import asyncio
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Add the core modules to path
sys.path.append(str(Path(__file__).parent))

try:
    from think_tank_integration import ghst_think_tank
except ImportError:
    print("Warning: Think tank integration not available")
    ghst_think_tank = None


class VSCodeColors:
    """VS Code dark theme colors"""
    BACKGROUND = "#1e1e1e"
    SIDEBAR = "#252526"
    EDITOR = "#1e1e1e"
    ACTIVE_TAB = "#1e1e1e"
    INACTIVE_TAB = "#2d2d30"
    TEXT = "#d4d4d4"
    ACCENT = "#007acc"
    SUCCESS = "#4ec9b0"
    WARNING = "#ffcc02"
    ERROR = "#f44747"
    BORDER = "#3e3e42"


class ThinkTankWorker(QThread):
    """Worker thread for think tank operations"""
    
    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(str)
    
    def __init__(self, problem, context):
        super().__init__()
        self.problem = problem
        self.context = context
    
    def run(self):
        """Run think tank analysis in background"""
        if not ghst_think_tank:
            self.result_ready.emit({
                'error': 'Think tank system not available',
                'solution': 'Mock solution for demo purposes',
                'confidence': 0.85,
                'phd_experts': {
                    'supporting': ['Dr. Algorithm', 'Dr. Architect'],
                    'dissenting': ['Dr. Performance']
                }
            })
            return
        
        try:
            self.progress_update.emit("🧠 Initializing PhD Think Tank...")
            
            # Create event loop for async operation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.progress_update.emit("🎓 Assembling PhD experts...")
            
            result = loop.run_until_complete(
                ghst_think_tank.solve_coding_problem(self.problem, self.context)
            )
            
            self.progress_update.emit("✅ Consensus reached!")
            self.result_ready.emit(result)
            
        except Exception as e:
            self.result_ready.emit({
                'error': str(e),
                'solution': 'Error occurred during analysis',
                'confidence': 0.0
            })


class ExpertCard(QWidget):
    """Card widget for displaying PhD expert info"""
    
    def __init__(self, name, field, specialization, status="active"):
        super().__init__()
        self.setup_ui(name, field, specialization, status)
    
    def setup_ui(self, name, field, specialization, status):
        """Setup expert card UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Expert name with PhD icon
        name_layout = QHBoxLayout()
        icon_label = QLabel("🎓")
        icon_label.setStyleSheet("font-size: 16px;")
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            color: {VSCodeColors.TEXT};
            font-weight: bold;
            font-size: 14px;
        """)
        
        status_dot = QLabel("●")
        status_color = VSCodeColors.SUCCESS if status == "active" else VSCodeColors.WARNING
        status_dot.setStyleSheet(f"color: {status_color}; font-size: 12px;")
        
        name_layout.addWidget(icon_label)
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        name_layout.addWidget(status_dot)
        
        # PhD field
        field_label = QLabel(f"PhD in {field}")
        field_label.setStyleSheet(f"""
            color: {VSCodeColors.ACCENT};
            font-size: 12px;
            font-weight: bold;
        """)
        
        # Specialization
        spec_label = QLabel(specialization)
        spec_label.setStyleSheet(f"""
            color: {VSCodeColors.TEXT};
            font-size: 11px;
            opacity: 0.8;
        """)
        spec_label.setWordWrap(True)
        
        layout.addLayout(name_layout)
        layout.addWidget(field_label)
        layout.addWidget(spec_label)
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {VSCodeColors.SIDEBAR};
                border: 1px solid {VSCodeColors.BORDER};
                border-radius: 6px;
                margin: 4px;
            }}
            QWidget:hover {{
                border-color: {VSCodeColors.ACCENT};
            }}
        """)
        
        self.setFixedHeight(100)


class ThinkTankGUI(QMainWindow):
    """Main think tank GUI window"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.worker = None
    
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("GHST PhD Think Tank - VS Code Style")
        self.setGeometry(100, 100, 1400, 900)
        
        # Apply VS Code dark theme
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {VSCodeColors.BACKGROUND};
                color: {VSCodeColors.TEXT};
            }}
            QTextEdit, QPlainTextEdit {{
                background-color: {VSCodeColors.EDITOR};
                color: {VSCodeColors.TEXT};
                border: 1px solid {VSCodeColors.BORDER};
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }}
            QPushButton {{
                background-color: {VSCodeColors.ACCENT};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #1177bb;
            }}
            QPushButton:pressed {{
                background-color: #0d5299;
            }}
            QLabel {{
                color: {VSCodeColors.TEXT};
            }}
            QScrollArea {{
                background-color: {VSCodeColors.SIDEBAR};
                border: 1px solid {VSCodeColors.BORDER};
            }}
        """)
        
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left sidebar - Expert panel
        self.setup_expert_panel(splitter)
        
        # Main content area
        self.setup_main_content(splitter)
        
        # Right panel - Results
        self.setup_results_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 700, 400])
        
        # Status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: {VSCodeColors.ACCENT};
                color: white;
                border: none;
            }}
        """)
        self.statusBar().showMessage("🧠 GHST PhD Think Tank Ready")
    
    def setup_expert_panel(self, parent):
        """Setup the expert panel (left sidebar)"""
        expert_widget = QWidget()
        expert_layout = QVBoxLayout()
        expert_widget.setLayout(expert_layout)
        
        # Panel title
        title = QLabel("🎓 PhD Experts")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {VSCodeColors.TEXT};
            padding: 12px;
            background-color: {VSCodeColors.SIDEBAR};
        """)
        expert_layout.addWidget(title)
        
        # Scroll area for expert cards
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        
        # Add expert cards
        experts = [
            ("Dr. Algorithm", "Computer Science", "Algorithms & Data Structures"),
            ("Dr. Architect", "Software Engineering", "Software Architecture"),
            ("Dr. Performance", "Systems Engineering", "Performance & Scalability"),
            ("Dr. Mathematics", "Mathematics", "Optimization Theory"),
            ("Dr. Security", "Security", "Cybersecurity"),
            ("Dr. MachineLearning", "Machine Learning", "AI/ML Systems"),
            ("Dr. UserExperience", "HCI", "Human-Computer Interaction"),
            ("Dr. Database", "Database Systems", "Data Management")
        ]
        
        for name, field, spec in experts:
            card = ExpertCard(name, field, spec)
            scroll_layout.addWidget(card)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        expert_layout.addWidget(scroll_area)
        
        expert_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {VSCodeColors.SIDEBAR};
                border-right: 1px solid {VSCodeColors.BORDER};
            }}
        """)
        expert_widget.setFixedWidth(320)
        parent.addWidget(expert_widget)
    
    def setup_main_content(self, parent):
        """Setup the main content area"""
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)
        
        # Title bar
        title_bar = QWidget()
        title_layout = QHBoxLayout()
        title_bar.setLayout(title_layout)
        
        title = QLabel("🧠 Problem Analysis")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {VSCodeColors.TEXT};
            padding: 12px;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        # Analyze button
        self.analyze_btn = QPushButton("🔍 Analyze with Think Tank")
        self.analyze_btn.clicked.connect(self.start_analysis)
        title_layout.addWidget(self.analyze_btn)
        
        content_layout.addWidget(title_bar)
        
        # Problem input area
        problem_label = QLabel("📝 Describe your coding problem:")
        problem_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {VSCodeColors.TEXT};
            margin-bottom: 8px;
        """)
        content_layout.addWidget(problem_label)
        
        self.problem_input = QPlainTextEdit()
        self.problem_input.setPlaceholderText(
            "Describe your coding problem here...\n\n"
            "Example:\n"
            "I need to optimize a Python function that processes large CSV files "
            "(10GB+) with memory constraints. Current implementation loads entire "
            "file into memory and causes out-of-memory errors."
        )
        self.problem_input.setMinimumHeight(200)
        content_layout.addWidget(self.problem_input)
        
        # Context area
        context_label = QLabel("⚙️ Additional Context (JSON format):")
        context_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {VSCodeColors.TEXT};
            margin-top: 16px;
            margin-bottom: 8px;
        """)
        content_layout.addWidget(context_label)
        
        self.context_input = QPlainTextEdit()
        self.context_input.setPlaceholderText(
            '{\n'
            '  "language": "Python",\n'
            '  "data_size": "10GB",\n'
            '  "memory_limit": "8GB",\n'
            '  "performance_requirement": "< 5 minutes"\n'
            '}'
        )
        self.context_input.setMinimumHeight(120)
        content_layout.addWidget(self.context_input)
        
        # Progress area
        self.progress_label = QLabel("💡 Ready to analyze your problem")
        self.progress_label.setStyleSheet(f"""
            font-size: 13px;
            color: {VSCodeColors.ACCENT};
            padding: 8px;
            background-color: {VSCodeColors.SIDEBAR};
            border-radius: 4px;
            margin-top: 16px;
        """)
        content_layout.addWidget(self.progress_label)
        
        parent.addWidget(content_widget)
    
    def setup_results_panel(self, parent):
        """Setup the results panel (right side)"""
        results_widget = QWidget()
        results_layout = QVBoxLayout()
        results_widget.setLayout(results_layout)
        
        # Panel title
        title = QLabel("📊 Think Tank Results")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {VSCodeColors.TEXT};
            padding: 12px;
            background-color: {VSCodeColors.SIDEBAR};
        """)
        results_layout.addWidget(title)
        
        # Results display area
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setPlaceholderText(
            "Think tank results will appear here...\n\n"
            "✅ Solution consensus\n"
            "📊 Confidence score\n" 
            "🎓 Supporting experts\n"
            "📋 Implementation plan\n"
            "🔬 Evidence quality"
        )
        results_layout.addWidget(self.results_display)
        
        results_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {VSCodeColors.BACKGROUND};
                border-left: 1px solid {VSCodeColors.BORDER};
            }}
        """)
        results_widget.setFixedWidth(420)
        parent.addWidget(results_widget)
    
    def start_analysis(self):
        """Start think tank analysis"""
        problem = self.problem_input.toPlainText().strip()
        if not problem:
            self.show_message("Please enter a problem description", "warning")
            return
        
        # Parse context
        context = {}
        context_text = self.context_input.toPlainText().strip()
        if context_text:
            try:
                import json
                context = json.loads(context_text)
            except json.JSONDecodeError:
                self.show_message("Invalid JSON in context field", "error")
                return
        
        # Disable button and start analysis
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setText("🔄 Analyzing...")
        
        # Start worker thread
        self.worker = ThinkTankWorker(problem, context)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.result_ready.connect(self.show_results)
        self.worker.start()
    
    def update_progress(self, message):
        """Update progress message"""
        self.progress_label.setText(message)
        self.statusBar().showMessage(message)
    
    def show_results(self, result):
        """Display think tank results"""
        self.analyze_btn.setEnabled(True)
        self.analyze_btn.setText("🔍 Analyze with Think Tank")
        
        if 'error' in result:
            self.results_display.setHtml(f"""
                <div style="color: {VSCodeColors.ERROR};">
                    <h3>❌ Error</h3>
                    <p>{result['error']}</p>
                </div>
            """)
            self.show_message("Analysis failed", "error")
            return
        
        # Format results
        supporting = ', '.join(result.get('phd_experts', {}).get('supporting', []))
        dissenting = ', '.join(result.get('phd_experts', {}).get('dissenting', []))
        
        html_content = f"""
        <div style="color: {VSCodeColors.TEXT}; font-family: 'Segoe UI', Arial;">
            <h3 style="color: {VSCodeColors.SUCCESS};">✅ Think Tank Consensus</h3>
            
            <h4 style="color: {VSCodeColors.ACCENT};">💡 Solution</h4>
            <p>{result.get('solution', 'No solution provided')}</p>
            
            <h4 style="color: {VSCodeColors.ACCENT};">📊 Metrics</h4>
            <ul>
                <li><strong>Confidence:</strong> {result.get('confidence', 0):.2f}</li>
                <li><strong>Evidence Quality:</strong> {result.get('evidence_quality', 0):.2f}</li>
                <li><strong>Analysis Time:</strong> {result.get('consensus_time', 0):.1f}s</li>
            </ul>
            
            <h4 style="color: {VSCodeColors.SUCCESS};">👥 Supporting Experts</h4>
            <p>{supporting or 'None'}</p>
            
            {f'<h4 style="color: {VSCodeColors.WARNING};">⚠️ Dissenting Experts</h4><p>{dissenting}</p>' if dissenting else ''}
            
            <h4 style="color: {VSCodeColors.ACCENT};">📋 Implementation Plan</h4>
            <ol>
        """
        
        for step in result.get('implementation_plan', []):
            html_content += f"<li>{step}</li>"
        
        html_content += """
            </ol>
        </div>
        """
        
        self.results_display.setHtml(html_content)
        self.progress_label.setText("✅ Analysis complete!")
        self.statusBar().showMessage("Think tank analysis completed successfully")
    
    def show_message(self, message, msg_type="info"):
        """Show status message"""
        colors = {
            "info": VSCodeColors.ACCENT,
            "warning": VSCodeColors.WARNING,
            "error": VSCodeColors.ERROR,
            "success": VSCodeColors.SUCCESS
        }
        
        color = colors.get(msg_type, VSCodeColors.ACCENT)
        self.progress_label.setStyleSheet(f"""
            font-size: 13px;
            color: {color};
            padding: 8px;
            background-color: {VSCodeColors.SIDEBAR};
            border-radius: 4px;
        """)
        self.progress_label.setText(message)


def main():
    """Run the think tank GUI"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = ThinkTankGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
