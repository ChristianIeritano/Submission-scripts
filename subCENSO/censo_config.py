import os, sys
from censo.ensembledata import EnsembleData
from censo.configuration import configure
from censo.ensembleopt import Prescreening, Screening, Optimization
#from censo.properties import NMR

##########
#CHECK FOR ACCURATE CHARGE AND MULT INPUTS
############

workdir = os.getcwd() # CENSO will put all files in this directory

for filename in os.listdir(workdir):

    if filename.lower().endswith('xyz'):
        input_path = os.path.join(workdir, filename) # path relative to the working directory

    if filename.lower().endswith('.censo2rc'):
        censorc_file = os.path.join(workdir, filename) # path relative to the working directory

ensemble = EnsembleData(workdir)
ensemble.read_input(input_path, charge=0, unpaired=0)

#If the user wants to use a specific rcfile:
configure(censorc_file)

# Get the number of available cpu cores on this machine
# This number can also be set to any other integer value and automatically checked for validity
#ncores = os.cpu_count()
ncores = 64

# Setup all the parts that the user wants to run
parts = [
    part(ensemble) for part in [Screening, Optimization]
    #part(ensemble) for part in [Optimization]
]
'''
# The user can also choose to change specific settings of the parts
# Please take note of the following:
# - the settings of certain parts, e.g. Prescreening are changed using set_setting(name, value)
# - general settings are changed by using set_general_setting(name, value) (it does not matter which part you call it from)
# - the values you want to set must comply with limits and the type of the setting
Prescreening.set_setting("threshold", 5.0)
Prescreening.set_general_setting("solvent", "dmso")

# It is also possible to use a dict to set multiple values in one step
settings = {
    "threshold": 3.5,
    "func": "r2scan-3c",
    "implicit": True,
}
Screening.set_settings(settings, complete=False)
'''
# Running a part will return it's runtime in seconds
part_timings = []
for part in parts:
    # Running the parts in order, while it is also possible to use a custom order or run some parts multiple times
    # Note though, that currently this will lead to results being overwritten in your working directory and
    # the ensembledata object
    part_timings.append(part.run(ncores))

# You access the results using the ensemble object
# You can also find all the results the <part>.json output files
print(ensemble.conformers[0].results["prescreening"]["sp"]["energy"])