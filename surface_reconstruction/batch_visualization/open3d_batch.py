from surface_reconstruction.open3d_surface import Open3dSurface
import os
import open3d as o3d

files_folder = os.path.join(os.path.abspath(os.getcwd()), '../../files', 'complex_terrain')
o3d_surface = Open3dSurface(
  point_cloud_file=os.path.join(files_folder, 'list_vertex.ply'),
  output_file=os.path.join(files_folder, 'terrain.ply')
)

mesh = o3d_surface.poisson_mesh()

mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.6, origin=[-2, -2, -2]
)
o3d.visualization.draw_geometries(
    [mesh, mesh_frame],
    window_name='OPEN3D Visualization',
    width=1024,
    height=768,
    mesh_show_back_face=True
)
