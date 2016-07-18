import sys
from utils.topic_coherence import TopicCoherence
from utils.TopicIO import TopicIO
from gensim import corpora, models
import os
#
# syntax: python  tcReader.py <input directory name> <corpus type> <# of topics> <src> <word count>
#  <dictionary name> the name of the input dictionary
#  <corpus type> default to bag of words. b for binary, t for tf-idf, anything else or missing for bag of words
#  <# of topics> number of topics. default to 8
#  <alpha> default ot 1/# of topics
#  <eta> default to 1/# of topics
#

#
# Read command line parameters
#
if len(sys.argv) <= 1:
    dname = 'pp_test_LDA'
else:
    dname = sys.argv[1]

if len(sys.argv) <= 2:
    corpus_type = "bow"
else:
    if sys.argv[2] == "t":
        corpus_type = "tfidf"
    elif sys.argv[2] == "b":
        corpus_type = "binary"
    else:
        corpus_type = "bow"

if len(sys.argv) <= 3:
    topics_count = 8;
else:
    topics_count = int(sys.argv[3]);

if len(sys.argv) <= 4:
    src = "pp_test"
else:
    src = sys.argv[4]

if len(sys.argv) <= 5:
    word_count =10
else:
    word_count = int(sys.argv[5])

print "input directory : " + dname
print "corpus type :" + corpus_type
print "# of topics : " + str(topics_count)
print "src : " + src
print "# of words used for topic coherence: " + str(word_count)
print "\n"

# Load directory
dictionary = corpora.Dictionary.load(dname + "/dict.dict")
print(dictionary)

# Load corpus
corpus_fname = dname + '/bow_corpus.mm'
print "Load Corpus File " + corpus_fname
corpus = corpora.MmCorpus(corpus_fname)

corpus_dict = []
for doc in corpus:
    corpus_dict.append(dict(doc))


topics_io = TopicIO()
output = "LDA_"+src+"_"+corpus_type+"_t"+str(topics_count)
tc = TopicCoherence()

# get all topics
tlist = topics_io.read_topics(output+"/topics")

# sort all words by decreasing frequency
tlist2 = []
for topic in tlist:
    tlist2.append(list(reversed(sorted(topic.words_dist, key=lambda x:x[1]))))


wd_dict = tc.read_flist(dname+"/wdoc_freq_"+corpus_type+"_t"+str(topics_count)+".txt")
cofreq_dict = tc.read_flist(dname+"/cofreq_"+corpus_type+"_t"+str(topics_count)+".txt")


# calculate topic coherence values for each topic with a specific number of words
ofile = open(output+"/tc_freq_"+str(word_count)+".txt", "w")
ctlist = []
for index, t in enumerate(tlist2):
    t = t[:word_count]
    subt = [wt[0] for wt in t]
    ofile.write("Topic "+str(index)+"\n")
    ctlist.append((index, tc.tc_dict(subt, wd_dict, cofreq_dict, ofile), t))
    ofile.write("\n")

# sort all topics by topic coherence
ctlist = list(reversed(sorted(ctlist, key=lambda x:x[1])))

ofile = open(output + "/top_topics_"+str(word_count)+".txt", "w")
for tctuple in ctlist:
    ofile.write("Topic  "+ str(tctuple[0])+"   "+str(tctuple[1]) + "\n\n")
    for item in tctuple[2]:
        ofile.write(item[0]+" : "+ str(item[1])+"\n")
    ofile.write("\n\n")
