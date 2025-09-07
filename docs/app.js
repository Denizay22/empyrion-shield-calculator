/**
 * Main application script for Empyrion Shield Calculator
 * Handles UI interactions and displays results
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize the shield calculator
    const calculator = new ShieldCalculator();
    
    // UI Elements
    const shieldTypeSelect = document.getElementById('shield-type');
    const totalCpuInput = document.getElementById('total-cpu');
    const availableCpuInput = document.getElementById('available-cpu');
    const smallFusionInput = document.getElementById('small-fusion');
    const largeFusionInput = document.getElementById('large-fusion');
    
    // Block Count Inputs
    const steelBlocksInput = document.getElementById('steel-blocks');
    const hardenedSteelInput = document.getElementById('hardened-steel');
    const combatSteelInput = document.getElementById('combat-steel');
    const xenoBlocksInput = document.getElementById('xeno-blocks');
    
    const cpuEfficiencyInput = document.getElementById('cpu-efficiency');
    const minRechargeInput = document.getElementById('min-recharge');
    const calculateBtn = document.getElementById('calculate-btn');
    const statusText = document.getElementById('status-text');
    
    // Result elements
    const generatorLabel = document.getElementById('shield-generator-label');
    const baseCapacityLabel = document.getElementById('base-capacity-label');
    const baseRechargeLabel = document.getElementById('base-recharge-label');
    const blockContributionLabel = document.getElementById('block-contribution-label');
    const totalCapacityLabel = document.getElementById('total-capacity-label');
    const totalRechargeLabel = document.getElementById('total-recharge-label');
    const rechargeTimeLabel = document.getElementById('recharge-time-label');
    const cpuUsageLabel = document.getElementById('cpu-usage-label');
    const cpuEfficiencyLabel = document.getElementById('cpu-efficiency-label');
    
    // Tier usage elements
    const basicTierLabel = document.getElementById('basic-tier-label');
    const improvedTierLabel = document.getElementById('improved-tier-label');
    const advancedTierLabel = document.getElementById('advanced-tier-label');
    
    const componentsGrid = document.getElementById('components-grid');
    
    // Initialize components grid with all possible components
    function initializeComponentsGrid() {
        componentsGrid.innerHTML = '';
        
        // Add shield boosters
        const boosterTypes = [
            'basic_capacitor', 'basic_charger', 
            'improved_capacitor', 'improved_charger',
            'advanced_capacitor', 'advanced_charger',
            'small_fusion', 'large_fusion'
        ];
        
        boosterTypes.forEach(type => {
            const div = document.createElement('div');
            div.className = 'component';
            div.id = `component-${type}`;
            div.textContent = `${getFriendlyName(type)}: 0`;
            componentsGrid.appendChild(div);
        });
    }
    
    // Get friendly name for booster types
    function getFriendlyName(boosterType) {
        const names = {
            'basic_capacitor': 'Basic Shield Capacitor',
            'basic_charger': 'Basic Shield Charger',
            'improved_capacitor': 'Improved Shield Capacitor',
            'improved_charger': 'Improved Shield Charger',
            'advanced_capacitor': 'Advanced Shield Capacitor',
            'advanced_charger': 'Advanced Shield Charger',
            'small_fusion': 'Small Fusion Reactor',
            'large_fusion': 'Large Fusion Reactor'
        };
        
        return names[boosterType] || boosterType;
    }
    
    // Update shield generator display based on selected generator
    function updateShieldGeneratorDisplay() {
        const shieldType = shieldTypeSelect.value;
        const generatorInfo = calculator.shieldData.shieldGenerators[shieldType];
        
        generatorLabel.textContent = generatorInfo.name;
        baseCapacityLabel.textContent = generatorInfo.capacity.toLocaleString();
        baseRechargeLabel.textContent = generatorInfo.recharge.toLocaleString();
    }
    
    // Calculate optimal shield configuration
    function calculateOptimalConfiguration() {
        // Display calculation in progress
        statusText.textContent = "Calculating optimal configuration... This may take a few seconds.";
        
        // Get input values
        const totalCpu = parseInt(totalCpuInput.value);
        const availableCpu = parseInt(availableCpuInput.value);
        const minCpuEfficiency = parseFloat(cpuEfficiencyInput.value); // Already in percentage format (0-100)
        const minRecharge = parseFloat(minRechargeInput.value);
        const smallFusion = parseInt(smallFusionInput.value);
        const largeFusion = parseInt(largeFusionInput.value);
        
        // Get block counts
        const steelBlocks = parseInt(steelBlocksInput.value);
        const hardenedSteel = parseInt(hardenedSteelInput.value);
        const combatSteel = parseInt(combatSteelInput.value);
        const xenoBlocks = parseInt(xenoBlocksInput.value);
        
        // Get shield generator type
        const shieldType = shieldTypeSelect.value;
        
        // Set up params for calculation
        const params = {
            generatorType: shieldType,
            totalCpu: totalCpu,
            availableCpu: availableCpu,
            smallFusionCount: smallFusion,
            largeFusionCount: largeFusion,
            blockCounts: {
                steel: steelBlocks,
                hardenedSteel: hardenedSteel,
                combatSteel: combatSteel,
                xeno: xenoBlocks
            },
            minEfficiency: minCpuEfficiency,
            minRechargeRate: minRecharge
        };
        
        // Small delay to allow UI update
        setTimeout(() => {
            // Perform calculation
            const result = calculator.calculateOptimalSetup(params);
            
            if (result.success) {
                displayResults(result);
                statusText.textContent = "Calculation complete!";
            } else {
                statusText.textContent = "No valid configuration found! Try adjusting your requirements.";
                clearResults();
            }
        }, 100);
    }
    
    // Display the calculation results
    function displayResults(result) {
        // Update shield statistics
        const blockContribution = result.blockContribution || 0;
        blockContributionLabel.textContent = blockContribution.toLocaleString();
        totalCapacityLabel.textContent = result.totalCapacity.toLocaleString();
        totalRechargeLabel.textContent = result.rechargeRate.toFixed(1);
        
        // Set recharge time from result
        rechargeTimeLabel.textContent = result.rechargeTime || "--";
        
        // Update CPU usage and efficiency
        if (result.cpuLimit > parseInt(availableCpuInput.value)) {
            // Display adjusted CPU usage when excess CPU from efficiency is used
            cpuUsageLabel.textContent = `${Math.floor(result.cpuUsed).toLocaleString()} / ${Math.floor(result.cpuLimit).toLocaleString()} (adjusted for ${cpuEfficiencyInput.value}% efficiency)`;
        } else {
            cpuUsageLabel.textContent = `${Math.floor(result.cpuUsed).toLocaleString()} / ${Math.floor(result.cpuLimit).toLocaleString()}`;
        }
        cpuEfficiencyLabel.textContent = `${(result.cpuEfficiency * 100).toFixed(2)}%`;
        
        // Update tier usage
        const tierCounts = result.tierCounts || {
            basic: 0,
            improved: 0,
            advanced: 0
        };
        
        basicTierLabel.textContent = `${tierCounts.basic}/8`;
        improvedTierLabel.textContent = `${tierCounts.improved}/6`;
        advancedTierLabel.textContent = `${tierCounts.advanced}/4`;
        
        // Update component labels
        // First reset all components
        const components = document.querySelectorAll('.component');
        components.forEach(comp => {
            const id = comp.id.replace('component-', '');
            comp.textContent = `${getFriendlyName(id)}: 0`;
            comp.classList.remove('active');
        });
        
        // Update used components
        for (const [booster, count] of Object.entries(result.boosterCounts)) {
            if (count > 0) {
                const component = document.getElementById(`component-${booster}`);
                if (component) {
                    component.textContent = `${getFriendlyName(booster)}: ${count}`;
                    component.classList.add('active');
                }
            }
        }
        
        // Update fusion reactors (if they were used in the calculation)
        if (result.smallFusionCount > 0) {
            const component = document.getElementById('component-small_fusion');
            component.textContent = `${getFriendlyName('small_fusion')}: ${result.smallFusionCount}`;
            component.classList.add('active');
        }
        
        if (result.largeFusionCount > 0) {
            const component = document.getElementById('component-large_fusion');
            component.textContent = `${getFriendlyName('large_fusion')}: ${result.largeFusionCount}`;
            component.classList.add('active');
        }
    }
    
    // Clear all result fields
    function clearResults() {
        blockContributionLabel.textContent = "0";
        totalCapacityLabel.textContent = "--";
        totalRechargeLabel.textContent = "--";
        rechargeTimeLabel.textContent = "--";
        cpuUsageLabel.textContent = "--";
        cpuEfficiencyLabel.textContent = "--";
        basicTierLabel.textContent = "0/8";
        improvedTierLabel.textContent = "0/6";
        advancedTierLabel.textContent = "0/4";
        
        // Reset component labels
        const components = document.querySelectorAll('.component');
        components.forEach(comp => {
            const id = comp.id.replace('component-', '');
            comp.textContent = `${getFriendlyName(id)}: 0`;
            comp.classList.remove('active');
        });
    }
    
    // Initialize the application
    function init() {
        // Initialize components grid
        initializeComponentsGrid();
        
        // Update shield generator display when type changes
        shieldTypeSelect.addEventListener('change', updateShieldGeneratorDisplay);
        
        // Set up initial shield generator display
        updateShieldGeneratorDisplay();
        
        // Calculate button click handler
        calculateBtn.addEventListener('click', calculateOptimalConfiguration);
    }
    
    // Start the application
    init();
});
