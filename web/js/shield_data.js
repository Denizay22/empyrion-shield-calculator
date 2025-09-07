/**
 * Shield Data for Empyrion Shield Calculator
 * Contains data for shield boosters and generator types
 */

const SHIELD_DATA = {
    // Shield Boosters data
    shieldBoosters: {
        basic_capacitor: {
            name: "Basic Shield Capacitor",
            cpu: 8000,
            recharge: -150,
            capacity: 8000,
            tier: "basic",
            maxCount: 8
        },
        improved_capacitor: {
            name: "Improved Shield Capacitor",
            cpu: 12000,
            recharge: -300,
            capacity: 16000,
            tier: "improved",
            maxCount: 6
        },
        advanced_capacitor: {
            name: "Advanced Shield Capacitor",
            cpu: 18000,
            recharge: -600,
            capacity: 32000,
            tier: "advanced",
            maxCount: 4
        },
        basic_charger: {
            name: "Basic Shield Charger",
            cpu: 8000,
            recharge: 300,
            capacity: -4000,
            tier: "basic",
            maxCount: 8
        },
        improved_charger: {
            name: "Improved Shield Charger",
            cpu: 12000,
            recharge: 600,
            capacity: -8000,
            tier: "improved",
            maxCount: 6
        },
        advanced_charger: {
            name: "Advanced Shield Charger",
            cpu: 18000,
            recharge: 1200,
            capacity: -16000,
            tier: "advanced",
            maxCount: 4
        },
        // Add fusion devices which don't use CPU but affect shield stats
        small_fusion: {
            name: "Small Fusion Reactor",
            cpu: 0,
            recharge: 300,
            capacity: 0,
            tier: "other",
            maxCount: 4
        },
        large_fusion: {
            name: "Large Fusion Reactor",
            cpu: 0,
            recharge: 1000,
            capacity: 0,
            tier: "other",
            maxCount: 4
        }
    },

    // Shield Generator Types
    shieldGenerators: {
        compact: {
            name: "Compact Shield Generator",
            capacity: 6000,
            recharge: 300
        },
        regular: {
            name: "Regular Shield Generator",
            capacity: 12000,
            recharge: 300
        },
        advanced: {
            name: "Advanced Shield Generator",
            capacity: 24000,
            recharge: 600
        },
        alien: {
            name: "Alien Shield Generator",
            capacity: 40000,
            recharge: 1000
        }
    },
    
    // Ship blocks contribution to shield capacity (per block)
    blockContributions: {
        steel: {
            name: "Steel Block",
            shieldContribution: 1
        },
        hardenedSteel: {
            name: "Hardened Steel Block",
            shieldContribution: 2
        },
        combatSteel: {
            name: "Combat Steel Block",
            shieldContribution: 4
        },
        xeno: {
            name: "Xeno Block",
            shieldContribution: 7
        }
    }
};
