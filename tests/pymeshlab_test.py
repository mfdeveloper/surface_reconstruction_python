from surface_reconstruction.pymeshlab_surface import PyMeshlabSurface
from plyfile import PlyData
import unittest
import os
import pymeshlab


class PyMeshlabTest(unittest.TestCase):

    poisson_parameters = {
      'filters': {
        'point_cloud_simplification': {
          # Best quality: 1000000, Simple/Low quality (default): 1000
          'samplenum': 1000000,
        },
        'compute_normals_for_point_sets': {
          'k': 5,
          'smoothiter': 0,
          'flipflag': False,
          'viewpos': [0, 0, 0]
        },
        'surface_reconstruction_screened_poisson': {
          'depth': 8,
          'cgdepth': 0,
          'fulldepth': 5,
          'visiblelayer': False,
          'scale': 1.1,
          'samplespernode': 1.5,
          'pointweight': 4,
          'iters': 8,
          'confidence': False,
          'preclean': False
        }
      }
    }

    def setUp(self):
        self.files_folder = os.path.join('../files', 'complex_terrain')
        self.point_cloud_file = os.path.join(self.files_folder, 'list_vertex.ply')
        self.output_file = os.path.join(self.files_folder, 'terrain.ply')

    def test_point_cloud_file(self):
        surface = PyMeshlabSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file
        )

        self.assertGreater(surface.point_cloud.vertex_number(), 0)

    def test_surface_reconstruction_mesh_filter_script(self):
        surface = PyMeshlabSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file,
          filter_script_file=os.path.join('../files', 'filter_scripts', 'filter_script.mlx')
        )

        mesh = surface.poisson_mesh(save_file=False, depth=8)

        self.assertIsNotNone(mesh)
        self.assertIsInstance(mesh, pymeshlab.Mesh)

    def test_surface_reconstruction_generated_file_filter_script(self):
        """
        Verify if the poisson algorithm generate a mesh file
        without any faces/triangles applying a invalid filters from a .mlx script file
        :return: None
        """
        surface = PyMeshlabSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file,
          filter_script_file=os.path.join('../files', 'filter_scripts', 'filter_script.mlx')
        )

        surface.poisson_mesh(save_file=True)
        plydata = PlyData.read(self.output_file)

        assertion_msg = f'The generated file "{self.output_file}" .ply surface file not contains faces/triangles'
        self.assertGreater(plydata["face"].count, 0, assertion_msg)

    def test_surface_reconstruction_generated_file_filter_script_invalid(self):
        """
        Verify if the poisson algorithm generate a mesh file
        applying filters from a .mlx script file
        :return: None
        """
        surface = PyMeshlabSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file,
          filter_script_file=os.path.join('../files', 'filter_scripts', 'filter_script_invalid.mlx')
        )

        surface.poisson_mesh(save_file=True)
        plydata = PlyData.read(self.output_file)

        self.assertEqual(plydata["face"].count, 0)

    def test_surface_reconstruction_generated_file_filters_parameters(self):
        """
        Verify if the poisson algorithm generate a mesh file
        applying filters passing parameters to poisson_mesh() method
        :return: None
        """
        surface = PyMeshlabSurface(
          point_cloud_file=self.point_cloud_file,
          output_file=self.output_file,
        )

        surface.poisson_mesh(save_file=True, **self.poisson_parameters)
        plydata = PlyData.read(self.output_file)

        assertion_msg = f'The generated file "{self.output_file}" .ply surface file not contains faces/triangles'
        self.assertGreater(plydata["face"].count, 0, assertion_msg)
