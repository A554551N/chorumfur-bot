from datetime import datetime
from ConstantData import Constants
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

    def __init__(self,ticket_id,ticket_name,ticket_requestor,creature_a,creature_b,
                 ticket_date=datetime.today(),ticket_status='New'):
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

    def output_ticket(self):
        """returns a formatted string with ticket details"""
        print(f"Ticket #{self.id} - {self.name}\n"\
              f"Open Date: {self.ticket_date}\n"\
              f"Status: {self.status}\n"\
              f"Parent A: {self.creature_a.creatureId}-{self.creature_a.name}"\
              f"Parent B: {self.creature_b.creatureId}-{self.creature_b.name}")

    def requestor_can_breed(self):
        """Confirms that at least one creature is owned by the Requestor and
        confirms that user account is able to breed.  Returns True if checks pass"""
        can_breed = True
        if self.creature_a.owner != self.requestor.userId and self.creature_b.owner != self.requestor.userId:
            can_breed = False
        elif self.requestor.breedingLevel() != 5:
            can_breed = False
        return can_breed
    
    def update_ticket_status(self,new_status_code):
        """Takes in a status code and updates the ticket_status parameter to match"""
        self.status = Constants.TICKET_STATUS[new_status_code]
#if __name__ == '__main__':

