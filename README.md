# JETSCAPE_GRID_MGR

## Run JETSCAPE with Singularity on WSU Grid

Load singularity and apptainer:
```bash
module load singularity
module load apptainer/1.2.2
```

Pull the image for JETSCAPE from Docker Hub

```bash
singularity pull jetbox.sif docker://jetscape/base:stable
```

Test. Shell into the container
```bash
singularity shell /path/to/my/jetbox.sif 
```
or execution with the container
```bash
singularity exec /path/to/my/jetbox.sif command
```
Bind directories
```bash
export APPTAINER_BIND="/wsu, /.rs"
```


## Main Code to Run JETSCAPE on WSU Grid
```python run_jetscape.py```
