#Roget Tools for Textual Analysis

##Overview

Following [Klingenstein, Hitchcock, and DeDeo 2014)'s work on the "Old Bailey" records](http://www.pnas.org/content/111/26/9419.full), Roget Tools is a Python library for tracking broad semantic categories through bodies of text using the top-down hierarchical structure of Peter Mark Roget's *Thesaurus*. These tools were derived from the 1911 index to and full text of the *Thesaurus* [available from Project Gutenberg](http://www.gutenberg.org/ebooks/search/?query=roget) and were generated using 1. automated regular expression text extraction on the [index](http://www.gutenberg.org/cache/epub/10681/pg10681.txt) and 2. reconstruction of the hierarchy represented by the headings of the [full 1911 edition](http://www.gutenberg.org/cache/epub/22/pg22.txt). This hierarchy is a comprehensive and unbroken network encompassing all of Roget's original thesaurus categories, and importing it into a Python-readable format allows an integration of network analysis techniques into the analysis of textual corpora.

With this integration in mind, the library opens up several methods of automated textual analysis. First, it enables Python-readable categorization of individual words at different levels of abstraction (i.e., specificity of semantic categorization). It also allows the user to return the full hierarchical path of all a given word's categories to the top of Roget's taxonomy, simultaneously measuring the path length. In addition to being applicable to individual words, both of these methods can be automatically applied to large samples of text, replacing words with their semantic categories. Roget Tools can also return the distance (in network edges) between any two words in the *Thesaurus* or any two nodes in the hierarchy. (See Jarmasz and Szpakowicz (2012) on the relevance of this measure.) Finally, given a text---be it a list of randomly selected words, a portion of a literary text, or part of the output from a topic modeling algorithm---the Roget tools can return the node or nodes that most accurately represent that text's semantic character; this representativeness is measured as the minimum average distance in edges from each word in the list to the selected node.


##Instructions

###Installation

As yet no standard Python installation is available. Instead, download roget.zip and copy the contents into your working directory.


###Use

Roget Tools is a Python class, so an object of class Roget needs to be instantiated before use. After navigating to the working directory containing 'roget.py' and the 'roget' folder, run
<pre><code>import roget</code></pre>
to make the class available. Next, instantiate a class object by running, e.g.,
<pre><code>r = roget.Roget()</code></pre>
In this example, variables can be accessed via
<pre><code>r.variable_name</code></pre>
and functions via
<pre><code>r.function_name()</code></pre>


###NetworkX

Exportability to NetworkX may be desirable for some applications; to eliminate dependencies, however, Roget Tools does not include a NetworkX export function. To do so, use the following code as a model:
<pre><code>
import networkx as nx
import roget
r = roget.Roget()
X = nx.DiGraph()
for x in r.node\_codes.keys():
    X.add_node(x)
edgelist = r.full_childparent.items()
X.add\_edges\_from(edgelist)
</code></pre>


##Variables

What follows is a list of the variables included in the Roget class. Some explanation of the data format is in order: every word in the thesaurus is linked to a base category, which are coded as "cat0001" through "cat1000". All nodes in the hierarchy also have codes, and the coding convention indicates their distance from the top node "WORDS". More specifically, the coding corresponds to level of abstraction via the following key, in order of increasing specificity: "WORDS", "0"; classes, "A-F"; divisions, "I-IV"; sections, "1,2,3" etc.; sub-sections, "a-zz"; and everything below indicated by e.g. appending "1-9" or "i-x" to the parent node's code. The semantic category corresponding to each of these nodes and categories can be accessed through the self.node\_codes dictionary. The reverse can be accessed through the self.code\_nodes dictionary. 

These basic functions have been rendered in several permuations and are loaded upon instantiation of a class object:


###Basic Thesaurus Dictionaries

The following variables can be used to access the thesaurus directly:

* **self.thes\_dict** - dictionary of word keys and category codes as values

* **self.thes\_cat** - dictionary of category code keys and words contained by that category as values

* **self.thes\_cat\_list** - thes\_cat formatted as a list


###Node Code -- Node Name Dictionaries

The following variables can be used to navigate between node names and node codes:

* **self.num\_cat** - dictionary of category code keys and category names as values

* **self.cat\_num** - dictionary of category name (always all caps) keys and category codes as values

* **self.node\_codes** - dictionary of node-code keys and node names (all caps) as values

* **self.code\_nodes** - dictionary of node-name keys and node codes as values


###Hierarchical Network Relationship Dictionaries

The following variables essentially construct the hierarchical network relationship between nodes, mapping parent nodes to their children and vice versa. 

* **self.basecat\_dict** - dictionary of parent-child relationships for all nodes with base categories as children

* **self.basecat\_parent** - dictionary of child-parent relationships with base category code keys and parent node codes as values

* **self.parent\_dict** - dictionary of parent-child relationships for all nodes with non-category children

* **self.node\_childparent** - dictionary of child-parent relationships for all non-base-category node codes

* **self.full\_childparent** - dictionary of child-parent relationships for all nodes in hierarchy, including base categories


##Methods

###Functional Methods

This wordlist method is defined for convenience in basic text manipulation and use in other methods.

* **self.make\_wordlist(text,lower=True)** - given a text, return wordlist with punctuation removed and all words made lowercase unless lower=False


###Thesaurus Access Methods

These methods are used for the individual and large-scale application of word-categorization. The "levels" flag indicates how many nodes up from a given word's base category the categorization should take place, or put another way, determines the semantic specificity of the category. These methods are also used in the more complex methods below.

* **self.word\_cat(word,levels=0)** - given a word, returns all base categories containing that word, up levels=n levels from the base category node

* **self.categorize\_words(text,levels=0)** - given a text, makes a wordlist and replaces each entry with the node levels=n levels up from the base category; if word is not in thesaurus, retains the word and assigns category code '0000'

* **self.category\_freqs(text,levels=0)** - given a text, return a dictionary of frequencies for categories levels=n levels up from the base category; excludes words not found in thesaurus

* **self.return\_cat\_words(cat)** - given a base category (code or name) return all words it contains

* **self.return\_word\_cat\_words(word)** - given a word, return all category names and other words in those categories; output format list of tuples: [(category-name,[wordlist]),...]


###Hierarchical Navigation Methods

These methods return various data relating to the network paths and hierarchical relationships between words and categories of the thesaurus. They enable basic network operations such as returning paths and finding common nodes.

* **self.word\_path(word)** - given a word, return the full path from each base category up to the top node ('WORDS') and the distance of each path node from the base category; format list of tuples: [(distance,node),...]

* **self.cat\_path(node)** - given node, returns path from node to top node ('WORDS') and distance from start node to node in path; output format list of tuples: [(distance,node),...]

* **self.two\_word\_common\_node(word1,word2)** - given two words, return a list of all shared nodes and the distance between the two words via that node; output format list of tuples: [(distance-via-node,node),...]


###Distance and Semantic Difference Methods

These methods convert hierarchical positions into distance relations, which in context can be taken as one measure of semantic difference. The first three are simple two-item distance calculations, while the last one extends the methods to n-item distance calculations.

* **self.distance\_to\_node(word,node)** - given a word and a node, return the minimum distance (in edges) between word's base category and target node

* **self.two\_word\_distance(word1,word2)** - given two words, return only minimum distance in edges between them; output format integer

* **self.two\_cat\_distance(category1,category2)** - given two categories, return only minimum distance; output format integer

* **self.clustering_node(wordlist,verbose=False,N=0)** - given a list of words, calculate aggregate and average distance from words' base categories to every node in hierarchy, then return the node code, node, aggregate distance, and average distance for every node with the minimum aggregate distance; if N>0, return the same for N nearest nodes; output format list of tuples: [(node code, node, aggregate distance, average distance),...]


##Future Development

This is the first iteration of Roget Tools, and many applications remain to be developed. The next probable step is to develop a version of self.clustering\_node() that can pick out two or more semantic categories contained in a wordlist in the way that topic modeling picks out a configurable number of topics. Other possibilities for expansion include using the clustering method to determine the likelihood that an unidentified word in a group with an otherwise high level of semantic coherence can also be described by that category. Comments on these or other expansions are welcome and solicited.

##References

Klingenstein, Sara, Tim Hitchcock, and Simon DeDeo. “The Civilizing Process in London’s Old Bailey.” *Proceedings of the National Academy of Sciences* 111.26 \(2014\): 9419–24. www.pnas.org. Web. 20 Aug. 2014. [http://www.pnas.org/content/111/26/9419.abstract](http://www.pnas.org/content/111/26/9419.abstract)

Jarmasz, Mario, and Stan Szpakowicz. “Roget’s Thesaurus and Semantic Similarity.” arXiv:1204.0245 \[cs\]\(2012\): n. pag. arXiv.org. Web. 20 Aug. 2014. [http://arxiv.org/abs/1204.0245](http://arxiv.org/abs/1204.0245)


