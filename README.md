### Walking dinner

Walking dinner is an event where participants are assigned a pair, and each pair needs to cook either an entrée, a main dish or a dessert for two other pairs. Then pairs visit each other and eat every dish in different company. For a walking dinner to work perfectly, you need at least 18 participants = 9 pairs. Currently, this is the minimum number of participants supported.

### Input

You need to input a .csv file with the following columns:

- Name
- Contact
- Diet
- Location (Optional, see below)

The name, contact information and diet of participants will be recorded in the result file, but do not affect pairing.

### Usage

#### Required software

First, you need Python 3.x (This was written on version 3.6.1). Then you need to install a Python library called numpy, e.g. ```pip install numpy```. That should do it!

#### Running the script

You need to have all the scripts in the same folder. The script can be run from the command line like this:
```python walking_dinner.py input_file.csv output_file.csv```