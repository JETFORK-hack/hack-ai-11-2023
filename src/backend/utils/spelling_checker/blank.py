import re


# Create dummy char for russian йё
char2idx_1 = re.compile(r"[йЙ]")
char2idx_2 = re.compile(r"[ёЁ]")
idx2char_1 = re.compile(r"<p>99</p>")
idx2char_2 = re.compile(r"<p>98</p>")

# Greek prefixes replacements
greek_replacer = {
    "ω-": "omega-",
    "β-": "beta-",
    "α-|ά-": "alpha-",
    "γ-": "gamma-"
}

# Greek characters replacements
greek_mapper = {
    "ω": "w",
    "β": "b",
    "α": "a",
    "ά": "a",
    "ß": "b",
    "œ": "e",
    "μ": "m",
    "∂": "d",
    "ι": "i",
    "ð": "d",
    "ø": "o",
    "γ": "y",
    "æ": "ai"
}

# Regexps for preprocessing
broken_hyphen = re.compile(r"-(?= )|-(?=$)|(?<=^)-|(?<= )-|(?<=\d)(-|\.)(?=\d)")

apostrophe = re.compile(r"[`’´]+")
multiple_in_one = re.compile(r"(?<=[0-9])([ ]*|-)(в|in)([ ]*|-)(?=1)")
colon_regex = re.compile(r"(?<=\d):|:(?=\d)")
ends_regex = re.compile(r"'(?=\w( |$))")
amp_regex = re.compile("(?<! )&(?! )")
final_regex = re.compile(r"[^ a-zа-яйё0-9!&'._|\-+:]")
concatenated_sent = re.compile(r"(?<=\w\w\w)[\.!:]|(?:^| )[!#$%\'._|\-+:](?:$| )")
multiple_dots = re.compile(r"[\.]{2,}")
space_regex = re.compile(r" +")
