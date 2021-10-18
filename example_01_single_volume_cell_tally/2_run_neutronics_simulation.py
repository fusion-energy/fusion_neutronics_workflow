# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import openmc_post_processor as opp
from spectrum_plotter import plot_spectra


# defines a simple DT neutron point source
my_source = ops.FusionPointSource(
    coordinate = (0,0,0),
    temperature = 20000.,
    fuel='DT'
)

# set the geometry file to use
geometry = odw.Geometry(
    h5m_filename='dagmc.h5m',
)

# sets the material to use
materials = odw.Materials(
    h5m_filename='dagmc.h5m',
    correspondence_dict={"mat1": "eurofer"}
)

# creates a cell tally for neutron flux
tally1 = odw.CellTally(
    tally_type="neutron_flux",
    target="mat1",
    materials=materials
)

# creates a cell tally for neutron spectra
tally2 = odw.CellTally(
    tally_type="neutron_spectra",
    target="mat1",
    materials=materials
)

tallies = openmc.Tallies([tally1, tally2])

settings = odw.FusionSettings()
settings.batches = 1
settings.particles = 50000

# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionRingSource(fuel="DT", radius=350)


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)

# starts the simulation
statepoint_file = my_model.run()

# loads up the statepoint file with simulation results
statepoint = opp.StatePoint(filepath=statepoint_file)

# gets the first tally using its name
my_tally_1 = statepoint.get_tally(name="mat1_neutron_flux")

# gets number of neutron for a 1.3 mega joule shot
source_strength = opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6)

# converts the flux units of the tally
result = statepoint.process_tally(
    source_strength=source_strength,
    tally=my_tally_1,
    required_units="centimeter / second",
)

print(f"flux per second = {result}", end="\n\n")

# gets the second tally using its name
my_tally_2 = statepoint.get_tally(name="mat1_neutron_spectra")

# returns the tally converted to MeV, scaled and normalisation for source strength
result = statepoint.process_tally(
    tally=my_tally_2,
    required_units=["MeV", "centimeter / second"],
    source_strength=source_strength
)

# creates a matplotlib figure of the tally
spectrum_plot = plot_spectra(
    spectra=(result[0], result[1]),
    x_label="Energy [MeV]",
    y_label="Flux [n/cm^2s]",
    x_scale="log",
    y_scale="log",
    title="neutron spectra tally",
)

spectrum_plot.show()
