import open3d as o3d
import numpy as np
from open3d.cpu.pybind.geometry import PointCloud, TriangleMesh
from .surface_strategy import SurfaceStrategy


class Open3dSurface(SurfaceStrategy):
    parameters = {
        'estimate_normals': [
            {
                'name': 'fast_normal_computation',
                'description': 'Fast normal estimation',
                'value': True
            },
            {
                'name': 'normals',
                'description': 'Points normals',
                'value': (1, 3)
            }
        ],
        'orient_normals_consistent_tangent_plane': [
            {
                'name': 'k',
                'description': 'Nearest neighbors',
                'value': 100
            }
        ],
        'surface_reconstruction_screened_poisson': [
            {
                'name': 'depth',
                'description': 'Maximum depth of the tree',
                'value': 8
            },
            {
                'name': 'width',
                'description': 'Target width',
                'value': 0
            },
            {
                'name': 'scale',
                'description': 'Ratio between the diameter of the cube',
                'value': 1.1
            },
            {
                'name': 'linear_fit',
                'description': 'Use linear interpolation?',
                'value': False
            },
            {
                'name': 'n_threads',
                'description': 'Number of threads used for reconstruction',
                'value': -1
            }
        ]
    }

    def __init__(self, point_cloud_file="", output_file="", clean_up=True):

        self.point_cloud = PointCloud()
        self.mesh = TriangleMesh()

        # raise ValueError(f"Contains the {point_cloud_file} attribute: {output_file}")

        super().__init__(point_cloud_file, output_file, clean_up)

    def load_file(self, file_path: str) -> PointCloud:
        print('Load point cloud file')

        self.point_cloud = o3d.io.read_point_cloud(
            file_path,
            print_progress=True
        )

        print(np.asarray(self.point_cloud.points))

        return self.point_cloud

    def estimate_normals(self, **params):

        # invalidate existing normals
        self.point_cloud.normals = o3d.utility.Vector3dVector(np.zeros(params['normals']))
        del params['normals']

        self.point_cloud.estimate_normals(**params)
        self.normals_estimated = True

        return self

    def poisson_mesh(self, save_file=True, **params: {}) -> TriangleMesh:

        def apply_filter(name: str, params_key_values: dict):

            if not self.normals_estimated and hasattr(self, name):
                fn = getattr(self, name)

                if callable(fn):
                    fn(**params_key_values)

                self.applied_filters = True
            elif self.point_cloud and hasattr(self.point_cloud, name):
                fn = getattr(self.point_cloud, name)

                if callable(fn):
                    fn(**params_key_values)

                self.applied_filters = True

            if name == 'surface_reconstruction_screened_poisson':
                with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug):
                    self.mesh, densities = TriangleMesh.create_from_point_cloud_poisson(
                        self.point_cloud,
                        **params_key_values
                    )
                    self.applied_filters = True

        self.poisson_filters(callback=apply_filter, **params)

        if save_file:

            output_file = self.output_file

            if 'output_file' in params:
                output_file = params.get('output_file')
                del params['output_file']

            # Save the generated Surface in a .ply file
            result = o3d.io.write_triangle_mesh(
                output_file,
                self.mesh,
                compressed=True,
                write_vertex_colors=True,
                write_vertex_normals=True,
                print_progress=True
            )

            if not result:
                return None

        return self.mesh
