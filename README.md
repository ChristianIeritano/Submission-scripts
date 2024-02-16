# Submission scripts
 Useful scripts for submitting jobs to HPC resources like Compute Canada.

## subSLURM
This Python script automates the job submission process on Compute Canada systems for Gaussian (g16), Python (.py), and ORCA (.inp) files. 

### Prerequisites 
- Python 3.10 or higher
    - Add the following line to the bottom of your bash profile to ensure python is globally available:
    ```bash
    module load python/3.10.2
    ```
- Access to a Compute Canada facility with a valid account
- Module availability for Gaussian (g16), Python, or ORCA. It is your responsbility to ensure these programs are available on the specific cluster. To check this use the commands:
    ```bash
    module spider G16
    module spider python
    module spidr orca
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
    - orca: `all` submits all files with a .inp extension. 
- **-n**: Number of cores; must be an integer.
- **-m**: Memory in MB (e.g., 4096mb); must be an integer that ends with mb
- **-t**: Runtime in the format ##-##:## (days-hours:minutes). A maximum of 2 digits for each input of days, hours, and minutes is permitted.
- **-p**: Program (g16, python, or orca)
- **-a**: Account type (def or rrg)
    - def is for the default allocation
    - rrg is for dedication queue awards from the RAC competition. 

### Examples
For submitting one file using 4 cores, 4096mb per core, 2h walltime, calling g16 on the default account:
```bash
subSLURM my_calculation.gjf -n 4 -m 4096mb -t 0-2:0 -p g16 -a def
```

For submitting all files with a .inp extension (calling ORCA) using 8 cores, 4096mb per core, 1day12h walltime, on the dedicated allocation (RRG):
```bash
subSLURM all -n 8 -m 4096mb -t 1-12:0 -p orca -a rrg
```

### Customization
#### Changing Account Credentials
If you belong to a different group or have different account credentials, you will need to modify the script to reflect your account details. Look for the section marked with !!!!!!!!!!!!!!!!!!!!!!!!! in the code, and update the account information with your Compute Canada information.

#### Adding support for other file types
To add support for other programs, extend the `extension_map` dictionary,  add the necessary conditional blocks in the submit_file function, and populate that block with the information necessary to make the SLURM .sh file.

### License
This script is provided as is; feel free to use and modify it as you see fit. 