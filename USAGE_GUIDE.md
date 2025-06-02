# Calibration Plate Designer - Usage Guide

## Quick Start

1. **Run the application**:
   ```bash
   python calibration_plate_designer.py
   ```

2. **Set plate dimensions** (default: 101.6mm x 101.6mm, 4-inch plate)

3. **Configure each of the 4 sections** with different pattern types

4. **Generate files** by clicking "Generate SVG" or "Generate DXF"

## Pattern Guidelines

### Resolution Patterns (Dot Arrays)
- **Recommended spacing**: 2-50 µm for typical applications
- **Very small spacing** (< 1 µm): Use for high-resolution testing
- **Larger spacing** (> 50 µm): Use for lower magnification work
- **Dot diameter**: Usually 20-50% of spacing for good visibility

**Example configurations**:
- High resolution: 0.5 µm spacing, 0.1 µm diameter
- Medium resolution: 5 µm spacing, 1 µm diameter  
- Low resolution: 20 µm spacing, 5 µm diameter

### Distortion Patterns (Checkerboard)
- **Recommended grid size**: 0.5-5 mm
- **Small grids** (< 0.5 mm): For fine distortion analysis
- **Large grids** (> 5 mm): For gross distortion measurement
- Creates alternating black/white squares

**Example configurations**:
- Fine analysis: 0.5 mm grid
- Standard analysis: 1-2 mm grid
- Coarse analysis: 5 mm grid

### Line Pair Patterns
- **Pattern Mode**: Choose between 'single' or 'multi' pattern mode
- **Single Mode**: Traditional single orientation pattern
  - **Recommended spacing**: 1-20 µm
  - **Line width**: Usually 30-50% of spacing
  - **Orientation**: Choose vertical or horizontal based on measurement needs
- **Multi Mode**: Creates comprehensive resolution test with multiple sub-patterns
  - **Creates 3x3 grid** within the section
  - **Line spacings**: 7µm, 5µm, 3µm, 2µm, 1µm, 700nm, 500nm, 300nm, 250nm
  - **Orientations**: 0° (horizontal), 45° (diagonal), 90° (vertical)
  - **Automatic labeling** with spacing values and orientations
  - **Sub-section borders** for easy identification

**Single Mode Example configurations**:
- High resolution: 1 µm spacing, 0.3 µm width
- Medium resolution: 5 µm spacing, 1.5 µm width
- Low resolution: 20 µm spacing, 6 µm width

**Multi Mode Features**:
- **Comprehensive testing**: Range from 7µm down to 250nm in a single section
- **Three orientations**: Tests resolution in different directions
- **Automatic optimization**: Each sub-pattern optimized for its area
- **Clear labeling**: Each pattern labeled with spacing and orientation
- **Performance optimized**: Limited line counts to prevent freezing

### Alignment Markers
- **Crosshair**: Simple + shape for basic alignment
- **Fiducial**: Circle with center dot for precise positioning
- **Scale bar**: Graduated ruler for size reference
- **Size**: 1-10 mm depending on application

## Performance Optimization

### Element Count Limits
The application automatically limits patterns to **10,000 elements** per section to prevent freezing. If your settings would create more elements, the application will:

1. **Show a warning** in the console
2. **Automatically reduce density** while maintaining pattern structure
3. **Continue generation** with the reduced pattern

### Avoiding Performance Issues

**For very small spacing values**:
- Use larger plate sections (increase plate size or reduce margin)
- Accept the automatic density reduction
- Consider if such fine resolution is actually needed

**For optimal performance**:
- Keep dot spacing ≥ 1 µm for resolution patterns
- Keep line spacing ≥ 1 µm for line pair patterns  
- Keep grid size ≥ 0.5 mm for distortion patterns

## File Output

### SVG Files
- **Best for**: Preview, documentation, web viewing
- **Compatible with**: Web browsers, Inkscape, Adobe Illustrator
- **Advantages**: Easy to view, smaller file sizes
- **Use when**: You want to preview the design or need vector graphics

