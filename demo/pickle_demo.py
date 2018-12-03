import pickle
import json

def save_pickle():
    dict_a = {1: 2, 2: 3, 3: 4}
    with open('dict_a.txt', 'w') as f:
        pickle.dump(dict_a, f, 0)

def read_pickle():
    with open('dict_a.txt', 'r') as f:
        dict_aa = pickle.load(f)
    print dict_aa

def save_json():
    dict_c = {4: 5, 5: 6, 6: 7}
    with open('dict_c.txt', 'w') as f:
        f.write(json.dumps(dict_c))

def read_json():
    with open('dict_c.txt', 'r') as f:
        dict_cc = json.loads(f.read())
    print dict_cc

# save_pickle()
read_pickle()
# save_json()
# read_json()