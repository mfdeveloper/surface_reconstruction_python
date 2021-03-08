import open3d as o3d
import numpy as np
import os

files_folder = os.path.join(os.path.abspath(os.getcwd()), 'files')
print('Load point cloud file')

pcd = o3d.io.read_point_cloud(
  os.path.join(files_folder, 'complex_terrain', 'list_vertex.ply'),
  print_progress=True
)

print(pcd)
print(np.asarray(pcd.points))

# invalidate existing normals
pcd.normals = o3d.utility.Vector3dVector(np.zeros((1, 3)))
pcd.estimate_normals()
pcd.orient_normals_consistent_tangent_plane(100)

print('run Poisson surface reconstruction')

with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)

print(mesh)

o3d.io.write_triangle_mesh(
  os.path.join(files_folder, 'complex_terrain', 'terrain.ply'),
  mesh,
  compressed=True,
  print_progress=True
)

o3d.visualization.draw_geometries(
    [mesh],
    zoom=0.664,
    front=[-0.4761, -0.4698, -0.7434],
    lookat=[1.8900, 3.2596, 0.9284],
    up=[0.2304, -0.8825, 0.4101]
)
