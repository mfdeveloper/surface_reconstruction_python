import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    install_requires = fr.readlines()

setuptools.setup(
     name='surface_reconstruction',
     author="Felipe Michel Ferreira",
     author_email="mfelipeof@gmail.com",
     description="""
     Import a point cloud file and perform poisson 3D surface reconstruction algorithm,
     integrated with third-party libraries (e.g. open3d, pymeshlab...)
     """,
     install_requires=install_requires,
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/mfdeveloper/surface_reconstruction_python",
     packages=setuptools.find_packages(),
     python_requires='>=3.6',
     classifiers=[
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Topic :: Multimedia :: Graphics :: 3D Rendering",
         "Environment :: GPU",
         "Development Status :: 5 - Production/Stable",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.8",
     ],
 )
