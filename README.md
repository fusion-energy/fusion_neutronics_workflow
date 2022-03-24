[![CI with docker build](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/ci_with_docker_build.yml/badge.svg)](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/ci_with_docker_build.yml)

[![CI with install](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/ci_with_install.yml)

[![docker-publish-release](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/docker_publish.yml/badge.svg?event=release)](https://github.com/fusion-energy/fusion_neutronics_workflow/actions/workflows/docker_publish.yml)


# Fusion Neutronics Workflow

![fusion neutronics workflow](https://user-images.githubusercontent.com/8583900/150701623-29fbf50b-0203-4818-b318-2f3a996e1db7.png)

Diagram showing the connectivity of software packages that make up the Fusion
Neutronics Workflow. Software that the user interacts with directly are shown
in blue.

This repository contains a containerized neutronics workflow for carrying out
standard neutronics simulations in a repeatable manner.

There are workflows for producing standard neutronics simulations such as dose
maps, DPA tallies, neutron/photon spectra, 3D VTK visualizations and the aim is
to provide working examples for mainstream fusion neutronics analysis.
Contributions are welcome.

This repository combines the several packages to create neutronics workflow
that is:

- Automated - the entire workflow can be run automatically. Care has been taken
    to code out all manual processes so that the neutronics analysis can be
    performed in an API manner. As a result it is therefore possible to drive
    the workflow with machine learning, optimization or parameter space
    sampling methods.
- Scalable - by using efficient interfaces (Embree, Double Down) and
    accelerated geometry (DAGMC) together with scalable Monte Carlo transport
    (OpenMC) the resulting workflow scales well with computational power.
- Deployable - By integrating open source software preferentially and ensuring
    compatibility with containerization the combined workflow is straight
    forward to deploy. Instances have been run everywhere from cloud computing
    to local compute.
- Modular - individual packages created as part of the workflow are all
    available to install via PyPi pip installers or Conda installs. This allows
    separate components of the workflow to be easily installed as well as the
    workflow asa  whole. All interfaces are exposed and there is no vendor lock
    in for any aspect.
- Documented - documentation of installation procedures, use cases, examples,
    tutorials and even demonstration videos are all available.

# Dockerfile

## Quick start

The Dockerfile can build locally or a prebuilt one can be downloaded with
```bash
docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow
```

The docker image can then be run with
```bash
docker run -it ghcr.io/fusion-energy/fusion-neutronics-workflow
```

## Sharing files

To map a local folder to the docker container a volume mount can be used.
The following example mounts the local folder that the command is being run from with the ```/home/fusion-neutronics-workflow/examples``` that is inside the docker
images
```bash
docker run -it -v $PWD:/home/fusion-neutronics-workflow/examples ghcr.io/fusion-energy/fusion-neutronics-workflow
```

## Performance builds

There are additional higher performance docker images available if your CPU
supports vectorization instructions available Embree.

Download a prebuilt docker image with Embree and Double Down enabled
```bash
docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow:embree
```

Download a prebuilt docker image with Embree compiled with AVX instruction set and Double Down enabled
```bash
docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow:embree-avx
```


# Software Packages included

Links to the packages that are utilized by the fusion-neutronics-workflow

* Open source projects created and maintained

    * [Paramak](https://github.com/fusion-energy/openmc_data_downloader) -
    automated production of fusion reactor CAD models (stp and stl files) from
    parameters.

    * [stl_to_h5m](https://github.com/fusion-energy/stl_to_h5m) automated
    conversion of STL files to h5m files compatible with DAGMC enabled
    particle transport codes.

    * [openmc_dagmc_wrapper](https://github.com/fusion-energy/openmc-dagmc-wrapper)
    allows one to quickly utilise the h5m geometry files in a range of
    standard OpenMC based neutronics simulations.

    * [neutronics-material-maker](https://github.com/fusion-energy/neutronics_material_maker)
    Create and customise materials from an internal database or from your own
    recipe, export to a wide range of neutronics codes.

    * [openmc_tally_unit_converter](https://github.com/openmc-data-storage/openmc_tally_unit_converter) converts the units of common tally such as
    heating, DPA, effective dose into user specified units. 

    * [openmc_data_downloader](https://github.com/openmc-data-storage/openmc_data_downloader) performs on the fly downloading of nuclear data
    needed for OpenMC neutronics simulations.

    * [openmc-plasma-source](https://github.com/fusion-energy/openmc-plasma-source/)
    Creates a plasma source as an openmc.source object from input parameters that describe the plasma 

    * [spectrum_plotter](https://github.com/fusion-energy/spectrum_plotter)
    A Python package for creating publication quality plots for neutron / photon / particle spectrum 

    * [openmc_mesh_tally_to_vtk](https://github.com/fusion-energy/openmc_mesh_tally_to_vtk)
    A Python package for converting OpenMC mesh tallies to VTK files and optionally converting the units 

    * [regular_mesh_plotter](https://github.com/fusion-energy/regular_mesh_plotter)
    A Python package for plotting regular mesh tally results from neutronics simulations. 

    * [dagmc_geometry_slice_plotter](https://github.com/fusion-energy/dagmc_geometry_slice_plotter) A minimal Python package that produces slice plots through h5m DAGMC geometry files 

    * [dagmc_bounding_box](https://github.com/fusion-energy/dagmc_bounding_box)
    Finds the bounding box and related properties of a DAGMC geometry 

    * [remove_dagmc_tags](https://github.com/svalinn/remove_dagmc_tags) A python package and command line tool for removing DAGMC tags such as graveyard and vacuum 

    * [dagmc_h5m_file_inspector](https://github.com/fusion-energy/dagmc_h5m_file_inspector)
    Extracts information from DAGMC h5m files including volumes number, material tags 

    * [brep_to_h5m](https://github.com/fusion-energy/brep_to_h5m) Converts Brep CAD geometry files to h5m geometry files compatible with DAGMC simulations 

    * [brep_part_finder](https://github.com/fusion-energy/brep_part_finder) A Python package to identify the part ID number in Brep format CAD files 

* Open source projects that are utilized and contributed to

    * [OpenMC](https://github.com/openmc-dev/openmc) The OpenMC project, a
    Monte Carlo particle transport code based on modern methods.

    * [DAGMC](https://github.com/svalinn/DAGMC) Direct Accelerated Geometry
    Monte Carlo Toolkit

    * [SphinxCadQuery](https://github.com/CadQuery/sphinxcadquery) An extension to visualize CadQuery 3D files in your Sphinx documentation 


* Open source projects utilized in the software stack

    * [MOAB and pymoab](https://github.com/svalinn/Cubit-plugin/) the
      Mesh-Oriented datABase MOAB is a component for representing and evaluating
      mesh data.

    * [CadQuery](https://github.com/cadquery/cadquery) A python parametric CAD
      scripting framework based on OCCT 

    * [Double-Down](https://github.com/pshriwise/double-down) A double precision 
       interface to Embree via the Mesh Oriented dAtaBase (MOAB). 

    * [Embree](https://github.com/embree/embree) high-performance ray tracing
       kernels
    
    * [Gmsh](https://gitlab.onelab.info/gmsh/gmsh) A three-dimensional finite
       element mesh generator with built-in pre- and post-processing facilities
    
    * Scipy, Numpy, Plotly, Pint and other standard scientific Python packages
