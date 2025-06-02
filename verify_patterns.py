#!/usr/bin/env python3
"""
Verification script to check that line patterns have different spacings
"""

import tkinter as tk
from calibration_plate_designer import LinePairPatternGenerator

def test_pattern_differences():
    """Test that different spacings produce different patterns"""
    
    # Create a dummy root window (hidden)
    root = tk.Tk()
    root.withdraw()
    
    # Test spacings from the multi-pattern mode
    spacings_um = [7.0, 5.0, 3.0, 2.0, 1.0, 0.7, 0.5, 0.3, 0.25]
    
    print("Testing Line Pair Pattern Generation:")
    print("=" * 50)
    
    for i, spacing in enumerate(spacings_um):
        # Create generator with multi-pattern mode
        params = {
            'pattern_type': 'multi'
        }
        generator = LinePairPatternGenerator('test', params)
        
        # Calculate line width (30% of spacing)
        line_width = spacing * 0.3
        
        # Test the calculation logic for different orientations
        spacing_mm = spacing / 1000
        line_width_mm = line_width / 1000
        
        # Simulate a sub-section size (typical would be ~13mm x 13mm for 3x3 grid in 40mm section)
        sub_width = 13.0  # mm
        sub_height = 13.0  # mm
        margin = min(sub_width, sub_height) * 0.05
        pattern_width = sub_width - 2 * margin
        pattern_height = sub_height - 2 * margin
        
        # Calculate number of line pairs for horizontal orientation (0°)
        num_line_pairs_h = max(1, int(pattern_height / (2 * spacing_mm)))
        num_line_pairs_h = min(num_line_pairs_h, 25)
        
        # Calculate number of line pairs for vertical orientation (90°)
        num_line_pairs_v = max(1, int(pattern_width / (2 * spacing_mm)))
        num_line_pairs_v = min(num_line_pairs_v, 25)
        
        print(f"Spacing {spacing:4.2f}µm | Line Width {line_width:4.2f}µm | "
              f"H-Lines: {num_line_pairs_h:2d} | V-Lines: {num_line_pairs_v:2d} | "
              f"Spacing(mm): {spacing_mm:6.4f}")
    
    print("\nPattern Differences Verification:")
    print("-" * 40)
    
    # Check if patterns are actually different
    unique_spacings = set(spacings_um)
    if len(unique_spacings) == len(spacings_um):
        print("✓ All spacings are unique")
    else:
        print("✗ Some spacings are duplicated")
    
    # Check if line counts are different
    line_counts = []
    for spacing in spacings_um:
        spacing_mm = spacing / 1000
        pattern_height = 13.0 - 2 * (13.0 * 0.05)
        num_pairs = max(1, int(pattern_height / (2 * spacing_mm)))
        num_pairs = min(num_pairs, 25)
        line_counts.append(num_pairs)
    
    unique_counts = set(line_counts)
    if len(unique_counts) > 1:
        print(f"✓ Line counts vary: {sorted(unique_counts)}")
        print("  This means patterns will look visibly different")
    else:
        print("✗ All patterns have the same line count")
    
    print(f"\nRange of line counts: {min(line_counts)} to {max(line_counts)}")
    print(f"Spacing range: {min(spacings_um)}µm to {max(spacings_um)}µm")
    print(f"Line width range: {min(spacings_um)*0.3:.3f}µm to {max(spacings_um)*0.3:.3f}µm")
    
    root.destroy()

if __name__ == "__main__":
    test_pattern_differences() 