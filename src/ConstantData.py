class Constants:
    DATETIMEFORMAT='''%Y-%m-%d %H:%M:%S.%f'''
    DATEONLYFORMAT='%Y-%m-%d'
    MAIN_HORN = {
        1 : ("Standard",70),
        2 : ("Alpine Goat",10),
        3 : ("Sheep 1",5),
        4 : ("Sheep 2",5),
        5 : ("Bighorn",2),
        6 : ("Water Buffalo",2),
        7 : ("Kudu",2),
        8 : ("Bison",2),
        9 : ("Wildebeest",2),
        10 : ("Jacobs",0)
    }
    CHEEK_HORN = {
        1 : ("Standard",70),
        2 : ("Nilgai",10),
        3 : ("Mountain Goat",5),
        4 : ("Impala",5),
        5 : ("Blackbuck",2),
        6 : ("Saiga",2),
        7 : ("Gerrenok",2),
        8 : ("Bongo",2),
        9 : ("Sitatunga",2),
        10 : ("Jacobs",0)
    }
    FACE_HORN = {
        1 : "Standard",
        2 : "Long",
        3 : "None",
        4 : "Black Rhino",
        5 : "White Rhino",
        6 : "Indian Rhino",
        7 : "Double Standard",
        8 : "Sumatran Rhino",
        9 : "Centrosaurus",
        10 : "Wooly Rhino",
        11 : "Spiral",
        12 : "Curled",
        13 : "Forked"
    }
    TAIL = {
        1 : "Standard",
        2 : "Long",
        3 : "Short",
        4 : "Nub",
        5 : "Feather",
        6 : "None",
        7 : "Curled"
    }
    TAIL_TIP = {
        1 : "Standard (Feather)",
        2 : "Paradise (Feather)",
        3 : "Long (Feather)",
        4 : "Trimmed (Feather)",
        5 : "Peacock (Feather)",
        6 : "Contour (Feather)",
        7 : "Semiplume (Feather)",
        8 : "Pinnately Lobed (Leaf)",
        9 : "Linear (Leaf)",
        10 : "Ovate (Leaf)",
        11 : "Obovate (Leaf)",
        12 : "Sagittate (Leaf)",
        13 : "Lanceolate (Leaf)",
        14 : "Palmately Lobed (Leaf)",
        15 : "Reniform (Leaf)"
    }
    FLUFF = {
        1 : "Standard",
        2 : "Long",
        3 : "Short",
        4 : "None",
        5 : "Angora",
        6 : "Curly",
        7 : "Wavy"
    }
    MUTATION = {
        1 : "Back Spines",
        2 : "Tail Spines",
        3 : "Dwarfism",
        4 : "Long Ears",
        5 : "Short Ears",
        6 : "Wings",
        7 : "Saber Fangs",
        8 : "Claws",
        9 : "Kirin Scales",
        10 : "Extra Feathers",
        11 : "Mane"
    }
    CHANCE_TO_PASS_TRAITS = 25
    GRANDPARENT_ADD_TRAITS = 15
    CHANCE_TO_PASS_MUTATION = 10
    CHANCE_TO_ADD_MUTATION = 1
    MAX_LITTER_SIZE = 4
