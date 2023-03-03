from random import randint
from collections import namedtuple
from ConstantData import Constants

def randomize_npc():
    return Constants.NPCS[randint(0,len(Constants.NPCS)-1)]
    
EventMessage = namedtuple('EventMessage','text type reward')
text_only_events = {
    EventMessage("{} darts off suddenly, they poke their head out of a nearby bush with a large bug in their mouth.  "\
    "Before anyone can react, they chomp it down. Well, at least they aren't picky.","text",None) : ".125",
    EventMessage("{} thinks today is a beautiful day.  Time for mischief!","text",None) : ".125",
    EventMessage("{} stares off into the distance, existential crisis or bug?  Only they know for sure","text",None) : ".125",
    EventMessage("{} begins to wiggle and hum, soon they're throwing "\
                 "themselves in a wild jumping dance as they scream at the "\
                 "top of their lungs, the song of their people. I'm sure someone enjoys it.","text",None) : ".125",
    EventMessage("{} chitters and hisses, looking rather unsure before "\
                "swatting at an odd looking item.  Before anyone can stop them, they swat "\
                "it hard into a puddle, oh well, hopefully it wasn't anything important.","text",None) : ".125",
    EventMessage("{} wanders off for a few minutes and comes back with a wet streak on their face. Someone had a sippy sip!","text",None) : ".125",
    EventMessage("{} grabs a small fuzzy worm near by and flings their head,"\
                 "throwing the worm into the distance before rushing after it.  "\
                 "They return and repeat the process until collapsing on the ground happily."\
                 "The worm hurries and scoots away. Be free, little worm!","text",None) : ".125",
    EventMessage("{} suddenly stops and looks embarrassed, as a stink begins to grow around them. DUDE! What did they eat?!","text",None) : ".125",
}

currency_events = {
    EventMessage("While walking along {} stops suddenly and starts chasing their tail!"\
                "Oh, seems there's something stuck to it!  They found {} baubles stuck to their butt!"
                ,"currency",randint(1,5)) : "1"
}
# will likely be supplanted by an imported Event
event_currency_events = {
    EventMessage("You got 1 {}!","event_curr",1) : "1"
}

npc_events = {
    EventMessage(f"{randomize_npc()} does a thing!","text",None) : "1"
}

lure_events = {
    EventMessage("A wild chorumfur joins your lair!","lure",None) : "1"
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
    "currency_event" : ".15",
    "lure_event" : ".05",
    "event_special_a" : ".05",
    "event_special_b" : ".05"
}

outcome_subtypes = {
    "text_event" : text_only_events,
    "event_curr" : event_currency_events,
    "npc_event" : npc_events,
    "currency_event" : currency_events,
    "lure_event" : lure_events,
    "event_special_a" : event_special_a_events,
    "event_special_b" : event_special_b_events
}