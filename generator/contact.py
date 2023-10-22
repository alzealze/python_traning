from model.contact import Contact
import random
import string
import os.path
import json
import getopt
import sys


try:
    # n- задает количество генерируемых данных, f-файл в который записываются n
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contact", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

# L_6_10
n = 5
f = "data/contact.json"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Contact(firstname="", lastname="", mobile="", nickname="")] + [
    Contact(firstname=random_string("firstname", 15), lastname=random_string("lastname", 15),
            mobile=random_string("mobile", 10), nickname=random_string("nickname", 20))
    for i in range(n)
]

file = config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    out.write(json.dumps(testdata, default=lambda x: x.__dict__, indent=2))
