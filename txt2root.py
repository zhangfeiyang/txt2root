#!/usr/bin/env python

import sys

def remove_symbol(data):

	result = []

	datas = data.split('\n')
	index = datas[0].split(':')[1]
	result.append(index)
	event_time = datas[1].split(':')[1].strip('ns')
	result.append(event_time)
	traceNumber = datas[3].split('=')[1]
	result.append(traceNumber)

	trs = list(map(lambda x:x.strip('tr_ind=').replace(' tr=','').strip('\n').split(','),datas[4:204]))
	result.append(trs)

	return result


from ROOT import *
from array import array

input_file_name = sys.argv[1]

file_id = sys.argv[2]

input_file = open(input_file_name,'r')

content = input_file.read()

contents = content.split('trigger index')

N = int((len(contents)-1)/3)


f0 = TFile('data'+file_id+'.root','recreate')

t = TTree('t',"")

index = array('f',[0.0])
event_time = array('f',[0.0])
traceNumber = array('f',[0.0])
tr_ind = array('f',200*[0.0])
tr = array('f',200*[0.0])

t.Branch("index",index,'index/F')
t.Branch("event_time",event_time,'event_time/F')
t.Branch("traceNumber",traceNumber,'traceNumber/F')
t.Branch("tr_ind",tr_ind,'tr_ind[200]/F')
t.Branch("tr",tr,'tr[200]/F')

for i in range(N):
	data = contents[i*3+int(file_id)+1]

	result = remove_symbol(data)	
	
	index[0] = float(result[0])
	event_time[0] = float(result[1])
	traceNumber[0] = float(result[2])
	for i,v in enumerate(list(float(x[0]) for x in result[3])):
		tr_ind[i] = v
	for i,v in enumerate(list(float(x[1]) for x in result[3])):
		tr[i] = v
	
	t.Fill()

t.Write()
f0.Close()
