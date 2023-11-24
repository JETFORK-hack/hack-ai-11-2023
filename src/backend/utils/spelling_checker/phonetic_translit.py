import eng_to_ipa as ipa

treegrams_mapper = {
    u"aɪə": u"ио",
    u"cch": u"чч",
    u"cci": u"чи",
    u"eau": u"ью",
    u"ieh": u"и",
    u"ssh": u"ш",
    u"sch": u"ш",
    u"weɪ": u"ью",
    u"you": u"ю",
    u"fum": u"фюм",
    u"æŋk": u"анк",
    u"uge": u"уж",
    u"ɔŋg": u"онг",
    u"jɪr": u"иар",
    u"cqua": u"ква",
    u"and": u"энд",
    u"are": u"а"
}

bigrams_mapper = {
    u"ˌɑ": u"а",
    u"ˈi": u"э",
    u"ˈə": u"у",
    u"zˈ": u"с",
    u"əˈ": u"а",
    u"ˌs": u"ш",
    u"iɑ": u"ио",
    u"ɪə": u"а",
    u"ɔɪ": u"уа",
    u"aɪ": u"aй",
    u"ɛm": u"эм",
    u"ɛs": u"эс",
    u"də": u"дэ",
    u"eɪ": u"ей",
    u"gʒ": u"кш",
    u"oʊ": u"о",
    u"ðə": u"зе",
    u"iɛ": u"ье",
    u"iə": u"йе",
    u"jɑ": u"я",
    u"jɛ": u"е",
    u"jə": u"у",
    u"ay": u"ай",
    u"ck": u"к",
    u"ch": u"ч",
    u"dj": u"дж",
    u"ei": u"ей",
    u"eu": u"о",
    u"ee": u"и",
    u"ew": u"ью",
    u"ie": u"и",
    u"ii": u"йи",
    u"ju": u"ю",
    u"oo": u"у",
    u"sc": u"сц",
    u"ts": u"ц",
    u"th": u"с",
    u"xx": u"кс",
    u"ya": u"я",
    u"yo": u"йо",
    u"yu": u"ю",
    u"zh": u"ж",
    u"ph": u"ф",
    u"sh": u"ш",
    u"ou": u"у",
    u"wɑ": u"ва",
    u"ər": u"ор",
    u"əl": u"ул",
    u"ɑr": u"ар",
    u"ju": u"ью"
}

unigrams_mapper = {
    u"ˈ": u"",
    u"ˌ": u"",
    u"*": u"",
    u"ʊ": u"у",
    u"ə": u"а",
    u"ɛ": u"e",
    u"ʤ": u"дж",
    u"ɔ": u"о",
    u"æ": u"а",
    u"ʃ": u"ш",
    u"ɑ": u"а",
    u"ŋ": u"нг",
    u"ɪ": u"и",
    u"ʒ": u"з",
    u"ʧ": u"ч",
    u"θ": u"с",
    u"ð": u"з",
    u"x": u"кс"
}

mapper = (
    u"abcdefghijklmnopqrstuvwxyz",
    u"абкдефгхигклмнопкрстуввкиз"
)

translation_table = {ord(key): ord(val) for key, val in zip(*mapper)}


def phonetic_translit(row):
    string = ipa.convert(row.replace("&", " and "))
    for rule in treegrams_mapper.keys():
        string = string.replace(rule, treegrams_mapper[rule])
    for rule in bigrams_mapper.keys():
        string = string.replace(rule, bigrams_mapper[rule])
    for rule in unigrams_mapper.keys():
        string = string.replace(rule, unigrams_mapper[rule])
    return string.translate(translation_table)
