# Konverter dari file OBJ ke CityJSON untuk objek jalan
# Berdasarkan skrip asli yang digunakan untuk objek bangunan

import json
import uuid
import sys
import os

# Fungsi untuk membaca file OBJ
def read_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 1:
                continue
            if parts[0] == 'v':
                vertices.append([float(x) for x in parts[1:4]])
            elif parts[0] == 'f':
                face = [int(x.split('/')[0]) - 1 for x in parts[1:]]
                faces.append(face)
    return vertices, faces

# Fungsi untuk membuat struktur CityJSON khusus jalan
def create_cityjson(vertices, faces, obj_name):
    cityjson = {
        "type": "CityJSON",
        "version": "1.1",
        "transform": {},
        "CityObjects": {},
        "vertices": vertices
    }

    road_id = str(uuid.uuid4())
    cityjson["CityObjects"][road_id] = {
        "type": "Road",
        "attributes": {
            "name": obj_name
        },
        "geometry": [{
            "type": "MultiSurface",
            "lod": 2.0,
            "boundaries": [[face] for face in faces]
        }]
    }

    return cityjson

# Fungsi utama
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python obj2roadjson.py <input.obj> <output.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    obj_name = os.path.basename(input_file).replace('.obj', '')
    vertices, faces = read_obj(input_file)
    
    cityjson = create_cityjson(vertices, faces, obj_name)
    
    with open(output_file, 'w') as f:
        json.dump(cityjson, f, indent=4)
    
    print(f"Konversi selesai: {output_file}")
