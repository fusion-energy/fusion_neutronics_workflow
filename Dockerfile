# This Dockerfile creates an enviroment / dependancies needed to run the
# fusion-neutronics-workflow.

# This Dockerfile can be build locally or a prebuild image can be downloaded

# To download the prebuild image
# docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow
# docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow:embree
# docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow:embree-avx

# To build this Dockerfile into a docker image:
# docker build -t fusion-neutronics-workflow .


# To build this Dockerfile with different options --build-arg can be used
# --build-arg compile_cores=1
#   int
#   number of cores to compile codes with
# --build-arg build_double_down=OFF
#   ON OFF
#   controls if DAGMC is built with double down (ON) or not (OFF). Note that if double down is OFF then Embree is not included
# --build-arg include_avx=true
#   true false
#   controls if the Embree is built to use AVX instruction set (true) or not (false). AVX is not supported by all CPUs 

# example builds
# simplest quickest build that does not contain the speed benefits of double down
# docker build -t fusion-neutronics-workflow --build-arg compile_cores=7 --build-arg build_double_down=OFF .
# medium level build that contain some of the speed benefits of double down
# docker build -t fusion-neutronics-workflow:embree-avx --build-arg compile_cores=7 --build-arg build_double_down=ON --build-arg include_avx=false .
# performance level build that contain all of the speed benefits of double down
# docker build -t fusion-neutronics-workflow:embree --build-arg compile_cores=7 --build-arg build_double_down=ON --build-arg include_avx=true .

# base image contains nuclear data
FROM continuumio/miniconda3:4.10.3

ARG compile_cores=1
ARG include_avx=true
ARG build_double_down=OFF


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH=/opt/openmc/bin:$PATH \
    LD_LIBRARY_PATH=/opt/openmc/lib:$LD_LIBRARY_PATH \
    CC=/usr/bin/mpicc CXX=/usr/bin/mpicxx \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get --allow-releaseinfo-change update
RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y libgl1-mesa-glx \
                       libgl1-mesa-dev \
                       libglu1-mesa-dev \
                       freeglut3-dev \
                       libosmesa6 \
                       libosmesa6-dev \
                       libgles2-mesa-dev \
                       curl && \
                       apt-get clean

# solves OSError: libXft.so.2: cannot open shared object file: No such file or directory
RUN apt-get install -y libxft2 

# upgrading numpy version
# RUN pip install "numpy>=1.21.4,<1.30" cython
RUN pip install cython
RUN conda install -c anaconda numpy==1.21.2

# Installing CadQuery add on
RUN pip install jupyter-cadquery==3.0.0

# Install neutronics dependencies from Debian package manager
RUN apt-get install -y \
    wget \
    git \
    gfortran \
    g++ \
    cmake \
    mpich \
    libmpich-dev \
    libhdf5-serial-dev \
    libhdf5-mpich-dev \
    imagemagick


# install addition packages required for MOAB
RUN apt-get --yes install libeigen3-dev && \
    apt-get --yes install libblas-dev && \
    apt-get --yes install liblapack-dev && \
    apt-get --yes install libnetcdf-dev && \
    apt-get --yes install libtbb-dev && \
    apt-get --yes install libglfw3-dev


# Clone and install Embree
# embree from conda is not supported yet
# conda install -c conda-forge embree >> version: 2.17.7
# requested version "3.6.1"
# added following two lines to allow use on AMD CPUs see discussion
# https://openmc.discourse.group/t/dagmc-geometry-open-mc-aborted-unexpectedly/1369/24?u=pshriwise  
RUN if [ "$build_double_down" = "ON" ] ; \
        then git clone --shallow-submodules --single-branch --branch v3.12.2 --depth 1 https://github.com/embree/embree.git ; \
        cd embree ; \
        mkdir build ; \
        cd build ; \
        if [ "$include_avx" = "false" ] ; \
            then cmake .. -DCMAKE_INSTALL_PREFIX=.. \
                        -DEMBREE_ISPC_SUPPORT=OFF \
                        -DEMBREE_MAX_ISA=NONE \
                        -DEMBREE_ISA_SSE42=ON ; \
        fi ; \
        if [ "$include_avx" = "true" ] ; \
            then cmake .. -DCMAKE_INSTALL_PREFIX=.. \
                        -DEMBREE_ISPC_SUPPORT=OFF ; \
        fi ; \
        make -j"$compile_cores" ; \
        make -j"$compile_cores" install ; \
    fi

