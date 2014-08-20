import cPickle
class Roget:
    def __init__(self):
        with open('roget/thes_dict.txt','r') as f:
            self.thes_dict = cPickle.load(f)
        with open('roget/thes_cat.txt','r') as f:
            self.thes_cat = cPickle.load(f)
        with open('roget/thes_cat_list.txt','r') as f:
            self.thes_cat_list = cPickle.load(f)
        with open('roget/cat_num.txt','r') as f:
            self.cat_num = cPickle.load(f)
        with open('roget/basecat_dict.txt','r') as f:
            self.basecat_dict = cPickle.load(f)
        with open('roget/parent_dict.txt','r') as f:
            self.parent_dict = cPickle.load(f)
        with open('roget/node_codes.txt','r') as f:
            self.node_codes = cPickle.load(f)
        with open('roget/code_nodes.txt','r') as f:
            self.code_nodes = cPickle.load(f)
        with open('roget/basecat_parent.txt','r') as f:
            self.basecat_parent = cPickle.load(f)
        with open('roget/node_child-parent.txt','r') as f:
            self.node_childparent = cPickle.load(f)
        with open('roget/full_childparent.txt','r') as f:
            self.full_childparent = cPickle.load(f)
        with open('roget/num_cat.txt','r') as f:
            self.num_cat = cPickle.load(f)

    def make_wordlist(self,myText,lower=True):
        '''Removes punctuation and returns list of words; 'lower' flag determines case'''
        puncMarks = [',', '.', '?', '!', ':', ';', '\'', '\"', '(', ')', '[', ']', '-']
        for item in puncMarks:
                myText = myText.replace(item, '')
        if lower:
            lowerText = myText.lower()
        textWords = lowerText.split()
        return textWords

    def word_cat(self,word,levels=0):
        '''Given a word, checks if in thesaurus and returns all base categories;
        if not in thesaurus, returns the word with category code "0000";
        "levels" sets the specificity of the categorization,
        viz. how many nodes up from the base category is the category returned'''
        if word in self.thes_dict:
            cats = [ (self.num_cat[x],x) for x in self.thes_dict[word] ] 
        else:
            cats = [(word,'0000')]
        counter = 0
        while counter < levels:
            for ndx,cat in enumerate(cats):
                if cat[1] != '0000':
                    if cat[1] not in ['A','B','C','D','E','F']:
                        node = self.full_childparent[cat[1]]
                        cats[ndx] = (self.node_codes[node],node)
            counter += 1
        return cats

    def categorize_words(self,text,levels=0):
        '''Given a text (type str), makes a list of words 
        and categorizes each up n levels from the base category; 
        words are replaced with their categories and returned as a list'''
        wordlist = self.make_wordlist(text)
        newlist = [ self.word_cat(x,levels=levels) for x in wordlist ]
        bagofwords = []
        for x in newlist:
            for y in x:
                bagofwords.append(y)
        return bagofwords

    def category_freqs(self,text,levels=0):
        '''returns dict of word category frequencies of levels=n for a text,
        throwing out words not in the thesaurus'''
        fcounts = {}
        bagofwords = self.categorize_words(text,levels=levels)
        good_cats = [ x for x in bagofwords if x[1] != '0000' ]
        for x in good_cats:
            if x in fcounts.keys():
                fcounts[x] += 1
            else:
                fcounts[x] = 1
        return fcounts

    def word_path(self,word):
        '''returns full hierarchical paths for word
        from base categories to parent node "WORDS" (code '0');
        also returns distance of each node from word/base category;
        return format tuple: (distance,node)'''
        all_cats = [ x for x in self.thes_dict[word] ]
        syn_paths = []
        for cat in all_cats:
            path = []
            counter = 0
            path.append((counter,self.num_cat[cat]))
            node = cat
            while True:
                counter += 1
                parent = self.full_childparent[node]
                path.append((counter,self.node_codes[parent]))
                node = parent
                if parent not in self.full_childparent.keys():
                    break
            syn_paths.append(path)
        return syn_paths

    def return_cat_words(self,cat):
        '''returns all words in given base category (accepts code or category name)'''
        cat_words = []
        if cat in self.num_cat.keys():
            cat_words.append((self.num_cat[cat],self.thes_cat[cat]))
        elif cat.upper() in self.num_cat.values():
            code = self.cat_num[cat.lower()]
            cat_words.append((cat.upper(),self.thes_cat[code]))
        return cat_words

    def return_word_cat_words(self,word):
        '''given word, return all other words in word's categories'''
        all_cats = [ x for x in self.thes_dict[word] ]
        cat_words = []
        for cat in all_cats:
            cat_words.append((self.num_cat[cat],self.thes_cat[cat]))
        return cat_words

    def distance_to_node(self,word1,node):
        '''given word and node, return distance (in nodes) from base category to node;
        if node not in path to "WORDS" node, distance equals sum of word's and node's
        path to "WORDS"'''
        if node in self.node_codes.keys():
            node = self.node_codes[node]
        wordcats = [ x[0] for x in self.word_cat(word1) ]
        word1 = word1.lower()
        distances = []
        paths = self.word_path(word1)
        for path in paths:
            for tup in path:
                if node in tup:
                    distances.append(tup[0])
        if distances == []:
            for cat in wordcats:
                pathlength1 = self.two_cat_distance(cat,'WORDS')
                pathlength2 = self.two_cat_distance(node,'WORDS')
                distances.append(pathlength1+pathlength2)
        dist = min(distances)
        return dist

    def two_word_common_node(self,word1,word2):
        '''given two words, returns tuples containing all shared nodes
        and minimum distance between the two words via that node;
        output format tuple: (distance,node)'''
        word1 = word1.lower()
        word2 = word2.lower()
        paths1 = self.word_path(word1)
        paths2 = self.word_path(word2)
        nodes1 = []
        nodes2 = []
        path_lengths = []
        for path in paths1:
            for node in path:
                nodes1.append(node[1])
        for path in paths2:
            for node in path:
                nodes2.append(node[1])
        common_nodes = list(set(nodes1).intersection(set(nodes2)))
        for node in common_nodes:
            distances1 = []
            distances2 = []
            for path in paths1:
                for n in path:
                    if node in n:
                        distances1.append(n[0])
            for path in paths2:
                for n in path:
                    if node in n:
                        distances2.append(n[0])
            path_length = min(distances1) + min(distances2)
            path_lengths.append((path_length,node))
        path_lengths.sort(key=lambda x: x[0])
        return path_lengths

    def two_word_distance(self,word1,word2):
        '''returns minimum distance between two words as int'''
        word1 = word1.lower()
        word2 = word2.lower()
        paths1 = self.word_path(word1)
        paths2 = self.word_path(word2)
        nodes1 = []
        nodes2 = []
        path_lengths = []
        for path in paths1:
            for node in path:
                nodes1.append(node[1])
        for path in paths2:
            for node in path:
                nodes2.append(node[1])
        common_nodes = list(set(nodes1).intersection(set(nodes2)))
        for node in common_nodes:
            distances1 = []
            distances2 = []
            for path in paths1:
                for n in path:
                    if node in n:
                        distances1.append(n[0])
            for path in paths2:
                for n in path:
                    if node in n:
                        distances2.append(n[0])
            path_length = min(distances1) + min(distances2)
            path_lengths.append(path_length)
        distance = min(path_lengths)
        return distance

    def cat_path(self,category):
        '''returns path from node to parent node "WORDS"
        and distance from given node to each node in path;
        output format list of tuples: [(distance,node),...]'''
        if category == '0':
            return [(0,'WORDS')]
        elif category.upper() == 'WORDS':
            return [(0,'WORDS')]
        elif category.lower() in self.node_codes.keys():
            cat = category.lower()
        elif category.upper() in self.node_codes.values():
            cat = self.code_nodes[category.upper()]
        #else:
            #NOTE: MAY NEED RETURN THAT DOESN'T MESS UP DISTANCE CALCULATIONS IN NODE CLUSTRING ALGORITHM BELOW
            #return [(0,'WORDS')]
        path = []
        counter = 0
        path.append((counter,self.node_codes[cat]))
        node = cat
        while True:
            counter += 1
            parent = self.full_childparent[node]
            path.append((counter,self.node_codes[parent]))
            node = parent
            if parent not in self.full_childparent.keys():
                break
        return path

    def two_cat_distance(self,category1,category2):
        '''return minimum distance between two categories as int'''
        paths1 = self.cat_path(category1)
        paths2 = self.cat_path(category2)
        nodes1 = []
        nodes2 = []
        path_lengths = []
        for path in paths1:
            nodes1.append(path[1])
        for path in paths2:
            nodes2.append(path[1])
        common_nodes = list(set(nodes1).intersection(set(nodes2)))
        for node in common_nodes:
            distances1 = []
            distances2 = []
            for n in paths1:
                if node in n:
                    distances1.append(n[0])
            for n in paths2:
                if node in n:
                    distances2.append(n[0])
            path_length = min(distances1) + min(distances2)
            path_lengths.append(path_length)
        distance = min(path_lengths)
        return distance

    def clustering_node(self,wlist,verbose=False,N=0):
        '''returns all nodes that minimize aggregate distance to all words in wordlist;
        output format list of tuples: (node,aggregate distance,average distance per word);
        verbose flag triggers running results; N flag determines number of nearest nodes printed'''
        notwords = []
        wordlist = []
        for word in wlist:
            if word not in self.thes_dict.keys():
                notwords.append(self.word_cat(word))
            else:
                wordlist.append(word)
        #notwords = list(set(notwords))
        word_basecats = [ ]
        if verbose:
            print "excluded words:",notwords
        node_distances = []
        nodelist = self.full_childparent.keys()
        for ndx,node in enumerate(nodelist):
            dists = [ self.distance_to_node(word,node) for word in wordlist ]
            if verbose:
                print dists
            aggdist = sum(dists)
            node_entry = (node,aggdist)
            node_distances.append(node_entry)
            avg_node_distance = aggdist/float(len(wordlist))
            if verbose:
                print ndx,node,aggdist,avg_node_distance
        node_distances = sorted(node_distances,key=lambda x: x[1])
        node_distances_named = [ (node,self.node_codes[node],dist,(float(dist)/len(wordlist))) for (node,dist) in node_distances ]
        distlist = [ x[1] for x in node_distances ]
        mindist = min(distlist)
        mindist_nodes = [ (node,self.node_codes[node],dist,(dist/float(len(wordlist)))) for (node,dist) in node_distances if dist == mindist ]
        if N>0:
            node_distances_named[:N]
        else:
            return mindist_nodes

    ##next: working on "4. given word and path distance, return all other words that are path distance"

    ##to do : dump into network x, different levels of coarse-graining (use x[0] for x in word_path(word); could make option in categorize-word function)


