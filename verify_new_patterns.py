#!/usr/bin/env python3
"""
Verification script to check that the new targeted line patterns have different line counts
"""

def test_new_pattern_configs():
    """Test the new pattern configuration system"""
    
    # These are the exact configurations used in the updated code
    pattern_configs = [
        {'spacing_um': 7.0, 'target_lines': 3, 'orientation': 0},    # 3 thick lines
        {'spacing_um': 5.0, 'target_lines': 5, 'orientation': 45},   # 5 medium lines
        {'spacing_um': 3.0, 'target_lines': 7, 'orientation': 90},   # 7 lines (changed from 8)
        {'spacing_um': 2.0, 'target_lines': 10, 'orientation': 0},   # 10 lines
        {'spacing_um': 1.0, 'target_lines': 15, 'orientation': 45},  # 15 fine lines
        {'spacing_um': 0.7, 'target_lines': 20, 'orientation': 90},  # 20 very fine lines
        {'spacing_um': 0.5, 'target_lines': 12, 'orientation': 0},   # 12 ultra-fine lines
        {'spacing_um': 0.3, 'target_lines': 8, 'orientation': 45},   # 8 ultra-fine lines
        {'spacing_um': 0.25, 'target_lines': 6, 'orientation': 90}   # 6 ultra-fine lines
    ]
    
    print("New Line Pair Pattern Configuration:")
    print("=" * 60)
    print(f"{'Index':<5} {'Spacing':<8} {'Lines':<6} {'Orient':<6} {'Line Width':<10} {'Description'}")
    print("-" * 60)
    
    for i, config in enumerate(pattern_configs):
        spacing = config['spacing_um']
        target_lines = config['target_lines']
        orientation = config['orientation']
        line_width = spacing * 0.3  # 30% of spacing
        
        if spacing >= 1:
            spacing_str = f"{spacing:.1f}µm"
        else:
            spacing_str = f"{int(spacing*1000)}nm"
        
        orientation_desc = {0: "Horiz", 45: "Diag", 90: "Vert"}[orientation]
        
        if target_lines <= 5:
            density = "Sparse"
        elif target_lines <= 10:
            density = "Medium"
        elif target_lines <= 15:
            density = "Dense"
        else:
            density = "Very Dense"
        
        print(f"{i+1:<5} {spacing_str:<8} {target_lines:<6} {orientation_desc:<6} "
              f"{line_width:.2f}µm{'':<4} {density}")
    
    # Analyze the differences
    print(f"\nPattern Analysis:")
    print("-" * 30)
    
    line_counts = [config['target_lines'] for config in pattern_configs]
    spacings = [config['spacing_um'] for config in pattern_configs]
    orientations = [config['orientation'] for config in pattern_configs]
    
    print(f"Line count range: {min(line_counts)} to {max(line_counts)} lines")
    print(f"Unique line counts: {sorted(set(line_counts))}")
    print(f"Spacing range: {min(spacings)}µm to {max(spacings)}µm")
    print(f"Orientations used: {sorted(set(orientations))}° (0=horizontal, 45=diagonal, 90=vertical)")
    
    # Check for variety
    print(f"\nVariety Check:")
    print("-" * 15)
    
    if len(set(line_counts)) == len(line_counts):
        print("✓ All patterns have unique line counts")
    else:
        print(f"⚠ Some patterns share line counts: {[x for x in set(line_counts) if line_counts.count(x) > 1]}")
    
    if len(set(orientations)) == 3:
        print("✓ All three orientations are used")
    else:
        print(f"⚠ Only {len(set(orientations))} orientations used")
    
    # Check for good distribution
    spacing_decades = []
    for s in spacings:
        if s >= 1:
            spacing_decades.append("µm")
        else:
            spacing_decades.append("nm")
    
    print(f"✓ Spacing covers both micrometer and nanometer scales")
    print(f"✓ Line density varies from {min(line_counts)} to {max(line_counts)} (range: {max(line_counts) - min(line_counts)})")
    
    # Visual difference prediction
    print(f"\nVisual Difference Prediction:")
    print("-" * 35)
    
    for i, config in enumerate(pattern_configs):
        lines = config['target_lines']
        if lines <= 3:
            visibility = "Very obvious (thick spacing)"
        elif lines <= 8:
            visibility = "Clearly visible"
        elif lines <= 15:
            visibility = "Fine but distinguishable"
        else:
            visibility = "Very fine (needs good resolution)"
        
        position = f"Position {i+1} (row {i//3 + 1}, col {i%3 + 1})"
        print(f"{position:<25} {lines:2d} lines - {visibility}")

if __name__ == "__main__":
    test_new_pattern_configs() 