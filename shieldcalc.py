import json
import itertools

def load_shield_info():
    """Load shield information from the JSON files"""
    try:
        # Load shield boosters
        with open('shieldinfo.json', 'r') as file:
            shield_info = json.load(file)
            
        # Load shield generators
        try:
            with open('shield_generators.json', 'r') as file:
                generators = json.load(file)
                shield_info['shieldGenerators'] = generators['shieldGenerators']
        except (FileNotFoundError, json.JSONDecodeError):
            # Default values if file not found or invalid
            shield_info['shieldGenerators'] = {
                "compact": {"capacity": 6000, "recharge": 300},
                "regular": {"capacity": 12000, "recharge": 300},
                "advanced": {"capacity": 24000, "recharge": 600},
                "alien": {"capacity": 40000, "recharge": 1000}
            }
            
        return shield_info
    except FileNotFoundError:
        print("Error: shieldinfo.json file not found!")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in shieldinfo.json!")
        exit(1)

def get_user_inputs(shield_info):
    """Get user inputs for total/available CPU, minimum CPU efficiency, recharge, and fusion reactors"""
    try:
        total_cpu = int(input("Enter total CPU points of the ship: "))
        if total_cpu <= 0:
            print("Total CPU must be greater than zero. Using 100,000 as default.")
            total_cpu = 100000
            
        available_cpu = int(input("Enter available CPU points for shields: "))
        if available_cpu < 0:
            print("Available CPU cannot be negative. Using total CPU as default.")
            available_cpu = total_cpu
            
        min_cpu_efficiency = float(input("Enter minimum CPU efficiency (0.0-1.0, used_cpu/total_cpu): "))
        if min_cpu_efficiency < 0 or min_cpu_efficiency > 1:
            print("CPU efficiency must be between 0.0 and 1.0. Using 0.5 as default.")
            min_cpu_efficiency = 0.5
            
        # Select shield generator type
        print("\nShield Generator Types:")
        print("1. Compact Shield Generator (6,000 capacity, 300 recharge)")
        print("2. Regular Shield Generator (12,000 capacity, 300 recharge)")
        print("3. Advanced Shield Generator (24,000 capacity, 600 recharge)")
        print("4. Alien Shield Generator (40,000 capacity, 1,000 recharge)")
        
        shield_type_choice = 0
        while shield_type_choice not in [1, 2, 3, 4]:
            try:
                shield_type_choice = int(input("Select shield generator type (1-4): "))
                if shield_type_choice not in [1, 2, 3, 4]:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Map choice to shield generator type
        shield_types = ["compact", "regular", "advanced", "alien"]
        selected_shield_type = shield_types[shield_type_choice - 1]
        
        min_recharge = float(input("Enter minimum required recharge rate: "))
        
        small_fusion_count = int(input("Enter number of small fusion reactors: "))
        large_fusion_count = int(input("Enter number of large fusion reactors: "))
        
        # Get ship block counts
        print("\nShip Block Counts (for shield capacity):")
        steel_blocks = int(input("Enter number of steel blocks (1 shield each): "))
        hardened_steel = int(input("Enter number of hardened steel blocks (2 shield each): "))
        combat_steel = int(input("Enter number of combat steel blocks (4 shield each): "))
        xeno_blocks = int(input("Enter number of xeno blocks (7 shield each): "))
        
        # Calculate block shield contribution
        block_shield_capacity = (
            steel_blocks * 1 +
            hardened_steel * 2 +
            combat_steel * 4 +
            xeno_blocks * 7
        )
        
        return total_cpu, available_cpu, min_cpu_efficiency, min_recharge, small_fusion_count, large_fusion_count, block_shield_capacity, selected_shield_type
    except ValueError:
        print("Error: Please enter valid numbers!")
        return get_user_inputs()

