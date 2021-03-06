### Walking dinner

Walking dinner is an event where participants are assigned a pair, and each pair needs to cook either an starter, a main dish or a dessert for two other pairs. Then pairs visit each other and eat every dish in different company. For a walking dinner to work perfectly, you need at least 18 participants = 9 pairs. Currently, this is the minimum number of participants supported.


### Usage

#### Required software

First, you need Python 3.x (This was written on version 3.6.1). Then you need to install two Python libraries called numpy and pandas, e.g. ```pip install numpy``` and ```pip install pandas```. That should do it!

#### Input

You need to input a .csv file (e.g. Excel and Google Sheets can save spreadsheets as csv) with the following columns:

- Name
- Contact
- Diet
- Location (Optional, see below)

The name, contact information and diet of participants will be recorded in the result file, but do not affect pairing.

#### Running the script

You need to have all the scripts in the same folder. The script can be run from the command line like this:

```python walking_dinner.py input_file.csv output_file.csv```

The script can take 3 command line parameters, of which 2 are required.

- input file path, always the first argument
- desired output file path, the second argument
- An optional -l or --location flag, indicating that location should be used in pair matchmaking (see below)

So adding the -l flag to the previous command:

```python walking_dinner.py input_file.csv output_file.csv -l```
OR
```python walking_dinner.py input_file.csv output_file.csv --location```

would use location in the matchmaking

#### Matchmaking

Matchmaking (= creating pairs) can be done completely by random (the default) or by using their location. This functionality was developed for events which are meant to be held in a specific location, such as a university campus. In this case, participants need to be classified into 3 groups: "Far", "Near" and "In", indicated in the Location column of the input file. How you choose to define these groups is of course up to you (you can only use 2 of them if you wish). 

If location is used, participants will be mathced so that in every pair at least one of the participants lives in the desired location or near it, if possible. This will decrease the need for transportation between meals. 

In the probable case that the number of participants is not divisible by 6 (the number of pairs always needs to be divisible by 3), some pairs will be turned into a group of three. The larger groups will be primarily assigned main courses, since they usually require more labour.

#### Output

The output file is a .csv file with 6 columns:

- Names
- Contact
- Diet
- Starter
- Main
- Dessert

The first three columns contain combined information of the participants in the pair/group. The last columns tell which pair is hosting them at which meal. For example, a pair with the following columns:

Starter          Main  Dessert

Donald & Enrique host  Angela & Emmanuel

would be hosted at starter by Donald and Enrique, cook main course themselves and finish the evening with a dessert made by Angela & Emmanuel.

Participants can use the output file to contact with each other and agree where they should cook/meet.

#### Testing

Test data and a sample result file are provided in the ```/data``` folder. The result file has been generated by running the following command in the repository main folder:

```python src/walking_dinner.py data/test_data.csv data/test_results.csv -l```

Note that since the matchmaking is randomized, you can (and probably will) get different results with the test data everytime the script is run.