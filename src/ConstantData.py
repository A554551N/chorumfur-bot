class Constants:
    DATETIMEFORMAT='''%Y-%m-%d %H:%M:%S.%f'''
    DATEONLYFORMAT='%Y-%m-%d'
    DEFAULT_TRAITS_DICT = {
        'MAIN_HORN' : "",
        'CHEEK_HORN' : "",
        'FACE_HORN' : "",
        'TAIL' : "",
        'TAIL_TIP' : "",
        'FLUFF' : "",
        'MUTATION' : ""
    }
    MAIN_HORN = {
        1 : ("Standard",".92"),
        2 : ("Alpine Goat",".01"),
        3 : ("Sheep 1",".01"),
        4 : ("Sheep 2",".01"),
        5 : ("Bighorn",".01"),
        6 : ("Water Buffalo",".01"),
        7 : ("Kudu",".01"),
        8 : ("Bison",".01"),
        9 : ("Wildebeest",".01"),
        10 : ("Jacobs",0)
    }
    CHEEK_HORN = {
        1 : ("Standard",".92"),
        2 : ("Nilgai",".01"),
        3 : ("Mountain Goat",".01"),
        4 : ("Impala",".01"),
        5 : ("Blackbuck",".01"),
        6 : ("Saiga",".01"),
        7 : ("Gerrenok",".01"),
        8 : ("Bongo",".01"),
        9 : ("Sitatunga",".01"),
        10 : ("Jacobs",0)
    }
    FACE_HORN = {
        1 : ("Standard",".435"),
        2 : ("Long",".23"),
        3 : ("Short",".23"),
        4 : ("Black Rhino",".01"),
        5 : ("White Rhino",".01"),
        6 : ("Indian Rhino",".01"),
        7 : ("Double Standard",".01"),
        8 : ("Sumatran Rhino",".01"),
        9 : ("Centrosaurus",".01"),
        10 : ("Wooly Rhino",".01"),
        11 : ("Spiral",".01"),
        12 : ("Curled",".01"),
        13 : ("Forked",".01"),
        14 : ("None",".005")
    }
    TAIL = {
        1 : ("Standard",".645"),
        2 : ("Long",".16"),
        3 : ("Short",".16"),
        4 : ("Short Curled",".01"),
        5 : ("Long Curled",".01"),
        6 : ("Nub",".005"),
        7 : ("Feather",".005"),
        8 : ("None",".005")
    }
    TAIL_TIP = {
        1 : ("Standard (Feather)",".93"),
        2 : ("Paradise (Feather)",".01"),
        3 : ("Long (Feather)",".01"),
        4 : ("Trimmed (Feather)",".01"),
        5 : ("Peacock (Feather)",".01"),
        6 : ("Contour (Feather)",".01"),
        7 : ("Semiplume (Feather)",".01"),
        8 : ("Pinnately Lobed (Leaf)",".001"),
        9 : ("Linear (Leaf)",".001"),
        10 : ("Ovate (Leaf)",".001"),
        11 : ("Obovate (Leaf)",".001"),
        12 : ("Sagittate (Leaf)",".001"),
        13 : ("Lanceolate (Leaf)",".001"),
        14 : ("Palmately Lobed (Leaf)",".001"),
        15 : ("Reniform (Leaf)",".001"),
        16 : ("Elliptical",".001"),
        17 : ("Truncate",".001")
    }
    FLUFF = {
        1 : ("Standard",".63"),
        2 : ("Long",".155"),
        3 : ("Short",".155"),
        4 : ("Angora",".01"),
        5 : ("Curly",".01"),
        6 : ("Wavy",".01"),
        7 : ("Wavy Long",".005"),
        8 : ("Wavy Short",".005"),
        9 : ("Curly Long",".005"),
        10 : ("Curly Short",".005"),
        11 : ("Angora Long",".005"),
        12 : ("Angora Short",".005")

    }
    MUTATION = {
        1 : ("None",".9986"),
        2 : ("Tail Spines",".0001"),
        3 : ("Dwarfism",".0001"),
        4 : ("Long Ears",".0001"),
        5 : ("Short Ears",".0001"),
        6 : ("Wings",".0001"),
        7 : ("Saber Fangs",".0001"),
        8 : ("Claws",".0001"),
        9 : ("Kirin Scales",".0001"),
        10 : ("Extra Feathers",".0001"),
        11 : ("Mane",".0001"),
        12 : ("Back Spines",".0001"),
        13 : ("Kentosaurus 1",".0001"),
        14 : ("Kentosaurus 2",".0001"),
        15 : ("Floppy Ears",".0001")

    }
    CHANCE_TO_PASS_TRAITS = 25
    GRANDPARENT_ADD_TRAITS = 15
    CHANCE_TO_PASS_MUTATION = 10
    CHANCE_TO_ADD_MUTATION = 1
    MAX_LITTER_SIZE = 4
