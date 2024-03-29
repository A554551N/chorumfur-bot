class Constants:
    DATETIMEFORMAT = '''%Y-%m-%d %H:%M:%S.%f'''
    DATEONLYFORMAT = '%Y-%m-%d'
    VERSION = 'v0.4.4'
    CRYSTAL_CHARGE_DAYS = 18
    FORAGE_COOLDOWN_HOURS = 6
    DEFAULT_TRAITS_DICT = {
        'MAIN_HORN': "",
        'CHEEK_HORN': "",
        'FACE_HORN': "",
        'TAIL': "",
        'TAIL_TIP': "",
        'FLUFF': "",
        'MUTATION': ""
    }
    MAIN_HORN = {
        "Standard": ".92",
        "Alpine Goat": ".01",
        "Sheep 1": ".01",
        "Sheep 2": ".01",
        "Bighorn": ".01",
        "Water Buffalo": ".01",
        "Kudu": ".01",
        "Bison": ".01",
        "Wildebeest": ".01",
        "Jacobs": "0"
    }

    CHEEK_HORN = {
        "Standard": ".30",
        "Standard (Medium)": ".30",
        "Standard (Short)": ".29",
        "Straight": ".01",
        "Straight (Short)": ".01",
        "Straight (Long)": ".01",
        "Nilgai": ".01",
        "Mountain Goat": ".01",
        "Impala": ".01",
        "Blackbuck": ".01",
        "Saiga": ".01",
        "Gerrenok": ".01",
        "Bongo": ".01",
        "Sitatunga": ".01",
        "Jacobs": "0"
    }

    FACE_HORN = {
        "Standard": ".435",
        "Long": ".23",
        "Short": ".23",
        "Black Rhino": ".01",
        "White Rhino": ".01",
        "Indian Rhino": ".01",
        "Double Standard": ".01",
        "Sumatran Rhino": ".01",
        "Centrosaurus": ".01",
        "Wooly Rhino": ".01",
        "Spiral": ".01",
        "Curled": ".01",
        "Forked": ".01",
        "None": ".005"
    }

    TAIL = {
        "Standard": ".645",
        "Long": ".16",
        "Short": ".16",
        "Short Curled": ".01",
        "Long Curled": ".01",
        "Nub": ".005",
        "Feather": ".005",
        "None": ".005"
    }

    TAIL_TIP = {
        "Standard (Feather)": ".93",
        "Paradise (Feather)": ".01",
        "Long (Feather)": ".01",
        "Trimmed (Feather)": ".01",
        "Peacock (Feather)": ".01",
        "Contour (Feather)": ".01",
        "Semiplume (Feather)": ".01",
        "Pinnately Lobed (Leaf)": ".001",
        "Linear (Leaf)": ".001",
        "Ovate (Leaf)": ".001",
        "Obovate (Leaf)": ".001",
        "Sagittate (Leaf)": ".001",
        "Lanceolate (Leaf)": ".001",
        "Palmately Lobed (Leaf)": ".001",
        "Reniform (Leaf)": ".001",
        "Elliptical": ".001",
        "Truncate": ".001"
    }

    FLUFF = {
        "Standard": ".63",
        "Long": ".155",
        "Short": ".155",
        "Angora": ".01",
        "Curly": ".01",
        "Wavy": ".01",
        "Wavy Long": ".005",
        "Wavy Short": ".005",
        "Curly Long": ".005",
        "Curly Short": ".005",
        "Angora Long": ".005",
        "Angora Short": ".005"
    }

    MUTATION = {
        "None": ".9986",
        "Tail Spines": ".0001",
        "Dwarfism": ".0001",
        "Long Ears": ".0001",
        "Short Ears": ".0001",
        "Wings": ".0001",
        "Saber Fangs": ".0001",
        "Claws": ".0001",
        "Kirin Scales": ".0001",
        "Extra Feathers": ".0001",
        "Mane": ".0001",
        "Back Spines": ".0001",
        "Kentosaurus 1": ".0001",
        "Kentosaurus 2": ".0001",
        "Floppy Ears": ".0001"
    }

    TICKET_STATUS = ['On Hold',
                     'New',
                     'Awaiting Confirmation',
                     'Ticket Pending',
                     'Ticket in Progress',
                     'Ready to Birth',
                     'Complete',
                     'Rejected']

    PUP_WEIGHTING = {
        2 : ".40",
        1 : ".25",
        3 : ".25",
        4 : ".10"
    }

    NPCS = (
        "Ruma",
        "Beans",
        "Rice",
        "Spork"
    )

    # PARENT_PASS_TRAITS = 25
    GRANDPARENT_PASS_TRAITS = 15
    CHANCE_TO_PASS_MUTATION = 10
    CHANCE_TO_ADD_MUTATION = 1
    MAX_LITTER_SIZE = 4

    CRYSTAL_IMAGE_STAGES = (
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal.png",
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal1.png",
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal2.png",
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal3.png",
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal4.png",
        "https://chorumfur-bot.s3.us-east-2.amazonaws.com/items/Breeding+Crystal5.png"
    )
