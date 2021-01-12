""" terms and soil types """

# conversion table for common alternate spellings or terms.
BASE_TYPES = {
    "gravelly": "gravel",
                "gravels": "gravel",
                "sandy": "sand",
                "sands": "sand",
                "silty": "silt",
                "silts": "silt",
                "clayey": "clay",
                "clays": "clay",
                "water bearing": "wet",
                "water": "wet",
}

# terms commonly used for primary soil types.
# they can also be used for secondary types in the form "SAND and GRAVEL",
# which the `determine_primary` function accounts for.
PRIMARY_TERMS = [
    "gravel",
    "sand",
    "clay",
    "silt",
    "hardpan",
    "soil",
    "bedrock",
    "muskeg",
    "topsoil",
    "mudstone",
    "granite",
    "conglomerate",
    "granodiorite",
    "basalt",
    "sandstone",
    "shale",
    "boulders",
    "cobbles",
    "gravels",
    "mud",
    "till",
    "rock",
    "gneiss",
    "quartz",
    "quartzite",
    "limestone",
    "pebbles",
    "organics",
    "volcanics",
    "feldspar"
]

# these terms have modifiers and indicate they are secondary materials
# note: secondary is used to describe any and all soil that appears after the primary
# type (in other words, there may be at most one primary and one or more secondary types).
SECONDARY_TERMS = [
    "sandy",
    "gravelly",
    "silty",
    "clayey",
    "some sand",
    "some gravel",
    "some silt",
    "some clay",
    "trace sand",
    "trace gravel",
    "trace silt",
    "trace clay",
]

# these terms are associated with bedrock
CONSOL_BEDROCK_TERMS = [
    "bedrock",
    "mudstone",
    "granite",
    "conglomerate",
    "granodiorite",
    "basalt",
    "sandstone",
    "shale",
    "rock",
    "gneiss",
    "quartz",
    "quartzite",
    "limestone",
    "pebbles",
    "volcanics",
    "feldspar"
]

# these terms are associated with unconsolidated soil.
UNCONSOL_SOIL_TERMS = [
    "gravel",
    "sand",
    "clay",
    "silt",
    "hardpan",
    "soil",
    "muskeg",
    "topsoil",
    "mud",
    "till",
    "organic",
    "boulder",
    "cobble"
]

# these terms indicate the consistency of the material
# this is a mix of terms used for coarse grained and fine grained soils.
CONSISTENCY_TERMS = [
    "loose", "soft", "firm", "compact", "hard", "dense"
]

# these terms indicate moisture.  Since it is commonplace to use non-standard
# terms like "water bearing", some of these terms may appear in the BASE_TYPES map
# to be converted to a standard term.
MOISTURE_TERMS = [
    "very dry", "very wet", "water bearing", "water", "dry", "damp", "moist", "wet"
]
