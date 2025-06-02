import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import os
from typing import Dict, Any, List, Tuple
import json

try:
    import svgwrite
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False

try:
    import ezdxf
    DXF_AVAILABLE = True
except ImportError:
    DXF_AVAILABLE = False

# Maximum number of elements per pattern to prevent freezing
MAX_ELEMENTS_PER_PATTERN = 10000

class PatternGenerator:
    """Base class for all pattern generators"""
    
    def __init__(self, name: str, parameters: Dict[str, Any]):
        self.name = name
        self.parameters = parameters
    
    def generate_svg_elements(self, dwg, x_offset: float, y_offset: float, 
                            section_width: float, section_height: float) -> List:
        """Generate SVG elements for this pattern"""
        raise NotImplementedError
    
    def generate_dxf_elements(self, msp, x_offset: float, y_offset: float,
                            section_width: float, section_height: float):
        """Generate DXF elements for this pattern"""
        raise NotImplementedError
    
    def _validate_element_count(self, estimated_count: int, pattern_name: str) -> bool:
        """Check if the estimated element count is reasonable"""
        if estimated_count > MAX_ELEMENTS_PER_PATTERN:
            print(f"Warning: {pattern_name} would create {estimated_count:,} elements (max: {MAX_ELEMENTS_PER_PATTERN:,})")
            print(f"Consider increasing spacing or reducing section size")
            return False
        return True


class ResolutionPatternGenerator(PatternGenerator):
    """Generator for dot array patterns"""
    
    def generate_svg_elements(self, dwg, x_offset: float, y_offset: float,
                            section_width: float, section_height: float) -> List:
        elements = []
        dot_spacing = self.parameters.get('dot_spacing', 5.0)  # µm
        dot_diameter = self.parameters.get('dot_diameter', 1.0)  # µm
        
        # Convert µm to mm
        spacing_mm = dot_spacing / 1000
        diameter_mm = dot_diameter / 1000
        
        # Calculate number of dots that fit
        cols = max(1, int(section_width / spacing_mm))
        rows = max(1, int(section_height / spacing_mm))
        
        # Validate element count
        total_dots = cols * rows
        if not self._validate_element_count(total_dots, f"Resolution pattern ({cols}x{rows} dots)"):
            # Reduce density by increasing effective spacing
            max_cols = int(math.sqrt(MAX_ELEMENTS_PER_PATTERN * section_width / section_height))
            max_rows = int(MAX_ELEMENTS_PER_PATTERN / max_cols)
            cols = min(cols, max_cols)
            rows = min(rows, max_rows)
            print(f"Reduced to {cols}x{rows} dots to prevent freezing")
        
        # Center the pattern
        actual_spacing_x = section_width / max(1, cols - 1) if cols > 1 else 0
        actual_spacing_y = section_height / max(1, rows - 1) if rows > 1 else 0
        
        start_x = x_offset + (section_width - (cols - 1) * actual_spacing_x) / 2 if cols > 1 else x_offset + section_width / 2
        start_y = y_offset + (section_height - (rows - 1) * actual_spacing_y) / 2 if rows > 1 else y_offset + section_height / 2
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * actual_spacing_x if cols > 1 else start_x
                y = start_y + row * actual_spacing_y if rows > 1 else start_y
                circle = dwg.circle(center=(x, y), r=diameter_mm/2, 
                                  fill='black', stroke='none')
                elements.append(circle)
        
        return elements
    
    def generate_dxf_elements(self, msp, x_offset: float, y_offset: float,
                            section_width: float, section_height: float):
        dot_spacing = self.parameters.get('dot_spacing', 5.0)  # µm
        dot_diameter = self.parameters.get('dot_diameter', 1.0)  # µm
        
        # Convert µm to mm
        spacing_mm = dot_spacing / 1000
        diameter_mm = dot_diameter / 1000
        
        # Calculate number of dots that fit
        cols = max(1, int(section_width / spacing_mm))
        rows = max(1, int(section_height / spacing_mm))
        
        # Validate element count
        total_dots = cols * rows
        if not self._validate_element_count(total_dots, f"Resolution pattern ({cols}x{rows} dots)"):
            # Reduce density by increasing effective spacing
            max_cols = int(math.sqrt(MAX_ELEMENTS_PER_PATTERN * section_width / section_height))
            max_rows = int(MAX_ELEMENTS_PER_PATTERN / max_cols)
            cols = min(cols, max_cols)
            rows = min(rows, max_rows)
            print(f"Reduced to {cols}x{rows} dots to prevent freezing")
        
        # Center the pattern
        actual_spacing_x = section_width / max(1, cols - 1) if cols > 1 else 0
        actual_spacing_y = section_height / max(1, rows - 1) if rows > 1 else 0
        
        start_x = x_offset + (section_width - (cols - 1) * actual_spacing_x) / 2 if cols > 1 else x_offset + section_width / 2
        start_y = y_offset + (section_height - (rows - 1) * actual_spacing_y) / 2 if rows > 1 else y_offset + section_height / 2
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * actual_spacing_x if cols > 1 else start_x
                y = start_y + row * actual_spacing_y if rows > 1 else start_y
                msp.add_circle(center=(x, y), radius=diameter_mm/2)


