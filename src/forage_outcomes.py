from random import randint
from collections import namedtuple
from ConstantData import Constants
import support_functions

def randomize_npc():
    return Constants.NPCS[randint(0,len(Constants.NPCS)-1)]
    
EventMessage = namedtuple('EventMessage','text type reward')
ItemReward = namedtuple('ItemReward','item_id quantity')
ChorumfurReward = namedtuple('ChorumfurReward','storage id')

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
    EventMessage("{creature_name}'s stomach rumbles fiercely as they stop beneath "\
    "a tree, a large green and blue hued bird takes flight from a nest, leaving it "\
    "unguarded. {creature_name} climbs the tree skillfully, keeping an eye out for "\
    "the mother or father before slipping in to crack open a tasty treat.  "\
    "Instead, they discover the contents are weird and colorful. Greed takes hold "\
    "and they snatch the egg up, scurrying home with their prize.\nYou gain one **Painted Egg**",
    "event_curr",1) : ".25",
    EventMessage("Oh no!  A nest has fallen in the middle of the path.  But wait, "\
                 "amongst the smashed eggs is a colorful one, a gift from the ancestors!"\
                "\nYou gain one **Painted Egg**",
                 "event_curr",
                 1) : ".25",
    EventMessage("Something catches {creature_name}'s eye off to the side of the "\
    "road, they approach and find a colorful egg on the ground, cocking their head "\
    "they puzzle at how it got there, before deciding to take it anyways."\
    "\nYou gain one **Painted Egg**",
    "event_curr",
    1) : ".25",
    EventMessage("While they're searching the woods, something falls out of the "\
    "treetops and bonks {creature_name} right on the head!  Looking down, they spot "\
    "a weird colorful egg and take it home with them for daring to hit them in the head."\
    "\nYou gain one **Painted Egg**",
    "event_curr",
    1) : ".25"
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
    EventMessage("{creature_name} approaches a wild chorumfur.","lure",ChorumfurReward(0,None)) : "1"
}

