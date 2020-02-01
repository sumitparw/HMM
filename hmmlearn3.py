import collections
import math
import io
model_file = "hmmmodel.txt"
# path = sys.argv[1]
path = "hmm-training-data\\ja_gsd_train_tagged.txt"


all_tags = set()
counter_tags = collections.Counter()
counter_abl_tags = collections.Counter()
lis_bigrams = collections.Counter()
counter_tw_pairs = collections.Counter()
dict_transitions = {}
dict_emissions = {}

with io.open(path, 'r', encoding="utf-8") as file:
    for li in file:
        counter_tags['BEGIN'] += 1
        lis_processed_text = li.split()
        for i in range(0, len(lis_processed_text)):
            lis_tw_pair1 = lis_processed_text[i][::-1].split('/', maxsplit=1)
            st_tag1 = lis_tw_pair1[0][::-1]
            st_word1 = lis_tw_pair1[1][::-1]
            counter_tags[st_tag1] += 1
            if i == 0 and i == len(lis_processed_text) - 1:
                counter_abl_tags[st_tag1] += 1
                lis_bigrams[('BEGIN', st_tag1)] += 1
                lis_bigrams[(st_tag1, 'END')] += 1
            elif i == 0:
                st_tag2 = lis_processed_text[i + 1][::-1].split('/', maxsplit=1)[0][::-1]
                counter_abl_tags[st_tag1] += 1
                lis_bigrams[('BEGIN', st_tag1)] += 1
                lis_bigrams[(st_tag1, st_tag2)] += 1
            elif i == len(lis_processed_text) - 1:
                lis_bigrams[(st_tag1, 'END')] += 1
            else:
                st_tag2 = lis_processed_text[i + 1][::-1].split('/', maxsplit=1)[0][::-1]
                counter_abl_tags[st_tag1] += 1
                lis_bigrams[(st_tag1, st_tag2)] += 1
            counter_tw_pairs[(st_tag1, st_word1)] += 1
        counter_tags['END'] += 1
    counter_abl_tags['BEGIN'] = counter_tags['BEGIN']

all_tags = {x for x in counter_tags.keys() if x not in ('BEGIN', 'END')}

for b in lis_bigrams:
    st_tag1 = b[0]

    dict_transitions[b] = math.log(
        ((lis_bigrams[b] + 1) * 1.0) / (counter_abl_tags[st_tag1] + len(all_tags)))


for t in counter_tw_pairs:
    st_tag = t[0]

    dict_emissions[t] = math.log((counter_tw_pairs[t] * 1.0) / counter_tags[st_tag])

counter_abl_tags = dict(counter_abl_tags)
with open(model_file, 'w+', encoding="utf-8") as fout:
    fout.write(str(all_tags))
    # print(str(len(self.all_tags)))
    fout.write('\n')
    fout.write(str(counter_abl_tags))
    # print(str(len(self.abl_tags)))
    fout.write('\n')
    fout.write(str(dict_transitions))
    fout.write('\n')
    fout.write(str(dict_emissions))
    fout.write('\n')

