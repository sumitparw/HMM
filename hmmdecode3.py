import sys
import collections
import ast
import math
import io

model_file = "hmmmodel.txt"
output_file = "hmmoutput.txt"
test_file = sys.argv[1]
# test_file = "hmm-training-data\\ja_gsd_dev_raw.txt"


dict_tags = {}
dict_abl_tags = {}

model_transitions = collections.defaultdict(float)
model_emissions = collections.defaultdict(float)
dict_viterbi = dict()
dict_backptr = dict()


def viterbi_algorithm(obs):
    is_token = False
    for s in dict_tags:
        if (s, obs[0]) in model_emissions:
            is_token = True
    for state in dict_tags:
        if is_token is True and (state, obs[0]) in model_emissions:
            if ('BEGIN', state) not in model_transitions:
                model_transitions[('BEGIN', state)] = math.log(1.0 / (dict_abl_tags[state] + len(dict_tags)))
            dict_viterbi[(state, 0)] = model_transitions[('BEGIN', state)]
            dict_viterbi[(state, 0)] += model_emissions[(state, obs[0])]
            dict_backptr[(state, 0)] = ''
        elif is_token is False:
            if ('BEGIN', state) not in model_transitions:
                model_transitions[('BEGIN', state)] = math.log(1.0 / (dict_abl_tags[state] + len(dict_tags)))
            dict_viterbi[(state, 0)] = model_transitions[('BEGIN', state)]
            dict_viterbi[(state, 0)] += 0
            dict_backptr[(state, 0)] = ''

    for t in range(1, len(obs)):
        is_token = False
        for s in dict_tags:
            if (s, obs[t]) in model_emissions:
                is_token = True

        for state in dict_tags:
            if is_token is True and (state, obs[t]) in model_emissions:
                v = {}
                for s in dict_tags:
                    if (s, state) not in model_transitions:
                        model_transitions[(s, state)] = math.log(1.0 / (dict_abl_tags[state] + len(dict_tags)))
                    if (s, t - 1) in dict_viterbi:
                        v[s] = (dict_viterbi[(s, t - 1)] + model_transitions[(s, state)])
                max_v= max(v.values())
                max_vs = max(v, key=v.get)
                dict_viterbi[(state, t)] = max_v + model_emissions[state, obs[t]]
                dict_backptr[(state, t)] = max_vs
            if is_token is False:
                v = {}
                for s in dict_tags:
                    if (s, state) not in model_transitions:
                        model_transitions[(s, state)] = math.log(1.0 / (dict_abl_tags[state] + len(dict_tags)))
                    if (s, t - 1) in dict_viterbi:
                        v[s] = (dict_viterbi[(s, t - 1)] + model_transitions[(s, state)])
                max_v = max(v.values())
                max_vs = max(v, key=v.get)
                dict_viterbi[(state, t)] = max_v
                dict_backptr[(state, t)] = max_vs

    si = len(obs)
    dict_v = {}
    for s in dict_tags:
        if (s, si - 1) in dict_viterbi:
            dict_v[s] = dict_viterbi[(s, si - 1)]
    max_v = max(dict_v.values())
    max_vs = max(dict_v, key=dict_v.get)

    best_path_prob = max_v
    best_path_pointer = max_vs

    return best_path_pointer


with io.open(model_file, 'r', encoding="utf-8") as fmodel:
    dict_tags = ast.literal_eval(fmodel.readline())
    dict_abl_tags = ast.literal_eval(fmodel.readline())
    model_transitions = ast.literal_eval(fmodel.readline())
    model_emissions = ast.literal_eval(fmodel.readline())

with io.open(test_file, 'r', encoding="utf-8") as fin:
    for line in fin:
        dict_viterbi = dict()
        dict_backptr = dict()
        obs = line.split()  # an array
        best_path_pointer = viterbi_algorithm(obs)
        with io.open(output_file, 'a+', encoding="utf-8") as fout:
            txt = ""

            for t in reversed(range(len(obs))):
                tmp_txt = str(obs[t]) + "/" + str(best_path_pointer)
                if t == len(obs) - 1:
                    txt = tmp_txt
                else:
                    txt = tmp_txt + " " + txt
                best_path_pointer = dict_backptr[(best_path_pointer, t)]
            txt += "\n"

            fout.write(str(txt))
