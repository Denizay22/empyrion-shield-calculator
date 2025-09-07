# Empyrion Shield Calculator

A calculator tool for optimizing shield configurations in Empyrion Galactic Survival.

## Features

- Command-line and graphical user interface options
- Calculates optimal shield configurations based on CPU constraints
- Supports different shield generator types
- Shows shield capacity, recharge rates, and time to fully recharge
- Calculates CPU efficiency
- Supports ship block contributions to shield capacity
- Enforces tier limits for shield boosters

## Screenshots

*[Add screenshots of your application here]*

## Installation

### Requirements

- Python 3.6+
- PyQt6 (for the GUI version)

### Setup

1. Clone this repository:
```
git clone https://github.com/Denizay22/empyrion-shield-calculator.git
cd empyrion-shield-calculator
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

## Usage

### GUI Version

Run the graphical user interface:
```
python shield_calculator_ui.py
```

### Command Line Version

Run the command line version:
```
python shieldcalc.py
```

## How It Works

The shield calculator uses an optimization algorithm to find the best combination of shield boosters that:
1. Stays within the available CPU limit
2. Meets the minimum CPU efficiency requirement
3. Achieves the minimum required recharge rate
4. Maximizes the total shield capacity
5. Respects the tier limits (8 basic, 6 improved, 4 advanced)

## Data Files

- **shieldinfo.json**: Contains information about shield boosters (capacitors and chargers)
- **shield_generators.json**: Contains information about different shield generator types

## License

*[Add your chosen license here]*

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
