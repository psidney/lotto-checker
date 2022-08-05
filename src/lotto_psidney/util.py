import re

def strip_xml(string_to_strip):
    return re.sub('<[^<]+>', '', string_to_strip)
