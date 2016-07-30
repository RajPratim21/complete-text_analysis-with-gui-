# -*- coding: utf-8 -*-
from nltk.book import *
from nltk import sent_tokenize, word_tokenize, pos_tag
from collections import Counter
#from nltk.corpus import stopwords
import nltk
import numpy
import sys
import time
import csv
#import trie_text
start_time = time.time()
reload(sys)
sys.setdefaultencoding("utf-8")
global stopwords
global delimiters
#import window
#from window import *
from Sparse_new import SparseVector

stopwords = ["a","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","a's","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","came","can","cannot","cant","can't","cause","causes","certain","certainly","changes","clearly","c'mon","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","c's","currently","dear","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","done","don't","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","hello","help","hence","her","here","hereafter","hereby","herein","here's","hereupon","hers","herself","he's","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","ie","if","ignored","i'll","i'm","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","its","it's","itself","i've","just","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","take","taken","tell","tends","th","than","thank","thanks","thanx","that","thats","that's","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","therefore","therein","theres","there's","thereupon","these","they","they'd","they'll","they're","they've","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","tis","to","together","too","took","toward","towards","stopwordsd","stopwordss","truly","try","trying","t's","twas","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","welcome","well","we'll","went","were","we're","weren't","we've","what","whatever","what's","when","whence","whenever","where","whereafter","whereas","whereby","wherein","where's","whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","who's","whose","why","will","willing","wish","with","within","without","wonder","won't","would","wouldn't","yes","yet","you","you'd","you'll","your","you're","yours","yourself","yourselves","you've","zero"]


delimiters=[".",",",";",":","?","/","!","'s","'ll","'d","'nt","(",")","{","}","[","]"]
class Unigram:
	def __init__(self,str):
		self.str = str
	def compute_unigrams(self,str):
		ugs = [word for word in str if (word not in stopwords and word not in delimiters)]
		return ugs
		

class Bigram:
	def __init__(self,str):
		self.str = str
	def compute_bigrams(self,str):
		final_list=[]
		bigramtext = list(nltk.bigrams(str))
		for item in bigramtext:
			if item[0] not in delimiters and item[len(item)-1] not in delimiters:
				if not item[0].isdigit() and not item[1].isdigit():
					if item[0] not in stopwords and item[len(item)-1] not in stopwords:	
						if len(item[0])>1  and len(item[len(item)-1])>1:
							final_list.append(item)	
		return final_list
		
class Trigram:
	def __init__(self,str):
		self.str = str
	def compute_trigrams(self,str):
		final_list=[]
		trigramtext = list(nltk.trigrams(str))
		for item in trigramtext:
			if item[0] not in delimiters and item[1] not in delimiters and item[len(item)-1] not in delimiters:
				if not item[0].isdigit() and not item[1].isdigit() and not item[len(item)-1].isdigit():
					if item[0] not in stopwords and item[len(item)-1] not in stopwords:	
						if len(item[0])>1  and len(item[len(item)-1])>1:
							final_list.append(item)	
		return final_list
		
		
