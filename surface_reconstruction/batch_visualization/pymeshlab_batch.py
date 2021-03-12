from surface_reconstruction import PyMeshlabSurface
import os
import open3d as o3d

files_folder = os.path.join(os.path.abspath(os.getcwd()), '../../files')

pymeshlab_surface = PyMeshlabSurface(
  point_cloud_file=os.path.join(files_folder, 'complex_terrain', 'list_vertex.ply'),
  output_file=os.path.join(files_folder, 'complex_terrain', 'terrain.ply'),
  filter_script_file=os.path.join(files_folder, 'filter_scripts', 'filter_script.mlx')
)

pymeshlab_surface.poisson_mesh()

mesh = o3d.io.read_triangle_mesh(
    os.path.join(files_folder, 'complex_terrain', 'terrain.ply'),
    print_progress=True
)
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.6, origin=[-2, -2, -2]
)
o3d.visualization.draw_geometries(
    [mesh, mesh_frame],
    window_name='Meshlab Visualization',
    width=1024,
    height=768,
    mesh_show_back_face=True
)

# meshset = pymeshlab.MeshSet()
# meshset.load_new_mesh(os.path.join(files_folder, 'complex_terrain', 'list_vertex.ply'))

# TODO: Extract parameters info from the CLI C++ output,
#  or ask on github to lib owner create a method that returns a dictionary/json with that
# pymeshlab.print_filter_parameter_list('compute_normals_for_point_sets')

# meshset.load_filter_script(os.path.join(files_folder, 'filter_scripts', 'filter_script.mlx'))
# meshset.apply_filter_script()

# meshset.save_current_mesh(
#   os.path.join(files_folder, 'complex_terrain', 'terrain.ply'),
#   save_vertex_color=True,
#   save_vertex_normal=True,
#   save_face_color=True,
#   binary=True
# )
