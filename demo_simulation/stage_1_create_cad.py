
# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak


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

        shapes_and_components = vessel[:-2]
        self.shapes_and_components = shapes_and_components

        return shapes_and_components


my_reactor = DEMOlight(rotation_angle=10)

my_reactor.export_stp(output_folder='stage_1_output')
my_reactor.export_neutronics_description('stage_1_output/manifest.json')
