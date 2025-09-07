# Empyrion Shield Calculator - Web Version

This is the web-based version of the Empyrion Shield Calculator, allowing players to optimize their shield configurations for Empyrion Galactic Survival directly in their web browsers.

## Live Demo

Access the calculator online at: [https://denizay22.github.io/empyrion-shield-calculator/](https://denizay22.github.io/empyrion-shield-calculator/)

## Features

- Calculate optimal shield booster configurations for all generator types
- Support for all hull types (Hull, Heavy Hull, Armored Hull, Combat Steel) with accurate shield contribution
- Include fusion reactor bonuses to shield recharge rates
- Track CPU usage and efficiency for shield systems
- Calculate exact recharge time for your shields
- Show booster usage by tier with limits (Basic: 8, Improved: 6, Advanced: 4)
- Detailed results showing base and total shield statistics
- Save your settings locally for future use

## How to Use

1. Open `index.html` in any modern web browser
2. Configure your ship specifications:
   - Select your shield generator type (Compact, Regular, Advanced, or Alien)
   - Enter your ship's total CPU and available CPU for shields
   - Specify the number of small and large fusion reactors
   - Enter the block counts for different hull types
   - Set minimum efficiency and recharge rate requirements
3. Click "Calculate" to generate the optimal shield configuration
4. View detailed results including:
   - Shield generator statistics
   - Block contribution to shields
   - Total shield capacity and recharge rate
   - CPU efficiency and usage
   - Booster usage by tier
   - Detailed breakdown of all boosters used

## Local Development

### Prerequisites

- Basic knowledge of HTML, CSS, and JavaScript
- A web browser
- Optional: A local web server (like Live Server extension for VS Code)

### Running Locally

1. Clone the repository:
```
git clone https://github.com/Denizay22/empyrion-shield-calculator.git
cd empyrion-shield-calculator/web
```

2. Open the `index.html` file in your web browser, or serve it using a local web server.

## Project Structure

- `index.html` - The main HTML file
- `css/styles.css` - Stylesheet
- `js/shield_data.js` - Shield generator and booster data
- `js/shield_calculator.js` - Core calculation logic
- `js/app.js` - UI interaction and display logic

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

Same as the main project.
