# Required libraries
import open3d as o3d
import trimesh
# import vtk
import numpy as np

def decimate_mesh_open3d(input_path, output_path, reduction_ratio=0.5):
    """
    Decimate mesh using Open3D
    reduction_ratio: target number of triangles = reduction_ratio * original triangle number
    """
    mesh = o3d.io.read_triangle_mesh(input_path)
    decimated_mesh = mesh.simplify_quadric_decimation(
        target_number_of_triangles=int(len(mesh.triangles) * reduction_ratio)
    )
    o3d.io.write_triangle_mesh(output_path, decimated_mesh)
    return decimated_mesh

def decimate_mesh_trimesh(input_path, output_path, face_count):
    """
    Decimate mesh using Trimesh
    face_count: target number of faces
    """
    mesh = trimesh.load_mesh(input_path)
    decimated_mesh = mesh.simplify_quadric_decimation(face_count)
    decimated_mesh.export(output_path)
    return decimated_mesh


