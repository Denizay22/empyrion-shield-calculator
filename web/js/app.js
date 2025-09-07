/**
 * Main application script for Empyrion Shield Calculator
 * Handles UI interactions and displays results
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize the shield calculator
    const calculator = new ShieldCalculator();
    
    // UI Elements
    const generatorTypeSelect = document.getElementById('generator-type');
    const totalCpuInput = document.getElementById('total-cpu');
    const availableCpuInput = document.getElementById('cpu-limit');
    const smallFusionInput = document.getElementById('small-fusion');
    const largeFusionInput = document.getElementById('large-fusion');
    
    // Block Count Inputs
    const hullBlocksInput = document.getElementById('steel-blocks');
    const heavyHullBlocksInput = document.getElementById('hardened-steel');
    const armoredHullBlocksInput = document.getElementById('combat-steel');
    const combatSteelBlocksInput = document.getElementById('xeno-blocks');
    
    const minEfficiencyInput = document.getElementById('min-efficiency');
    const minRechargeRateInput = document.getElementById('min-recharge-rate');
    const calculateBtn = document.getElementById('calculate-btn');
    
    // Result elements
    const shieldGeneratorTypeEl = document.getElementById('shield-generator-type');
    const baseCapacityEl = document.getElementById('base-capacity');
    const baseRechargeEl = document.getElementById('base-recharge');
    const blockContributionEl = document.getElementById('block-contribution');
    const totalCapacityEl = document.getElementById('total-capacity');
    const rechargeRateEl = document.getElementById('recharge-rate');
    const rechargeTimeEl = document.getElementById('recharge-time');
    const cpuEfficiencyEl = document.getElementById('cpu-efficiency');
    const cpuUsedEl = document.getElementById('cpu-used');
    
    // Tier usage elements
    const basicTierUsageEl = document.getElementById('basic-tier-usage');
    const improvedTierUsageEl = document.getElementById('improved-tier-usage');
    const advancedTierUsageEl = document.getElementById('advanced-tier-usage');
    
    const boostersTableBody = document.querySelector('#boosters-table tbody');
    
    // Populate generator types dropdown
    function populateGeneratorTypes() {
        const generatorTypes = calculator.getGeneratorTypes();
        generatorTypeSelect.innerHTML = '';
        
        generatorTypes.forEach(generator => {
            const option = document.createElement('option');
            option.value = generator.id;
            option.textContent = generator.name;
            generatorTypeSelect.appendChild(option);
        });
    }
    
    // Load saved settings from localStorage
    function loadSavedSettings() {
        const savedSettings = JSON.parse(localStorage.getItem('empyrionShieldCalc')) || {};
        
        if (savedSettings.generatorType) {
            generatorTypeSelect.value = savedSettings.generatorType;
        }
        
        if (savedSettings.totalCpu) {
            totalCpuInput.value = savedSettings.totalCpu;
        }
        
        if (savedSettings.availableCpu) {
            availableCpuInput.value = savedSettings.availableCpu;
        }
        
        if (savedSettings.smallFusionCount) {
            smallFusionInput.value = savedSettings.smallFusionCount;
        }
        
        if (savedSettings.largeFusionCount) {
            largeFusionInput.value = savedSettings.largeFusionCount;
        }
        
        // Load block counts
        if (savedSettings.blockCounts) {
            if (savedSettings.blockCounts.hull) {
                hullBlocksInput.value = savedSettings.blockCounts.hull;
            }
            if (savedSettings.blockCounts.heavyHull) {
                heavyHullBlocksInput.value = savedSettings.blockCounts.heavyHull;
            }
            if (savedSettings.blockCounts.armoredHull) {
                armoredHullBlocksInput.value = savedSettings.blockCounts.armoredHull;
            }
            if (savedSettings.blockCounts.combatSteel) {
                combatSteelBlocksInput.value = savedSettings.blockCounts.combatSteel;
            }
        }
        
        if (savedSettings.minEfficiency) {
            minEfficiencyInput.value = savedSettings.minEfficiency;
        }
        
        if (savedSettings.minRechargeRate) {
            minRechargeRateInput.value = savedSettings.minRechargeRate;
        }
    }
    
    // Save current settings to localStorage
    function saveSettings() {
        const settings = {
            generatorType: generatorTypeSelect.value,
            totalCpu: totalCpuInput.value,
            availableCpu: availableCpuInput.value,
            smallFusionCount: smallFusionInput.value,
            largeFusionCount: largeFusionInput.value,
            blockCounts: {
                hull: hullBlocksInput.value,
                heavyHull: heavyHullBlocksInput.value,
                armoredHull: armoredHullBlocksInput.value,
                combatSteel: combatSteelBlocksInput.value
            },
            minEfficiency: minEfficiencyInput.value,
            minRechargeRate: minRechargeRateInput.value
        };
        
        localStorage.setItem('empyrionShieldCalc', JSON.stringify(settings));
    }
    
    // Display calculation results
    function displayResults(result) {
        // Update result fields
        if (result.success) {
            shieldGeneratorTypeEl.textContent = result.generatorName;
            baseCapacityEl.textContent = formatNumber(result.baseCapacity);
            baseRechargeEl.textContent = formatNumber(result.baseRecharge) + "/sec";
            blockContributionEl.textContent = formatNumber(result.blockContribution);
            totalCapacityEl.textContent = formatNumber(result.totalCapacity);
            rechargeRateEl.textContent = formatNumber(result.rechargeRate) + "/sec";
            rechargeTimeEl.textContent = result.rechargeTime;
            cpuEfficiencyEl.textContent = formatNumber(result.cpuEfficiency * 100, 2) + '%';
            
            // Display the CPU usage with the adjusted limit (if applicable)
            if (result.cpuLimit > Number(availableCpuInput.value)) {
                cpuUsedEl.textContent = formatNumber(result.cpuUsed) + ' / ' + formatNumber(result.cpuLimit) + 
                    ' (adjusted for ' + minEfficiencyInput.value + '% efficiency)';
            } else {
                cpuUsedEl.textContent = formatNumber(result.cpuUsed) + ' / ' + formatNumber(result.cpuLimit);
            }
            
            // Update tier usage displays
            basicTierUsageEl.textContent = `${result.tierCounts.basic}/8`;
            improvedTierUsageEl.textContent = `${result.tierCounts.improved}/6`;
            advancedTierUsageEl.textContent = `${result.tierCounts.advanced}/4`;
        } else {
            // Show error message
            shieldGeneratorTypeEl.textContent = '-';
            baseCapacityEl.textContent = '-';
            baseRechargeEl.textContent = '-';
            blockContributionEl.textContent = '-';
            totalCapacityEl.textContent = formatNumber(result.totalCapacity);
            rechargeRateEl.textContent = formatNumber(result.rechargeRate) + "/sec";
            rechargeTimeEl.textContent = '-';
            cpuEfficiencyEl.textContent = formatNumber(result.cpuEfficiency * 100, 2) + '%';
            
            // Display the CPU usage with the adjusted limit (if applicable)
            if (result.cpuLimit > Number(availableCpuInput.value)) {
                cpuUsedEl.textContent = formatNumber(result.cpuUsed) + ' / ' + formatNumber(result.cpuLimit) + 
                    ' (adjusted for ' + minEfficiencyInput.value + '% efficiency)';
            } else {
                cpuUsedEl.textContent = formatNumber(result.cpuUsed) + ' / ' + formatNumber(result.cpuLimit);
            }
            
            basicTierUsageEl.textContent = '0/8';
            improvedTierUsageEl.textContent = '0/6';
            advancedTierUsageEl.textContent = '0/4';
            
            alert(`Calculation issue: ${result.message}`);
        }
        
        // Update boosters table
        boostersTableBody.innerHTML = '';
        
        for (const [boosterId, count] of Object.entries(result.boosterCounts)) {
            if (count > 0) {
                const booster = calculator.getBoosterDetails(boosterId);
                const row = document.createElement('tr');
                
                // Create booster name cell
                const nameCell = document.createElement('td');
                nameCell.textContent = booster.name;
                row.appendChild(nameCell);
                
                // Create count cell
                const countCell = document.createElement('td');
                countCell.textContent = count;
                row.appendChild(countCell);
                
                // Create contribution cell
                const contribCell = document.createElement('td');
                if (booster.capacity !== 0) {
                    const capEffect = booster.capacity > 0 ? "+" : "-";
                    contribCell.textContent = `${capEffect}${formatNumber(Math.abs(booster.capacity * count))} shield capacity`;
                }
                if (booster.recharge !== 0) {
                    if (contribCell.textContent) contribCell.textContent += ', ';
                    const rechEffect = booster.recharge > 0 ? "+" : "-";
                    contribCell.textContent += `${rechEffect}${formatNumber(Math.abs(booster.recharge * count))}/min recharge`;
                }
                row.appendChild(contribCell);
                
                boostersTableBody.appendChild(row);
            }
        }
    }
    
    // Format number with commas and specified decimal places
    function formatNumber(num, decimals = 0) {
        return num.toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }
    
    // Calculate optimal setup
    function calculateOptimalSetup() {
        // Get input values
        const params = {
            generatorType: generatorTypeSelect.value,
            totalCpu: Number(totalCpuInput.value),
            availableCpu: Number(availableCpuInput.value),
            smallFusionCount: Number(smallFusionInput.value),
            largeFusionCount: Number(largeFusionInput.value),
            blockCounts: {
                steel: Number(hullBlocksInput.value),
                hardenedSteel: Number(heavyHullBlocksInput.value),
                combatSteel: Number(armoredHullBlocksInput.value),
                xeno: Number(combatSteelBlocksInput.value)
            },
            minEfficiency: Number(minEfficiencyInput.value),
            minRechargeRate: Number(minRechargeRateInput.value)
        };
        
        // Save settings
        saveSettings();
        
        // Calculate and display results
        const result = calculator.calculateOptimalSetup(params);
        displayResults(result);
    }
    
    // Update available CPU when total CPU changes
    function updateAvailableCpu() {
        const totalCpu = Number(totalCpuInput.value);
        // Let's assume 50% of total CPU is available for shields by default
        const suggestedAvailable = Math.floor(totalCpu * 0.5);
        
        // Only update if the available CPU input hasn't been manually changed
        if (!availableCpuInput.dataset.manuallySet) {
            availableCpuInput.value = suggestedAvailable;
        }
    }

    // Update shield generator base stats in real time
    function updateGeneratorStats() {
        const generatorType = generatorTypeSelect.value;
        const generator = calculator.shieldData.shieldGenerators[generatorType];
        
        // Update the UI with base stats
        shieldGeneratorTypeEl.textContent = generator.name;
        baseCapacityEl.textContent = formatNumber(generator.capacity);
        baseRechargeEl.textContent = formatNumber(generator.recharge) + "/sec";
    }

    // Initialize the app
    function init() {
        populateGeneratorTypes();
        loadSavedSettings();
        
        // Add event listeners
        calculateBtn.addEventListener('click', calculateOptimalSetup);
        totalCpuInput.addEventListener('input', updateAvailableCpu);
        generatorTypeSelect.addEventListener('change', updateGeneratorStats);
        
        // Mark when available CPU is manually changed
        availableCpuInput.addEventListener('input', () => {
            availableCpuInput.dataset.manuallySet = 'true';
        });
        
        // Update generator stats initially
        updateGeneratorStats();
        
        // Calculate initial results
        calculateOptimalSetup();
    }
    
    // Start the app
    init();
});
