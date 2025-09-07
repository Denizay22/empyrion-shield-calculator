/**
 * Shield Calculator Logic
 * Core functionality for the Empyrion Shield Calculator
 */

class ShieldCalculator {
    constructor() {
        this.shieldData = SHIELD_DATA;
        this.result = null;
    }

    /**
     * Calculate the optimal shield booster configuration
     * @param {Object} params - Calculation parameters
     * @param {string} params.generatorType - The type of shield generator
     * @param {number} params.totalCpu - Total CPU available on the vessel
     * @param {number} params.availableCpu - Available CPU for shield boosters
     * @param {number} params.smallFusionCount - Number of small fusion reactors
     * @param {number} params.largeFusionCount - Number of large fusion reactors
     * @param {Object} params.blockCounts - Counts of different block types
     * @param {number} params.minEfficiency - Minimum CPU efficiency (%)
     *                 Lower values allow algorithm to use more CPU while maintaining efficiency target
     * @param {number} params.minRechargeRate - Minimum shield recharge rate
     * @returns {Object} - Calculation results
     */
    calculateOptimalSetup(params) {
        const { 
            generatorType,
            totalCpu = 0,
            availableCpu = 0,
            smallFusionCount = 0,
            largeFusionCount = 0,
            blockCounts = {},
            minEfficiency = 0,
            minRechargeRate = 0
        } = params;
        
        // Calculate additional available CPU based on minimum efficiency
        // Formula: available cpu + ((total cpu * min cpu efficiency) - total cpu)
        // This allows for more CPU to be used if user inputs lower efficiency target
        let adjustedAvailableCpu = availableCpu;
        
        if (totalCpu > 0 && minEfficiency > 0) {
            // Convert minEfficiency from percentage to decimal (e.g., 80% → 0.8)
            const minEfficiencyDecimal = minEfficiency / 100;
            
            // Calculate how much additional CPU we can use while maintaining the minimum efficiency
            const additionalCpu = Math.max(0, (totalCpu * (1 / minEfficiencyDecimal)) - totalCpu);
            
            // Add this to the available CPU
            adjustedAvailableCpu = availableCpu + additionalCpu;
        }
        
        // Use the adjusted available CPU for calculations
        const cpuLimit = adjustedAvailableCpu;
        
        // Get base values from the selected generator
        const generator = this.shieldData.shieldGenerators[generatorType];
        let baseCapacity = generator.capacity;
        let baseRecharge = generator.recharge;
        
        // Calculate block contribution to shield capacity
        let blockContribution = 0;
        for (const [blockType, count] of Object.entries(blockCounts)) {
            if (this.shieldData.blockContributions[blockType]) {
                blockContribution += count * this.shieldData.blockContributions[blockType].shieldContribution;
            }
        }
        
        // Add block contribution to base capacity
        baseCapacity += blockContribution;
        
        // Add fusion reactor bonuses to base recharge
        baseRecharge += smallFusionCount * this.shieldData.shieldBoosters.small_fusion.recharge;
        baseRecharge += largeFusionCount * this.shieldData.shieldBoosters.large_fusion.recharge;
        
        // Set up tier limits
        const tierLimits = {
            basic: 8,
            improved: 6,
            advanced: 4
        };
        
        // Initialize variables for the best configuration
        let bestConfig = null;
        let bestCapacity = 0;
        
        // Get all boosters
        const boosters = {};
        for (const [id, booster] of Object.entries(this.shieldData.shieldBoosters)) {
            boosters[id] = {
                id,
                ...booster
            };
        }
        
        // Generate all valid configurations using a more exhaustive approach
        // This will more thoroughly explore the space of possible configurations
        
        // Initialize arrays to store all possible counts for each tier
        const generateAllConfigs = () => {
            // For basic tier (max 8 total): try all combinations of capacitors and chargers
            for (let basicCapCount = 0; basicCapCount <= tierLimits.basic; basicCapCount++) {
                for (let basicCharCount = 0; basicCharCount <= tierLimits.basic - basicCapCount; basicCharCount++) {
                    
                    // For improved tier (max 6 total): try all combinations
                    for (let improvedCapCount = 0; improvedCapCount <= tierLimits.improved; improvedCapCount++) {
                        for (let improvedCharCount = 0; improvedCharCount <= tierLimits.improved - improvedCapCount; improvedCharCount++) {
                            
                            // For advanced tier (max 4 total): try all combinations
                            for (let advancedCapCount = 0; advancedCapCount <= tierLimits.advanced; advancedCapCount++) {
                                for (let advancedCharCount = 0; advancedCharCount <= tierLimits.advanced - advancedCapCount; advancedCharCount++) {
                                    
                                    // Create config with these counts
                                    const config = {
                                        basic_capacitor: basicCapCount,
                                        basic_charger: basicCharCount,
                                        improved_capacitor: improvedCapCount,
                                        improved_charger: improvedCharCount,
                                        advanced_capacitor: advancedCapCount,
                                        advanced_charger: advancedCharCount
                                    };
                                    
                                    // Calculate total stats for this config
                                    let totalCapacity = baseCapacity;
                                    let totalRecharge = baseRecharge;
                                    let cpuUsed = 0;
                                    
                                    for (const [id, count] of Object.entries(config)) {
                                        if (count > 0) {
                                            const booster = boosters[id];
                                            totalCapacity += booster.capacity * count;
                                            totalRecharge += booster.recharge * count;
                                            cpuUsed += (booster.cpu || 0) * count;
                                        }
                                    }
                                    
                                    // Check constraints
                                    if (cpuUsed > cpuLimit) {
                                        continue;  // CPU limit exceeded
                                    }
                                    
                                    if (totalRecharge < minRechargeRate) {
                                        continue;  // Recharge rate too low
                                    }
                                    
                                    // Check efficiency if CPU is used
                                    if (cpuUsed > 0) {
                                        const efficiency = totalCpu / (totalCpu - availableCpu + cpuUsed);
                                        if (efficiency < (minEfficiency / 100)) {
                                            continue;  // Efficiency too low
                                        }
                                    }
                                    
                                    // This is a valid configuration - check if it's better than our current best
                                    if (totalCapacity > bestCapacity) {
                                        bestCapacity = totalCapacity;
                                        bestConfig = {
                                            config: {...config},
                                            capacity: totalCapacity,
                                            recharge: totalRecharge,
                                            cpu: cpuUsed
                                        };
                                    }
                                }
                            }
                        }
                    }
                }
            }
        };
        
        // Generate all possible configurations using our exhaustive approach
        generateAllConfigs();
        
        // If we didn't find a valid config, return failure
        if (!bestConfig) {
            return {
                success: false,
                message: "No valid configuration found. Try adjusting your requirements.",
                rechargeRate: baseRecharge,
                totalCapacity: baseCapacity,
                cpuUsed: 0,
                cpuLimit: cpuLimit,
                originalCpuLimit: availableCpu,
                cpuEfficiency: 0,
                boosterCounts: {},
                generatorName: generator.name,
                baseCapacity: generator.capacity,
                baseRecharge: generator.recharge,
                blockContribution: blockContribution
            };
        }
        
        // Calculate recharge time and return results
        const rechargeTime = this.calculateRechargeTime(bestConfig.capacity, bestConfig.recharge);
        const cpuEfficiency = this.calculateEfficiency(bestConfig.capacity, bestConfig.cpu, totalCpu, availableCpu);
        
        // Organize booster counts by tier
        const tierCounts = {
            basic: (bestConfig.config.basic_capacitor || 0) + (bestConfig.config.basic_charger || 0),
            improved: (bestConfig.config.improved_capacitor || 0) + (bestConfig.config.improved_charger || 0),
            advanced: (bestConfig.config.advanced_capacitor || 0) + (bestConfig.config.advanced_charger || 0)
        };
        
        return {
            success: true,
            generatorName: this.shieldData.shieldGenerators[generatorType].name,
            baseCapacity: generator.capacity,
            baseRecharge: generator.recharge,
            blockContribution: blockContribution,
            totalCapacity: bestConfig.capacity,
            rechargeRate: bestConfig.recharge,
            rechargeTime: rechargeTime,
            cpuUsed: bestConfig.cpu,
            cpuLimit: cpuLimit,
            originalCpuLimit: availableCpu,
            cpuEfficiency: cpuEfficiency,
            boosterCounts: bestConfig.config,
            tierCounts: tierCounts
        };
    }
    
