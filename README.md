# Submission scripts
 Useful scripts for submitting jobs to HPC resources like Compute Canada. All scripts provided are free use; feel free to use and modify and use them in your workflows as you see fit. 

## subSLURM and subSLURM_node
These Python scripts automates the job submission process on Compute Canada systems for Gaussian (g16), Python (.py), ORCA (.inp), and MobCal-MPI (.mfj) files. There is one minor difference between them, namely:

- subSLURM: The user-specified memory allocates memory per CPU. 
- subSLURM_node: The user-specified memory allocates the total memory for the node.

### Prerequisites 
- Python 3.10 or higher
    - Add the following line to the bottom of your bash profile to ensure python is globally available. Note that your version of python is specific to your systems configuration. Syntax for loading a specific python version may vary *or* python may be be enabled by default:
    ```bash
    module load python/3.10.2
    ```
- Access to a Compute Canada facility with a valid account
- Module availability for Gaussian (g16), Python, or ORCA. It is your responsbility to ensure these programs are available on the specific cluster. To check this use the commands:
    ```bash
    module spider G16
    module spider python
    module spider orca
    ```
### Installation
- Add `subSLURM` to a directory available in your systems PATH. I reccomend a folder called `/bin` located in `/home/{your_username}`. To add this location to your PATH, add the following line to `.bash_profile`:
    ```bash
    PATH=$PATH:$HOME/.local/bin:$HOME/bin

    export PATH
    ```
- Enable execute permissions for subSLURM via:
    ```bash
    cd /home/{your_username}/bin
    chmod a+x subSLURM
    ```

### Usage
Since subSLURM is in systems PATH, it can be called from any directory. Usage is as follows: 

```console
subSLURM filename -n # -m ####mb -t ##-##:## -p program -a account_type
```
- **filename**: Name of the file to submit, or type `all` to submit all files of the type associated with the program entry.
    - g16: `all` submits all files with a .gjf extension. 
    - python: `all` submits all files with a .py extension. 
    - orca5: `all` submits all files with a .inp extension to ORCA v 5.0.4.
    - orca5: `all` submits all files with a .inp extension to ORCA v 6.0.0. 
    - mobcal: `all` submits all files with the .mfj extension. 
    - crest: `all` submits all files with the .xyz extension. 

- **-n**: Number of cores; must be an integer.
- **-m**: Memory in MB (e.g., 4096mb) or GB (e.g., 1gb); must be an integer that ends with mb
- **-t**: Runtime in the format ##d##h##m##s. A maximum of 2 digits for each input of days, hours, minutes, and seconds is permitted. For example, to specify a walltime of 1 day and 1 hour, you can enter `1d1h` or `25h`.
- **-p**: Program (g16, python, orca5, orca6, crest, or mobcal)
- **-a**: Account type (def or rrg)
    - def is for the default allocation
    - rrg is for dedication queue awards from the RAC competition. 

**Optional arguements only for ORCA calculations only (-p orca5 or orca6)**
- **-temp**: Work in a temporary directory via the local node storage of compute canada/DRAC clusters [optional: defaults to true]. For details, see https://docs.alliancecan.ca/wiki/Using_node-local_storage
    - true (default): Runs ORCA calculations using the local node storage of compute canada/DRAC clusters. 
    - false: Runs ORCA calculations on the directory where the .inp file is located. 

**CREST submissions**
- It is reccomended that you run each CREST job in separate directories, as CREST outputs uniquue conformers to a filename with the same prefix. 
- Note that `CREST` is an external package that requires `xtb` from the following links [xtb](https://xtb-docs.readthedocs.io/en/latest/setup.html) and [CREST](https://crest-lab.github.io/crest-docs/page/installation).
- Note also that subSLURMs core operation limits the user input for CREST to the default `gfn2` semi-empirical method and defining a charge of +1. If alternatives are needed, you will need to edit the code manually at the following line:

```python
#######   CREST    #######
elif sub_info['program'] == 'crest':
    sh_file.write(f'\nsrun crest {file_name} --gfn2 -T {sub_info["ncores"]} --chrg 1\n\n')
```

### Examples
For submitting one file using 4 cores, 4096mb (4GB) per core, 2h walltime, calling g16 on the default account:
```bash
subSLURM my_calculation.gjf -n 4 -m 4096mb -t 2h -p g16 -a def
```

For submitting all files with a .inp extension (calling ORCA) using 8 cores, 4096mb per core, 1day12h walltime, on the dedicated allocation (RRG) while bypassing the default for working in the local node storage :
```bash
subSLURM all -n 8 -m 4096mb -t 1d12h -p orca -a rrg -temp false
```

### Customization
#### Changing Account Credentials
If you belong to a different group or have different account credentials, you will need to modify the script to reflect your account details. Look for the section marked with !!!!!!!!!!!!!!!!!!!!!!!!! in the code, and update the account information with your Compute Canada information.

#### Adding support for other file types
To add support for other programs, extend the `extension_map` dictionary,  add the necessary conditional blocks in the submit_file function, and populate that block with the information necessary to make the SLURM .sh file.

