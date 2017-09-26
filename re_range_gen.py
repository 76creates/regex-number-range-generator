#!/usr/bin/env python
'''
==============================================================
REGEX NUMBER RANGE GENERATOR
==============================================================
name: re_range_gen
author: Dusan Gligoric
email: dusan76shi@gmail.com
date: May 12th 2017
version: 1.0
python version: 2.7 and 3.4 tested
lincese : GNU General Public License v3.0
==============================================================
DESCRIPION
This script will generate regex number range selector based
uppon arguments pased, it prints out expression ready to use
for whole line validating(start to end), you could modify this
to fit into any regex expression that would preceed or have
something behind the range validator.
==============================================================
RANGE ARGUMENTS
range
  x:y
    range define, x has to be greater than y, ranges that
    overlap will be merged, one could define as many 
    ranges as needed
==============================================================
EXAMPLE
  python re_range_gen.py 1:100
  python re_range_gen.py 10:40 60:1240 3000:1251251
==============================================================
OUTPUT EXAMPLE
  python re_range_gen.py 10:100 60:200 500:1000
  ^(1000|[5-9][0-9]{2}|200|1[0-9]{2}|[1-9][0-9])$
==============================================================

'''

import re
from sys import argv, exit

def reToRange(arg='system arguments by default'):
	if arg=='system arguments by default':
		arg=argv
		del arg[0] # remove script as an arg
	# Argument check
	if len(arg) == 0:
		print ("Not enough arguments")
		exit()
	
	# regex validator
	case_range= re.compile("^(\d+)\:(\d+)$")
    # initialising lists
	global range_vector; range_vector=[] 
	# Arugment validation
	for i in arg:
		if case_range.match(i) != None:
			range_vector.append(i)
		else:
			print("Unknown argument: %s" % i)
			exit()
	
	# Range Validator
	for i in range_vector:
		nums=re.match('(.*?)\:(.*?)$',i)
		if int(nums.group(1)) > int(nums.group(2)):
			exit("First number of range has to be greater than second: %s" % i) 
	# call range collapsor
	colapseRanges()
	global regex_raw; regex_raw=[]
	for rng in range_vector:
		rangeToRegex(rng)
	# optimize regex expressions, especially usefull for long expressions
	expressionOptimizator(regex_raw)
	# format for regex and spit it out
	prepForRegex()

def cruncher(x, fix=''):
	'''
		This function generates regex matches from the number given to
		the smallest number containing same amount of decimal places
		example: From 1234 to 1000 / from 87 to 10 / from 1 to 0
		Two special decinal places are firt one and the last one, you
		will note special rules applying when those are handled
		-
		Varliables:
			li - represents last itteration which is allways 1
			fi - represents first itteration which is number of characters
			nine - indicates that collapsing 9's is possible
			nine_c - indicates how many 9's are consecutive
			str_rep - string representation of number pluged in
		
		NOTE: unlike regex_to_number, these itterations are going from lowest
			decimal spot to the greatest one, right -> left
	'''
	li=1; fi=len(str(x)); nine=False; nine_c=0 # check description
	str_rep=str(x); num_rep=int(x); regex=[] # check description
	#
	for it in range(fi,0,-1):
		temp_num=int(str_rep[it-1])
		if it==fi: # first itteration or the lowest decimal spot
			if temp_num == 9: # collapsing first set of 9's
				'''
				nine collapsing will work only if there is nine flow
					starting from the smallest decimal, here its checked
					and continuation of nines is recorded
				'''
				nine=True
				nine_c+=1
			elif temp_num > 0:
				# does not subtract 1 since its first decimal
				apnd='' if fi==1 else str_rep[:-1]
				regex.append(apnd+str('[0-%i]'%temp_num))
			else:
				# will add starting num as constant 
				regex.append(str_rep)
		elif temp_num==9 and nine==True and it != li:
			nine_c+=1 # adds to nine flow
		elif it==li: # case for last itteration
			if nine==True:
				'''
					this is the case when all numbers till the last one
					are 9's. Easy mode and will be used alot when you 
					calculate ranges that have difference in decimal places
				'''
				apnd='1' if temp_num == 1 else '[1-%i]'%temp_num
				regex.append(apnd+str(('[0-9]') if nine_c==1 else ('[0-9]{%s}'%nine_c)))
				nine=False; nine_c=0
			elif temp_num != 1:
				'''
					most regular case, if first digit was '1' if would be
					taken care of in the previous itterations
				'''
				apnd='1' if temp_num==2 else '[1-%i]'%int(temp_num-1)
				regex.append(str(apnd+str(('[0-9]'*int(fi-li)) if int(fi-li)<=1 else \
					('[0-9]{%s}'%int(fi-li)))))
		elif it<fi and it>li: # greater than first and lesser than last
			if nine==True:
				apnd=str(str_rep[:it-1]+'0') if temp_num==0 else str(str_rep[:it-1]+'[0-%i]'%temp_num)
				regex.append(apnd+str(('[0-9]') if nine_c==1 else ('[0-9]{%s}'%nine_c)))
				nine=False; nine_c=0
			elif temp_num==0:
				pass # skipps turn if middle num is 0
			else:
				regex.append(str(str_rep[:it-1])+str('[0-%i]'%int(temp_num-1))+ \
					str((('[0-9]'*int(fi-it)) if int(fi-it)<=1 else \
						('[0-9]{%s}'%int(fi-it)))))
	# adds to global regex raw
	global regex_raw, regex_raw_negative
	for i in regex:
            regex_raw.append(str(fix+i))

