from collections import namedtuple
from random import randint

Event = namedtuple('Event','event_name event_currency_name event_currency_id,event_forage_outcomes')
EventMessage = namedtuple('EventMessage','text type reward')
ItemReward = namedtuple('ItemReward','item_id quantity')

march_outcomes = {
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

march_currency_events = {
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

march_event = Event('March Event','Clover',29,march_outcomes)
april_event = Event('Hunt and Feast','Painted Egg',34)