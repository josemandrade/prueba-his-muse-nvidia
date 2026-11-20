#!/usr/bin/env python3
"""
Sequence Diagram Renderer - Converts Mermaid sequence diagrams to SVG.
Uses mermaid-cli (mmdc) if available, otherwise provides validation only.
"""

import subprocess
import sys
import os
import re
from pathlib import Path

def extract_mermaid_diagrams(markdown_file):
    """Extract mermaid diagrams from a markdown file."""
    with open(markdown_file, 'r') as f:
        content = f.read()
    
    # Find all mermaid code blocks
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    diagrams = []
    for i, match in enumerate(matches):
        # Extract the flow name from the preceding header
        lines = content[:content.find(match)].split('\n')
        flow_name = f"sequence-{i}"
        for line in reversed(lines):
            if line.startswith('## Flow ') or line.startswith('### Flow '):
                flow_name = line.replace('#', '').strip().lower().replace(' ', '-').replace('flow-', 'sequence-')
                break
        diagrams.append((flow_name, match.strip()))
    
    return diagrams

def render_mermaid_to_svg(mermaid_code, output_path):
    """Render mermaid code to SVG using mmdc (mermaid-cli)."""
    try:
        # Write mermaid code to temp file
        temp_mmd = output_path.with_suffix('.mmd')
        with open(temp_mmd, 'w') as f:
            f.write(mermaid_code)
        
        # Run mmdc
        result = subprocess.run(
            ['mmdc', '-i', str(temp_mmd), '-o', str(output_path), '--backgroundColor', 'white'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Clean up temp file
        if temp_mmd.exists():
            temp_mmd.unlink()
        
        if result.returncode == 0:
            print(f"  ✓ Rendered: {output_path}")
            return True
        else:
            print(f"  ✗ Failed to render {output_path}: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print(f"  ⚠ mmdc (mermaid-cli) not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout rendering {output_path}")
        return False
    except Exception as e:
        print(f"  ✗ Error rendering {output_path}: {e}")
        return False

def validate_mermaid_syntax(mermaid_code):
    """Basic validation of mermaid sequence diagram syntax."""
    errors = []
    lines = mermaid_code.split('\n')
    
    # Check for sequenceDiagram keyword
    if not any('sequenceDiagram' in line for line in lines):
        errors.append("Missing 'sequenceDiagram' declaration")
    
    # Check for participant declarations
    participants = []
    for line in lines:
        line = line.strip()
        if line.startswith('actor ') or line.startswith('participant ') or line.startswith('actor ') or line.startswith('participant '):
            parts = line.split()
            if len(parts) >= 2:
                participants.append(parts[1].split('as')[0].strip())
    
    if not participants:
        errors.append("No participants declared")
    
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python render_sequence.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    markdown_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else markdown_file.parent
    
    if not markdown_file.exists():
        print(f"File not found: {markdown_file}")
        sys.exit(1)
    
    print(f"Processing: {markdown_file}")
    print(f"Output directory: {output_dir}")
    
    diagrams = extract_mermaid_diagrams(markdown_file)
    
    if not diagrams:
        print("No mermaid diagrams found.")
        sys.exit(0)
    
    print(f"Found {len(diagrams)} diagram(s):")
    for name, _ in diagrams:
        print(f"  - {name}")
    
    success_count = 0
    for name, code in diagrams:
        print(f"\nRendering: {name}")
        
        # Validate syntax
        errors = validate_mermaid_syntax(code)
        if errors:
            print(f"  ⚠ Validation warnings: {errors}")
        
        # Render to SVG
        svg_path = output_dir / f"04-{name}.svg"
        if render_mermaid_to_svg(code, svg_path):
            success_count += 1
    
    print(f"\nSuccessfully rendered {success_count}/{len(diagrams)} diagrams.")
    
    if success_count == 0:
        print("Note: Install mermaid-cli for SVG rendering: npm install -g @mermaid-js/mermaid-cli")
        sys.exit(1)

if __name__ == '__main__':
    main()