def rangeToRegex(rng):
	'''
		this one is heart of the ops, it will convert ranges to regex values
		and call uppon cruncher for processing of median decimals
		NOTE: unlike cruncher, these itterations are going from greatest
			decimal spot to the lowest one, left -> right
	'''
	nums=re.match('(.*)\:(.*)$', rng)
	x_str=str(nums.group(1))
	y_str=str(nums.group(2))
	global regex_raw
	nine=False
	fi=len(str(x_str)); li=1
	# deal with difference in lenght of two range points
	while True:
		if len(y_str)>len(x_str):
			cruncher(y_str)
			y_str='9'*(len(y_str)-1) # fill with 9's
		else: break
	# deal with zero flow on x
	if str('1'+'0'*(fi-1))==x_str and fi>1:
		cruncher(y_str)
	# this one is wicked, deals with same decimal places numbers
	else:
		reserve=0
		for pos in range(reserve, fi):
			# catches everything except the first itteration if y is greater than x
			if int(y_str[pos]) > int(x_str[pos]) and pos!=fi-1:
				# handle nine flow on y
				nine=True
				for nine_pos in range(pos+1, fi):
					if int(y_str[nine_pos])!=9: nine=False
				# handle zero flow on x
				zero=True
				for zero_pos in range(pos+1, fi):
					if int(x_str[zero_pos])!=0: zero=False
				if nine==True:
					apnd='' if reserve==0 else y_str[:reserve]
					pos_num=str('[%s-%s]'%(str(int(x_str[pos])+ int(0  if zero==True \
							else 1)),str(y_str[pos])))
					nine_flow=str(('[0-9]'*int(fi-pos-1)) if int(fi-pos-1)<=1 \
							else ('[0-9]{%s}'%int(fi-pos-1)))
					regex_raw.append(str(apnd+pos_num+nine_flow))
					y_str=apnd+str(int(y_str[pos])-(int(y_str[pos])-int(x_str[pos])))+ \
						str('9'*(fi-pos-1))
					# breaks the line since the loop will finish when zero and nine flow are true
					if zero==True: break
				else:
					# crunch y with current pos decimal as constant
					# check for zero flow in y string
					apnd_lenght=0
					for i in range(pos+1, fi):
						if int(y_str[i])==0:
							apnd_lenght+=1
						else: break
					if fi-pos-1-apnd_lenght!=0: # in this case there is NO zero flow with y
						print(y_str[:0-pos-1-apnd_lenght])
						cruncher(int(y_str[pos+1+apnd_lenght:]), \
							fix=y_str[:0-pos-2-apnd_lenght])
					else: # in this case we append whole y as it has 0 till last char
						regex_raw.append(y_str)
					#
					if int(x_str[pos])+1==int(y_str[pos]):
						# does not append anymore numbers, just replaces y for next itteration
						y_str=y_str[:reserve]+str(int(y_str[pos])-1)+str('9'*int(fi-pos-1))
					else:
						# crunches median numbers
						crunch_apnd=y_str[:reserve]+str('[%s:%s]'%(int(x_str[pos])+1,\
								int(y_str[pos])-1))
						regex_raw.append(str(crunch_apnd + \
								(('[0-9]'*int(fi-pos-1)) if int(fi-pos-1)<=1 else \
								('[0-9]{%s}'%int(fi-pos-1)))))
						y_str=y_str[:reserve]+x_str[pos]+str('9'*int(fi-pos-1))
			# this one is handling only last digit, or the smallest decimal spot
			elif pos==fi-1:
				apnd=x_str[pos] if x_str[pos]==y_str[pos] else str('[%s-%s]'%(x_str[pos],y_str[pos]))
				regex_raw.append(y_str[:-1]+apnd)
			# passes the itteration if digits are same number
			elif int(y_str[pos])==int(x_str[pos]):
				pass
			reserve+=1

