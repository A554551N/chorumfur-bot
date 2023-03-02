from random import randint
from collections import namedtuple
from ConstantData import Constants

def randomize_npc():
    return Constants.NPCS[randint(0,len(Constants.NPCS)-1)]
    
EventMessage = namedtuple('EventMessage','text type reward')
text_only_events = {
    EventMessage("This is sample text event A","text",None) : ".5",
    EventMessage("This is sample text event B","text",None) : ".5"
}
# will likely be supplanted by an imported Event
event_currency_events = {
    EventMessage("You got 1 event currency!","event_curr",1) : "1"
}

npc_events = {
    EventMessage(f"{randomize_npc()} does a thing!","text",None) : "1"
}

lure_events = {
    EventMessage("A wild chorumfur joins your lair!","lure","ID#HERE") : "1"
}

# I think both of these will eventually be supplanted by an imported Event
event_special_a_events = {
    EventMessage("This is a Special A event","special",None) : "1"
}

event_special_b_events = {
    EventMessage("This is a Special B event","special",None) : "1"
}

outcome_types = {
    "text_event" : ".25",
    "event_curr" : ".25",
    "npc_event" : ".2",
    "lure_event" : ".1",
    "event_special_a" : ".1",
    "event_special_b" : ".1"
}

outcome_subtypes = {
    "text_event" : text_only_events,
    "event_curr" : event_currency_events,
    "npc_event" : npc_events,
    "lure_event" : lure_events,
    "event_special_a" : event_special_a_events,
    "event_special_b" : event_special_b_events,
}