import csv
from participant import Participant


# Reader class for the .csv files
# Returns dict of participants with 3 fields based on location
class Reader:

    def __init__(self, file, delimiter=","):
        self.file = file
        self.delimiter = delimiter

    def read_to_objects(self):

        far = []
        near = []
        inda = []
        with open(self.file) as csv_file:
            rdr = csv.reader(csv_file, delimiter=self.delimiter)
            next(rdr, None)
            for row in rdr:
                if row[2] == "Far from Otaniemi":
                    far.append(Participant(*row))
                elif row[2] == "Near Otaniemi":
                    near.append(Participant(*row))
                else:
                    inda.append(Participant(*row))

        participants = {"near": near, "far": far, "inda": inda}

        return participants
