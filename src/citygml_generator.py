from pathlib import Path
from typing import Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

class CityGMLGenerator:
    """Generator class for CityGML format"""
    
    def __init__(self):
        self.gml_ns = "http://www.opengis.net/gml"
        self.citygml_ns = "http://www.opengis.net/citygml/2.0"
        self.ns = {
            "gml": self.gml_ns,
            "core": self.citygml_ns,
            "bldg": f"{self.citygml_ns}/building"
        }
        
    def generate(self, model_data: Dict[str, Any], output_path: Path) -> None:
        """
        Generate CityGML file from model data
        
        Args:
            model_data: Dictionary containing parsed 3D model data
            output_path: Path where the CityGML file will be saved
        """
        try:
            # Create root element
            root = ET.Element(f"{{{self.citygml_ns}}}CityModel")
            for prefix, uri in self.ns.items():
                root.set(f"xmlns:{prefix}", uri)
            
            # Add city object member
            city_object_member = ET.SubElement(root, f"{{{self.citygml_ns}}}cityObjectMember")
            building = self._create_building(model_data)
            city_object_member.append(building)
            
            # Write to file
            xml_str = ET.tostring(root, encoding='unicode')
            pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
                
        except Exception as e:
            raise Exception(f"Failed to generate CityGML: {str(e)}")
    
    def _create_building(self, model_data: Dict[str, Any]) -> ET.Element:
        """Create Building element with geometry"""
        building = ET.Element(f"{{{self.ns['bldg']}}}Building")
        
        # Add geometry
        lod2_solid = ET.SubElement(building, f"{{{self.ns['bldg']}}}lod2Solid")
        solid = self._create_solid(model_data)
        lod2_solid.append(solid)
        
        # Add attributes
        if 'properties' in model_data:
            self._add_attributes(building, model_data['properties'])
        
        return building
    
    def _create_solid(self, model_data: Dict[str, Any]) -> ET.Element:
        """Create GML Solid element"""
        solid = ET.Element(f"{{{self.ns['gml']}}}Solid")
        
        # Add exterior shell
        exterior = ET.SubElement(solid, f"{{{self.ns['gml']}}}exterior")
        composite_surface = ET.SubElement(exterior, f"{{{self.ns['gml']}}}CompositeSurface")
        
        # Add surfaces
        if 'faces' in model_data:
            for face in model_data['faces']:
                surface_member = self._create_surface_member(face, model_data['vertices'])
                composite_surface.append(surface_member)
        
        return solid
    
    def _create_surface_member(self, face: list, vertices: list) -> ET.Element:
        """Create surface member for a face"""
        surface_member = ET.Element(f"{{{self.ns['gml']}}}surfaceMember")
        polygon = ET.SubElement(surface_member, f"{{{self.ns['gml']}}}Polygon")
        
        # Add exterior ring
        exterior = ET.SubElement(polygon, f"{{{self.ns['gml']}}}exterior")
        linear_ring = ET.SubElement(exterior, f"{{{self.ns['gml']}}}LinearRing")
        
        # Add coordinates
        pos_list = ET.SubElement(linear_ring, f"{{{self.ns['gml']}}}posList")
        coordinates = []
        for vertex_idx in face:
            vertex = vertices[vertex_idx]
            coordinates.extend([str(vertex[0]), str(vertex[1]), str(vertex[2])])
        pos_list.text = " ".join(coordinates)
        
        return surface_member
    
    def _add_attributes(self, building: ET.Element, properties: dict) -> None:
        """Add attributes to building element"""
        for key, value in properties.items():
            attribute = ET.SubElement(building, f"{{{self.ns['bldg']}}}{key}")
            attribute.text = str(value)
