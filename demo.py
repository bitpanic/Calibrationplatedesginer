#!/usr/bin/env python3
"""
Demo script for the Calibration Plate Designer
This script demonstrates how to use the application programmatically
and generates sample SVG and DXF files.
"""

import os
import tkinter as tk
from calibration_plate_designer import CalibrationPlateDesigner

def create_demo_files():
    """Create demo calibration plate files"""
    
    # Create a hidden root window (we won't show the GUI for this demo)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create the designer instance
    designer = CalibrationPlateDesigner(root)
    
    # Configure demo settings
    designer.plate_width.set(50.0)  # 50mm x 50mm plate
    designer.plate_height.set(50.0)
    designer.margin.set(5.0)  # 5mm margin
    
    # Configure section 1: Resolution pattern with 2µm dots
    designer.section_configs[0]['pattern_type'].set('Resolution Patterns')
    designer.update_parameters(0)
    designer.section_configs[0]['params']['dot_spacing'].set(2.0)
    designer.section_configs[0]['params']['dot_diameter'].set(0.5)
    
    # Configure section 2: Distortion pattern with 1mm grid
    designer.section_configs[1]['pattern_type'].set('Distortion Patterns')
    designer.update_parameters(1)
    designer.section_configs[1]['params']['grid_size'].set(1.0)
    
    # Configure section 3: Line pairs with 1µm spacing
    designer.section_configs[2]['pattern_type'].set('Line Pair Patterns')
    designer.update_parameters(2)
    designer.section_configs[2]['params']['line_spacing'].set(1.0)
    designer.section_configs[2]['params']['line_width'].set(0.3)
    designer.section_configs[2]['params']['orientation'].set('vertical')
    
    # Configure section 4: Crosshair alignment markers
    designer.section_configs[3]['pattern_type'].set('Alignment Markers')
    designer.update_parameters(3)
    designer.section_configs[3]['params']['marker_type'].set('crosshair')
    designer.section_configs[3]['params']['marker_size'].set(3.0)
    
    # Generate demo files
    demo_files = []
    
    try:
        # Generate SVG file
        import svgwrite
        
        plate_w = designer.plate_width.get()
        plate_h = designer.plate_height.get()
        
        # Create SVG
        svg_filename = "demo_calibration_plate.svg"
        dwg = svgwrite.Drawing(svg_filename, size=(f'{plate_w}mm', f'{plate_h}mm'),
                             viewBox=f'0 0 {plate_w} {plate_h}')
        
        # Add plate outline
        plate_outline = dwg.rect(insert=(0, 0), size=(plate_w, plate_h),
                               fill='none', stroke='black', stroke_width=0.1)
        dwg.add(plate_outline)
        
        # Get section dimensions and positions
        sections, section_w, section_h = designer.calculate_section_dimensions()
        
        # Generate patterns for each section
        for i, (x_offset, y_offset) in enumerate(sections):
            pattern_type = designer.section_configs[i]['pattern_type'].get()
            params = designer.get_section_parameters(i)
            
            # Create pattern generator
            generator_class = designer.pattern_generators[pattern_type]
            generator = generator_class(pattern_type, params)
            
            # Generate SVG elements
            elements = generator.generate_svg_elements(dwg, x_offset, y_offset, 
                                                     section_w, section_h)
            
            # Add elements to drawing
            for element in elements:
                dwg.add(element)
            
            # Add section outline
            section_outline = dwg.rect(insert=(x_offset, y_offset), 
                                     size=(section_w, section_h),
                                     fill='none', stroke='gray', 
                                     stroke_width=0.05, stroke_dasharray='1,1')
            dwg.add(section_outline)
        
        # Save SVG
        dwg.save()
        demo_files.append(svg_filename)
        print(f"✓ Created demo SVG file: {svg_filename}")
        
    except ImportError:
        print("✗ SVG generation skipped (svgwrite not available)")
    except Exception as e:
        print(f"✗ Error generating SVG: {e}")
    
    try:
        # Generate DXF file
        import ezdxf
        
        dxf_filename = "demo_calibration_plate.dxf"
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # Add plate outline
        plate_outline = [
            (0, 0),
            (plate_w, 0),
            (plate_w, plate_h),
            (0, plate_h),
            (0, 0)
        ]
        msp.add_lwpolyline(plate_outline, close=True)
        
        # Generate patterns for each section
        for i, (x_offset, y_offset) in enumerate(sections):
            pattern_type = designer.section_configs[i]['pattern_type'].get()
            params = designer.get_section_parameters(i)
            
            # Create pattern generator
            generator_class = designer.pattern_generators[pattern_type]
            generator = generator_class(pattern_type, params)
            
            # Generate DXF elements
            generator.generate_dxf_elements(msp, x_offset, y_offset, 
                                          section_w, section_h)
            
            # Add section outline
            section_outline = [
                (x_offset, y_offset),
                (x_offset + section_w, y_offset),
                (x_offset + section_w, y_offset + section_h),
                (x_offset, y_offset + section_h),
                (x_offset, y_offset)
            ]
            msp.add_lwpolyline(section_outline, close=True)
        
        # Save DXF
        doc.saveas(dxf_filename)
        demo_files.append(dxf_filename)
        print(f"✓ Created demo DXF file: {dxf_filename}")
        
    except ImportError:
        print("✗ DXF generation skipped (ezdxf not available)")
    except Exception as e:
        print(f"✗ Error generating DXF: {e}")
    
    root.destroy()
    return demo_files

def print_demo_info():
    """Print information about the demo"""
    print("=" * 60)
    print("Calibration Plate Designer - Demo")
    print("=" * 60)
    print()
    print("This demo creates sample calibration plate files with:")
    print("• Plate size: 50mm x 50mm")
    print("• Margin: 5mm")
    print("• Section 1: Resolution dots (2µm spacing, 0.5µm diameter)")
    print("• Section 2: Distortion grid (1mm squares)")
    print("• Section 3: Line pairs (1µm spacing, 0.3µm width, vertical)")
    print("• Section 4: Crosshair alignment markers (3mm size)")
    print()

if __name__ == "__main__":
    print_demo_info()
    
    print("Generating demo files...")
    demo_files = create_demo_files()
    
    print()
    if demo_files:
        print(f"Successfully created {len(demo_files)} demo file(s):")
        for filename in demo_files:
            file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
            print(f"  • {filename} ({file_size:,} bytes)")
        
        print()
        print("To view the files:")
        print("• SVG files can be opened in web browsers or vector graphics software")
        print("• DXF files can be opened in CAD software like AutoCAD or FreeCAD")
        
        print()
        print("To run the GUI application:")
        print("  python calibration_plate_designer.py")
    else:
        print("No demo files were created. Please check the error messages above.")
    
    print()
    print("=" * 60) 