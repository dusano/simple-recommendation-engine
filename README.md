Simple Recommendation Service
=============================

This is a simple recommendation engine for matching blog posts. It
works by autotagging posts first, followed by matching of posts based
on the autotags. The autotagging is based on the list of unigrams
suitable for tagging blog posts. The unigram list is provided by Zemanta
(http://developer.zemanta.com/)

Example usage:
--------------
python sre.py avc_blog.json unigrams.csv 


This routine uses porter stemming algorithm. For details about this algorithm
see http://www.tartarus.org/~martin/PorterStemmer

Author: Dusan Omercevic (dusan.omercevic@fri.uni-lj.si)
Initial release: October 2012