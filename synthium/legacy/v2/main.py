#!/usr/bin/env python3
"""
Synthium Omega v2.0: Unified 8D Reality Compiler
"""

import sys
import math
import random
from .transducer import Transducer
from .science import HolisticScience
from .recorder import Recorder
from .reality_field import FieldManager
from .vectors import RealityVector, SynthiumVector


def print_banner():
    banner = r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                 SYNTHIUM OMEGA v2.0                       ║
    ║            UNIFIED 8D REALITY COMPILER                    ║
    ║        "Mapping the Geometry of Existence"                ║
    ╚══════════════════════════════════════════════════════════╝
    
    Dimensions: 3D Space (x,y,z) + 5D Qualities (v,R,r,C,S)
    """
    print(banner)


def main():
    print_banner()
    
    # Initialize components
    tool = Transducer()
    lab = HolisticScience()
    scribe = Recorder()
    field_manager = FieldManager()
    
    while True:
        print("\n" + "="*60)
        print("📋 8D REALITY MENU")
        print("="*60)
        print("1. 🎯 Quantify phenomenon at specific location (8D)")
        print("2. 📍 Map quality field across space")
        print("3. 🔍 Search quality lexicon (5D)")
        print("4. 🗺️  Explore reality fields (8D)")
        print("5. 📊 System statistics")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            quantify_8d_mode(tool, lab, scribe)
        elif choice == "2":
            map_field_mode(tool, lab, scribe)
        elif choice == "3":
            search_lexicon_mode(scribe)
        elif choice == "4":
            explore_fields_mode(field_manager, lab)
        elif choice == "5":
            show_statistics(scribe, field_manager)
        elif choice == "6":
            print("\n👋 Preserving reality mappings... Goodbye!\n")
            sys.exit(0)
        else:
            print("Invalid choice.")


def quantify_8d_mode(tool, lab, scribe):
    """Quantify a phenomenon at a specific location."""
    print("\n" + "="*60)
    print("🎯 8D REALITY QUANTIFICATION")
    print("="*60)
    
    name = input("\nPhenomenon name: ").strip()
    desc = input(f"Describe '{name}': ").strip()
    
    # Get location
    print("\n📍 Enter location (meters from origin):")
    try:
        x = float(input("  x (east-west): ") or "0.0")
        y = float(input("  y (north-south): ") or "0.0")
        z = float(input("  z (up-down): ") or "0.0")
    except ValueError:
        print("Invalid coordinates. Using origin.")
        x, y, z = 0.0, 0.0, 0.0
    
    try:
        # Create 8D reality vector
        reality_vector = tool.quantify(desc, location=(x, y, z))
        print(f"\n[8D REALITY VECTOR]:")
        print(f"  {reality_vector}")
        
        # Analyze
        analysis = lab.analyze_reality_vector(reality_vector)
        print("\n[8D ANALYSIS]:")
        for key, value in analysis.items():
            if key != "violations" or value:  # Only show violations if present
                print(f"  • {key}: {value}")
        
        # Save options
        print("\n💾 Save options:")
        print("  1. Save as quality definition (5D to lexicon)")
        print("  2. Save as reality field point (8D)")
        print("  3. Both")
        print("  4. Don't save")
        
        save_choice = input("\nSelect (1-4): ").strip()
        
        if save_choice in ["1", "3"]:
            # Extract 5D quality
            quality_vector = SynthiumVector(
                reality_vector.v, reality_vector.R, reality_vector.r,
                reality_vector.C, reality_vector.S
            )
            formulas = analysis.get("derived_formulas", ["Complex = f(v,R,r,C,S)"])
            scribe.save_quality(name, quality_vector, formulas[0])
        
        if save_choice in ["2", "3"]:
            # Save as field point
            field_name = input("Field name (or press Enter for default): ").strip()
            if not field_name:
                field_name = f"{name}_field"
            
            scribe.save_reality_field(field_name, [reality_vector])
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def map_field_mode(tool, lab, scribe):
    """Map a quality field across multiple spatial points."""
    print("\n" + "="*60)
    print("📍 QUALITY FIELD MAPPING")
    print("="*60)
    
    field_name = input("\nField name: ").strip()
    quality_desc = input("Quality to map: ").strip()
    
    print("\n📐 Define mapping area:")
    try:
        center_x = float(input("  Center x: ") or "0.0")
        center_y = float(input("  Center y: ") or "0.0")
        center_z = float(input("  Center z: ") or "0.0")
        radius = float(input("  Radius (m): ") or "10.0")
        points = int(input("  Number of sample points: ") or "9")
    except ValueError:
        print("Invalid input. Using defaults.")
        center_x, center_y, center_z, radius, points = 0.0, 0.0, 0.0, 10.0, 9
    
    # Generate sample points
    vectors = []
    for i in range(points):
        # Generate random point within sphere
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(0, radius)
        
        x = center_x + r * math.sin(phi) * math.cos(theta)
        y = center_y + r * math.sin(phi) * math.sin(theta)
        z = center_z + r * math.cos(phi)
        
        # Create vector at this location
        vector = tool.quantify(quality_desc, location=(x, y, z))
        vectors.append(vector)
        
        print(f"  Point {i+1}: ({x:.1f}, {y:.1f}, {z:.1f}) → v={vector.v:.2f}, R={vector.R:.2f}")
    
    # Analyze field
    print("\n📊 FIELD ANALYSIS:")
    field_analysis = lab.analyze_spatial_quality_field(vectors)
    for key, value in field_analysis.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    # Save field
    if input("\nSave this field? (y/n): ").lower() == 'y':
        scribe.save_reality_field(field_name, vectors)
        print(f"✅ Field '{field_name}' saved with {len(vectors)} points.")


def search_lexicon_mode(scribe):
    """Search the quality lexicon."""
    print("\n" + "="*60)
    print("🔍 QUALITY LEXICON SEARCH")
    print("="*60)
    
    term = input("\nSearch term: ").strip()
    entry = scribe.find_quality(term)
    
    if entry:
        print(f"\n✅ FOUND: {entry['term']}")
        print(f"   Formula: {entry.get('formula', 'N/A')}")
        print(f"   Category: {entry.get('category', 'N/A')}")
        print(f"   Vector: v={entry['vector']['v']:.3f}, R={entry['vector']['R']:.3f}, "
              f"r={entry['vector']['r']:.3f}, C={entry['vector']['C']:.3f}, S={entry['vector']['S']:.3f}")
        print(f"   Discovered: {entry.get('timestamp', 'Unknown')}")
    else:
        print(f"\n❌ '{term}' not found in lexicon.")


def explore_fields_mode(field_manager, lab):
    """Explore existing reality fields."""
    print("\n" + "="*60)
    print("🗺️  REALITY FIELD EXPLORER")
    print("="*60)
    
    fields = field_manager.list_fields()
    if not fields:
        print("No fields found. Create one first.")
        return
    
    print(f"\nAvailable fields ({len(fields)}):")
    for i, field_name in enumerate(fields, 1):
        print(f"  {i}. {field_name}")
    
    try:
        choice = int(input("\nSelect field (number): ").strip())
        if 1 <= choice <= len(fields):
            field_name = fields[choice-1]
            field = field_manager.get_field(field_name)
            
            if field:
                print(f"\n📋 FIELD: {field.name}")
                print(f"   Vectors: {len(field.vectors)}")
                print(f"   Bounds: {field.metadata['bounds']}")
                print(f"   Quality types: {field.metadata['quality_types']}")
                
                # Analyze field
                analysis = lab.analyze_spatial_quality_field(field.vectors)
                print("\n📊 FIELD ANALYSIS:")
                for key, value in analysis.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    {k}: {v}")
                    else:
                        print(f"  {key}: {value}")
        else:
            print("Invalid selection.")
    except (ValueError, IndexError):
        print("Invalid input.")


def show_statistics(scribe, field_manager):
    """Display system statistics."""
    print("\n" + "="*60)
    print("📊 SYNTHIUM OMEGA v2.0 STATISTICS")
    print("="*60)
    
    # Quality lexicon stats
    qual_stats = scribe.get_quality_statistics()
    print(f"\n📚 QUALITY LEXICON:")
    print(f"   Total qualities: {qual_stats['total_qualities']}")
    print(f"   By category: {qual_stats['by_category']}")
    print(f"   Last modified: {qual_stats['last_modified']}")
    
    # Reality field stats
    field_stats = scribe.get_field_statistics()
    print(f"\n🗺️  REALITY FIELDS:")
    print(f"   Total fields: {field_stats['total_fields']}")
    print(f"   Total vectors: {field_stats['total_vectors']}")
    if field_stats['total_fields'] > 0:
        print(f"   Avg vectors/field: {field_stats['average_vectors_per_field']:.1f}")
    
    # Field manager stats
    fm_stats = field_manager.get_field_statistics()
    print(f"\n🌐 FIELD MANAGER:")
    print(f"   Total fields: {fm_stats['total_fields']}")
    print(f"   Total vectors: {fm_stats['total_vectors']}")
    print(f"   Spatial coverage: {fm_stats['spatial_coverage']}")
    print(f"   Field types: {fm_stats['field_types']}")


if __name__ == "__main__":
    main()
