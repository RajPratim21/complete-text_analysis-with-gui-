class SparseVector:

    #keys  = []
    #values = []
	def __init__(self,wv1,wv2):
		self.wv1 = wv1
		self.wv2 = wv2
	def union_intersection(self,wv1,wv2):
		#wv1=[1,3,4,6,9]
		#wv2=[2,3,4,5,6,7]

		len1=len(wv1)
		len2=len(wv2)

		union_size=0
		intersect_size=0
		i=0
		j=0
		#for i, j in zip(range(0,len1-1), range(0,len2-1)):
		while(i<len1 and j<len2):
		#for i in range(0,len1 - 1):
			#for j in range(0,len2 - 1):
				idx1=wv1[i]
				idx2=wv2[j]
				if(idx1<idx2):
					union_size=union_size + 1
					i=i + 1
				elif(idx2<idx1):
					union_size=union_size + 1
					j=j + 1
				elif(idx1==idx2):
					union_size=union_size + 1
					intersect_size=intersect_size + 1
					i=i + 1
					j=j + 1
			

		if(i<len1 and j>=len2):
			while(i<len1):
				union_size = union_size + 1
				i= i + 1	
		elif(i>=len1 and j<len2):
			while(j<len2):
				union_size = union_size + 1
				j= j + 1

		#print union_size
		return(union_size,intersect_size)

