import sys
import unicodedata

def is_string_contains_all_words(string, all_words):
    for word in all_words:
        if word not in string:
            return False

    return True

def print_unicode_table(words):
    print("decimal hex chr {0:^40}".format("name"))
    print("------- ----- --- {0:-<40}".format(""))

    code = ord(" ")
    end = sys.maxunicode

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")
        if words is None or is_string_contains_all_words(name.lower(), words):
            print("{0:7} {0:5X} {0:^3c} {1}".format(code, name.title()))
        code += 1

words = []

if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("usage: {0} [{{strings}}]".format(sys.argv[0]))
        words = None
    else:
        words = [arg.lower() for arg in sys.argv[1:]]

if words is not None:
    print_unicode_table(words)
