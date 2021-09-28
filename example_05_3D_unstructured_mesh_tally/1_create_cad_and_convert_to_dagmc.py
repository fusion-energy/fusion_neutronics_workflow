
# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import paramak
from cad_to_h5m import cad_to_h5m

my_shape = paramak.ExtrudeStraightShape(
    points=[
        (200, 10),
        (200, 20),
        (250, 20),
        (250, 10)
        ],
    distance = 5,
)

my_shape.export_stp('steel.stp')

# This script converts the CAD stp files generated into h5m files that can be
# used in DAGMC enabled codes. h5m files created in this way are imprinted,
# merged, faceted and ready for use in OpenMC. One of the key aspects of this
# is the assignment of materials to the volumes present in the CAD files.

cad_to_h5m(
    files_with_tags=[
        {
            'cad_filename':'steel.stp',
            'material_tag':'mat1',
            'tet_mesh': 'size 10',
        },
    ],
    make_watertight=False,
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
    cubit_filename='unstructured_mesh.cub'
)
