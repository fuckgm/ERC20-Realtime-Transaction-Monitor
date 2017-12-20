import time
import json
import codecs

def logy(*args):
  print('-' * 40)
  print(time.ctime())
  print(args)

def prettify(d):
    print json.dumps(d, indent=3)

def logy_unknown_txs(hash):
  with open("unknown_transactions.txt", "a") as myfile:
      myfile.write(hash+'\n')

def save_dictionary_to_json(path, jsonDump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(jsonDump, indent=3))

# load dictionary from JSON-file
def load_dictionary_from_json(filename):
    with open (filename) as data_file:
        return json.load(data_file)

def load_list_from_file(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return lines