# Clone and install MOAB
RUN mkdir MOAB && \
    cd MOAB && \
    mkdir build && \
    git clone --shallow-submodules --single-branch --branch 5.3.1 --depth 1 https://bitbucket.org/fathomteam/moab.git && \
    cd build && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_NETCDF=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DENABLE_BLASLAPACK=OFF \
                  -DBUILD_SHARED_LIBS=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make -j"$compile_cores" && \
    make -j"$compile_cores" install && \
    rm -rf * && \
    cmake ../moab -DENABLE_HDF5=ON \
                  -DENABLE_PYMOAB=ON \
                  -DENABLE_FORTRAN=OFF \
                  -DBUILD_SHARED_LIBS=ON \
                  -DENABLE_BLASLAPACK=OFF \
                  -DCMAKE_INSTALL_PREFIX=/MOAB && \
    make -j"$compile_cores" && \
    make -j"$compile_cores" install && \
    cd pymoab && \
    bash install.sh && \
    python setup.py install


# Clone and install Double-Down
RUN if [ "$build_double_down" = "ON" ] ; \
        then git clone --shallow-submodules --single-branch --branch v1.0.0 --depth 1 https://github.com/pshriwise/double-down.git && \
        cd double-down ; \
        mkdir build ; \
        cd build ; \
        cmake .. -DMOAB_DIR=/MOAB \
                -DCMAKE_INSTALL_PREFIX=.. \
                -DEMBREE_DIR=/embree ; \
        make -j"$compile_cores" ; \
        make -j"$compile_cores" install ; \
    fi


# Clone and install DAGMC
RUN mkdir DAGMC && \
    cd DAGMC && \
    git clone --single-branch --branch v3.2.2 --depth 1 https://github.com/svalinn/DAGMC.git && \
    mkdir build && \
    cd build && \
    cmake ../DAGMC -DBUILD_TALLY=ON \
                   -DMOAB_DIR=/MOAB \
                   -DDOUBLE_DOWN=${build_double_down} \
                   -DBUILD_STATIC_EXE=OFF \
                   -DBUILD_STATIC_LIBS=OFF \
                   -DCMAKE_INSTALL_PREFIX=/DAGMC/ \
                   -DDOUBLE_DOWN_DIR=/double-down  && \
    make -j"$compile_cores" install && \
    rm -rf /DAGMC/DAGMC /DAGMC/build

# Clone OpenMC and install OpenMC with DAGMC
RUN cd /opt && \
    git clone --single-branch --branch v0.13.0 --depth 1 https://github.com/openmc-dev/openmc.git && \
    cd openmc && \
    cd /opt/openmc && \
    mkdir build && \
    cd build && \
    cmake -Doptimize=on \
          -Ddagmc=ON \
          -DDAGMC_DIR=/DAGMC/ \
          -DHDF5_PREFER_PARALLEL=on ..  && \
    make -j"$compile_cores" && \
    make -j"$compile_cores" install && \
    cd ..  && \
    pip install -e .[test]

COPY environment.yml .
RUN conda env update -f environment.yml

# downloads nuclear data from zip file an uncompress
# RUN download_nndc

# this is an optional way to install python packages and nuclear data (quick as it does not overwrite existing h5 files)
RUN openmc_data_downloader -d nuclear_data -e all -i H3 -l ENDFB-7.1-NNDC TENDL-2019 -p neutron photon --no-overwrite

# setting enviromental varibles
ENV OPENMC_CROSS_SECTIONS=/nuclear_data/cross_sections.xml
# ENV OPENMC_CROSS_SECTIONS=/nndc-b7.1-hdf5/endfb71_hdf5/cross_sections.xml
ENV PATH="/MOAB/build/bin:${PATH}"
ENV PATH="/DAGMC/bin:${PATH}"

RUN mkdir /home/fusion-neutronics-workflow
EXPOSE 8888
WORKDIR /home/fusion-neutronics-workflow

# subfolder used to avoid overlapping with the testing of examples in GH actions
RUN mkdir examples
COPY example_01_single_volume_cell_tally examples/example_01_single_volume_cell_tally/
COPY example_02_multi_volume_cell_tally examples/example_02_multi_volume_cell_tally/
COPY example_04_multi_volume_regular_mesh_tally examples/example_04_multi_volume_regular_mesh_tally/
COPY example_05_3D_unstructured_mesh_tally examples/example_05_3D_unstructured_mesh_tally/


#this sets the port, gcr looks for this varible
ENV PORT 8888

# could switch to --ip='*'
# CMD ["jupyter", "notebook", "--notebook-dir=/tasks", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
