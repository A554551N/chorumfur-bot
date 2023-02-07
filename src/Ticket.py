from datetime import datetime
from ConstantData import Constants
from Breeding import Breeding

class Ticket:
    """Implements a breeding order and methods for managing breeding orders
    Parameters
    ----------
    id INTEGER - ticket ID from the database
    name STRING - Friendly name for ticket
    requestor USER - user object of user who requested breeding
    ticket_date DATETIME - datetime when ticket was instantiated
    status STRING - indicator of ticket's current status
    creature_a CREATURE - Creature object representing parent A
    creature_b CREATURE - Creature object representing parent B
    """

    def __init__(self,ticket_name,ticket_requestor,creature_a,creature_b,
                 ticket_id=None,ticket_date=datetime.today(),ticket_status=Constants.TICKET_STATUS[1],
                 parents_of_a=None,parents_of_b=None,pups=None):
        self.id = ticket_id
        self.name = ticket_name
        self.requestor = ticket_requestor
        if isinstance(ticket_date,str):
            self.ticket_date = datetime.strptime(ticket_date,Constants.DATETIMEFORMAT)
        else:
            self.ticket_date = ticket_date
        self.status = ticket_status
        self.creature_a = creature_a
        self.creature_b = creature_b
        self.parents_of_a = parents_of_a
        self.parents_of_b = parents_of_b
        self.pups = pups

    def output_ticket(self):
        """returns a formatted string with ticket details"""
        return f"Ticket #{self.id} - {self.name}\n"\
              f"Requesting User: <@{self.requestor.userId}>\n"\
              f"Open Date: {self.ticket_date}\n"\
              f"Status: {self.status}\n"\
              f"Parent A: {self.creature_a.creatureId}-{self.creature_a.name}\n"\
              f"Parent B: {self.creature_b.creatureId}-{self.creature_b.name}\n"

    def perform_breeding(self):
        """Creates a Breeding object and performs breeding, returns an array of pups
        and updates Ticket object pups."""
        requested_breed = Breeding(creature_a=self.creature_a,
                                   creature_b=self.creature_b,
                                   new_creature_owner=1)
        self.pups = requested_breed.breed()
        return self.pups

    def output_detailed_ticket(self):
        """Outputs a detailed ticket for the #breeding-tickets channel"""
        output=self.output_ticket()+"\n------------\n"
        for pup in self.pups:
            output+=pup.outputCreature(output_all=True)[0]
            output+="----------------------\n"
        return output

    def requestor_can_breed(self):
        """Confirms that at least one creature is owned by the Requestor and
        confirms that user account is able to breed.
        Also confirms that all creatures involved are adults.
        Returns True if checks pass, or False and an error message if checks fail."""
        can_breed = True
        breed_error = "No Error"
        if self.creature_a.owner != self.requestor.userId and self.creature_b.owner != self.requestor.userId:
            can_breed = False
            breed_error = "You must own at least one of the creatures in the pairing."
        elif self.requestor.breedingLevel() != 5:
            can_breed = False
            breed_error = "Your breeding crystal is not full.  Use `.crystal` to "\
                          "see when you can breed again."
        elif self.creature_a.creatureId == self.creature_b.creatureId:
            can_breed = False
            breed_error = "You cannot breed a creature with itself."
        elif (self.creature_a.calculate_age().days < 15 and self.creature_a.generation != 0) or (self.creature_b.calculate_age().days < 15  and self.creature_b.generation != 0):
            can_breed = False
            breed_error = "Both creatures in the pairing must be adults."
        elif (self.requestor.is_breeding_pending):
            can_breed = False
            breed_error = "You are currently awaiting a response to a pending breeding,"\
            " no new breeding requests can be generated while one is pending.  If you would like to "\
            "cancel your existing request, use `.decline <ticket #> and then try again.`"
        return (can_breed,breed_error)

    def requestor_owns_both(self):
        """Confirms that the user owns both creatures and returns True if checks pass."""
        if self.creature_a.owner == self.requestor.userId and self.creature_b.owner == self.requestor.userId:
            return True
        return False
    def other_user(self):
        """Checks owners of both creatures and returns the ID of the user
        who is not the requestor"""
        if self.creature_a.owner != self.requestor.userId:
            return self.creature_a.owner
        return self.creature_b.owner

    def update_ticket_status(self,new_status_code):
        """Takes in a status code and updates the ticket_status parameter to match"""
        self.status = Constants.TICKET_STATUS[new_status_code]

#if __name__ == '__main__':

