# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_tally_unit_converter as otuc

# makes an OpenMC geometry object from the dagmc file
geometry = odw.Geometry(
    h5m_filename="dagmc.h5m",
    reflective_angles=(0, 180)
)


# this links the material tags in the dagmc h5m file with materials.
# these materials are input as strings so they will be looked up in the
# neutronics material maker package
materials = odw.Materials(
    h5m_filename=geometry.h5m_filename,
    correspondence_dict={
        "mat_plasma": "DT_plasma",
        "mat_inboard_tf_coils": "copper",
        "mat_center_column_shield": "tungsten",
        "mat_firstwall": "tungsten",
        "mat_blanket": "Li4SiO4",
        "mat_blanket_rear_wall": "eurofer",
        "mat_divertor_upper": "tungsten",
        "mat_divertor_lower": "tungsten",
    }
)

tally1 = odw.CellTally(tally_type="TBR", target="blanket", materials=materials)

# creates a dose tally for neutrons with the required EnergyFunctionFilter,
# ParticleFilter, MaterialFilter etc
tally2 = odw.CellTally(
    tally_type="neutron_effective_dose", target="firstwall", materials=materials
)

tallies = openmc.Tallies([tally1, tally2])

settings = odw.FusionSettings()
settings.batches = 2
settings.particles = 100
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()

statepoint = openmc.StatePoint(statepoint_file)

# gets the second tally using its name
my_tally_1 = statepoint.get_tally(name="blanket_TBR")

# no unit coversion is needed for the TBR (tritium breeding ratio) tally
print(f'TBR is {my_tally_1}')


my_tally_2 = statepoint.get_tally(name="firstwall_neutron_effective_dose")

# returns the tally with normalisation for source strength
result = otuc.process_dose_tally(
    source_strength=1.3e6,
    tally=my_tally_2,
    required_units="Sv / second",
    volume= 100 # in the future this volume of the component will be found automatically
)
print(f"effective dose = {result}", end="\n\n")
