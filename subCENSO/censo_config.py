from censo.ensemble import EnsembleData
from censo.config.setup import configure
from censo.ensembleopt import prescreening, screening, optimization
from censo.properties import nmr
from censo.config import PartsConfig
from censo.parallel import get_cluster

from multiprocessing import freeze_support
import os 

##########
#CHECK FOR ACCURATE CHARGE AND MULT INPUTS
############

def main():

    workdir = os.getcwd() # CENSO will put all files in this directory

    for filename in os.listdir(workdir):

        if filename.lower().endswith('xyz'):
            ensemble_file = os.path.join(workdir, filename) # path relative to the working directory

        if filename.lower().endswith('.censo2rc'):
            censorc_file = os.path.join(workdir, filename) # path relative to the working directory

    ensemble = EnsembleData()
    ensemble.read_input(ensemble_file, charge=0, unpaired=0)

    # Load a custom rcfile (optional)
    config = configure(censorc_file)

    # Ensure valid configuration
    #config.general.solvent = "dmso"
    config = PartsConfig.model_validate(
        config.model_dump(),
        context={
            "check": [
                "prescreening",
                "screening",
                "optimization",
                "nmr",
            ]
        },
    )

    # Total cores available to CENSO (SLURM)
    maxcores = int(
        os.environ.get(
            "SLURM_NTASKS",
            os.cpu_count() or 1,
        )
    )

    print(f'maxcores variable: {maxcores}')
    preferred_ompmin = 4
    ompmin = max(1, min(preferred_ompmin, maxcores))

    cluster = get_cluster(
        maxcores=maxcores,
        ompmin=ompmin,
    )

    client = cluster.get_client()

    # passing a context enables paths and solvent validation, which is usually skipped

    # Execute workflow steps
    try:
        results = [
            part(ensemble, config, client)
            for part in [
        #        prescreening, 
        #        screening, 
                optimization, 
        #        nmr
            ]
        ]

    finally:
        client.close()
        cluster.close()

    # The results are then also output to json files in the working directory
    # The molecules stored in the ensemble contain the most up-to-date energy values and geometries

if __name__ == "__main__":
    freeze_support()
    main()