class Sentence:
	#----------------Global variable declaration------------
	global sents
	global sents1
	global tokens
	global sentenceugs
	global sentencebgs
	global sentencetgs
	global weight_list
	global l1
	global sparseVector
	weight_list = []
	l1=[]
	Textpath = sys.argv[1]
	'''
	input_file = sys.argv[1]
	fo = open(input_file , "r")
	'''
	with open('input_file.txt', 'wb') as f: # output csv file
    #writer = csv.writer(f)
		with open(Textpath,'r') as csvfile: # input csv file
			reader = csv.DictReader(csvfile)
			for row in reader:
				row['Review'] = unicode(row['Review'], errors='ignore')
				f.write(row['Review'])
				f.write('.')
				f.write("\n")
	
	#input_file = sys.argv[1]
	fo = open("input_file.txt" , "r")
	
	text1 =fo.read()
	
	text = text1.lower()
	#-----------------Sentence representation-----------------
	sents = sent_tokenize(text)
	print len(sents)
	sents1 = sent_tokenize(text1)
	
	#sentences = [nltk.word_tokenize(sent) for sent in sents]
	#print sentences
	#------------------Word representation------------------------
	tokens = [nltk.word_tokenize(sent) for sent in sents]
	#print tokens
	
	
	#---------Object Creation of Unigram,Bigram and Trigram class--------
	unigram_obj = Unigram("")
	bigram_obj = Bigram("")
	trigram_obj = Trigram("")
	
	#----------Accessing the computed List of Unigram,Bigram and Trigram---------
	sentenceugs=[]
	sentencebgs=[]
	sentencetgs=[]
	for token in tokens:
		a = unigram_obj.compute_unigrams(token)
		sentenceugs.append(a)
		b = bigram_obj.compute_bigrams(token)
		sentencebgs.append(b)
		c = trigram_obj.compute_trigrams(token)
		sentencetgs.append(c)
	#print sentenceugs	
	#print sentencebgs	
	#print sentencetgs	
	#print "whfioehfoiejfopjfpoejfp[ekfp[eofp[eof[epof[eolpevldjkvhdkjvhdivhdjhvkdhvkdhvkdhkvh"	
	#print sentencebgs	
	#-----------------Constructor of Sentence Class-----------------
	def __init__(self,sents,sentenceugs,sentencebgs,sentencetgs):
		self.sentenceugs = sentenceugs
		self.sentencebgs = sentencebgs
		self.sentencetgs = sentencetgs
		self.sents = sents
		
	
	#-----------------Diplaying All the Sentence of the Given Text with Corresponding Unigram,Bigram and Trigram---------------
	'''
	def display(self):
		for i in range(0,len(sents)):
			#print "hello"
			#print i + "th sentence is"
			print sents[i],sentenceugs[i],sentencebgs[i],sentencetgs[i]
			print "\n"
	'''		
	#--------------------Returning the Sentence depending on their proximity----------------	
	@staticmethod
	def build_dictionary():
		hashedugs = []
		finalhashedugs = []
		
		ui=0
		d={}
		#print sentenceugs
		for sentence in sentenceugs:
				for unigram in sentence:
					if unigram not in d:
						d.update({unigram : ui})
						#print unigram, str(ui)
						
						ui+= 1				
						
	
		for lst in sentenceugs:
			l = len(lst)
			for i in range(0,l):
				lst[i]=d[lst[i]]
			#sorted_list=sorted(sent_index_list)	
			#print lst
		return sentenceugs
		'''
		word_list=[]
		freq_list=[]
		for lst in sentenceugs:
			sorted_list=sorted(lst)
			c=Counter(sorted_list)
			word_list.append(c.keys())
			freq_list.append(c.values())
			
			
		for word,rank in zip(word_list,freq_list):
			print word,rank	
		
		'''	
		
	@staticmethod
	def compute_ugs_proximity_list():
	
		#-------------------Unigram proximity computation--------------------
		sparseVector = SparseVector([],[])
		len_list=len(sentenceugs)
		i_rng = range(len_list)
		ugs_intersect_list = []
		ugs_proximity_list = []
		for i in i_rng:	
			#for j in range(i+1,len_list):
			for j in i_rng:
				wv1 = sentenceugs[i]
				wv2 = sentenceugs[j]
				set_ugs = sparseVector.union_intersection(wv1,wv2)
				#print set_ugs
				ugs_intersect_list.append(set_ugs)
		#print ugs_intersect_list
		for i in ugs_intersect_list:
			try:
				unigram_proximity = round((float(i[1])/float(i[0])),3)
			except ZeroDivisionError:
				print "divide by zero"	
			ugs_proximity_list.append(unigram_proximity)
			
		ugs_proximity_list = [0.333*x for x in ugs_proximity_list]
		return ugs_proximity_list
		
		
		#-------------------Bigram proximity computation--------------------
	@staticmethod	
	def compute_bgs_proximity_list():	
		bgs_intersect_list = []
		for i in range(len(sentencebgs)):	
			for j in range(len(sentencebgs)):
				set_bgs = len(list(set(sentencebgs[i]).intersection(sentencebgs[j])))
				#pos = (i,j)
				#ugs_intersect_list.append(pos)
				bgs_intersect_list.append(set_bgs)
		
		bgs_union_list = []
		for i in range(len(sentencebgs)):	
			#for j in range(i+1,len(sentenceugs)):
			for j in range(len(sentencebgs)):
				set_bgs = len(list(set(sentencebgs[i]).union(sentencebgs[j])))
				bgs_union_list.append(set_bgs)
	
		bgs_proximity_list = []
		for i in range(0,len(bgs_intersect_list)):	
			for j in range(0,len(bgs_union_list)):
				if i!=j:
					continue
				if	bgs_union_list[j]!=0:
					bigram_proximity = round((float(bgs_intersect_list[i])/float(bgs_union_list[j])),3)
					bgs_proximity_list.append(bigram_proximity)
				else:
					bigram_proximity = 0
					bgs_proximity_list.append(bigram_proximity)
		#print bgs_proximity_list
		bgs_proximity_list = [0.333*x for x in bgs_proximity_list]
		return bgs_proximity_list
		
		#-------------------Trigram proximity computation--------------------
	@staticmethod	
	def compute_tgs_proximity_list():	
		tgs_intersect_list = []
		for i in range(len(sentencetgs)):	
			for j in range(len(sentencetgs)):
				set_tgs = len(list(set(sentencetgs[i]).intersection(sentencetgs[j])))
				tgs_intersect_list.append(set_tgs)
		
		tgs_union_list = []
		for i in range(len(sentencetgs)):	
			#for j in range(i+1,len(sentenceugs)):
			for j in range(len(sentencetgs)):
				set_tgs = len(list(set(sentencetgs[i]).union(sentencetgs[j])))
				tgs_union_list.append(set_tgs)
				
		tgs_proximity_list = []
		for i in range(0,len(tgs_intersect_list)):	
			for j in range(0,len(tgs_union_list)):
				if i!=j:
					continue
				if	tgs_union_list[j]==0:
					trigram_proximity = 0
					tgs_proximity_list.append(trigram_proximity)
				else:	
					trigram_proximity = round((float(tgs_intersect_list[i])/float(tgs_union_list[j])),3)
					tgs_proximity_list.append(trigram_proximity)
		#print tgs_proximity_list
		tgs_proximity_list = [0.333*x for x in tgs_proximity_list]
		return tgs_proximity_list
		#-----------------Final proximity calculation among all sentences and building the nxn matrix ---------------
		
	@staticmethod
	def compute_final_proximity():
		
		#bgs_proximity_list = Sentence.compute_bgs_proximity_list()
		#tgs_proximity_list = Sentence.compute_tgs_proximity_list()
		#z  = [round(sum(x),3) for x in zip(tgs_proximity_list,bgs_proximity_list,ugs_proximity_list)]
		z =ugs_proximity_list
		i=0
		new_list=[]
		while i<len(z):
			new_list.append(z[i:i+len(sents)])
			i+=len(sents)
		#print new_list
		proximity_matrix = numpy.array(new_list)
		#print proximity_matrix # The nxn Proximity Matrix
		
		i,j = numpy.indices(proximity_matrix.shape)
		proximity_matrix[i==j] = 0
		#print proximity_matrix # Proximity Matrix after replacing the diagonal elements with 0
		len_prox_mat=len(proximity_matrix)
		rng_prox_mat=range(len_prox_mat)
		avg_mat = [sum(proximity_matrix[i])/len_prox_mat for i in rng_prox_mat]
		#print avg_mat # Calculating the average value of each row of the Proximity Matrix
		#---------------Sorting the matrix element in descending order and getting the index-------------
		B=sorted(range(len(avg_mat)),key=lambda x:avg_mat[x],reverse=True) 
		return B
	@staticmethod	
	def rank_sentence():	
		
		#print sorted_list
		#f = open('D:\\Python\\output.txt', 'w+')
		sorted_list = Sentence.compute_final_proximity()
		sent_list = []
		sent_index_list = []
		for i in sorted_list:
			#print sents[i] # Displaying the sentences in sorted order
			sent_list.append(sents1[i])
		len_sents = int(len(sent_list)*0.1)
		final_sent_list = sent_list[:len_sents]
		#print final_sent_list
		for i in final_sent_list:
			sent_index_list.append(sents1.index(i))
		#print sent_index_list
		sorted_list1=sorted(sent_index_list)
		#print sorted_list	
		sys.stdout = open('summary_output.txt', 'w')	
		for i in sorted_list1:
			print sents1[i]
			
	
	
			
sent_obj = Sentence([],[],[],[])
dictionary_building_start_time = time.time()
dictionary = Sentence.build_dictionary()
dictionary_building_end_time = time.time()
print("--- %s dictionary time---" % (dictionary_building_end_time - dictionary_building_start_time))


ugsproximity_building_start_time = time.time()
ugs_proximity_list = Sentence.compute_ugs_proximity_list()
ugsproximity_building_end_time = time.time()
print("--- %s proximty computation time---" % (ugsproximity_building_end_time - ugsproximity_building_start_time))

sorted_list = Sentence.compute_final_proximity()
#sent_obj.display()	
Sentence.rank_sentence()
#print("--- %s seconds ---" % (time.time() - start_time))