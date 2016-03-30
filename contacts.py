from os import listdir
from os.path import isfile, join
import re
import operator


def load_contacts(directory):
    contacts = []

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    p = re.compile("^([0-9]+)_[^_]+_([^.]+)\.wav$")
    for possible_contact_file in files:
        m = p.match(possible_contact_file)
        if m:
            sound_filename = join(directory, possible_contact_file)
            sequence_number = int(m.group(1)) #parsing to int makes "10_foo_123.wav" sort after "2_bar_234.wav"
            phone_number = m.group(2)
            contacts.extend([Contact(sound_filename, phone_number, sequence_number)])

    #sort by its sequence number
    contacts.sort(key=operator.attrgetter('sequence_number'))

    return contacts


class Contact:
    def __init__(self, sound_filename, phone_number, sequence_number):
        self.sound_filename = sound_filename
        self.phone_number = phone_number
        self.sequence_number = sequence_number
