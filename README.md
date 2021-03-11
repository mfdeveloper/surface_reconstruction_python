# Poisson Surface Reconstruction: 3D point cloud

Import a point cloud file and perform poisson 3D surface reconstruction algorithm, 
integrated with third-party libraries like [open3d](http://www.open3d.org/docs/release/tutorial/geometry/surface_reconstruction.html?highlight=surface%20reconstruction#Poisson-surface-reconstruction) and [pymeshlab](https://github.com/cnr-isti-vclab/PyMeshLab)


## Dependencies

- [python 3](https://www.python.org/downloads/) <= *3.8.x*
  > **Recommended:** Use [pyenv](https://github.com/pyenv/pyenv) to install and manage Python versions
- [numpy](https://numpy.org) >= *1.20*
- [open3d](http://www.open3d.org) >= *0.12*
- [pymeshlab](https://github.com/cnr-isti-vclab/PyMeshLab) >= *0.2*


## Development dependencies

- [setuptools](https://pypi.org/project/setuptools): For installation via `setup.py`
- [setuptools-scm](https://pypi.org/project/setuptools-scm): To generate version numbers from **git tags**
- [wheel](https://pypi.org/project/wheel/): Built packages `.whl` to install packages with PIP 
- [twine](https://pypi.org/project/twine): Publish packages to https://pypi.org
- [tqdm](https://pypi.org/project/tqdm): CLI progressbar when publish a package

## Development guide

For local installation and develop new features for this package, follow the steps below:


### Windows

> Run unassigned powershell scripts on Windows requires change your execution policy with `Set-ExecutionPolicy` to `AllSigned`, or `Bypass -Scope Process`. 

>See: [Execution Policies](https://docs.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.1)

Run the script `setup.ps1` with [powershell](https://docs.microsoft.com/pt-pt/powershell/scripting/overview?view=powershell-7.1)

```powershell
# Default virtualenv folder is "venv"
.\setup.ps1

# Optionally, pass a custom virtualenv folder
.\setup.ps1 -VirtualEnvFolder myenv
```

If you wish run just an specific function from `setup.ps1` (e.g. `Install-Python`), execute:

```powershell
powershell -command "& { . .\setup.ps1 'venv' -Execute 0; Install-Python }"
```

### Unix systems (Comming soon)

```bash
# Default virtualenv folder is "venv"
./setup.sh

# Optionally, pass a custom virtual enviroment folder
./setup.sh --virtual-env-folder myenv
```

For more detailed installation, see the Wiki pages in: [Installation Development](https://github.com/mfdeveloper/surface_reconstruction_python/wiki/Installation-Details)

## Install this package

Quick way:

```bash
pip install surface_reconstruction
```

Or clone this repository and build the `.whl` file from the project root:

```bash
cd [your-project-root]

# Build the .whl package file
python -m build --sdist --wheel .

# Install locally from the .whl file
# Where: x.x.x is the generated version from git tag
pip install dist/surface_reconstruction-x.x.x-py3-none-any.whl
```
> For more detailed, see the Wiki pages in: [Generate package](https://github.com/mfdeveloper/surface_reconstruction_python/wiki/Generate-package)


### Run the unit tests

```bash
# Run all tests of the module "surface_reconstruction_test`
python -m unittest tests/surface_reconstruction_test.py
```

## Usage

Import a `.ply` file with point cloud vertices, and generate the mesh file

```python
from surface_reconstruction import SurfaceReconstruction
import os

# Pass a method/library that contains a Poisson algorithm implementation
surface = SurfaceReconstruction(
  method_type='open3d',
  point_cloud_file=os.path.join('files', 'point_cloud.ply'),
  output_file=os.path.join('files', 'terrain_mesh.ply')
)

# Call the method from the specific library, and export a mesh file
surface.poisson_mesh()
```

You can pass custom filters/parameters for the specific library. This is important because 
poisson algorithm requires some pre-filters before to be applied (e.g **estimate normals** in the point cloud)

```python
# ...
parameters = {
  'estimate_normals': {
    'fast_normal_computation': False,
    'normals': (1, 3)
  }
}

# Unpack the dictionary "parameters" as a **kwargs
surface.poisson_mesh(**{'filters': parameters})
```
> **PS:** See the unittests inside **[tests](./tests)** folder for more usage examples

# Extending: Add new libraries

Is possible create and register custom strategies to allow others libraries (`Python`, `C++` bindings...)

```python
from surface_reconstruction import SurfaceStrategy, SurfaceReconstruction 

# Create a class that inherit from "SurfaceStrategy"
class MyCustomSurface(SurfaceStrategy):
  
      def __init__(self, my_custom_param: dict):
        """
        Custom constructor with custom parameters
        """
        super().__init__()
  
      def load_file(self, file_path: str):
        """
        Custom load point cloud file implementation here
        """
        pass

    def poisson_mesh(self, save_file=True, **params: {}):
      """
      Generate the mesh file with faces/triangles here
      """
      pass

# Register your custom strategy here
SurfaceReconstruction.register_type(MyCustomSurface)


# Pass a method/library that contains a Poisson algorithm implementation
surface = SurfaceReconstruction(
  method_type='mycustom', # Don't pass the "surface" suffix
  my_custom_param={'extra_config': 'some_value'},
)

# Call the method from the specific library, and export a mesh file
surface.poisson_mesh()
```