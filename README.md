# Neutronics Workflow

This repository contains a containerized neutronics workflow for carrying out
standard neutronics simulations in a repeatable manner.

This repository combines the several packages to create neutronics workflow
that is:

- Automated - the entire workflow can be run automatically. Care has been taken
    to code out all manual processes so that the neutronics analysis can be
    performed in an API manner. As a result it is therefore possible to drive
    the workflow with machine learning, optimization or parameter space sampling methods.
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

The Dockerfile can build locally or a prebuilt one can be downloaded with
```bash
docker pull ghcr.io/fusion-energy/neutronics-workflow
```

The docker image can then be run with
```bash
docker run -it ghcr.io/fusion-energy/neutronics-workflow
```

Links to the packages that are utilized by the neutronics-workflow

<!--TODO * `stl_to_h5m <https://github.com/fusion-energy/stl_to_h5m) allows automated conversion of stl files to h5m files compatible with DAGMC enabled neutronics codes. -->

* Open source projects created and maintained

    * [Paramak](https://github.com/fusion-energy/openmc_data_downloader) -
    automated production of fusion reactor CAD models (stp and stl files) from
    parameters.

    * [cad_to_h5m](https://github.com/fusion-energy/cad_to_h5m) automated
    conversion of stp or sat CAD files to h5m files compatible with DAGMC
    enabled particle transport codes.

    * [openmc_dagmc_wrapper](https://github.com/fusion-energy/openmc-dagmc-wrapper)
    allows one to quickly utilise the h5m geometry files in a range of
    standard OpenMC based neutronics simulations.

    * [openmc_data_downloader](https://github.com/openmc-data-storage/openmc_data_downloader) performs on the fly downloading of nuclear data
    needed for OpenMC neutronics simulations.

    * [neutronics-material-maker](https://github.com/fusion-energy/neutronics_material_maker)
    Create and customise materials from an internal database or from your own
    recipe, export to a wide range of neutronics codes.


* Open source projects that are utilised and contributed to

    * [OpenMC](https://github.com/openmc-dev/openmc) The OpenMC project, a
    Monte Carlo particle transport code based on modern methods.

    * [DAGMC](https://github.com/svalinn/DAGMC) Direct Accelerated Geometry
    Monte Carlo Toolkit 

    * [Svalinn Cubit Plugin](https://github.com/svalinn/Cubit-plugin/) a plugin
    and command extensions for Cubit that allows h5m files to be exported.

    * [SphinxCadQuery](https://github.com/CadQuery/sphinxcadquery)


* OpenMC source projects utilised in the software stack

    * [MOAB and pymoab](https://github.com/svalinn/Cubit-plugin/) the
      Mesh-Oriented datABase MOAB is a component for representing and evaluating
      mesh data.

    * [CadQuery](https://github.com/cadquery/cadquery)

    * [Double-Down](https://github.com/pshriwise/double-down)

    * [Embree](https://github.com/embree/embree)
    
    * Scipy, Numpy, Plotly and others


* Commercial codes (with non commercial license available)

    * [Coreform Cubit](https://github.com/svalinn/Cubit-plugin/) - advanced
    meshing for challenging simulations. Supports imprinting and merging of
    surfaces which speed up the neutronics transport time required for
    simulations through faceted geometry.
