from topic_evaluation.wn import WordNetEvaluator
import sys
import utils.name_convention as name
from topic.topicio import TopicIO
from nltk.corpus import wordnet as wn
from nltk.corpus import reuters
import os

if len(sys.argv) <= 1:
    corpus_type = "bow"
else:
    if sys.argv[1] == "t":
        corpus_type = "tfidf"
    elif sys.argv[1] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 2:
    topics_count = 3
else:
    topics_count = int(sys.argv[2])

if len(sys.argv) <= 3:
    src = "pp_reuters"
else:
    src = sys.argv[3]

if len(sys.argv) <= 4:
    tc = "path"
else:
    tc = sys.argv[4]

if len(sys.argv) <= 5:
    words_count = 10
else:
    words_count = int(sys.argv[5])

if len(sys.argv) <= 6:
    max_words = 250
else:
    max_words = int(sys.argv[6])

if len(sys.argv) <= 7:
    startw = 0
else:
    startw = int(sys.argv[7])

dname = name.get_output_dir(corpus_type, topics_count, src)

# read topics
tio = TopicIO()
tlist = tio.read_topics(dname + "/topics_ptipc_norm2")

ifname = dname + "/" + tc + "/pre_norm2_"+str(max_words)+"_start"+str(startw)+".txt"

# calculate topic evaluation values
tclist = []
te = WordNetEvaluator()

for index, topic in enumerate(tlist):
    tclist.append([index, te.get_values(topic, words_count, ifname, startw=startw)])

# sort the list by a descending order
tclist = list(reversed(sorted(tclist, key=lambda x: x[1][2])))

# output results
if not os.path.exists(dname+"/"+tc):
    os.makedirs(dname+"/"+tc)
    
ofname = dname + "/" + tc + "/norm2" + str(words_count) + "_start"+str(startw) + ".txt"
ofile = open(ofname, "w")
for value in tclist:
    ofile.write("Topic " + str(value[0]) + "\n")
    ofile.write("Mean " + str(value[1][1]) + "\n")
    ofile.write("Median " + str(value[1][2]) + "\n")
    ofile.write("Sum " + str(value[1][0]) + "\n")
    for tcnum in value[1][3]:
        ofile.write(str(tcnum) + "\n")
    ofile.write("\n")