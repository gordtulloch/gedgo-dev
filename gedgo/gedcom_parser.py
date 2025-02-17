import re


class GedcomParser(object):
    """
    File class represents a GEDCOM file.
    Attributes are header, trailer, and entries where header and trailer
    are a single entry each and entries is the dictionary of all entries
    parsed in between.
    """

    line_re = re.compile(
        r'^(\d{1,2})' +          # Level
        r'(?: @([A-Z\d]+)@)?' +  # Pointer, optional
        r' _?([A-Z\d_]{3,})' +   # Tag
        r'(?: (.+))?$'           # Value, optional
    )

    def __init__(self, file_name_or_stream):
        if isinstance(file_name_or_stream, str):
            self.file = open(file_name_or_stream, 'r', encoding='utf-8-sig')
        else:
            self.file = file_name_or_stream
        self.__parse()

    def __parse(self):
        self.entries = {}

        while True:
            line = self.file.readline()
            print("Line is: "+repr(line.strip()))
            if not line:
                break
            tag, entry = self.__parse_element(line)
            if 'pointer' in entry:
                pointer = entry['pointer']
                self.entries[pointer] = entry
            elif tag == 'HEAD':
                self.header = entry
            elif tag == 'TRLR':
                self.trailer = entry

    def __parse_element(self, line):
        parsed = self.line_re.findall(line.strip())

        if not parsed:
            print("Bad GEDCOM syntax in line: '%s'" % line)
            exit()

        level, pointer, tag, value = parsed[0]

        entry = {
            "tag": tag,
            "pointer": pointer,
            "value": value,
            "children": []
        }

        level = int(level)

        # Consume lines from the file while the level of the next line is
        # deeper than that of the current element, and recurse down.
        while True:
            current_position = self.file.tell()
            try:
                next_line = self.file.readline().strip()
            except Exception as e:
                print('Skipping Error '+str(e)+' decoding line: '+repr(next_line))
                continue

            if next_line and int(next_line[:2]) > level:
                _, child_element = self.__parse_element(next_line)
                entry['children'].append(child_element)
            else:
                self.file.seek(current_position)
                break

        # Keep the entry trimmed down
        entry = dict((key, entry[key]) for key in entry.keys() if entry[key])

        return tag, entry

    def __unicode__(self):
        return "Gedcom file (%s)" % self.file