def calculate_optimal_configuration(shield_info, total_cpu, available_cpu, min_cpu_efficiency, min_recharge, 
                              small_fusion, large_fusion, block_shield_capacity=0, shield_type="advanced"):
    """Calculate the optimal shield configuration"""
    boosters = shield_info['shieldBoosters']
    generators = shield_info['shieldGenerators']
    
    # Base shield values from selected generator
    base_capacity = generators[shield_type]["capacity"] + block_shield_capacity
    base_recharge = generators[shield_type]["recharge"]
    
    # Calculate base values from fusion reactors
    fusion_recharge = base_recharge + (small_fusion * boosters['small_fusion']['recharge'] + 
                     large_fusion * boosters['large_fusion']['recharge'])
    
    # Note: We'll calculate and check CPU efficiency during the configuration evaluation
    
    # Use available CPU for shields
    remaining_cpu = available_cpu
    
    # Required recharge after accounting for fusion reactors
    required_recharge = max(0, min_recharge - fusion_recharge)
    
    # Filter out fusion reactors for booster combinations
    booster_types = [name for name in boosters.keys() if name not in ['small_fusion', 'large_fusion']]
    
    # Define tier limits
    tier_limits = {
        'basic': 8,    # Max 8 basic tier boosters
        'improved': 6, # Max 6 improved tier boosters
        'advanced': 4  # Max 4 advanced tier boosters
    }
    
    best_config = None
    max_capacity = float('-inf')
    
    # Try different combinations of boosters
    for r in range(len(booster_types) + 1):
        for combo in itertools.product(range(9), repeat=len(booster_types)):  # Limit to max 8 of any individual type
            # Create a configuration with counts for each booster
            config = dict(zip(booster_types, combo))
            
            # Check tier limits
            basic_count = config.get('basic_capacitor', 0) + config.get('basic_charger', 0)
            improved_count = config.get('improved_capacitor', 0) + config.get('improved_charger', 0)
            advanced_count = config.get('advanced_capacitor', 0) + config.get('advanced_charger', 0)
            
            if (basic_count > tier_limits['basic'] or 
                improved_count > tier_limits['improved'] or 
                advanced_count > tier_limits['advanced']):
                continue
            
            # Calculate total CPU usage
            total_cpu = sum(count * boosters[booster]['cpu'] for booster, count in config.items())
            
            # Calculate total CPU usage
            total_cpu_used = sum(count * boosters[booster]['cpu'] for booster, count in config.items())
            
            # Check if CPU usage is within available limit
            if total_cpu_used > remaining_cpu:
                continue
            
            # Calculate CPU efficiency as used_cpu / total_cpu (prevent division by zero)
            if total_cpu > 0:
                cpu_efficiency = total_cpu_used / total_cpu
            else:
                # If total_cpu is 0, set efficiency to 0 (will fail the check below)
                cpu_efficiency = 0
            
            # Check if CPU efficiency meets or exceeds the minimum requirement
            if cpu_efficiency < min_cpu_efficiency:
                continue
            
            # Calculate total recharge and capacity
            total_recharge = fusion_recharge + sum(count * boosters[booster]['recharge'] for booster, count in config.items())
            total_capacity = base_capacity + sum(count * boosters[booster]['capacity'] for booster, count in config.items())
            
            # Check if recharge requirement is met
            if total_recharge < min_recharge:
                continue
            
                # Update best configuration if this one has higher capacity
            if total_capacity > max_capacity:
                max_capacity = total_capacity
                # Calculate CPU efficiency safely
                cpu_efficiency = total_cpu_used / total_cpu if total_cpu > 0 else 0
                best_config = {
                    'configuration': config,
                    'total_cpu': total_cpu_used,
                    'cpu_efficiency': cpu_efficiency,
                    'total_recharge': total_recharge,
                    'total_capacity': total_capacity,
                    'small_fusion_count': small_fusion,
                    'large_fusion_count': large_fusion,
                    'block_shield_capacity': block_shield_capacity,
                    'shield_type': shield_type
                }
    
    return best_config

