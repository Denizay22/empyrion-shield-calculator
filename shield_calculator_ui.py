import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QDoubleSpinBox, QPushButton, QGroupBox,
    QGridLayout, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor, QFont

# Import calculation function from original script
from shieldcalc import load_shield_info, calculate_optimal_configuration

class DarkPalette(QPalette):
    """Dark palette for the application"""
    def __init__(self):
        super().__init__()
        self.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        self.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        self.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        self.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))
        self.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        self.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        self.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        self.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)


class ShieldCalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shield_info = load_shield_info()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Empyrion Shield Calculator")
        self.setGeometry(100, 100, 1000, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Input Group
        input_group = QGroupBox("Input Parameters")
        input_layout = QGridLayout()
        
        # CPU inputs
        input_layout.addWidget(QLabel("Total CPU Points:"), 0, 0)
        self.total_cpu_input = QSpinBox()
        self.total_cpu_input.setRange(1, 10000000)
        self.total_cpu_input.setValue(400000)
        self.total_cpu_input.setSingleStep(10000)
        input_layout.addWidget(self.total_cpu_input, 0, 1)
        
        input_layout.addWidget(QLabel("Available CPU for Shields:"), 0, 2)
        self.available_cpu_input = QSpinBox()
        self.available_cpu_input.setRange(1, 10000000)
        self.available_cpu_input.setValue(200000)
        self.available_cpu_input.setSingleStep(10000)
        input_layout.addWidget(self.available_cpu_input, 0, 3)
        
        # Shield generator selection
        input_layout.addWidget(QLabel("Shield Generator Type:"), 1, 0)
        self.shield_type_combo = QComboBox()
        # Populate shield generator types from shield_info.json
        shield_types = ["compact", "regular", "advanced", "alien"]
        shield_items = []
        for stype in shield_types:
            info = self.shield_info['shieldGenerators'][stype]
            name_map = {
            'compact': 'Compact Shield Generator',
            'regular': 'Regular Shield Generator',
            'advanced': 'Advanced Shield Generator',
            'alien': 'Alien Shield Generator'
            }
            display_name = name_map.get(stype, stype)
            shield_items.append(f"{display_name} ({info['capacity']:,} cap, {info['recharge']:,} rech)")
        self.shield_type_combo.addItems(shield_items)
        self.shield_type_combo.setCurrentIndex(2)  # Set Advanced as default
        self.shield_type_combo.currentIndexChanged.connect(self.update_shield_generator_display)
        input_layout.addWidget(self.shield_type_combo, 1, 1)
        
        input_layout.addWidget(QLabel("Min CPU Efficiency (0-1):"), 1, 2)
        self.cpu_efficiency_input = QDoubleSpinBox()
        self.cpu_efficiency_input.setRange(0.0, 1.0)
        self.cpu_efficiency_input.setValue(0.8)
        self.cpu_efficiency_input.setSingleStep(0.05)
        input_layout.addWidget(self.cpu_efficiency_input, 1, 3)
        
        input_layout.addWidget(QLabel("Min Recharge Rate:"), 2, 2)
        self.min_recharge_input = QDoubleSpinBox()
        self.min_recharge_input.setRange(0, 10000)
        self.min_recharge_input.setValue(1500)
        self.min_recharge_input.setSingleStep(100)
        input_layout.addWidget(self.min_recharge_input, 2, 3)
        
        input_layout.addWidget(QLabel("Small Fusion Reactors:"), 2, 0)
        self.small_fusion_input = QSpinBox()
        self.small_fusion_input.setRange(0, 20)
        self.small_fusion_input.setValue(0)
        input_layout.addWidget(self.small_fusion_input, 2, 1)
        
        input_layout.addWidget(QLabel("Large Fusion Reactors:"), 3, 0)
        self.large_fusion_input = QSpinBox()
        self.large_fusion_input.setRange(0, 20)
        self.large_fusion_input.setValue(0)
        input_layout.addWidget(self.large_fusion_input, 3, 1)
        
        # Block counts for shield capacity
        blocks_group = QGroupBox("Ship Blocks (Shield Capacity)")
        blocks_layout = QGridLayout()
        
        blocks_layout.addWidget(QLabel("Steel Blocks:"), 0, 0)
        self.steel_blocks_input = QSpinBox()
        self.steel_blocks_input.setRange(0, 100000)
        self.steel_blocks_input.setValue(0)
        self.steel_blocks_input.setSingleStep(100)
        blocks_layout.addWidget(self.steel_blocks_input, 0, 1)
        
        blocks_layout.addWidget(QLabel("Hardened Steel:"), 0, 2)
        self.hardened_steel_input = QSpinBox()
        self.hardened_steel_input.setRange(0, 100000)
        self.hardened_steel_input.setValue(0)
        self.hardened_steel_input.setSingleStep(100)
        blocks_layout.addWidget(self.hardened_steel_input, 0, 3)
        
        blocks_layout.addWidget(QLabel("Combat Steel:"), 1, 0)
        self.combat_steel_input = QSpinBox()
        self.combat_steel_input.setRange(0, 100000)
        self.combat_steel_input.setValue(0)
        self.combat_steel_input.setSingleStep(100)
        blocks_layout.addWidget(self.combat_steel_input, 1, 1)
        
        blocks_layout.addWidget(QLabel("Xeno Blocks:"), 1, 2)
        self.xeno_blocks_input = QSpinBox()
        self.xeno_blocks_input.setRange(0, 100000)
        self.xeno_blocks_input.setValue(0)
        self.xeno_blocks_input.setSingleStep(100)
        blocks_layout.addWidget(self.xeno_blocks_input, 1, 3)
        
        blocks_group.setLayout(blocks_layout)
        input_layout.addWidget(blocks_group, 4, 0, 1, 4)
        
        # Calculate button
        self.calculate_btn = QPushButton("Calculate Optimal Configuration")
        self.calculate_btn.clicked.connect(self.calculate)
        input_layout.addWidget(self.calculate_btn, 5, 0, 1, 4)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Add spacing between input and results sections
        main_layout.addSpacing(10)
        
        # Results Group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        # Shield stats
        shield_stats_group = QGroupBox("Shield Statistics")
        shield_stats_layout = QGridLayout()
        
        shield_label = QLabel("Shield Generator:")
        shield_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(shield_label, 0, 0)
        self.shield_generator_label = QLabel("Advanced Shield Generator")
        self.shield_generator_label.setMinimumWidth(180)
        self.shield_generator_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.shield_generator_label, 0, 1)
        
        capacity_label = QLabel("Base Shield Capacity:")
        capacity_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(capacity_label, 0, 2)
        self.base_capacity_label = QLabel("24,000")
        self.base_capacity_label.setMinimumWidth(120)
        self.base_capacity_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.base_capacity_label, 0, 3)
        
        block_label = QLabel("Block Shield Contribution:")
        block_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(block_label, 1, 0)
        self.block_contribution_label = QLabel("0")
        self.block_contribution_label.setMinimumWidth(120)
        self.block_contribution_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.block_contribution_label, 1, 1)
        
        recharge_label = QLabel("Base Shield Recharge:")
        recharge_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(recharge_label, 1, 2)
        self.base_recharge_label = QLabel("600")
        self.base_recharge_label.setMinimumWidth(120)
        self.base_recharge_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.base_recharge_label, 1, 3)
        
        total_cap_label = QLabel("Total Shield Capacity:")
        total_cap_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(total_cap_label, 2, 0)
        self.total_capacity_label = QLabel("--")
        self.total_capacity_label.setMinimumWidth(120)
        self.total_capacity_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.total_capacity_label, 2, 1)
        
        total_recharge_label = QLabel("Total Recharge Rate:")
        total_recharge_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(total_recharge_label, 2, 2)
        self.total_recharge_label = QLabel("--")
        self.total_recharge_label.setMinimumWidth(120)
        self.total_recharge_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.total_recharge_label, 2, 3)
        
        time_label = QLabel("Time to Fully Recharge:")
        time_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(time_label, 3, 0)
        self.recharge_time_label = QLabel("--")
        self.recharge_time_label.setMinimumWidth(120)
        self.recharge_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.recharge_time_label, 3, 1)
        
        cpu_usage_label = QLabel("CPU Usage:")
        cpu_usage_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(cpu_usage_label, 3, 2)
        self.cpu_usage_label = QLabel("--")
        self.cpu_usage_label.setMinimumWidth(120)
        self.cpu_usage_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.cpu_usage_label, 3, 3)
        
        cpu_eff_label = QLabel("CPU Efficiency:")
        cpu_eff_label.setMinimumWidth(150)
        shield_stats_layout.addWidget(cpu_eff_label, 4, 0)
        self.cpu_efficiency_label = QLabel("--")
        self.cpu_efficiency_label.setMinimumWidth(120)
        self.cpu_efficiency_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        shield_stats_layout.addWidget(self.cpu_efficiency_label, 4, 1)
        
        shield_stats_group.setLayout(shield_stats_layout)
        results_layout.addWidget(shield_stats_group)
        
        # Add spacing between sections
        results_layout.addSpacing(5)
        
        # Tier usage
        tier_usage_group = QGroupBox("Booster Usage by Tier")
        tier_usage_layout = QGridLayout()
        
        # Use a consistent width for tier labels
        basic_tier_lbl = QLabel("Basic Tier:")
        basic_tier_lbl.setMinimumWidth(100)
        tier_usage_layout.addWidget(basic_tier_lbl, 0, 0)
        self.basic_tier_label = QLabel("0/8")
        self.basic_tier_label.setMinimumWidth(50)
        self.basic_tier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tier_usage_layout.addWidget(self.basic_tier_label, 0, 1)
        
        improved_tier_lbl = QLabel("Improved Tier:")
        improved_tier_lbl.setMinimumWidth(100)
        tier_usage_layout.addWidget(improved_tier_lbl, 0, 2)
        self.improved_tier_label = QLabel("0/6")
        self.improved_tier_label.setMinimumWidth(50)
        self.improved_tier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tier_usage_layout.addWidget(self.improved_tier_label, 0, 3)
        
        advanced_tier_lbl = QLabel("Advanced Tier:")
        advanced_tier_lbl.setMinimumWidth(100)
        tier_usage_layout.addWidget(advanced_tier_lbl, 0, 4)
        self.advanced_tier_label = QLabel("0/4")
        self.advanced_tier_label.setMinimumWidth(50)
        self.advanced_tier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tier_usage_layout.addWidget(self.advanced_tier_label, 0, 5)
        
        tier_usage_group.setLayout(tier_usage_layout)
        results_layout.addWidget(tier_usage_group)
        
        # Add spacing between sections
        results_layout.addSpacing(5)
        
        # Components grid layout instead of table
        components_group = QGroupBox("Components")
        components_layout = QGridLayout()
        
        # Create labels for each possible component
        self.component_labels = {
            'basic_capacitor': QLabel("Basic Capacitor: 0"),
            'basic_charger': QLabel("Basic Charger: 0"),
            'improved_capacitor': QLabel("Improved Capacitor: 0"),
            'improved_charger': QLabel("Improved Charger: 0"),
            'advanced_capacitor': QLabel("Advanced Capacitor: 0"),
            'advanced_charger': QLabel("Advanced Charger: 0"),
            'small_fusion': QLabel("Small Fusion Reactor: 0"),
            'large_fusion': QLabel("Large Fusion Reactor: 0")
        }
        
        # Add labels to grid layout - 4 columns for better spacing
        row, col = 0, 0
        for component_name, label in self.component_labels.items():
            components_layout.addWidget(label, row, col)
            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1
                
        # Set font for component labels
        font = QFont()
        font.setPointSize(10)
        for label in self.component_labels.values():
            label.setFont(font)
            label.setMinimumWidth(180)  # Ensure labels have enough width
        
        components_group.setLayout(components_layout)
        results_layout.addWidget(components_group)
        
        # Status area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        results_layout.addWidget(self.status_text)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        self.setCentralWidget(main_widget)
        
        # Update shield generator display with default values
        self.update_shield_generator_display()
        
    def calculate(self):
        """Calculate and display the optimal configuration"""
        # Show a loading message
        self.status_text.setPlainText("Calculating optimal configuration... This may take a few seconds.")
        QApplication.processEvents()
        
        # Get input values
        total_cpu = self.total_cpu_input.value()
        available_cpu = self.available_cpu_input.value()
        min_cpu_efficiency = self.cpu_efficiency_input.value()
        min_recharge = self.min_recharge_input.value()
        small_fusion = self.small_fusion_input.value()
        large_fusion = self.large_fusion_input.value()
        
        # Get block counts
        steel_blocks = self.steel_blocks_input.value()
        hardened_steel = self.hardened_steel_input.value()
        combat_steel = self.combat_steel_input.value()
        xeno_blocks = self.xeno_blocks_input.value()
        
        # Calculate block shield contribution
        block_shield_capacity = (
            steel_blocks * 1 +         # Steel blocks add 1 shield
            hardened_steel * 2 +       # Hardened steel blocks add 2 shield
            combat_steel * 4 +         # Combat steel blocks add 4 shield
            xeno_blocks * 7            # Xeno blocks add 7 shield
        )
        
        # Calculate optimal configuration in a small delay to allow UI update
        QTimer.singleShot(100, lambda: self._perform_calculation(
            total_cpu, available_cpu, min_cpu_efficiency, min_recharge, 
            small_fusion, large_fusion, block_shield_capacity
        ))
        
    def _perform_calculation(self, total_cpu, available_cpu, min_cpu_efficiency, min_recharge, 
                         small_fusion, large_fusion, block_shield_capacity=0):
        """Perform the actual calculation and update UI"""
        # Get the selected shield generator type
        shield_type_index = self.shield_type_combo.currentIndex()
        shield_types = ["compact", "regular", "advanced", "alien"]
        selected_shield_type = shield_types[shield_type_index]
        
        # Calculate optimal configuration
        result = calculate_optimal_configuration(
            self.shield_info, total_cpu, available_cpu, min_cpu_efficiency,
            min_recharge, small_fusion, large_fusion, block_shield_capacity,
            shield_type=selected_shield_type
        )
        
        # Display results
        if result:
            self.display_results(result, total_cpu, available_cpu)
            self.status_text.setPlainText("Calculation complete!")
        else:
            self.status_text.setPlainText("No valid configuration found! Try adjusting your requirements.")
            self.clear_results()
    
    def display_results(self, result, total_cpu, available_cpu=None):
        """Display the results in the UI"""
        # If available_cpu is not provided, use the input value
        if available_cpu is None:
            available_cpu = self.available_cpu_input.value()
        
        # Get shield type info
        shield_type = result.get('shield_type', 'advanced')
        shield_type_names = {
            'compact': 'Compact Shield Generator',
            'regular': 'Regular Shield Generator',
            'advanced': 'Advanced Shield Generator',
            'alien': 'Alien Shield Generator'
        }
        shield_type_name = shield_type_names.get(shield_type, shield_type)
        
        # Get base shield values
        base_capacity = self.shield_info['shieldGenerators'][shield_type]['capacity']
        base_recharge = self.shield_info['shieldGenerators'][shield_type]['recharge']
        
        # Update shield generator info
        self.shield_generator_label.setText(shield_type_name)
        self.base_capacity_label.setText(f"{base_capacity:,}")
        self.base_recharge_label.setText(f"{base_recharge:,}")
            
        # Shield statistics
        block_contribution = result.get('block_shield_capacity', 0)
        self.block_contribution_label.setText(f"{block_contribution:,}")
        self.total_capacity_label.setText(f"{result['total_capacity']:,}")
        self.total_recharge_label.setText(f"{result['total_recharge']:.1f}")
        
        # Calculate time to fully recharge
        time_to_recharge = result['total_capacity'] / result['total_recharge'] if result['total_recharge'] > 0 else float('inf')
        minutes = int(time_to_recharge // 60)
        seconds = int(time_to_recharge % 60)
        self.recharge_time_label.setText(f"{minutes} minutes {seconds} seconds")
        
        # CPU usage and efficiency
        self.cpu_usage_label.setText(f"{result['total_cpu']:,} of {available_cpu:,}")
        self.cpu_efficiency_label.setText(f"{result['cpu_efficiency']:.2%}")
        
        # Count boosters by tier
        basic_count = sum(result['configuration'].get(b, 0) for b in ['basic_capacitor', 'basic_charger'])
        improved_count = sum(result['configuration'].get(b, 0) for b in ['improved_capacitor', 'improved_charger'])
        advanced_count = sum(result['configuration'].get(b, 0) for b in ['advanced_capacitor', 'advanced_charger'])
        
        self.basic_tier_label.setText(f"{basic_count}/8")
        self.improved_tier_label.setText(f"{improved_count}/6")
        self.advanced_tier_label.setText(f"{advanced_count}/4")
        
        # Update component labels
        # First reset all labels
        for key, label in self.component_labels.items():
            label.setText(f"{self._get_friendly_name(key)}: 0")
        
        # Update booster component counts from configuration
        for booster, count in result['configuration'].items():
            if count > 0 and booster in self.component_labels:
                self.component_labels[booster].setText(f"{self._get_friendly_name(booster)}: {count}")
                # Highlight components that are used
                self.component_labels[booster].setStyleSheet("font-weight: bold; color: #42A5F5;")
            else:
                # Reset style for unused components
                if booster in self.component_labels:
                    self.component_labels[booster].setStyleSheet("")
        
        # Update fusion reactor counts
        if result['small_fusion_count'] > 0:
            self.component_labels['small_fusion'].setText(f"Small Fusion Reactor: {result['small_fusion_count']}")
            self.component_labels['small_fusion'].setStyleSheet("font-weight: bold; color: #42A5F5;")
        else:
            self.component_labels['small_fusion'].setStyleSheet("")
            
        if result['large_fusion_count'] > 0:
            self.component_labels['large_fusion'].setText(f"Large Fusion Reactor: {result['large_fusion_count']}")
            self.component_labels['large_fusion'].setStyleSheet("font-weight: bold; color: #42A5F5;")
        else:
            self.component_labels['large_fusion'].setStyleSheet("")
    
    def clear_results(self):
        """Clear all result fields"""
        self.block_contribution_label.setText("0")
        self.total_capacity_label.setText("--")
        self.total_recharge_label.setText("--")
        self.recharge_time_label.setText("--")
        self.cpu_usage_label.setText("--")
        self.cpu_efficiency_label.setText("--")
        self.basic_tier_label.setText("0/8")
        self.improved_tier_label.setText("0/6")
        self.advanced_tier_label.setText("0/4")
        
        # Reset component labels
        for key, label in self.component_labels.items():
            label.setText(f"{self._get_friendly_name(key)}: 0")
            label.setStyleSheet("")
            
    def update_shield_generator_display(self):
        """Update the shield generator display based on the selected generator type"""
        shield_type_index = self.shield_type_combo.currentIndex()
        shield_types = ["compact", "regular", "advanced", "alien"]
        selected_shield_type = shield_types[shield_type_index]
        
        # Get shield generator info
        generator_info = self.shield_info['shieldGenerators'][selected_shield_type]
        
        # Update UI display
        shield_type_names = {
            'compact': 'Compact Shield Generator',
            'regular': 'Regular Shield Generator',
            'advanced': 'Advanced Shield Generator',
            'alien': 'Alien Shield Generator'
        }
        shield_type_name = shield_type_names.get(selected_shield_type, selected_shield_type)
        
        self.shield_generator_label.setText(shield_type_name)
        self.base_capacity_label.setText(f"{generator_info['capacity']:,}")
        self.base_recharge_label.setText(f"{generator_info['recharge']:,}")
    
    def _get_friendly_name(self, component_key):
        """Convert component keys to friendly display names"""
        name_map = {
            'basic_capacitor': 'Basic Capacitor',
            'basic_charger': 'Basic Charger',
            'improved_capacitor': 'Improved Capacitor',
            'improved_charger': 'Improved Charger',
            'advanced_capacitor': 'Advanced Capacitor',
            'advanced_charger': 'Advanced Charger',
            'small_fusion': 'Small Fusion Reactor',
            'large_fusion': 'Large Fusion Reactor'
        }
        return name_map.get(component_key, component_key)


def main():
    """Main function to start the UI application"""
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyle("Fusion")
    app.setPalette(DarkPalette())
    
    window = ShieldCalculatorUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