class DistortionPatternGenerator(PatternGenerator):
    """Generator for checkerboard/grid patterns"""
    
    def generate_svg_elements(self, dwg, x_offset: float, y_offset: float,
                            section_width: float, section_height: float) -> List:
        elements = []
        grid_size = self.parameters.get('grid_size', 1.0)  # mm
        
        cols = max(1, int(section_width / grid_size))
        rows = max(1, int(section_height / grid_size))
        
        # Validate element count (only half the squares are filled)
        filled_squares = (cols * rows) // 2
        if not self._validate_element_count(filled_squares, f"Distortion pattern ({cols}x{rows} grid)"):
            # Reduce density
            max_total = MAX_ELEMENTS_PER_PATTERN * 2  # Since only half are filled
            max_cols = int(math.sqrt(max_total * section_width / section_height))
            max_rows = int(max_total / max_cols)
            cols = min(cols, max_cols)
            rows = min(rows, max_rows)
            print(f"Reduced to {cols}x{rows} grid to prevent freezing")
        
        # Adjust grid size to fit exactly
        actual_grid_w = section_width / cols
        actual_grid_h = section_height / rows
        
        # Center the pattern
        start_x = x_offset
        start_y = y_offset
        
        for row in range(rows):
            for col in range(cols):
                # Checkerboard pattern
                if (row + col) % 2 == 0:
                    x = start_x + col * actual_grid_w
                    y = start_y + row * actual_grid_h
                    rect = dwg.rect(insert=(x, y), size=(actual_grid_w, actual_grid_h),
                                  fill='black', stroke='none')
                    elements.append(rect)
        
        return elements
    
    def generate_dxf_elements(self, msp, x_offset: float, y_offset: float,
                            section_width: float, section_height: float):
        grid_size = self.parameters.get('grid_size', 1.0)  # mm
        
        cols = max(1, int(section_width / grid_size))
        rows = max(1, int(section_height / grid_size))
        
        # Validate element count (only half the squares are filled)
        filled_squares = (cols * rows) // 2
        if not self._validate_element_count(filled_squares, f"Distortion pattern ({cols}x{rows} grid)"):
            # Reduce density
            max_total = MAX_ELEMENTS_PER_PATTERN * 2  # Since only half are filled
            max_cols = int(math.sqrt(max_total * section_width / section_height))
            max_rows = int(max_total / max_cols)
            cols = min(cols, max_cols)
            rows = min(rows, max_rows)
            print(f"Reduced to {cols}x{rows} grid to prevent freezing")
        
        # Adjust grid size to fit exactly
        actual_grid_w = section_width / cols
        actual_grid_h = section_height / rows
        
        # Center the pattern
        start_x = x_offset
        start_y = y_offset
        
        for row in range(rows):
            for col in range(cols):
                # Checkerboard pattern
                if (row + col) % 2 == 0:
                    x = start_x + col * actual_grid_w
                    y = start_y + row * actual_grid_h
                    points = [
                        (x, y),
                        (x + actual_grid_w, y),
                        (x + actual_grid_w, y + actual_grid_h),
                        (x, y + actual_grid_h),
                        (x, y)
                    ]
                    msp.add_lwpolyline(points, close=True)


