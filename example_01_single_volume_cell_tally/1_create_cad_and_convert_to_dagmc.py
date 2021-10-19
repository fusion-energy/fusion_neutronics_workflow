# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
from stl_to_h5m import stl_to_h5m


my_shape = paramak.ExtrudeStraightShape(
    points=[(400, 100), (400, 200), (600, 200), (600, 100)],
    distance=180,
)

my_shape.export_stl("steel.stl")

# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. One of the key aspects of this is the assignment
# of materials to the volumes present in the CAD files.

stl_to_h5m(
    files_with_tags=[
        ("steel.stl", "mat1"),
    ],
    h5m_filename="dagmc.h5m",
)
