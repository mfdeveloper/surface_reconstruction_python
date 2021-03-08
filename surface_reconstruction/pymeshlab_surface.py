from .surface_strategy import SurfaceStrategy
import pymeshlab


class PyMeshlabSurface(SurfaceStrategy):

    parameters = {
      'point_cloud_simplification': [
        {
          'name': 'samplenum',
          'description': 'Number of samples',
          'value': 1000
        },
        {
          'name': 'radius',
          'description': 'Explicit Radius',
          'value': 0
        },
        {
          'name': 'bestsampleflag',
          'description': 'Best Sample Heuristic',
          'value': True
        },
        {
          'name': 'bestsamplepool',
          'description': 'Best Sample Pool Size',
          'value': True
        },
        {
          'name': 'exactnumflag',
          'description': 'Exact number of samples',
          'value': 10
        }
      ],
      'compute_normals_for_point_sets': [
        {
          'name': 'k',
          'description': 'Neighbour num',
          'value': 5
        },
        {
          'name': 'smoothiter',
          'description': 'Smooth Iteration',
          'value': 0
        },
        {
          'name': 'flipflag',
          'description': 'Flip normals w.r.t. viewpoint',
          'value': False
        },
        {
          'name': 'viewpos',
          'description': 'Viewpoint Pos',
          'value': [0, 0, 0]
        }
      ],
      'surface_reconstruction_screened_poisson': [
        {
          'name': 'depth',
          'description': 'Reconstruction Depth',
          'value': 8
        },
        {
          'name': 'cgdepth',
          'description': 'Conjugate Gradients Depth',
          'value': 0
        },
        {
          'name': 'fulldepth',
          'description': 'Adaptive Octree Depth',
          'value': 5
        },
        {
          'name': 'visiblelayer',
          'description': 'Merge all visible layers',
          'value': False
        },
        {
          'name': 'scale',
          'description': 'Scale Factor',
          'value': 1.1
        },
        {
          'name': 'samplespernode',
          'description': 'Minimum Number of Samples',
          'value': 1.5
        },
        {
          'name': 'pointweight',
          'description': 'Interpolation Weight',
          'value': 4
        },
        {
          'name': 'iters',
          'description': 'Gauss-Seidel Relaxations',
          'value': 8
        },
        {
          'name': 'confidence',
          'description': 'Confidence Flag',
          'value': False
        },
        {
          'name': 'preclean',
          'description': 'Pre-Clean',
          'value': False
        }
      ]
    }

    # noinspection PyArgumentList
    def __init__(self, point_cloud_file="", output_file="", filter_script_file="", clean_up=True):
        self.mesh_set = pymeshlab.MeshSet()
        self.point_cloud = pymeshlab.Mesh()
        self.mesh = pymeshlab.Mesh()
        self.__filter_script_file = filter_script_file

        super().__init__(point_cloud_file, output_file, clean_up)

    def load_file(self, file_path: str) -> pymeshlab.Mesh:
        self.mesh_set.load_new_mesh(file_path)

        if len(self.__filter_script_file) > 0:
            self.mesh_set.load_filter_script(self.__filter_script_file)

        self.point_cloud = self.mesh_set.current_mesh()
        return self.mesh_set.current_mesh()

    def poisson_mesh(self, save_file=True, **params: {}) -> pymeshlab.Mesh:

        self.applied_filters = False

        if len(self.__filter_script_file) > 0:
            self.mesh_set.apply_filter_script()
            self.applied_filters = True
        else:
            def apply_filter(name: str, params_key_values: dict):
                self.mesh_set.apply_filter(name, **params_key_values)
                self.applied_filters = True

            self.poisson_filters(callback=apply_filter, **params)

        # Save the generated Surface in a .ply file
        if save_file:

            output_file = self.output_file

            if 'output_file' in params:
                output_file = params.get('output_file')
                del params['output_file']

            self.mesh_set.save_current_mesh(
              output_file,
              save_vertex_color=True,
              save_vertex_normal=True,
              save_face_color=True,
              binary=True
            )

        return self.mesh_set.current_mesh()