class LinePairPatternGenerator(PatternGenerator):
    """Generator for line pair patterns"""
    
    def generate_svg_elements(self, dwg, x_offset: float, y_offset: float,
                            section_width: float, section_height: float) -> List:
        elements = []
        line_spacing = self.parameters.get('line_spacing', 5.0)  # µm
        line_width = self.parameters.get('line_width', 1.0)  # µm
        orientation = self.parameters.get('orientation', 'vertical')
        
        # Convert µm to mm
        spacing_mm = line_spacing / 1000
        width_mm = line_width / 1000
        
        if orientation == 'vertical':
            num_lines = max(1, int(section_width / spacing_mm))
            num_drawn_lines = (num_lines + 1) // 2  # Every other line
            
            if not self._validate_element_count(num_drawn_lines, f"Line pattern ({num_drawn_lines} vertical lines)"):
                max_lines = MAX_ELEMENTS_PER_PATTERN * 2
                num_lines = min(num_lines, max_lines)
                num_drawn_lines = (num_lines + 1) // 2
                print(f"Reduced to {num_drawn_lines} lines to prevent freezing")
            
            # Adjust spacing to fit exactly
            actual_spacing = section_width / max(1, num_lines - 1) if num_lines > 1 else section_width
            start_x = x_offset + (section_width - (num_lines - 1) * actual_spacing) / 2 if num_lines > 1 else x_offset + section_width / 2
            
            for i in range(0, num_lines, 2):  # Every other line
                x = start_x + i * actual_spacing if num_lines > 1 else start_x
                line = dwg.rect(insert=(x - width_mm/2, y_offset), 
                              size=(width_mm, section_height),
                              fill='black', stroke='none')
                elements.append(line)
        else:  # horizontal
            num_lines = max(1, int(section_height / spacing_mm))
            num_drawn_lines = (num_lines + 1) // 2  # Every other line
            
            if not self._validate_element_count(num_drawn_lines, f"Line pattern ({num_drawn_lines} horizontal lines)"):
                max_lines = MAX_ELEMENTS_PER_PATTERN * 2
                num_lines = min(num_lines, max_lines)
                num_drawn_lines = (num_lines + 1) // 2
                print(f"Reduced to {num_drawn_lines} lines to prevent freezing")
            
            # Adjust spacing to fit exactly
            actual_spacing = section_height / max(1, num_lines - 1) if num_lines > 1 else section_height
            start_y = y_offset + (section_height - (num_lines - 1) * actual_spacing) / 2 if num_lines > 1 else y_offset + section_height / 2
            
            for i in range(0, num_lines, 2):  # Every other line
                y = start_y + i * actual_spacing if num_lines > 1 else start_y
                line = dwg.rect(insert=(x_offset, y - width_mm/2), 
                              size=(section_width, width_mm),
                              fill='black', stroke='none')
                elements.append(line)
        
        return elements
    
    def generate_dxf_elements(self, msp, x_offset: float, y_offset: float,
                            section_width: float, section_height: float):
        line_spacing = self.parameters.get('line_spacing', 5.0)  # µm
        line_width = self.parameters.get('line_width', 1.0)  # µm
        orientation = self.parameters.get('orientation', 'vertical')
        
        # Convert µm to mm
        spacing_mm = line_spacing / 1000
        width_mm = line_width / 1000
        
        if orientation == 'vertical':
            num_lines = max(1, int(section_width / spacing_mm))
            num_drawn_lines = (num_lines + 1) // 2  # Every other line
            
            if not self._validate_element_count(num_drawn_lines, f"Line pattern ({num_drawn_lines} vertical lines)"):
                max_lines = MAX_ELEMENTS_PER_PATTERN * 2
                num_lines = min(num_lines, max_lines)
                num_drawn_lines = (num_lines + 1) // 2
                print(f"Reduced to {num_drawn_lines} lines to prevent freezing")
            
            # Adjust spacing to fit exactly
            actual_spacing = section_width / max(1, num_lines - 1) if num_lines > 1 else section_width
            start_x = x_offset + (section_width - (num_lines - 1) * actual_spacing) / 2 if num_lines > 1 else x_offset + section_width / 2
            
            for i in range(0, num_lines, 2):  # Every other line
                x = start_x + i * actual_spacing if num_lines > 1 else start_x
                points = [
                    (x - width_mm/2, y_offset),
                    (x + width_mm/2, y_offset),
                    (x + width_mm/2, y_offset + section_height),
                    (x - width_mm/2, y_offset + section_height),
                    (x - width_mm/2, y_offset)
                ]
                msp.add_lwpolyline(points, close=True)
        else:  # horizontal
            num_lines = max(1, int(section_height / spacing_mm))
            num_drawn_lines = (num_lines + 1) // 2  # Every other line
            
            if not self._validate_element_count(num_drawn_lines, f"Line pattern ({num_drawn_lines} horizontal lines)"):
                max_lines = MAX_ELEMENTS_PER_PATTERN * 2
                num_lines = min(num_lines, max_lines)
                num_drawn_lines = (num_lines + 1) // 2
                print(f"Reduced to {num_drawn_lines} lines to prevent freezing")
            
            # Adjust spacing to fit exactly
            actual_spacing = section_height / max(1, num_lines - 1) if num_lines > 1 else section_height
            start_y = y_offset + (section_height - (num_lines - 1) * actual_spacing) / 2 if num_lines > 1 else y_offset + section_height / 2
            
            for i in range(0, num_lines, 2):  # Every other line
                y = start_y + i * actual_spacing if num_lines > 1 else start_y
                points = [
                    (x_offset, y - width_mm/2),
                    (x_offset + section_width, y - width_mm/2),
                    (x_offset + section_width, y + width_mm/2),
                    (x_offset, y + width_mm/2),
                    (x_offset, y - width_mm/2)
                ]
                msp.add_lwpolyline(points, close=True)


