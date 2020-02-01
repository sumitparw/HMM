import sys
import io

tagged_final = []

#path = sys.argv[1]
path ="hmm-training-data\\ja_gsd_dev_raw.txt"
with io.open('hmmmodel.txt', "r", encoding="utf-8") as f:
    l = f.readlines()

emission = eval(l[0])
transition = eval(l[1])

wordAllTag = eval(l[2])
distinctTag = eval(l[3])
transition = eval(l[4])

tagCount = eval(l[5])



class HMMDecode:
    def decode(self, all_words):
            prev_List = []
            prev_List.append('start')

            wordTag = []
            index = 1

            x = None

            backptr = {}
            final_Line = []

            viterbi_algo = {}
            viterbi_algo['start', 0] = 1

            all_words = line.split()
            for word in all_words:
                tags = wordAllTag.get(word, distinctTag)
                for tag in tags:
                    for prevState in prev_List:
                        tag_ind_pair = (tag, index)
                        pair_1 = (word, tag)
                        probT = (transition.get((prevState, tag), 0) + 1) / (tagCount[prevState] + len(distinctTag))
                        if viterbi_algo.get(tag_ind_pair, -1) < probT * viterbi_algo[prevState, index - 1] * emission.get(pair_1, 1):
                            x = prevState
                            viterbi_algo[tag, index] = probT * viterbi_algo[prevState, index - 1] * emission.get(pair_1, 1)
                            backptr[tag, index] = x

                prev_List = tags
                index = index + 1
            maxP = 0
            for tag in prev_List:
                tag_ind_pair = (tag, index - 1)
                if viterbi_algo.get(tag_ind_pair, 0) > maxP:
                    x = tag
                    maxP = viterbi_algo.get(tag_ind_pair, 0)
            backptr['last', index] = x
            currentT = "last"

            prevT = backptr[(currentT, index)]
            while prevT != 'start':
                prevT = backptr[(currentT, index)]

                wordTag.insert(0, all_words[index - 2] + "/" + prevT)
                currentT = prevT
                index -= 1
            final_Line = wordTag[1:]

            return final_Line


if __name__  == "__main__":
    f = open(path, 'r', encoding="utf8")
    lines = f.readlines()

    hmmdecode = HMMDecode()

    for line in lines:
        tagged_final.append(hmmdecode.decode(line))
    f.close()

    with io.open('hmmoutput.txt', "w+", encoding="utf-8") as f1:
        for line in tagged_final:
            f1.write(str(' '.join(line)))
            f1.write('\n')
    f1.close()