from surface_reconstruction.open3d_surface import Open3dSurface
from plyfile import PlyData
import unittest
import os
import numpy
import open3d as o3d


class Open3dTest(unittest.TestCase):

    parameters = {
        'filters': {
            'estimate_normals': {
                'fast_normal_computation': True,
                'normals': (1, 3)
            },
            'orient_normals_consistent_tangent_plane': {
                'k': 100,
            },
            'surface_reconstruction_screened_poisson': {
                'depth': 8,
                'width': 0,
                'scale': 1.1,
                'linear_fit': False,
                'n_threads': -1
            }
        }
    }

    def setUp(self):
        self.files_folder = os.path.join('../files', 'complex_terrain')
        self.point_cloud_file = os.path.join(self.files_folder, 'list_vertex.ply')
        self.output_file = os.path.join(self.files_folder, 'terrain.ply')

    def test_point_cloud_file(self):
        o3d_surface = Open3dSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file
        )

        points = numpy.asarray(o3d_surface.point_cloud.points)

        self.assertGreater(points.size, 0)

    def test_surface_reconstruction_mesh(self):
        surface = Open3dSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file
        )

        mesh = surface.poisson_mesh(save_file=False, depth=8)

        self.assertIsNotNone(mesh)
        self.assertIsInstance(mesh, o3d.geometry.TriangleMesh)

    def test_surface_reconstruction_generated_file(self):

        o3d_surface = Open3dSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file
        )

        o3d_surface.poisson_mesh(**self.parameters)

        plydata = PlyData.read(self.output_file)

        assertion_msg = f'The generated file "{self.output_file}" .ply surface file not contains faces/triangles'
        self.assertGreater(plydata["face"].count, 0, assertion_msg)

    def test_surface_reconstruction_generated_file_with_default_filters(self):

        o3d_surface = Open3dSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file
        )

        o3d_surface.poisson_mesh()

        plydata = PlyData.read(self.output_file)

        assertion_msg = f'The generated file "{self.output_file}" .ply surface file not contains faces/triangles'
        self.assertGreater(plydata["face"].count, 0, assertion_msg)


if __name__ == '__main__':
    unittest.main()