# I think both of these will eventually be supplanted by an imported Event
event_special_events = {
    EventMessage("Bongo Bongos Like He's Never Bongo-ed Before",
                 "text",
                 None) : "odds",
    EventMessage("{creature_name} wanders through the forest, fresh with bright greens"\
                 "and flowering trees, a noise above calls their attention up, "\
                 "the unmistakable form of Ulnran runs chasing what looks like a "\
                 "squirrel? A weasel? Something, that stops momentarily to put down "\
                 "a nest for the returning birds, before scampering off into the "\
                 "higher branches of the canopy.","text",None):".106875",
    EventMessage("{creature_name} sits in the middle of the road, admiring the scenery as the "\
                 "cold harsh sleep of the cold season is replaced with the start "\
                 "of warmth and wakefulness. They blink slowly as a small caterpillar "\
                 "crawls onto their muzzle, inching along. It will be a good warm season.","text",None):".106875",
    EventMessage("{creature_name} stops in their tracks, cocking their head. "\
                 "Someone is talking, but they don't seem to understand the language, "\
                 "though they catch what is said. *'Eraandic goulsht phimnas, urt i kroan, ot tother genine.'* "\
                 "as they sneak forward to find out what is going on, there is no one around, "\
                 "just the songs of birds, and the hum of insects.","text",None):".106875",
    EventMessage("{creature_name} wanders out into the open grasses, heeding the "\
    "sky in case of a bird of prey. They wander a ways, before finding a small nest "\
    "in the tall grass. They crack and devour two of the seven, before snatching up "\
    "a third and scampering back home with a treat for later. They know Urntos would "\
    "be displeased if they took the whole nest and didn't allow the population to grow."\
    "\nYou gain one **Quail Egg**",
    'item',ItemReward(35,1)) : ".0625",
    EventMessage("A small nest of eggs lays on the ground.  It's too early to eat, "\
    "and {creature_name} decides to take one 'for a walk'.\n"\
    "You gain one **Quail Egg**",
    'item',
    ItemReward(35,1)) : ".0625",
    EventMessage("As {creature_name} approaches the edge of the forest, a quail "\
    "squawks and flies out of the brush, leaving her nest unguarded, as a tasty "\
    "meal, and later snack."\
    "\nYou gain one **Quail Egg**",
    "item",
    ItemReward(35,1)) : ".0625",
    EventMessage("An agile weasel bounds from side-to-side along the path.  As if "\
    "sensing they're being watched, the odd-colored beast stops, turning to look "\
    "back at {creature_name} for a moment before smiling gently, holding out what "\
    "they're hiding beside the path. In their paws are {amount} egg(s), and they "\
    "motion for {creature_name} to take them. *'Urt, yr Qruxtiansy, dimney irth yn merti'*"
    "\nYou gain {amount} **Painted Egg(s)**",
    "event_curr",randint(2,3)) : ".0625",
    EventMessage("{creature_name} cocks their head, looking around the area as "\
    "the sounds of laughter and conversation drift through the trees. Two plump "\
    "minks sit in a clearing not far off surrounded by piles of quail, rabbit, and eggs; "\
    "feasting and laughing as they carry on about... something. "\
    "{creature_name} moves to leave the two in peace, only to find a rock at their "\
    "feet. That wasn't there before . . . was it? "\
    "\nYou gain one **Spring Bounty Palette Rock**",
    'item',
    ItemReward(36,1)) : ".0625",
    EventMessage("{creature_name} moves through the forest like the predator they "\
    "are, sliding beneath the brush, keeping to the shadows.  They pounce from "\
    "under an especially lush fern, landing on what they think to be a squirrel "\
    "only to be flipped on their back with a hiss. The odd creature streaks away "\
    "before {creature_name} can stop it, but where the creature had been there is "\
    "a small rock on the ground, camouflaging with the forest around."\
    "\nYou gain one **Hunter's Forest Palette Rock**",
    'item',
    ItemReward(33,1)) : ".0625",
    EventMessage("{creature_name} wanders aimlessly for some time, not sure what "\
    "they are going to do.  Life is pleasureable, it is lovely, the heat of the "\
    "warm season begins to seep into their fur and bones. They stretch out, yawning "\
    "deeply, before curling into a ball. They wake some time later warm and refreshed, "\
    "their head resting on a colorful rock, making them think of the lazy day they just had"\
    "\nYou gain one **Lazy Afternoon Palette Rock**",
    'item',
    ItemReward(37,1)) : ".0625",
    EventMessage("{creature_name} decides to visit the meadow on the edge of the "\
    "forest.  They move up to the edge, marveling at the early blooming flowers.  "\
    "In the middle of the field of flowers the oddly colored weasel **Ulnran** "\
    "throws a stone about, batting it with their paws and coloring it with the "\
    "wildflowers as it hits the petals. Eventually they leave, the foliage trampled "\
    "in the shape of a large flower.  The stone lays there, colored with swirls and petals."\
    "\nYou gain one **Petal Bloom Palette Rock**",
    'item',
    ItemReward(38,1)) : ".0625",
    EventMessage("{creature_name} steps along the path, lost in their own mind "\
    "when suddenly, the blossoms of the trees begin falling in the wind.  They look "\
    "up, just in time to dive out of the way as a stone falls from the sky and "\
    "bounces where their head had just been."\
    "You gain one **Spring Blossom Palette Rock",
    'item',
    ItemReward(39,1)) : ".0625",
    EventMessage("A fluffy squirrel like creature bounds out of the trees tackling "\
    "{creature_name}.  The creature chitters a moment before standing at full height, "\
    "a whole head larger than the largest of Chorumfurs. *'Tother sont ern, prup. "\
    "Radney urt, yr phimnas rymir'* the creature says, before flicking its bushy "\
    "tail, and leaping back into the underbrush. without knowing how, {creature_name} "\
    "knows they've just encountered **Urntos**.  Perhaps the pile of bones they left, "\
    "or the odd appearance gave it away."\
    "\nYou gain one **Pile of Bones**",
    'item',
    ItemReward(40,1)) : ".005",
    EventMessage("A large egg sits off to the side, shining brightly as the warm "\
    "sun filters through the forest canopy sending small rainbows all along the "\
    "forest floor. Something about the egg says that {creature_name} was meant to "\
    "find it, and they go about dragging it back to their nook wondering the whole "\
    "way what it could be.",
    "lure",
    ChorumfurReward(2,None)) : ".0025",
    EventMessage("Waking early, {creature_name} discovers an egg shaped crystal "\
    "outside their nook. As they push it inside they ponder, food, or gift?",
    "lure",
    ChorumfurReward(2,None)) : ".0025"
}

outcome_types = {
    "text_event" : ".27",
    "event_curr" : ".25",
    "npc_event" : ".22",
    "currency_event" : ".15",
    "event_special" : ".10",
    "lure_event" : ".01"
}

outcome_subtypes = {
    "text_event" : text_only_events,
    "event_curr" : event_currency_events,
    "npc_event" : npc_events,
    "currency_event" : currency_events,
    "lure_event" : lure_events,
    "event_special" : event_special_events
}

if __name__ == '__main__':
    types_dict = {'text_event':0,'event_curr':0,'npc_event':0,'currency_event':0,'lure_event':0,'event_special_a':0,'event_special_b':0}
    for i in range(1000):
        event_type = support_functions.roll_random_result(outcome_types)
        types_dict[event_type] += 1
    print(types_dict)