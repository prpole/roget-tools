#Roget Tools for Textual Analysis

##Overview

Following on [Simon DeDeo et al. (2014)'s work on the "Old Bailey" records](http://www.pnas.org/content/111/26/9419.full), the Roget tools are a Python library for tracking broad semantic categories in bodies of text using the top-down hierarchical structure of Peter Mark Roget's *Thesaurus*. These tools were derived from the 1911 index to and full text of the *Thesaurus* [available from Project Gutenberg](http://www.gutenberg.org/ebooks/search/?query=roget) and were generated using 1. automated regular expression text extraction on the [index](http://www.gutenberg.org/cache/epub/10681/pg10681.txt) and 2. semi-automated reconstruction of the hierarchy mirrored in the chapter headings of the [full 1911 edition](http://www.gutenberg.org/cache/epub/22/pg22.txt). 

This library opens up several methods of automated textual analysis. First, it enables Python-readable categorization of individual words at different levels of abstraction (i.e., specificity of semantic categorization). It also allows the user to return the full hierarchical path of all a given word's categories to the top of Roget's taxonomy, simultaneously measuring the path length. In addition to being applicable to individual words, both of these methods can be automatically applied to large samples of text, replacing words with their semantic categories. These tools can also return the distance (in network edges)[^See Jarmasz and Szpakowicz (2012) on the relevance of this measure.] between any two words in the *Thesaurus* or any two nodes in the hierarchy. Finally, given a text---be it a list of randomly selected words, a portion of a literary text, or part of the output from a topic modeling algorithm---the Roget tools can return the node or nodes that most accurately represent that text's semantic character; this representativeness is measured as the minimum average distance in edges from each word in the list to the selected node.

##Instructions

###Installation

As yet no standard Python installation is available. Instead, download roget.zip and copy the contents into your working directory.

###Use

Roget Tools is a Python class, so an object of class Roget needs to be instantiated for use. First, run
<pre><code>import roget</code></pre>
to make the class available. Next, instantiate a class object by running, e.g.,
<pre><code>r = roget.Roget()</code></pre>
In this example, variables can be accessed via
<pre><code>r.variable_name</code></pre>
and functions via
<pre><code>r.function_name()</code></pre>


##Variables

What follows is a list of the variables included in the Roget class. Some explanation of the data format is in order: every word in the thesaurus is linked to a base category, which are coded as "cat0001" through "cat1000". All nodes in the hierarchy also have codes, and the coding convention indicates their distance from the top node "WORDS". More specifically: "WORDS", "0"; classes, "A-F"; divisions, "I-IV"; sections, "1,2,3" etc.; sub-sections, "a-zz"; and everything below indicated by e.g. appending "1-9" to the parent code. The semantic category corresponding to each of these nodes and categories can be accessed through the self.node\_codes dictionary. The reverse can be accessed through the self.code\_nodes dictionary. 

These basic functions have been rendered in several permuations and are loaded upon instantiation of a class object:

###Basic Thesaurus Dictionaries

* **self.thes\_dict** - dictionary of word keys and category codes as values

* **self.thes\_cat** - dictionary of category code keys and words contained by that category as values

* **self.thes\_cat\_list** - thes\_cat formatted as a list


###Node Code -- Node Name Dictionaries

* **self.num\_cat** - dictionary of category code keys and category names as values

* **self.cat\_num** - dictionary of category name (always all caps) keys and category codes as values

* **self.node\_codes** - dictionary of node-code keys and node names (all caps) as values

* **self.code\_nodes** - dictionary of node-name keys and node codes as values


###Hierarchical Network Relationship Dictionaries

* **self.basecat\_dict** - dictionary of parent-child relationships for all nodes with base categories as children

* **self.basecat\_parent** - dictionary of child-parent relationships with base category code keys and parent node codes as values

* **self.parent\_dict** - dictionary of parent-child relationships for all nodes with non-category children

* **self.node\_childparent** - dictionary of child-parent relationships for all non-base-category node codes

* **self.full\_childparent** - dictionary of child-parent relationships for all nodes in hierarchy, including base categories


##Methods

* **self.make\_wordlist(text,lower=True)** - given a text, return wordlist with punctuation removed and all words made lowercase unless lower=False

* **self.word\_cat(word,levels=0)** - given a word, returns all base categories containing that word, up levels=n levels from the base category node

* **self.categorize\_words(text,levels=0)** - given a text, makes a wordlist and replaces each entry with the node levels=n levels up from the base category; if word is not in thesaurus, retains the word and assigns category code '0000'

* **self.category\_freqs(text,levels=0)** - given a text, return a dictionary of frequencies for categories levels=n levels up from the base category; excludes words not found in thesaurus

* **self.word\_path(word)** - given a word, return the full path from each base category up to the top node ('WORDS') and the distance of each path node from the base category; format list of tuples: [(distance,node),...]

* **self.return\_cat\_words(cat)** - given a base category (code or name) return all words it contains

* **self.return\_word\_cat\_words(word)** - given a word, return all category names and other words in those categories; output format list of tuples: [(category-name,[wordlist]),...]

* **self.distance\_to\_node(word,node)** - given a word and a node, return the minimum distance (in edges) between word's base category and target node

* **self.two\_word\_common_node(word1,word2)** - given two words, return a list of all shared nodes and the distance between the two words via that node; output format list of tuples: [(distance-via-node,node),...]

* **self.two\_word\_distance(word1,word2)** - given two words, return only minimum distance in edges between them; output format integer

* **self.cat\_path(node)** - given node, returns path from node to top node ('WORDS') and distance from start node to node in path; output format list of tuples: [(distance,node),...]

* **self.two\_cat\_distance(category1,category2)** - given two categories, return only minimum distance; output format integer

* **self.clustering_node(wordlist,verbose=False,N=0)** - given a list of words, calculate aggregate and average distance from words' base categories to every node in hierarchy, then return the node code, node, aggregate distance, and average distance for every node with the minimum aggregate distance; if N>0, return the same for N nearest nodes; output format list of tuples: [(node code, node, aggregate distance, average distance),...]
