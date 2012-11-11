#!/usr/bin/env python

"""Simple Recommendation Engine
This is a simple recommendation engine for matching blog posts. It
works by autotagging posts first, followed by matching of posts based
on the autotags. The autotagging is based on the list of unigrams
suitable for tagging blog posts. The unigram list is provided by Zemanta
- your blogging assistant (http://developer.zemanta.com/)

Example usage:
python sre.py avc_blog.json unigrams.csv 

It uses porter stemming algorithm. For details about this algorithm
see http://www.tartarus.org/~martin/PorterStemmer

Author: Dusan Omercevic (dusan.omercevic@fri.uni-lj.si)
Initial release: October 2012
"""
import re

from porter import PorterStemmer


porter_stemmer = PorterStemmer()

def get_bag_of_words(text, max_words = None):

	words = text.split()
	if max_words:
		words = words[0:max_words]

	bag_of_words = []
	for word in words:
		word = word.lower()
		word = re.sub('[\W_]+', '', word)
		stem = porter_stemmer.stem(word, 0,len(word)-1)
		if stem:
			bag_of_words.append(stem)
		
	return bag_of_words

