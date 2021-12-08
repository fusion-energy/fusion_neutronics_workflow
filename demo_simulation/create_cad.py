
# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
import openmc_plasma_source as ops
from stl_to_h5m import stl_to_h5m

from openmc_plasma_source.plotting import scatter_tokamak_source
import matplotlib.pyplot as plt


class DEMOlight(paramak.EuDemoFrom2015PaperDiagram):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def create_solids(self):
        """Creates a 3d solids for each component.
        Returns:
            A list of CadQuery solids: A list of 3D solid volumes
        """

        self.create_plasma()
        self.create_pf_coils()
        vessel = self.create_vessel_components()
        vessel[0].name = "divertor"
        vessel[1].name = "blanket"

        shapes_and_components = vessel[:-2]
        self.shapes_and_components = shapes_and_components

        return shapes_and_components


my_reactor = DEMOlight(rotation_angle=10)


stl_filenames = my_reactor.export_stl()
compentent_names = my_reactor.name

stl_to_h5m(
    files_with_tags=[(stl_filename, name) for name, stl_filename in zip(compentent_names, stl_filenames)],
    h5m_filename='dagmc_not_merged.h5m',
)

# my_reactor.export_2d_image(xmax=1200)
# fig, ax = plt.subplots()
# for entry in my_reactor.shapes_and_components:
#     patch = entry._create_patch()
#     ax.add_collection(patch)

# my_source = ops.TokamakSource(
#     elongation=1.557,
#     ion_density_centre=1.09e20,
#     ion_density_peaking_factor=1,
#     ion_density_pedestal=1.09e20,
#     ion_density_separatrix=3e19,
#     ion_temperature_centre=45.9,
#     ion_temperature_peaking_factor=8.06,
#     ion_temperature_pedestal=6.09,
#     ion_temperature_separatrix=0.1,
#     major_radius=9.06*100,
#     minor_radius=2.1*100,
#     pedestal_radius=0.8 * 2.1*100,
#     mode="H",
#     shafranov_factor=0.44789,
#     triangularity=0.270,
#     ion_temperature_beta=6
#   )
# scatter_tokamak_source(my_source, quantity="neutron_source_density", s=1000*my_source.strengths/sum(my_source.strengths))
# plt.colorbar(label="")
# plt.savefig("out.png")