def display_results(result, shield_info, total_cpu, available_cpu=None):
    """Display the results of the calculation"""
    if not result:
        print("\nNo valid configuration found! Try adjusting your requirements.")
        return
    
    # If available_cpu is not provided, use total_cpu as fallback
    if available_cpu is None:
        available_cpu = total_cpu
    
    print("\n===== Optimal Shield Configuration =====")
    
    # Get shield generator info
    shield_type = result.get('shield_type', 'advanced')
    shield_generator = shield_info['shieldGenerators'][shield_type]
    base_shield_capacity = shield_generator["capacity"]
    base_shield_recharge = shield_generator["recharge"]
    
    # Get friendly name for shield generator
    shield_type_names = {
        'compact': 'Compact Shield Generator',
        'regular': 'Regular Shield Generator',
        'advanced': 'Advanced Shield Generator',
        'alien': 'Alien Shield Generator'
    }
    shield_type_name = shield_type_names.get(shield_type, shield_type)
    
    # Display generator info
    print(f"Shield Generator: {shield_type_name}")
    print(f"Base Shield Capacity: {base_shield_capacity:,}")
    print(f"Base Shield Recharge: {base_shield_recharge:,}")
    
    # Display block contribution if any
    block_contribution = result.get('block_shield_capacity', 0)
    if block_contribution > 0:
        total_base_capacity = base_shield_capacity + block_contribution
        print(f"Block Shield Contribution: {block_contribution:,}")
        print(f"Total Base Capacity: {total_base_capacity:,}")
    print(f"Total Shield Capacity: {result['total_capacity']:,}")
    print(f"Total Recharge Rate: {result['total_recharge']:.1f}")
    
    # Calculate time to fully recharge in seconds
    time_to_recharge_seconds = result['total_capacity'] / result['total_recharge'] if result['total_recharge'] > 0 else float('inf')
    
    # Convert seconds to minutes and seconds
    minutes = int(time_to_recharge_seconds // 60)
    seconds = int(time_to_recharge_seconds % 60)
    
    print(f"Time to Fully Recharge: {minutes} minutes {seconds} seconds")
    print(f"CPU Usage: {result['total_cpu']:,} of {available_cpu:,}")
    print(f"CPU Efficiency: {result['cpu_efficiency']:.2%} (used_cpu/total_cpu)")
    
    # Count boosters by tier for display
    basic_count = sum(result['configuration'].get(b, 0) for b in ['basic_capacitor', 'basic_charger'])
    improved_count = sum(result['configuration'].get(b, 0) for b in ['improved_capacitor', 'improved_charger'])
    advanced_count = sum(result['configuration'].get(b, 0) for b in ['advanced_capacitor', 'advanced_charger'])
    
    print(f"\nBooster Usage by Tier:")
    print(f"- Basic Tier: {basic_count}/8")
    print(f"- Improved Tier: {improved_count}/6")
    print(f"- Advanced Tier: {advanced_count}/4")
    
    print("\nComponents:")
    # Define the order of components to display
    ordered_boosters = [
        ('basic_capacitor', 'Basic Capacitor'),
        ('basic_charger', 'Basic Charger'),
        ('improved_capacitor', 'Improved Capacitor'),
        ('improved_charger', 'Improved Charger'),
        ('advanced_capacitor', 'Advanced Capacitor'),
        ('advanced_charger', 'Advanced Charger')
    ]
    
    # Display boosters in order
    for booster_key, friendly_name in ordered_boosters:
        count = result['configuration'].get(booster_key, 0)
        if count > 0:
            print(f"- {friendly_name}: {count}")
    
    # Display fusion reactors separately
    if 'small_fusion_count' in result and result['small_fusion_count'] > 0:
        print(f"- Small Fusion Reactor: {result['small_fusion_count']}")
    if 'large_fusion_count' in result and result['large_fusion_count'] > 0:
        print(f"- Large Fusion Reactor: {result['large_fusion_count']}")

def run_test():
    """Run a simple test calculation to verify functionality"""
    print("===== Testing Empyrion Shield Calculator =====")
    shield_info = load_shield_info()
    
    # Use default values for testing
    total_cpu = 100000
    available_cpu = 50000
    min_cpu_efficiency = 0.8
    min_recharge = 1000
    small_fusion = 1
    large_fusion = 0
    block_shield_capacity = 1000
    shield_type = "advanced"
    
    print("\nCalculating test configuration...")
    result = calculate_optimal_configuration(shield_info, total_cpu, available_cpu, min_cpu_efficiency,
                                          min_recharge, small_fusion, large_fusion, block_shield_capacity, shield_type)
    
    if result:
        print("Test calculation successful!")
        return True
    else:
        print("Test calculation failed!")
        return False

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        success = run_test()
        sys.exit(0 if success else 1)
        
    print("===== Empyrion Shield Calculator =====")
    shield_info = load_shield_info()
    
    total_cpu, available_cpu, min_cpu_efficiency, min_recharge, small_fusion, large_fusion, block_shield_capacity, shield_type = get_user_inputs(shield_info)
    
    print("\nCalculating optimal configuration...")
    result = calculate_optimal_configuration(shield_info, total_cpu, available_cpu, min_cpu_efficiency,
                                           min_recharge, small_fusion, large_fusion, block_shield_capacity, shield_type)
    
    display_results(result, shield_info, total_cpu, available_cpu)

if __name__ == "__main__":
    main()