### DXF Files  
- **Best for**: Manufacturing, CAD software
- **Compatible with**: AutoCAD, FreeCAD, SolidWorks, manufacturing software
- **Advantages**: Industry standard for fabrication
- **Use when**: Sending to fabrication services like Compugraphics Jena GmbH

## Fabrication Considerations

### For Compugraphics Jena GmbH
- **Preferred format**: DXF
- **Minimum feature size**: Check their specifications (typically 100-500 nm)
- **Recommended approach**: Start with larger features and scale down as needed
- **File organization**: Include section outlines for reference (automatically added)

### General Fabrication Tips
1. **Check minimum feature sizes** with your fabrication service
2. **Include alignment markers** in at least one section
3. **Use consistent units** (application uses millimeters)
4. **Test with simple patterns** before complex designs

## Troubleshooting

### Application Freezes or Hangs
**Fixed in current version!** The application now:
- Limits element count automatically
- Shows progress during generation
- Provides warnings for problematic settings

### "Too Many Elements" Warning
**Meaning**: Your spacing settings would create more than 10,000 pattern elements
**Solution**: 
- Increase spacing values
- Reduce section size (increase margin)
- Accept the automatic reduction

### Empty or Missing Patterns
**Possible causes**:
- Pattern spacing larger than section size
- Very small feature sizes (< 0.001 mm)
**Solution**: Adjust spacing to fit within section boundaries

### File Generation Errors
**Check**:
- File permissions in target directory
- Available disk space
- Valid plate dimensions (positive numbers)

## Advanced Tips

### Custom Plate Sizes
- **Standard sizes**: 4" (101.6mm), 6" (152.4mm), 8" (203.2mm)
- **Custom sizes**: Any positive dimensions in millimeters
- **Margin considerations**: Leave enough space for handling and mounting

### Section Layout Strategy
- **Section 1 (top-left)**: High-resolution features
- **Section 2 (top-right)**: Medium-resolution features  
- **Section 3 (bottom-left)**: Alignment/measurement features
- **Section 4 (bottom-right)**: Large-scale features

### Pattern Combination Ideas
1. **Resolution characterization**: Different dot spacings across sections
2. **Multi-scale testing**: Combine dots, lines, and grids
3. **Alignment focused**: Multiple alignment marker types
4. **Process development**: Systematic variation of line widths

## Example Configurations

### Microscopy Calibration Plate
- **Plate**: 50mm x 50mm, 5mm margin
- **Section 1**: Resolution dots, 2 µm spacing, 0.5 µm diameter
- **Section 2**: Distortion grid, 1 mm squares
- **Section 3**: Line pairs, multi-pattern mode (comprehensive resolution test)
- **Section 4**: Crosshair markers, 3 mm size

### Lithography Test Plate  
- **Plate**: 101.6mm x 101.6mm, 10mm margin
- **Section 1**: Resolution dots, 0.5 µm spacing, 0.1 µm diameter
- **Section 2**: Line pairs, multi-pattern mode (7µm down to 250nm)
- **Section 3**: Distortion grid, 0.5 mm squares
- **Section 4**: Fiducial markers, 2 mm size

### High-Resolution Research Plate
- **Plate**: 50mm x 50mm, 3mm margin
- **Section 1**: Line pairs, single mode, 250nm spacing, vertical
- **Section 2**: Line pairs, single mode, 250nm spacing, horizontal
- **Section 3**: Resolution dots, 200nm spacing, 50nm diameter
- **Section 4**: Line pairs, multi-pattern mode

### Multi-Scale Characterization Plate
- **Plate**: 101.6mm x 101.6mm, 15mm margin
- **Section 1**: Resolution dots, 5µm spacing (low magnification)
- **Section 2**: Resolution dots, 1µm spacing (medium magnification)
- **Section 3**: Line pairs, multi-pattern mode (comprehensive)
- **Section 4**: Alignment markers, scale bars, 5mm size

Remember: 
- The generated files include **section numbering** (Section 1-4) in blue text
- **Pattern type labels** are shown under each section number
- **Section outlines** (gray dashed lines) help identify different pattern areas
- **Multi-pattern sections** include **sub-section borders** and **individual pattern labels** 