def colapseRanges():
	'''
		this function sorts ranges to fit for regex, largest number to smallest
		also colapses ranges that share portion of range. Example:
		10:100, 50:150 >> 10:150
	'''
	global range_vector
	grouped=[]
	for i in range_vector:
		nums=re.match('(.*)\:(.*)$', i)
		x=int(nums.group(1))
		y=int(nums.group(2))
		grouped.append([x,y])
	# sort by x
	group_sorted=sorted(grouped, key= lambda x: x[0])
	# compares the results and compresses them
	final_group=[]
	compare_me=[None]
	for i in group_sorted:
		if compare_me[0]==None:
			compare_me=[i[0], i[1]]
		elif i[0]<=compare_me[1]:
			if i[1]>compare_me[1]:
				compare_me=[compare_me[0], i[1]]
		else:
			final_group.append(str(str(compare_me[0])+':'+str(compare_me[1])))
			compare_me=[i[0], i[1]]
	# finally
	if compare_me[0]!=None: 
		final_group.append(str(str(compare_me[0])+':'+str(compare_me[1])))
	# apply fix reverse it to have decending order
	range_vector=reversed(final_group)

def expressionOptimizator(regex_group):
	'''
		function to optimize expressions
	'''
	'''
		=== optimize number flow ===
		example: 11111[0-9]
		optimized: 1{5}[0-9]
		will reduce only if there are 5+ same characters
	'''
	for exp, index in zip(regex_group, range(0, len(regex_group))):
		buff=''
		buff_count=1
		return_buffer=''
		for char in exp:
			if char==buff:
				buff_count+=1
			else:
				if buff_count>=5:
					return_buffer+=str(buff+str('{%s}'%buff_count))
				else:
					return_buffer+=buff*buff_count
				buff=char
				buff_count=1
		return_buffer+=str((buff*buff_count) if buff_count<5 else \
			str(buff+str('{%s}'%buff_count)))
		regex_group[index]=return_buffer
	'''
		=== collapse repetitions ===
		example: [1-9][0-9]{20},[1-9][0-9]{19}..[1-9][0-9]{2}
		optimized: [1-9][0-9]{2,20}
	'''
	return_buffer=[]
	buff=''; match=False
	# detecting string
	rep_finder=re.compile('(.*)\{(\d+)\}$')
	for exp in regex_group:
		x=rep_finder.match(exp)
		if x!=None:
			if match==True and buff[0]==x.group(1) and int(buff[2])-1==int(x.group(2)):
				buff=[buff[0], buff[1], x.group(2)]
			else:
				if match==True:
					return_buffer.append(buff[0]+(('{%s}'%buff[1]) if buff[1]==buff[2] else \
						('{%s,%s}'%(buff[2], buff[1]))))
				buff=[x.group(1), x.group(2), x.group(2)]
				match=True
		else:
			if match==True:
				return_buffer.append(buff[0]+(('{%s}'%buff[1]) if buff[1]==buff[2] else \
					('{%s,%s}'%(buff[2], buff[1]))))
			match=False
			buff=[]
			return_buffer.append(exp)
	if match==True:
		return_buffer.append(buff[0]+(('{%s}'%buff[1]) if buff[1]==buff[2] else \
			('{%s,%s}'%(buff[2], buff[1]))))
	del regex_group[:]
	regex_group.extend(return_buffer)

def prepForRegex():
	'''
		this function does what all have been waiting for
	'''
	global regex_raw
	out='^('
	for rng in regex_raw:
		out+=rng+'|'
	out=out[:-1]
	out+=')$'
	print(out)
		
if __name__ == "__main__" : reToRange()
