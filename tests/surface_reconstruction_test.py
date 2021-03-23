from __future__ import annotations

from surface_reconstruction import SurfaceStrategy, PyMeshlabSurface, Open3dSurface, SurfaceReconstruction
import unittest
import json
import os


class SurfaceReconstructionTest(unittest.TestCase):

    def setUp(self):
        self.files_folder = os.path.join('../files', 'complex_terrain')
        self.point_cloud_file = os.path.join(self.files_folder, 'list_vertex.ply')
        self.output_file = os.path.join(self.files_folder, 'terrain.ply')

    def test_factory_strategies_libraries(self):

        surface = SurfaceReconstruction(method_type='pymeshlab')
        surface2 = SurfaceReconstruction(method_type='open3d')
        surface_default = SurfaceReconstruction()

        self.assertIsInstance(surface, PyMeshlabSurface)
        self.assertIsInstance(surface2, Open3dSurface)
        self.assertIsInstance(surface_default, Open3dSurface)

        # A same instance from the same 'method_type' should be a singleton
        surface3 = SurfaceReconstruction(method_type='open3d')
        self.assertEqual(id(surface2), id(surface3), 'The surface instances are not equal')

    def test_factory_strategy_register_library(self):

        self.assertRaisesRegex(TypeError, 'was not registered', SurfaceReconstruction, method_type='otherlibrary')

        class OtherLibrarySurface(SurfaceStrategy):

            def load_file(self, file_path: str):
                pass

            def poisson_mesh(self, save_file=True, **params: {}):
                pass

        SurfaceReconstruction.register_type(OtherLibrarySurface)

        surface_other = SurfaceReconstruction(method_type='otherlibrary')
        self.assertIsInstance(surface_other, OtherLibrarySurface)

    def test_factory_strategy_parameters(self):

        meshlab_surface: SurfaceStrategy = SurfaceReconstruction(method_type='pymeshlab')
        meshlab_parameters = meshlab_surface.default_parameters()

        # Load the params string to verify if is a valid json
        json_data = json.loads(meshlab_parameters)

        self.assertIsInstance(meshlab_parameters, str)
        self.assertGreater(len(meshlab_parameters), 0)

        self.assertIsInstance(json_data, dict)
        self.assertGreater(len(json_data), 0)

        open3d_surface: SurfaceStrategy = SurfaceReconstruction(method_type='open3d')
        open3d_parameters = open3d_surface.default_parameters()

        self.assertIsInstance(open3d_parameters, str)
        self.assertGreater(len(open3d_parameters), 0)

    def test_strategy_pass_json_parameters(self):

        json_str = """
        {"estimate_normals":{"fast_normal_computation":true,"normals":[1,3]},"orient_normals_consistent_tangent_plane":{"k":100},"surface_reconstruction_screened_poisson":{"depth":8,"width":0,"scale":1.1,"linear_fit":false,"n_threads":-1}}
        """

        surface: SurfaceStrategy = SurfaceReconstruction(
            method_type='open3d',
            point_cloud_file=self.point_cloud_file,
            output_file=self.output_file
        )

        surface.poisson(json_filters=json_str)





