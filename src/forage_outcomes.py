from random import randint
from collections import namedtuple
from ConstantData import Constants
import support_functions

def randomize_npc():
    return Constants.NPCS[randint(0,len(Constants.NPCS)-1)]
    
EventMessage = namedtuple('EventMessage','text type reward')
ItemReward = namedtuple('ItemReward','item_id quantity')
text_only_events = {
    EventMessage("{creature_name} darts off suddenly, they poke their head out of a nearby bush with a large bug in their mouth.  "\
    "Before anyone can react, they chomp it down. Well, at least they aren't picky.","text",None) : "0.07692307693",
    EventMessage("{creature_name} thinks today is a beautiful day.  Time for mischief!","text",None) : "0.07692307693",
    EventMessage("{creature_name} stares off into the distance, existential crisis or bug?  Only they know for sure","text",None) : "0.07692307693",
    EventMessage("{creature_name} begins to wiggle and hum, soon they're throwing "\
                 "themselves in a wild jumping dance as they scream at the "\
                 "top of their lungs, the song of their people. I'm sure someone enjoys it.","text",None) : "0.07692307693",
    EventMessage("{creature_name} chitters and hisses, looking rather unsure before "\
                "swatting at an odd looking item.  Before anyone can stop them, they swat "\
                "it hard into a puddle, oh well, hopefully it wasn't anything important.","text",None) : "0.07692307692",
    EventMessage("{creature_name} wanders off for a few minutes and comes back with a wet streak on their face. Someone had a sippy sip!","text",None) : "0.07692307692",
    EventMessage("{creature_name} grabs a small fuzzy worm near by and flings their head,"\
                 "throwing the worm into the distance before rushing after it.  "\
                 "They return and repeat the process until collapsing on the ground happily."\
                 "The worm hurries and scoots away. Be free, little worm!","text",None) : "0.07692307692",
    EventMessage("{creature_name} suddenly stops and looks embarrassed, as a stink begins to grow around them. DUDE! What did they eat?!","text",None) : "0.07692307692",
    EventMessage("A fly buzzes around annoyingly. Shoo Fly, don't bother me!","text",None) : "0.07692307692",
    EventMessage("A flash of lightning cracks the sky overhead, followed "\
                 "closely by a rumble of thunder before rain swiftly begins falling. "\
                 "Seems Tyzxyn may have angered Ysies again.","text",None) : "0.07692307692",
    EventMessage("A small shrine to Zarobs sits by the trail, a perfect place to sit and relax in the sun.","text",None) : "0.07692307692",
    EventMessage("Oh my! Something shiny lays on the ground, is it a bauble? Treasure? "\
                 "A crystal? Oh, no it's just a rock, that someone slobbered on? Ewwww!","text",None) : "0.07692307692",
    EventMessage("Someone seems to have come through here, their foot prints are deep and weird, "\
                 "maybe it's best not to hang around and find out what left these!","text",None) : "0.07692307692",
}

currency_events = {
    EventMessage("While walking along {creature_name} stops suddenly and starts chasing their tail!  "\
                "Oh, seems there's something stuck to it!  They found {amount} baubles stuck to their butt!"
                ,"currency",randint(1,5)) : ".4",
    EventMessage("{creature_name} cocks their head and stands perfectly still, listening. Suddenly "\
                 "a squirrel above begins chittering and throwing shiny objects and acorns down on them. "\
                 "You find {amount} baubles among the debris."
                ,"currency",randint(1,5)) : ".4",
    EventMessage("{creature_name} digs a small hole, uncovering a small bag with {amount} baubles in it."
                ,"currency",randint(5,10)) : ".1",
    EventMessage("{creature_name} darts up a near by log and leaps to the top of a rock, pulling "\
                 "in the pile of baubles that a lesser chorumfur would have missed."
                ,"currency",randint(5,10)) : ".1",
}
# will likely be supplanted by an imported Event
event_currency_events = {
    EventMessage("{creature_name} wanders deeper into the forest then they'd normally do, "\
                 "enjoying the change of season as bird song begins to fill the world once more. "\
                 "They are distracted as they walk, suddenly finding themselves amongst a "\
                 "patch of clovers, delightedly picking {amount} with four leaves from the patch.",
                 "event_curr",randint(1,5)) : ".25",
    EventMessage("A lovely patch of clovers stands glistening in the morning dew as the sun "\
                 "peaks the horizon, {creature_name} manages to find {amount} {curr_name} "\
                 "in the patch with four leaves! They pluck them quickly and rush "\
                 "back to their stash, sure Aoltl would be pleased.",'event_curr',randint(2,5)) : ".25",
    EventMessage("Something green sits in the road ahead, looks like someone had "\
                 "the bad luck to drop their clovers, what a lucky day for {creature_name}!",'event_curr',randint(1,3)) : ".25",
    EventMessage("{creature_name} doesn't get far before they find a large patch of "\
                 "clovers, among them {amount} with four leaves.  They pick them up, "\
                 "but that seems to be all the luck they have for now, returning "\
                 "home with a small bunch of clovers for their stash",'event_curr',randint(3,5)) : ".25",

}

