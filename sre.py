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

import sys
import math
import json
import csv
import operator

from nlp import get_bag_of_words


if len(sys.argv) != 3:
	print "Usage: python sre.py <posts_file> <suitable_tagging_words_file>"
	exit(1)

	
posts_file = sys.argv[1]
suitable_tagging_words_file = sys.argv[2]

print "Loading posts file %s" % posts_file
posts = json.load(open(posts_file,"r"))
print "Loaded %i posts" % len(posts)

print "Loading words file %s" % suitable_tagging_words_file
count = 0
suitable_tagging_words = {}
with open(suitable_tagging_words_file, 'rb') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter='\t')
	for csv_row in csv_reader:
		word = csv_row[0]
		df = csv_row[1]
		idf = csv_row[2]
		tagging_frequency = csv_row[3]
		# score = tagging_frequency / df
		score = csv_row[4]	
		suitable_tagging_words[word] = score
		count += 1

print "Loaded %i words" % count

MAX_NUM_OF_WORDS_TO_PROCESS = 200
MAX_NUM_OF_AUTOTAGS = 25
for post in posts:
	bag_of_words = get_bag_of_words("%s %s" % (post['title'], post['body']), MAX_NUM_OF_WORDS_TO_PROCESS)

	post_bag_of_words = {}
	for word in bag_of_words:
		if word not in suitable_tagging_words:
			continue

		if word not in post_bag_of_words:
			post_bag_of_words[word] = 0
		post_bag_of_words[word] += 1

	for word in post_bag_of_words:
		tf = math.sqrt(1.0 * post_bag_of_words[word])
		score = float(suitable_tagging_words[word])
		post_bag_of_words[word] = tf * score 
		
	post_bag_of_words = sorted(post_bag_of_words.iteritems(), key=operator.itemgetter(1), reverse=True)

	post["autotags"] = set([word[0] for word in post_bag_of_words[:MAX_NUM_OF_AUTOTAGS]])
	print "%s: %s" % (post["title"], ", ".join(post["autotags"]))

	
# Evaluation
for post in posts:
	print "Most related posts for post '%s'" % post["title"]
	related_posts = []
	for related_post in posts:
		intersection = post["autotags"] & related_post["autotags"]
		union = post["autotags"] | related_post["autotags"]
		if len(union) == 0:
			continue

		# See http://en.wikipedia.org/wiki/Jaccard_index for explanation
		jaccard_coefficient = 1.0 * len(intersection) / len(union)

		related_posts.append((related_post, jaccard_coefficient))
	
	related_posts.sort(key=operator.itemgetter(1), reverse=True)
	for related_post in related_posts[1:4]:
		common_autotags = ", ".join(list(post["autotags"] & related_post[0]["autotags"]))
		print "\t%s (%.2f, %s)" % (related_post[0]["title"], related_post[1], common_autotags)