    /**
     * Calculate the time to fully recharge shields
     * @param {number} capacity - Total shield capacity
     * @param {number} rechargeRate - Shields recharged per second
     * @returns {string} - Formatted time string
     */
    calculateRechargeTime(capacity, rechargeRate) {
        if (rechargeRate <= 0) return "∞";
        
        const seconds = capacity / rechargeRate;
        return this.formatTime(seconds / 60); // Convert to minutes for formatting
    }
    
    /**
     * Calculate CPU efficiency percentage
     * @param {number} capacity - Total shield capacity
     * @param {number} cpuUsed - Total CPU used by shields
     * @param {number} totalCpu - Total CPU available on the vessel
     * @param {number} availableCpu - Available CPU for shields
     * @returns {number} - Efficiency percentage (capped at 100%)
     */
    calculateEfficiency(capacity, cpuUsed, totalCpu, availableCpu) {
        if (cpuUsed <= 0 || totalCpu <= 0) return 0;
        
        // Calculate efficiency using formula: totalCpu / (totalCpu - availableCpu + cpuUsed)
        const efficiency = totalCpu / (totalCpu - availableCpu + cpuUsed);
        
        // Cap efficiency at 1.0 (100%)
        return Math.min(efficiency, 1.0);
    }
    
    /**
     * Format time in minutes to a readable string
     * @param {number} minutes - Time in minutes
     * @returns {string} - Formatted time string
     */
    formatTime(minutes) {
        if (minutes < 1) {
            // Less than a minute, show seconds
            const seconds = Math.round(minutes * 60);
            return `${seconds} sec`;
        } else if (minutes < 60) {
            // Less than an hour
            const mins = Math.floor(minutes);
            const secs = Math.round((minutes - mins) * 60);
            return `${mins}m ${secs}s`;
        } else {
            // Hours and minutes
            const hours = Math.floor(minutes / 60);
            const mins = Math.floor(minutes % 60);
            const secs = Math.round(((minutes % 60) - mins) * 60);
            
            if (secs > 0) {
                return `${hours}h ${mins}m ${secs}s`;
            } else {
                return `${hours}h ${mins}m`;
            }
        }
    }
    
    /**
     * Get all available generator types
     * @returns {Array} - List of generator types
     */
    getGeneratorTypes() {
        return Object.entries(this.shieldData.shieldGenerators)
            .map(([id, data]) => ({
                id,
                name: data.name
            }));
    }
    
    /**
     * Get details about a specific booster
     * @param {string} boosterId - The ID of the booster
     * @returns {Object} - Booster details
     */
    getBoosterDetails(boosterId) {
        return {
            id: boosterId,
            ...this.shieldData.shieldBoosters[boosterId]
        };
    }
}