npc_events = {
    EventMessage("A small blue pup runs up to {creature_name}, bouncing in excitement as they make a small spin, "\
                 "yelling 'For real life?!' They don't wait for an answer, instead "\
                "running off after a dragonfly, giggling the whole time.","text",None) : ".25",
    EventMessage("Beans and Rice sit facing each other in a beam of light, without "\
                "warning they leap in the air and beginning dancing to a music only "\
                "they can hear. {creature_name} decides it's best to leave them alone for now, they "\
                "probably wouldn't want to be bothered anyway.","text",None) : ".25",
    EventMessage("Ruma sits outside their nook, organizing their crystals. They turn "\
                 "to look at who's coming, before wrapping around their treasures "\
                 "jealously as they watch {creature_name} move on.","text",None) : ".25",
    EventMessage("{random_npc} charges up to {creature_name}.  They begin to play, and suddenly "\
                 "the other chorumfur starts growling and hissing, before charging off again. Odd.","text",None) : ".25",
}

lure_events = {
    EventMessage("A wild chorumfur joins your lair!","lure",None) : "1"
}

# I think both of these will eventually be supplanted by an imported Event
event_special_a_events = {
    EventMessage("The sky is full of stars above, shooting stars flying across the "\
                 "blanket of calm peaceful night. Silhouetted against the stars a "\
                 "small black shape sits, staring longingly at the scene overhead. "\
                 "{creature_name} feels peaceful, yawning and stretching before "\
                 "they curl up for a well deserved sleep.  When they wake up, a "\
                 "small stone sits by their head, the color of the night and stars.",'item',ItemReward(31,1)) : ".25",
    EventMessage("A thin chorumfur stands in the path . . . no, not a chorumfur, it "\
                 "has no horns! It shimmers with a pelt of stars as a milky white "\
                 "and a night black eye turns towards you, the weasel like creature "\
                 "grins at {creature_name}, and disappears. Rushing forward, "\
                 "{creature_name} finds {amount} {curr_name}.",'event_curr',randint(3,5)) : ".25",
    EventMessage("{creature_name} steps along, when a rustling to their right "\
                 "draws their attention.  Ahead, a thin wispy tail disappears into the bush "\
                 "calling for them to follow. As they travel through the brush, they "\
                 "step out on a golden paved road.  A large ruin stands ahead "\
                 "but it's too late, time to turn back for the night.","text",None) : "0.25",
    EventMessage("{creature_name} stops, turning their head to the left before darting "\
                 "into the bush after a quiet laughter. They find nothing living, "\
                 "but instead a pot of clovers. They scoop them up and return to "\
                 "the path confused by what just happened.",'event_curr',randint(5,10)) : ".25",
}

event_special_b_events = {
    EventMessage("The cold winds of the season blow, ruffling {creature_name}'s fur "\
                 "and chilling noses, but suddenly a warmer breath, as if exhaled "\
                 "from a great being passes over, dismissing the cold harsh season "\
                 "with a honeysuckle scented gust.","text",None) : ".25",
    EventMessage("Two large eyes stare out from the greenery, sparkling in the long "\
                 "reptilian face, before blinking out of existence in an explosion of "\
                 "flowers and feathers. {creature_name} decides that's enough "\
                 "adventuring for now, and returns home. ","text",None) : ".25",
    EventMessage("Ahead on the road {creature_name} hesitates, watching a large "\
                 "furred creature run a golden scaled paw over it's head, slicking "\
                 "back large ornamental feathers.  The entity laps a tongue over "\
                 "its' paw, about to repeat the gesture when they stop, tongue "\
                 "extended, and turn. In a whirl of flowers, leaves and warm air "\
                 "it disappears, leaving {creature_name} alone, with the undeniable "\
                 "knowledge that the Gods do in fact blep.","text",None) : ".25",
    EventMessage("{creature_name} sets out earlier than usual, looking to get a "\
                 "head start in the day's adventure.  Walking with a tune in their "\
                 "heart and a bounce in their step.  They stop suddenly, realizing "\
                 "the forest around them has come to life in the short time they've "\
                 "travelled. Where the trees were bare and dead in their torpor, "\
                 "they now bear the green of new growth.","text",None) : ".25"
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

if __name__ == '__main__':
    types_dict = {'text_event':0,'event_curr':0,'npc_event':0,'currency_event':0,'lure_event':0,'event_special_a':0,'event_special_b':0}
    for i in range(1000):
        event_type = support_functions.roll_random_result(outcome_types)
        types_dict[event_type] += 1
    print(types_dict)