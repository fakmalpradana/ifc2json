from pathlib import Path
import json
from typing import Dict, Any

class CityJSONGenerator:
    """Generator class for CityJSON format"""
    
    def __init__(self):
        self.version = "1.0"
        
    def generate(self, model_data: Dict[str, Any], output_path: Path) -> None:
        """
        Generate CityJSON file from model data
        
        Args:
            model_data: Dictionary containing parsed 3D model data
            output_path: Path where the CityJSON file will be saved
        """
        try:
            cityjson_data = {
                "type": "CityJSON",
                "version": self.version,
                "metadata": {
                    "referenceSystem": "urn:ogc:def:crs:EPSG::7415"
                },
                "vertices": self._convert_vertices(model_data['vertices']),
                "CityObjects": self._create_city_objects(model_data)
            }
            
            # Add transform object for coordinate compression
            cityjson_data["transform"] = {
                "scale": [0.001, 0.001, 0.001],
                "translate": [0.0, 0.0, 0.0]
            }
            
            # Write to file
            with open(output_path, 'w') as f:
                json.dump(cityjson_data, f, indent=2)
                
        except Exception as e:
            raise Exception(f"Failed to generate CityJSON: {str(e)}")
    
    def _convert_vertices(self, vertices: list) -> list:
        """Convert vertices to CityJSON format"""
        return [[v[0], v[1], v[2]] for v in vertices]
    
    def _create_city_objects(self, model_data: Dict[str, Any]) -> dict:
        """Create CityObjects section of CityJSON"""
        city_objects = {
            "Building_1": {
                "type": "Building",
                "geometry": [{
                    "type": "Solid",
                    "lod": 2,
                    "boundaries": self._create_boundaries(model_data),
                    "semantics": self._create_semantics(model_data)
                }],
                "attributes": model_data.get('properties', {})
            }
        }
        return city_objects
    
    def _create_boundaries(self, model_data: Dict[str, Any]) -> list:
        """Create boundaries array for CityJSON geometry"""
        boundaries = []
        if 'faces' in model_data:
            # Convert faces to CityJSON boundary format
            # Each face should be a list of vertex indices
            for face in model_data['faces']:
                boundaries.append([[face]])
        return boundaries
    
    def _create_semantics(self, model_data: Dict[str, Any]) -> dict:
        """Create semantics object for CityJSON geometry"""
        return {
            "surfaces": [
                {"type": "WallSurface"},
                {"type": "RoofSurface"},
                {"type": "GroundSurface"}
            ],
            "values": [[0], [1], [2]]  # Map boundaries to surface types
        }
