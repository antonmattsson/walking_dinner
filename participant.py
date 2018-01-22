
class Participant:
    """
    Class for holding basic participant information
        - name: string
        - diet: string
        - contact: string
    """

    def __init__(self, name, contact, diet):
        self.name = name
        self.diet = diet
        self.contact = contact

    def __str__(self):
        return "Participant object. Name:" + self.name + " Diet:" + self.diet


# Class for pairs
class Pair:
    """
    Class for pairs of participants
        - participants: list of Participant objects
        - starter_host: Pair to visit for starter
        - main_host: Pair to visit for main course
        - dessert_host: Pair to visit for dessert

        one of the host fields is always None, indicating the meal the Pair is cooking themselves
    """

    def __init__(self, participants):
        self.participants = participants
        self.starter_host = None
        self.main_host = None
        self.dessert_host = None

    def __str__(self):
        names_str = ""
        for p in self.participants:
            names_str = names_str + p.name + ", "
        starter = self.starter_host.get_names() if self.starter_host is not None else "host"
        return "Pair object. Participants:" + names_str + "Starter host" + starter

    def get_names(self):
        names = ""
        for participant in self.participants:
            if names != "":
                names += " & "
            names += participant.name
        return names

    def get_info(self):
        """
        Get information about the pair for writing results
        :return: list of strings
        """

        names = self.get_names()
        contacts = ""
        diets = ""
        for participant in self.participants:

            if participant.contact != "":
                if contacts != "":
                    contacts += " & "
                contacts += participant.contact
            if participant.diet != "":
                if diets != "":
                    diets += " & "
                diets += participant.diet

        starter = self.starter_host.get_names() if self.starter_host is not None else "host"
        main = self.main_host.get_names() if self.main_host is not None else "host"
        dessert = self.dessert_host.get_names() if self.dessert_host is not None else "host"

        info = [names, contacts, diets, starter, main, dessert]

        return info
