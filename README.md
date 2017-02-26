# Topic Distance and Coherence

## Table of Contents
 * Introduction
 * Requirements
 * Usage

## Introduction
* ##### Topic Model

    A tool to extract thematic structures in a discrete data collection.

    Dr.Blei gives an example ([see original paper](http://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)). Words in the following text are organized in four topics

    <img src="/image/topic-models.png" width="400">

* ##### Latent Dirichlet Allocation

    LDA is a generative probabilistic topic model.

    ![LDA graph model](/image/lda_begin.png)

    In LDA:
    * A topic is a distribution over the vocabulary
    * A document is a distribution over topics
    * Both distributions are generated by dirichlet processes

    [See LDA Paper](http://www.cs.princeton.edu/~blei/papers/BleiNgJordan2003.pdf)
* #####  Current Code

    Analyze topic coherence and topic distance by various methods
    * Similarity
        * [Bhattacharyya Distance](https://en.wikipedia.org/wiki/Bhattacharyya_distance)
        * [KL Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
        * [Cos Distance](https://en.wikipedia.org/wiki/Cosine_similarity)
        * [Jaccard Distance](https://en.wikipedia.org/wiki/Jaccard_index)
        * [Kendall's Tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient)
    * Coherence
        * [UMass](paperhttp://dirichlet.net/pdf/mimno11optimizing.pdf)
        * [tfidf-version of UMass](http://logic.pdmi.ras.ru/~sergey/slides/N14_PhMLtalk.pdf)
        * [WordNet related methods](http://www.aclweb.org/anthology/N10-1012)
* #### Run LDA
## Requirements
* [Gensim: A Python library for topic Modeling](https://radimrehurek.com/gensim/)
* [NLTK: Natural Language Toolkit](http://www.nltk.org/)
* [NumPy: A Python package for scientific computing](http://www.numpy.org/)
* [Matplotlib: A Python 2D plotting library](http://matplotlib.org/)

## Usage

#### Classes
* ##### Topic Representation
    * Topic Class  - A topic is represented by a list of (word, probability value) tuples

        i.e.  [(“a”,0.3), (“b”, 0.5)....]
    * TopicIO Class - Read and write topics
* ##### Processes
    * 	MySentenceStemmer Class  -  Stemming and Lemmatizing tokens
    * 	MyTextPreProcess Class
        *	Remove stop words
        *	Keep tokens with letters, hyphens/numbers in letters, abbreviations
    *	DocTokenizer
        *	DirDocTokenizer Class  -  Assume the input corpus is a directory and each file is a document
        *	FileDocTokenizer Class - Assume the input corpus is a file and each line is a document
        *   Main Methods
            *   a. Orig
                * Tokenize the corpus and keep tokens with letters, hyphens/numbers in letters and abbreviations
                * Also return a list of doc name
            *   b. Preprocess
                *  Tokenize the corpus
                *	Lemmatize and Stem each token
                *	Keep tokens with letters, hyphens/numbers in letters and abbreviations
                *	Also return a list of doc name

        ```python
        dt=DirDocTokenizer()
        doc_list, token_list = dt.orig(src)
        doc_list, token_list = dt.preprocess(src)
        ````
* ##### Similarity
    * Similarity: include six similarity/distance measurements between topics
        * [Bhattacharyya Distance](https://en.wikipedia.org/wiki/Bhattacharyya_distance)
        * [KL Divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
        * [Cos Distance](https://en.wikipedia.org/wiki/Cosine_similarity)
        * [Jaccard Distance](https://en.wikipedia.org/wiki/Jaccard_index)
        * [Kendall's Tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient)
    ```python
    # Assume t1, t2 are two topics
    sim = Similarity()
    bha_dist_t1_t2 = sim.bha_distance(t1, t2)
    ```

    * SimTopicLists    Measure similarity values between each pair of topics in two topic lists.
    ```python
    """
    Assume t_list1, t_list2 are two topic lists
    t_list1 contains t1_0, t1_1, t1_2
    t_list2 contains t2_0, t2_1, t2_2
    Output distance 2D list:
    [[sim(t1_0,t2_0), sim(t1_0, t2_1), sim(t1_0, t2_2)],
    [sim(t1_1,t2_0), sim(t1_1, t2_1), sim(t1_1, t2_2)],
    [sim(t1_2,t2_0), sim(t1_2, t2_1), sim(t1_2, t2_2)]]
    """
    sim = SimTopicLists()
    bha_dist_t1_t2 = sim.bha_distance(t1, t2)
    ```
* #####  Coherence
    *	umass - Calculate co-occurrence based topic coherence
        * [Based on bow corpus](paperhttp://dirichlet.net/pdf/mimno11optimizing.pdf)
        * [Based on tfidf corpus](http://logic.pdmi.ras.ru/~sergey/slides/N14_PhMLtalk.pdf)
    *   wn - WordNet-based coherence methods
        * [WordNet: A large lexical database of English](https://wordnet.princeton.edu/)
        * [Coherence measures](http://www.aclweb.org/anthology/N10-1012)

#### Run LDA
* Prepare for dictionary and corpus files
```
$python lda_process.py lda_dir(default src_LDA) corpus_type num_of_topics alpha eta
```
    * Preprocessing Output Directory: pp_src
    * Default LDA Directory: src_LDA
	* For a raw corpus, lda_prepare.py generates
        * a) Dictionary file   dict.dict
        *  b)	Three types of corpus files  -   tfidf, bow, binary
            * tfidf_corpus.mm, tfidf_corpus.mm.index
            * bow_corpus.mm, bow_corpus.mm.index
            * binary_corpus.mm, binary_corpus.mm.index
* Run LDA
```
$python lda_process.py lda_dir(default src_LDA) corpus_type num_of_topics alpha eta
```
    * lda_process.py performs a specific LDA and save it to the LDA directory
    * Output these two files in the lda_dir
        * <corpus_type>_t<num_of_topics>.lda
        * <corpus_type>_t<num_of_topics>.lda.index
        * i.e. tfidf_t3.lda, tfidf_t3.lda.index
* Analyze data
```
$python lda_analyze.py lda_dir(default src_LDA) corpus_type num_of_topics src alpha eta
```
    * Output Topics: /topics folder
	* Document-topic matrix
        * unsorted_doc_topics.txt
	    * sorted_doc_topics.txt
	* Topic-document matrix: td_cluster.txt
	* Topic-word matrix: words_in_topics.txt
	* Output topics - sort words by probability differences: /topics_wp

        For each word - probability difference is defined as (P(w) in the topic - P(w) in the corpus)

#### Similarity and Coherence
* Similarity
```
python sim_write.py <corpus_type> <num_of_topics> <src>
```
Output 5 files in the output directory  LDA_<src>_<corpus_type>_t<num_of_topics>
    * sim_jaccard.txt
    * sim_kendall.txt
    * sim_cosine.txt
    * sim_kl.txt
    * sim_bha.txt

* Coherence

    Since coherence calculation often takes a long time, it is separated by two programs.

    One program writes individual word pair contributions to output files, and one program uses those output files to calculate coherence.

    * Co-occurrence Based Coherence
         * Write: Output two files in the LDA folder -  src_LDA
            ```
                python coh_tc_write.py test_LDA <LDA folder><corpus_type> <num_of_topics> <src> <words_count><start_index><tfidf_or_not>
             ```
            * For Bow TC
                * Document Frequency: wdoc_freq_<corpus_type>_t<topics_count>_start<start_index>.txt
                * Co-occurrence Frequency: cofreq_<corpus_type>_t<topics_count>_start<start_index>.txt
                * i.e. wdoc_freq_tfidf_t3_start0.txt,   cofreq_tfidf_t3_start0.txt
            * For Tfidf TC (parameter <tfidf_or_not> ==  “t”)
                * Document Frequency: wdoc_freq_tfidf_<corpus_type>_t<topics_count>_start<start_index>.txt
                * Co-occurrence Frequency: cofreq_tfidf_<corpus_type>_t<topics_count>_start<start_index>.txt
                * i.e. wdoc_freq_tfidf_tfidf_t3_start0.txt,   cofreq_tfidf_tfidf_t3_start0.txt
         * Calculation:
            ```
            python coh_tc_read.py test_LDA <corpus_type> <num_of_topics> <src><words_count><start_index><tfidf_or_not>
            ```
            Output two files in the output directory LDA_<src>_<corpus_type>_t<num_of_topics>
             * top_topics_<words_count>.txt   i.e. top_topics_5.txt

	          Topic coherence values and words with top probabilities in each topic
             * tr_freq_<words_count>.txt  i.e. tc_freq_5.txt

                 Contribution of each pair of words in the coherence value

    * WordNet-Based Coherence
        * Write
            ```
            python coh_wn_write.py test_LDA <corpus_type> <num_of_topics> <src><wn_methods><need_ic_or_not><words_count><start_index>
            ```
            Output two file in the output directory  LDA_<src>_<corpus_type>_t<num_of_topics>
            * "zeros_" + tc + "_w" + str(words_count) + ".txt"

	         All word pairs that results in zero similarity values
            * "pre_" + te + "_w" + str(max_words) + ".txt"

	            Similarity values between each word pair in the sub-topic
        * Calculation
            ```
            python coh_wn_read.py test_LDA  <corpus_type> <num_of_topics> <src><wn_methods><words_count><max_words><start_index>
            ```

            <max_words> refer to <words_count> used in the coh_wn_write.py

            Output one file in the output directory LDA_<src>_<corpus_type>_t<num_of_topics>
            * /wn_methods/w0<words_count>_start<startw>.txt



