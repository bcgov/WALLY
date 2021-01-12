"""
Parsing soil visual descriptions from field notes into a Python class
"""
import regex as re

from api.v1.wells.soil_types import PRIMARY_TERMS, SECONDARY_TERMS, CONSOL_BEDROCK_TERMS, UNCONSOL_SOIL_TERMS, BASE_TYPES, CONSISTENCY_TERMS, MOISTURE_TERMS


class Description:
    """ holds information about a soil visual description"""

    def __init__(
        self,
        original,
        primary=None,
        secondary=None,
        ordered=None,
        consistency=None,
        moisture=None
    ):
        self.original = original
        self.primary = primary
        self.secondary = secondary
        self.ordered = ordered if ordered else []
        self.consistency = consistency
        self.moisture = moisture


# unused (for now)
# class Token:
#     def __init__(
#         self,
#         original: str,
#         modifier: str = None,
#         position: int = None,
#         capitalized: bool = None,
#         term: str = None,
#         material_class: str = None
#     ):
#         self.original = original
#         self.modifier = modifier
#         self.position = position
#         self.capitalized = capitalized
#         self.term = term
#         self.material_class = material_class


class SoilToken:
    def __init__(
        self,
        original,
        modifier=None,
        capitalized=None,
        term=None,
        material_class=None
    ):
        self.original = original
        self.modifier = modifier
        self.capitalized = capitalized
        self.term = term
        self.material_class = material_class


def split_words(original: str):
    """ splits up all words into a list, replacing any symbols, punctuation, or excess whitespace """

    processed = re.sub(r"(\p{P}|\s|\$|\+|\^|\|)+", " ", original)
    return processed.split(" ")


def trim_suffix(word, suffix):
    """ trims a suffix from word
        used to remove suffixes like "ly" from "gravelly"
    """


def determine_primary(desc, single_words):
    """
    Try to determine the primary soil type.
    Also picks up secondary soil type if it was styled like another primary type e.g. "SAND and GRAVEL".
    """
    prev = ""
    for word in single_words:
        # determine primary constituent before moving on to other properties
        for term in PRIMARY_TERMS:
            if word in (term, term+"s") and prev not in ["some", "trace"]:
                if not desc.primary and prev not in ("and", "&"):

                    desc.primary = term
                    desc.ordered.insert(0, term)

                # some secondary soil types might come in the form "sand and gravel" (e.g. gravel will be secondary)
                # we can catch these while searching for primary terms
                elif desc.secondary == "":
                    desc.secondary = term
                    desc.ordered.append(term)
                    return (desc, prev)

        prev = word
    return (desc, prev)


def determine_secondary_soil_and_attributes(desc, single_words, prev):
    """ determines secondary soil type(s) along with soil attributes like moisture and consistency. """
    soil = None
    for word in single_words:
        for term in SECONDARY_TERMS:
            if term in (word, prev+" "+word):

                # try to convert, if necessary.
                # if word not in BASE_TYPES, default to using the original word.
                # this means BASE_TYPES didn't have a mapping for the original word;
                # it could be valid as-is or it could be another unknown variation.
                soil = BASE_TYPES.get(word, word)

                # if secondary soil not populated yet, use the current soil.
                if desc.secondary == "":
                    desc.secondary = soil

                desc.ordered.append(soil)

        if not desc.consistency and word in CONSISTENCY_TERMS:
            desc.consistency = word

        if not desc.moisture and (word in MOISTURE_TERMS or prev+" "+word in MOISTURE_TERMS):
            # word was found in list of moisture terms;
            # find a standard moisture term or fall back on the original word
            # from the field description.
            desc.moisture = BASE_TYPES.get(term, term)

        prev = word
    return (desc, prev)


def parse_description(original: str):
    """ Parses a soil visual description in string form
        e.g. parse_description("gravel, sandy, trace silt, wet")
    """

    desc = Description(original, ordered=[])
    single_words = split_words(original)

    prev = ""

    # parsing a description works by brute force - words in the original description
    # are matched against the `terms` map.

    desc, prev = determine_primary(desc, single_words)
    desc, prev = determine_secondary_soil_and_attributes(
        desc, single_words, prev)

    return desc


def classify_soil(word: str, prev: str):
    """ classifies soil into soil (unconsolidated) or bedrock (consolidated) """
    orig = word
    word = word.lower()
    prev = prev.lower()

    if prev not in ("some", "trace", "and"):
        prev = ""

    word_list = [
        (word, prev),
        (trim_suffix(word, "y"), "y"),
        (trim_suffix(word, "ey"), "y"),
        (trim_suffix(word, "ly"), "y"),
    ]

    # try variations of the soil term against unconsolidated (soil) and consolidated (bedrock) terms.
    # warning: as with the other word lists, these word lists may not be complete.
    for test_word in word_list:
        if test_word in UNCONSOL_SOIL_TERMS:
            return SoilToken(
                orig,
                term=test_word[0],
                modifier=test_word[1],
                material_class="soil"
            )
        if test_word in CONSOL_BEDROCK_TERMS:
            return SoilToken(
                orig,
                term=test_word[0],
                modifier=test_word[1],
                material_class="bedrock"
            )
    return SoilToken(
        orig
    )