class AlignmentPatternGenerator(PatternGenerator):
    """Generator for alignment markers and scale bars"""
    
    def generate_svg_elements(self, dwg, x_offset: float, y_offset: float,
                            section_width: float, section_height: float) -> List:
        elements = []
        marker_type = self.parameters.get('marker_type', 'crosshair')
        marker_size = self.parameters.get('marker_size', 2.0)  # mm
        
        center_x = x_offset + section_width / 2
        center_y = y_offset + section_height / 2
        
        if marker_type == 'crosshair':
            # Horizontal line
            h_line = dwg.line(start=(center_x - marker_size/2, center_y),
                            end=(center_x + marker_size/2, center_y),
                            stroke='black', stroke_width=0.1)
            elements.append(h_line)
            
            # Vertical line
            v_line = dwg.line(start=(center_x, center_y - marker_size/2),
                            end=(center_x, center_y + marker_size/2),
                            stroke='black', stroke_width=0.1)
            elements.append(v_line)
            
        elif marker_type == 'fiducial':
            # Outer circle
            outer_circle = dwg.circle(center=(center_x, center_y), 
                                    r=marker_size/2,
                                    fill='none', stroke='black', stroke_width=0.1)
            elements.append(outer_circle)
            
            # Inner dot
            inner_dot = dwg.circle(center=(center_x, center_y), 
                                 r=marker_size/8,
                                 fill='black', stroke='none')
            elements.append(inner_dot)
            
        elif marker_type == 'scale_bar':
            # Scale bar with graduations
            bar_length = marker_size
            num_graduations = 10
            grad_spacing = bar_length / num_graduations
            
            # Main bar
            main_bar = dwg.line(start=(center_x - bar_length/2, center_y),
                              end=(center_x + bar_length/2, center_y),
                              stroke='black', stroke_width=0.1)
            elements.append(main_bar)
            
            # Graduations
            for i in range(num_graduations + 1):
                x = center_x - bar_length/2 + i * grad_spacing
                grad_height = 0.2 if i % 5 == 0 else 0.1
                grad = dwg.line(start=(x, center_y - grad_height/2),
                              end=(x, center_y + grad_height/2),
                              stroke='black', stroke_width=0.05)
                elements.append(grad)
        
        return elements
    
    def generate_dxf_elements(self, msp, x_offset: float, y_offset: float,
                            section_width: float, section_height: float):
        marker_type = self.parameters.get('marker_type', 'crosshair')
        marker_size = self.parameters.get('marker_size', 2.0)  # mm
        
        center_x = x_offset + section_width / 2
        center_y = y_offset + section_height / 2
        
        if marker_type == 'crosshair':
            # Horizontal line
            msp.add_line(start=(center_x - marker_size/2, center_y),
                        end=(center_x + marker_size/2, center_y))
            
            # Vertical line
            msp.add_line(start=(center_x, center_y - marker_size/2),
                        end=(center_x, center_y + marker_size/2))
            
        elif marker_type == 'fiducial':
            # Outer circle
            msp.add_circle(center=(center_x, center_y), radius=marker_size/2)
            
            # Inner dot (filled circle)
            msp.add_circle(center=(center_x, center_y), radius=marker_size/8)
            
        elif marker_type == 'scale_bar':
            # Scale bar with graduations
            bar_length = marker_size
            num_graduations = 10
            grad_spacing = bar_length / num_graduations
            
            # Main bar
            msp.add_line(start=(center_x - bar_length/2, center_y),
                        end=(center_x + bar_length/2, center_y))
            
            # Graduations
            for i in range(num_graduations + 1):
                x = center_x - bar_length/2 + i * grad_spacing
                grad_height = 0.2 if i % 5 == 0 else 0.1
                msp.add_line(start=(x, center_y - grad_height/2),
                           end=(x, center_y + grad_height/2))


class CalibrationPlateDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Calibration Plate Designer")
        self.root.geometry("800x900")
        
        # Default values
        self.plate_width = tk.DoubleVar(value=101.6)  # 4 inches in mm
        self.plate_height = tk.DoubleVar(value=101.6)  # 4 inches in mm
        self.margin = tk.DoubleVar(value=10.0)  # mm
        
        # Pattern generators
        self.pattern_generators = {
            'Resolution Patterns': ResolutionPatternGenerator,
            'Distortion Patterns': DistortionPatternGenerator,
            'Line Pair Patterns': LinePairPatternGenerator,
            'Alignment Markers': AlignmentPatternGenerator
        }
        
        # Section configurations
        self.section_configs = [
            {'pattern_type': tk.StringVar(value='Resolution Patterns'), 'params': {}},
            {'pattern_type': tk.StringVar(value='Distortion Patterns'), 'params': {}},
            {'pattern_type': tk.StringVar(value='Line Pair Patterns'), 'params': {}},
            {'pattern_type': tk.StringVar(value='Alignment Markers'), 'params': {}}
        ]
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Plate dimensions
        dimensions_frame = ttk.LabelFrame(main_frame, text="Plate Dimensions", padding="10")
        dimensions_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(dimensions_frame, text="Width (mm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(dimensions_frame, textvariable=self.plate_width, width=10).grid(row=0, column=1, padx=(5, 20))
        
        ttk.Label(dimensions_frame, text="Height (mm):").grid(row=0, column=2, sticky=tk.W)
        ttk.Entry(dimensions_frame, textvariable=self.plate_height, width=10).grid(row=0, column=3, padx=(5, 20))
        
        ttk.Label(dimensions_frame, text="Margin (mm):").grid(row=0, column=4, sticky=tk.W)
        ttk.Entry(dimensions_frame, textvariable=self.margin, width=10).grid(row=0, column=5, padx=(5, 0))
        
        # Section configurations
        self.create_section_widgets(main_frame)
        
        # Generate button
        generate_frame = ttk.Frame(main_frame)
        generate_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(generate_frame, text="Generate SVG", 
                  command=self.generate_svg).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(generate_frame, text="Generate DXF", 
                  command=self.generate_dxf).grid(row=0, column=1)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
    
    def create_section_widgets(self, parent):
        sections_frame = ttk.LabelFrame(parent, text="Section Configurations", padding="10")
        sections_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        for i in range(4):
            section_frame = ttk.LabelFrame(sections_frame, text=f"Section {i+1}", padding="5")
            section_frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=5, pady=5)
            
            # Pattern type dropdown
            ttk.Label(section_frame, text="Pattern Type:").grid(row=0, column=0, sticky=tk.W)
            pattern_combo = ttk.Combobox(section_frame, 
                                       textvariable=self.section_configs[i]['pattern_type'],
                                       values=list(self.pattern_generators.keys()),
                                       state="readonly", width=20)
            pattern_combo.grid(row=0, column=1, padx=(5, 0), pady=(0, 5))
            pattern_combo.bind('<<ComboboxSelected>>', lambda e, idx=i: self.update_parameters(idx))
            
            # Parameters frame
            params_frame = ttk.Frame(section_frame)
            params_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
            
            self.section_configs[i]['params_frame'] = params_frame
            self.update_parameters(i)
    
    def update_parameters(self, section_idx):
        # Clear existing parameter widgets
        params_frame = self.section_configs[section_idx]['params_frame']
        for widget in params_frame.winfo_children():
            widget.destroy()
        
        pattern_type = self.section_configs[section_idx]['pattern_type'].get()
        self.section_configs[section_idx]['params'] = {}
        
        if pattern_type == 'Resolution Patterns':
            # Dot spacing parameter
            ttk.Label(params_frame, text="Dot Spacing (µm):").grid(row=0, column=0, sticky=tk.W)
            dot_spacing_var = tk.DoubleVar(value=5.0)
            ttk.Entry(params_frame, textvariable=dot_spacing_var, width=10).grid(row=0, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['dot_spacing'] = dot_spacing_var
            
            # Dot diameter parameter
            ttk.Label(params_frame, text="Dot Diameter (µm):").grid(row=1, column=0, sticky=tk.W)
            dot_diameter_var = tk.DoubleVar(value=1.0)
            ttk.Entry(params_frame, textvariable=dot_diameter_var, width=10).grid(row=1, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['dot_diameter'] = dot_diameter_var
            
        elif pattern_type == 'Distortion Patterns':
            # Grid size parameter
            ttk.Label(params_frame, text="Grid Size (mm):").grid(row=0, column=0, sticky=tk.W)
            grid_size_var = tk.DoubleVar(value=1.0)
            ttk.Entry(params_frame, textvariable=grid_size_var, width=10).grid(row=0, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['grid_size'] = grid_size_var
            
        elif pattern_type == 'Line Pair Patterns':
            # Line spacing parameter
            ttk.Label(params_frame, text="Line Spacing (µm):").grid(row=0, column=0, sticky=tk.W)
            line_spacing_var = tk.DoubleVar(value=5.0)
            ttk.Entry(params_frame, textvariable=line_spacing_var, width=10).grid(row=0, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['line_spacing'] = line_spacing_var
            
            # Line width parameter
            ttk.Label(params_frame, text="Line Width (µm):").grid(row=1, column=0, sticky=tk.W)
            line_width_var = tk.DoubleVar(value=1.0)
            ttk.Entry(params_frame, textvariable=line_width_var, width=10).grid(row=1, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['line_width'] = line_width_var
            
            # Orientation parameter
            ttk.Label(params_frame, text="Orientation:").grid(row=2, column=0, sticky=tk.W)
            orientation_var = tk.StringVar(value='vertical')
            orientation_combo = ttk.Combobox(params_frame, textvariable=orientation_var,
                                           values=['vertical', 'horizontal'], state="readonly", width=8)
            orientation_combo.grid(row=2, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['orientation'] = orientation_var
            
        elif pattern_type == 'Alignment Markers':
            # Marker type parameter
            ttk.Label(params_frame, text="Marker Type:").grid(row=0, column=0, sticky=tk.W)
            marker_type_var = tk.StringVar(value='crosshair')
            marker_combo = ttk.Combobox(params_frame, textvariable=marker_type_var,
                                      values=['crosshair', 'fiducial', 'scale_bar'], 
                                      state="readonly", width=10)
            marker_combo.grid(row=0, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['marker_type'] = marker_type_var
            
            # Marker size parameter
            ttk.Label(params_frame, text="Marker Size (mm):").grid(row=1, column=0, sticky=tk.W)
            marker_size_var = tk.DoubleVar(value=2.0)
            ttk.Entry(params_frame, textvariable=marker_size_var, width=10).grid(row=1, column=1, padx=(5, 0))
            self.section_configs[section_idx]['params']['marker_size'] = marker_size_var
    
    def get_section_parameters(self, section_idx):
        """Get the parameter values for a section"""
        params = {}
        for key, var in self.section_configs[section_idx]['params'].items():
            if hasattr(var, 'get'):
                params[key] = var.get()
        return params
    
    def calculate_section_dimensions(self):
        """Calculate the dimensions and positions of the four sections"""
        plate_w = self.plate_width.get()
        plate_h = self.plate_height.get()
        margin = self.margin.get()
        
        # Available space after margins
        available_w = plate_w - 2 * margin
        available_h = plate_h - 2 * margin
        
        # Each section is half the available space
        section_w = available_w / 2
        section_h = available_h / 2
        
        # Section positions (top-left, top-right, bottom-left, bottom-right)
        sections = [
            (margin, margin),  # Top-left
            (margin + section_w, margin),  # Top-right
            (margin, margin + section_h),  # Bottom-left
            (margin + section_w, margin + section_h)  # Bottom-right
        ]
        
        return sections, section_w, section_h
    
    def generate_svg(self):
        if not SVG_AVAILABLE:
            messagebox.showerror("Error", "svgwrite library not available. Please install it with: pip install svgwrite")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".svg",
                filetypes=[("SVG files", "*.svg"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Update status to show progress
            self.status_label.config(text="Generating SVG file...")
            self.root.update()
            
            plate_w = self.plate_width.get()
            plate_h = self.plate_height.get()
            
            # Validate plate dimensions
            if plate_w <= 0 or plate_h <= 0:
                messagebox.showerror("Error", "Plate dimensions must be positive numbers")
                self.status_label.config(text="Ready")
                return
            
            # Create SVG drawing
            dwg = svgwrite.Drawing(filename, size=(f'{plate_w}mm', f'{plate_h}mm'),
                                 viewBox=f'0 0 {plate_w} {plate_h}')
            
            # Add plate outline
            plate_outline = dwg.rect(insert=(0, 0), size=(plate_w, plate_h),
                                   fill='none', stroke='black', stroke_width=0.1)
            dwg.add(plate_outline)
            
            # Get section dimensions and positions
            sections, section_w, section_h = self.calculate_section_dimensions()
            
            # Generate patterns for each section
            total_elements = 0
            for i, (x_offset, y_offset) in enumerate(sections):
                self.status_label.config(text=f"Generating SVG - Section {i+1}/4...")
                self.root.update()
                
                pattern_type = self.section_configs[i]['pattern_type'].get()
                params = self.get_section_parameters(i)
                
                # Create pattern generator
                generator_class = self.pattern_generators[pattern_type]
                generator = generator_class(pattern_type, params)
                
                # Generate SVG elements
                elements = generator.generate_svg_elements(dwg, x_offset, y_offset, 
                                                         section_w, section_h)
                
                # Add elements to drawing
                for element in elements:
                    dwg.add(element)
                
                total_elements += len(elements)
                
                # Add section outline for debugging
                section_outline = dwg.rect(insert=(x_offset, y_offset), 
                                         size=(section_w, section_h),
                                         fill='none', stroke='gray', 
                                         stroke_width=0.05, stroke_dasharray='1,1')
                dwg.add(section_outline)
            
            # Save the file
            self.status_label.config(text="Saving SVG file...")
            self.root.update()
            
            dwg.save()
            self.status_label.config(text=f"SVG saved: {filename} ({total_elements:,} elements)")
            messagebox.showinfo("Success", f"SVG file saved successfully:\n{filename}\n\nTotal elements: {total_elements:,}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate SVG: {str(e)}")
            self.status_label.config(text="Error generating SVG")
    
    def generate_dxf(self):
        if not DXF_AVAILABLE:
            messagebox.showerror("Error", "ezdxf library not available. Please install it with: pip install ezdxf")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Update status to show progress
            self.status_label.config(text="Generating DXF file...")
            self.root.update()
            
            plate_w = self.plate_width.get()
            plate_h = self.plate_height.get()
            
            # Validate plate dimensions
            if plate_w <= 0 or plate_h <= 0:
                messagebox.showerror("Error", "Plate dimensions must be positive numbers")
                self.status_label.config(text="Ready")
                return
            
            # Create DXF document
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
            
            # Get section dimensions and positions
            sections, section_w, section_h = self.calculate_section_dimensions()
            
            # Generate patterns for each section
            for i, (x_offset, y_offset) in enumerate(sections):
                self.status_label.config(text=f"Generating DXF - Section {i+1}/4...")
                self.root.update()
                
                pattern_type = self.section_configs[i]['pattern_type'].get()
                params = self.get_section_parameters(i)
                
                # Create pattern generator
                generator_class = self.pattern_generators[pattern_type]
                generator = generator_class(pattern_type, params)
                
                # Generate DXF elements
                generator.generate_dxf_elements(msp, x_offset, y_offset, 
                                              section_w, section_h)
                
                # Add section outline for debugging
                section_outline = [
                    (x_offset, y_offset),
                    (x_offset + section_w, y_offset),
                    (x_offset + section_w, y_offset + section_h),
                    (x_offset, y_offset + section_h),
                    (x_offset, y_offset)
                ]
                msp.add_lwpolyline(section_outline, close=True)
            
            # Save the file
            self.status_label.config(text="Saving DXF file...")
            self.root.update()
            
            doc.saveas(filename)
            
            # Count entities for feedback
            entity_count = len(list(msp))
            self.status_label.config(text=f"DXF saved: {filename} ({entity_count:,} entities)")
            messagebox.showinfo("Success", f"DXF file saved successfully:\n{filename}\n\nTotal entities: {entity_count:,}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate DXF: {str(e)}")
            self.status_label.config(text="Error generating DXF")


def main():
    root = tk.Tk()
    app = CalibrationPlateDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main() 