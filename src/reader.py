import csv
from participant import Participant
import sys


class Reader:
    """
    Reader class for the .csv files
    Currently, a minimum number of 18 participants is required
    """

    def __init__(self, file, delimiter=","):
        self.file = file
        self.delimiter = delimiter

    def check_header(self, hdr, location):
        """
        Checks that the header of the file (column names) looks OK, exits if not
        :param hdr: the header as list of strings
        :param location: whether location will be used to create pairs
        :return: None
        """
        hdr_ok = True
        if hdr[0] != "Name":
            hdr_ok = False
            print("First column is not called 'Name'")
        if hdr[1] != "Contact":
            hdr_ok = False
            print("Second column is not called 'Contact'")

        if hdr[2] != "Diet":
            hdr_ok = False
            print("Third column is not called 'Diet'")

        if location:
            if len(hdr) < 4:
                hdr_ok = False
                print("Too few columns!")
            elif hdr[3] != "Location":
                hdr_ok = False
                print("Fourth column is not called 'Location'")
        else:
            if len(hdr) > 3:
                if hdr[3] == "Location":
                    print("Note that location is not used for pairing, you can turn the feature on"
                          " by using the -l or --location flag")


        if not hdr_ok:
            print("Please check the input file")
            sys.exit()

    def read_by_location(self):
        """
        Read the file and create Participant objects
        Group participants into 3 groups based on location
            - far
            - near
            - inda (because they are in da hood, sorry, 'in' is reserved)
        :return: dict with 3 fields, each holding a list of Participant objects
        """

        far = []
        near = []
        inda = []
        with open(self.file) as csv_file:
            rdr = csv.reader(csv_file, delimiter=self.delimiter)
            hdr = next(rdr, None)
            self.check_header(hdr, location=True)
            for row in rdr:
                if row[3] == "Far":
                    far.append(Participant(row[0], row[1], row[2]))
                elif row[3] == "Near":
                    near.append(Participant(row[0], row[1], row[2]))
                else:
                    inda.append(Participant(row[0], row[1], row[2]))
        if (len(inda) + len(far) + len(near)) < 18:
            print("Currently you need to have at least 18 participants!")
            sys.exit()
        participants = {"near": near, "far": far, "inda": inda}

        return participants

    def read_simple(self):
        """
        Read the file and create Participant objects without grouping
        :return: list of Participant objects
        """

        participants = []
        with open(self.file) as csv_file:
            rdr = csv.reader(csv_file, delimiter=self.delimiter)
            hdr = next(rdr, None)
            self.check_header(hdr, location=False)
            for row in rdr:
                participants.append(Participant(row[0], row[1], row[2]))
        if len(participants) < 18:
            print("Currently you need to have at least 18 participants!")
            sys.exit()
        return participants
