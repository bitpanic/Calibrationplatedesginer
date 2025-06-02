# Calibration Plate Designer

A Python GUI application for designing calibration plates with various pattern types for microscopy and fabrication purposes. The application generates SVG or DXF files that can be sent to fabrication services like Compugraphics Jena GmbH.

## Features

- **Intuitive GUI**: Built with tkinter for easy configuration
- **Multiple Pattern Types**:
  - Resolution Patterns (dot arrays with configurable spacing from 5 µm to 200 nm)
  - Distortion Patterns (checkerboard/grid patterns)
  - Line Pair Patterns (configurable line spacing and orientation)
  - Alignment and Scale Markers (crosshairs, fiducials, scale bars)
- **Flexible Layout**: 4-section plate design with configurable dimensions and margins
- **Multiple Export Formats**: SVG and DXF output formats
- **Precise Measurements**: All dimensions in millimeters with micrometer-level pattern precision

## Installation

1. **Clone or download** this repository to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install svgwrite>=1.4.0
   pip install ezdxf>=1.0.0
   ```

3. **Run the application**:
   ```bash
   python calibration_plate_designer.py
   ```

## Usage

### 1. Set Plate Dimensions
- **Width/Height**: Default is 101.6 mm (4 inches)
- **Margin**: Default is 10 mm border around the plate

### 2. Configure Each Section
The plate is divided into 4 equal sections. For each section:

#### Resolution Patterns
- **Dot Spacing**: Distance between dot centers (in micrometers)
- **Dot Diameter**: Size of each dot (in micrometers)
- Creates arrays of circular dots for resolution testing

#### Distortion Patterns
- **Grid Size**: Size of each checkerboard square (in millimeters)
- Creates alternating black/white squares for distortion analysis

#### Line Pair Patterns
- **Line Spacing**: Distance between line centers (in micrometers)
- **Line Width**: Width of each line (in micrometers)
- **Orientation**: Vertical or horizontal lines
- Creates alternating lines for resolution testing

#### Alignment Markers
- **Marker Type**: Choose from crosshair, fiducial, or scale_bar
- **Marker Size**: Overall size of the marker (in millimeters)
- Creates reference markers for alignment and measurement

### 3. Generate Files
- Click **"Generate SVG"** to create an SVG file
- Click **"Generate DXF"** to create a DXF file
- Choose the save location when prompted

## Output Files

### SVG Format
- Vector graphics format suitable for web viewing and some fabrication processes
- Includes precise measurements and can be opened in web browsers or vector graphics software
- Good for preview and documentation

### DXF Format
- CAD format widely used in manufacturing and fabrication
- Can be opened in AutoCAD, FreeCAD, and other CAD software
- Preferred format for sending to fabrication services

## Technical Specifications

### Coordinate System
- Origin (0,0) at top-left corner of the plate
- X-axis increases to the right
- Y-axis increases downward
- All measurements in millimeters

### Pattern Details

#### Resolution Patterns
- Dots are perfectly circular
- Spacing measured center-to-center
- Patterns automatically centered within their section

#### Distortion Patterns
- Checkerboard pattern with alternating filled/empty squares
- Top-left square is always filled (black)
- Grid automatically centered within section

#### Line Pair Patterns
- Every other line is drawn (creating line pairs)
- Lines can be vertical or horizontal
- Pattern automatically centered within section

#### Alignment Markers
- **Crosshair**: Simple cross with configurable size
- **Fiducial**: Circle with center dot for precise alignment
- **Scale Bar**: Graduated scale with major/minor tick marks

### File Structure
```
calibration_plate_designer.py  # Main application
requirements.txt               # Python dependencies
README.md                     # This documentation
```

## Use Cases

### Microscopy Calibration
- Resolution testing with dot arrays
- Distortion measurement with grid patterns
- Field calibration with scale bars

### Lithography Process Development
- Line/space resolution testing
- Alignment marker placement
- Process uniformity assessment

### Quality Control
- Measurement standards
- Reference patterns for comparison
- Batch-to-batch consistency checking

## Fabrication Compatibility

The generated files are designed to be compatible with:
- **Compugraphics Jena GmbH** lithography services
- Standard CAD/CAM software
- CNC machining systems
- Laser engraving/cutting systems
- Chemical etching processes

## Advanced Configuration

### Custom Pattern Sizes
- Micrometer-level precision for small features
- Millimeter-level sizing for larger structures
- Automatic unit conversion throughout the application

### Pattern Optimization
- Patterns automatically sized to fit within section boundaries
- Centering ensures optimal use of available space
- Integer calculations prevent partial features at edges

## Troubleshooting

### Missing Dependencies
If you get import errors:
```bash
pip install svgwrite ezdxf
```

### File Generation Errors
- Ensure you have write permissions to the selected directory
- Check that the filename doesn't contain invalid characters
- Verify plate dimensions are positive numbers

### Pattern Issues
- Very small spacing values may create too many elements
- Very large spacing values may create too few elements
- Adjust parameters if patterns don't appear as expected

## Contributing

Feel free to extend the application with:
- Additional pattern types
- More export formats
- Enhanced GUI features
- Pattern optimization algorithms

## License

This project is open source. Use it freely for research, education, and commercial applications. 