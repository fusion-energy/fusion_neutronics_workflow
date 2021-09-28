# This Dockerfile creates an enviroment / dependancies needed to run the
# fusion-neutronics-workflow.

# This Dockerfile can be build locally or a prebuild image can be downloaded

# To download the prebuild image
# docker pull ghcr.io/fusion-energy/fusion-neutronics-workflow

# To build this Dockerfile into a docker image:
# docker build -t fusion-neutronics-workflow .

# To build this Dockerfile and use multiple cores to compile:
# docker build -t fusion-neutronics-workflow --build-arg compile_cores=7 .

# To run the locally built Docker image:
# docker run -it fusion-neutronics-workflow

# To run the prebuilt Docker image:
# docker run -it ghcr.io/fusion-energy/fusion-neutronics-workflow

# Run with the following command for a shared folder between base OS and the
# locally built docker image
# docker run -it -v $PWD:/local_dir fusion-neutronics-workflow

# Run with the following command for a shared folder between base OS and the
# locally built docker image
# docker run -it -v $PWD:/local_dir fusion-neutronics-workflow

# Run with the following command for a shared folder between base OS and the
# prebuild docker image
# docker run -it -v $PWD:/local_dir ghcr.io/fusion-energy/fusion-neutronics-workflow

# TODO save build time by basing this on FROM ghcr.io/fusion-energy/paramak:latest
# This can't be done currently as the base images uses conda installs for moab / dagmc which don't compile with OpenMC
FROM continuumio/miniconda3:4.9.2 as dependencies

ARG compile_cores=1

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

# Installing CadQuery
RUN conda install -c conda-forge -c cadquery cadquery=2.1 && \
    pip install jupyter-cadquery==2.1.0

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

# install Cubit dependencies
RUN apt-get install -y libx11-6
RUN apt-get install -y libxt6
RUN apt-get install -y libgl1
RUN apt-get install -y libglu1-mesa
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libxcb-icccm4
RUN apt-get install -y libxcb-image0
RUN apt-get install -y libxcb-keysyms1
RUN apt-get install -y libxcb-render-util0
RUN apt-get install -y libxkbcommon-x11-0
RUN apt-get install -y libxcb-randr0
RUN apt-get install -y libxcb-xinerama0


# Clone and install Embree
RUN git clone --shallow-submodules --single-branch --branch v3.12.2 --depth 1 https://github.com/embree/embree.git && \
    cd embree && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=.. \
             -DEMBREE_ISPC_SUPPORT=OFF && \
    make -j"$compile_cores" && \
    make -j"$compile_cores" install


# Clone and install MOAB
RUN pip install --upgrade numpy cython && \
    mkdir MOAB && \
    cd MOAB && \
    mkdir build && \
    git clone --shallow-submodules --single-branch --branch 5.3.0 --depth 1 https://bitbucket.org/fathomteam/moab.git && \
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
RUN git clone --shallow-submodules --single-branch --branch main --depth 1 https://github.com/pshriwise/double-down.git && \
    cd double-down && \
    mkdir build && \
    cd build && \
    cmake .. -DMOAB_DIR=/MOAB \
             -DCMAKE_INSTALL_PREFIX=.. \
             -DEMBREE_DIR=/embree && \
    make -j"$compile_cores" && \
    make -j"$compile_cores" install


# Clone and install DAGMC
RUN mkdir DAGMC && \
    cd DAGMC && \
    # change to version 3.2.1 when released
    # git clone --single-branch --branch 3.2.1 --depth 1 https://github.com/svalinn/DAGMC.git && \
    git clone --shallow-submodules --single-branch --branch develop --depth 1 https://github.com/svalinn/DAGMC.git && \
    mkdir build && \
    cd build && \
    cmake ../DAGMC -DBUILD_TALLY=ON \
                   -DMOAB_DIR=/MOAB \
                   -DDOUBLE_DOWN=ON \
                   -DBUILD_STATIC_EXE=OFF \
                   -DBUILD_STATIC_LIBS=OFF \
                   -DCMAKE_INSTALL_PREFIX=/DAGMC/ \
                   -DDOUBLE_DOWN_DIR=/double-down  && \
    make -j"$compile_cores" install && \
    rm -rf /DAGMC/DAGMC /DAGMC/build

# Clone and install OpenMC with DAGMC
# TODO clone a specific release when the next release containing (PR 1825) is avaialble.
RUN git clone --shallow-submodules --recurse-submodules --single-branch --branch develop --depth 1 https://github.com/openmc-dev/openmc.git  /opt/openmc && \
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

# installs python packages and nuclear data
RUN pip install openmc_data_downloader && \
    openmc_data_downloader -d nuclear_data -e all -i H3 -l ENDFB-7.1-NNDC TENDL-2019 -p neutron photon

# Download Cubit
RUN wget -O coreform-cubit-2021.5.deb https://f002.backblazeb2.com/file/cubit-downloads/Coreform-Cubit/Releases/Linux/Coreform-Cubit-2021.5%2B15962_5043ef39-Lin64.deb

# Install cubit
RUN dpkg -i coreform-cubit-2021.5.deb

# installs svalinn plugin for cubit
RUN wget https://github.com/svalinn/Cubit-plugin/releases/download/0.2.1/svalinn-plugin_debian-10.10_cubit_2021.5.tgz
RUN tar -xzvf svalinn-plugin_debian-10.10_cubit_2021.5.tgz -C /opt/Coreform-Cubit-2021.5

# writes a non commercial license file
RUN mkdir -p /root/.config/Coreform/licenses
RUN printf 'Fri May 28 2021' >> /root/.config/Coreform/licenses/cubit-learn.lic

# helps to identify Cubit related errrors
ENV CUBIT_VERBOSE=5

# needed to prevent hdf5 conflict between MOAB and Cubit
ENV HDF5_DISABLE_VERSION_CHECK=1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


# setting enviromental varibles
ENV OPENMC_CROSS_SECTIONS=/nuclear_data/cross_sections.xml
ENV PATH="/MOAB/build/bin:${PATH}"
ENV PATH="/DAGMC/bin:${PATH}"

RUN mkdir /home/fusion-neutronics-workflow
EXPOSE 8888
WORKDIR /home/fusion-neutronics-workflow



FROM ghcr.io/fusion-energy/fusion-neutronics-workflow:dependencies as final

COPY example_01_single_volume_cell_tally example_01_single_volume_cell_tally/
COPY example_02_multi_volume_cell_tally example_02_multi_volume_cell_tally/
COPY example_04_multi_volume_regular_mesh_tally example_04_multi_volume_regular_mesh_tally/
COPY example_05_3D_unstructured_mesh_tally example_05_3D_unstructured_mesh_tally/
