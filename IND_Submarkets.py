# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:17:20 2016

ideas for simplification: 
    -create new submarket objects with each combine rather than track in existing submarket objects 
    -add a "new_submarkets" dictionary for tracking above....starts with 

@author: cmelo
"""

from collections import defaultdict
import pandas 
import numpy as np 
import json
import os 
import sys 
import math as m 

os.chdir('P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets') 

class Submarket(object): 
    def __init__(self,SubmarketCode="",Inventory=0,Avg_Building_Size=0,x=0,y=0): 
        self.orig_Inventory=Inventory
        self.orig_Avg_Building_Size=Avg_Building_Size
        self.originalcode=SubmarketCode 
        self.neighbors=[]
        self.combine_with=set([SubmarketCode])
        self.combine=0
        self.new_Inv=Inventory
        self.mean=(x,y)
        self.currmean=(x,y)
        if Avg_Building_Size>0:
            self.orig_N=Inventory/Avg_Building_Size 
            self.curr_N=Inventory/Avg_Building_Size 
        else:
            self.orig_N=0
            self.curr_N=0
            
    def getInventory(self):
        return self.orig_Inventory
    def getCurrentInventory(self):
        return self.new_Inv
    def getAvg_Building_Size(self):
        return self.orig_Avg_Building_Size 
    def getcode(self):
        return self.originalcode 
    def getcurrentcode(self):
        code=''
        for s in sorted(self.combine_with):
            code=code+s
        return code 
        #return self.currentcode
    def AddNeighbor(self,submarket): 
        self.neighbors.append(submarket) 
    def PrintNeighbors(self):
        for neighbor in self.neighbors: 
            print '{0}: ({1},{2})'.format(neighbor.getcode(), str(self.Inventory), str(self.Avg_Building_Size))
    def PrintSubmarket(self):
        print "Submarket,", self.code
        self.PrintNeighbors()
    def Neighbors(self):
        return self.neighbors
    def getComboList(self):
        return self.combine_with
    def setNewCode(self,new_code):
        self.currentcode=new_code 
    def update(self,combined_with_list,new_inv,new_N):
        self.combine=1
        self.new_Inv=new_inv 
        self.curr_N=new_N
        new_combine_list= self.combine_with.union(combined_with_list)
        self.combine_with=new_combine_list
    def combinestatus(self):
        return self.combine
    def printcombinelist(self):
        print self.combine_with


def calc_distance(p1,p2):
    return m.sqrt(m.pow(p2[0]-p1[0],2)+m.pow(p2[1]-p1[1],2))
    
def newmid(CodeList): 
    print "called new mid"
    w=0
    points=[]
    for Code in CodeList:
        if submarkets[Code].mean!=(0,0):
            points.append([submarkets[Code].mean,submarkets[Code].getInventory()])
    runx=0
    runy=0
    if len(points)>1:
        for point in points:
            print point
            runx=runx+point[0][0]*point[1]
            runy=runy+point[0][1]*point[1]
            w=w+point[1]
        new_mid=(float(runx/w),float(runy/w))
        for Code in CodeList:
            submarkets[Code].currmean=new_mid 
        
def combine(s1,s2): 
    #combines two current submarkets into a new submarket 
    
    s1_start_inv=s1.getCurrentInventory()
    s2_start_inv=s2.getCurrentInventory()
    s1_N=s1.curr_N
    s2_N=s2.curr_N
    print "combining", s1.getcode(), "with", s2.getcode()
    #s1 gets combined with everyone s2 is connected with b/c a)we add all elements in s2's combo list to s1 and b) we add their codes together 
    s1.update(set([s2.getcode()]).union(s2.getComboList()),s1_start_inv+s2_start_inv,s1_N+s2_N)
    s2.update(set([s1.getcode()]).union(s1.getComboList()),s1_start_inv+s2_start_inv,s1_N+s2_N)
    print s1.getcode(), "has the following in combine list", s1.printcombinelist(), "and new inventory of", s1.getCurrentInventory()
    print s2.getcode(), "has the following in combine list", s2.printcombinelist(), "and new inventory of", s2.getCurrentInventory()
    print s1.getcode(), ", combine set to 1"
    print s2.getcode(), ", combine set to 1"
   # print s1.getcode(), "NOW has the following in combine list", s1.printcombinelist(), "AND code of" s1.getcurrentcode()
   # print s2.getcode(), "NOW has the following in combine list", s2.printcombinelist(), "AND code of" s2.getcurrentcode()
    #now, we must update any submarkets they peviously combine with-> combo list of s1 is same as s2, so only need to iter through 1 list 
    if len(s1.getComboList())>2:
        for sub in s1.getComboList():
            print "updating", sub
            submarkets[sub].update(s1.getComboList(),s1.getCurrentInventory(),s1.curr_N)
            print "now has combine list of" , submarkets[sub].printcombinelist(), "and new inventory of", submarkets[sub].getCurrentInventory()
    newmid(s1.getComboList())
#HOME FILE PATHS 
#neighbors_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/LOSA_Neighbors.csv"
#submarkets_file="/Users/cmelo/Google Drive/Costar work/IND Submarkets/SubmarketList.csv"

#WORK FILE PATHS
neighbors_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\LOSA_Neighbors_v2.csv"
submarkets_file="P:\Work in Progress\Carlota Melo\IND Submarkets\Submarkets\SubmarketList.csv"

#reads in csv neighbors data as a pandas dataframe 
neighbors_raw=pandas.read_csv(neighbors_file, header=0, index_col=0)

submarkets={}
subs_sortedbyN=[]
previous_index=0

#convert raw data into submarkets  and store them in a DICTIONARY where key=submarketcode and value is submarket OBJECT
for index, row in neighbors_raw.iterrows(): 
    #I'm only trying to combine submarkets less than 10million SF in size; with other submarkets less than 15millionSF in size 
    if index!=previous_index: 
        subs_sortedbyN.append(index)
        current_sub=Submarket(index,float(row['src_Inventory']), float(row['src_Avg_Building_Size']), float(row['src_Xcoord']), 
            float(row['src_YCoord']))
    current_sub.AddNeighbor(row['nbr_LOGCode'])
    previous_index=index
    submarkets[index]=current_sub 

#for k,v in submarkets.iteritems(): 
    #print k
    #print v.Neighbors()

print subs_sortedbyN 
i=0
for s in subs_sortedbyN:
    submarket=submarkets[s]
    #print submarket.getcode()
    zero=0   
    if i<10000:
        print "NEW SUBMARKET:In submarket", submarket.getcode(),"with inventory", submarket.getInventory()
        #n=raw_input("Press any key to continue:")
        combine_flag=0
        curr_diff=10000000
        s_Inventory=submarket.getInventory()
        s_avg=submarket.getAvg_Building_Size() 
        for n in submarket.Neighbors():
            neighbor=submarkets[n]
            print "examining neighbor",neighbor.getcode(),"with", neighbor.getInventory(),"inventory"
            print "with combine code of",neighbor.combinestatus() 
            n_avg=neighbor.getAvg_Building_Size()
            #1. always combine submarket with any neigbors that have no Inventory that have not already been combined 
            if neighbor.getCurrentInventory()==0 and neighbor.combinestatus()==0 and zero<2:
                    print "calling combine from 0 if statement"
                    combine(neighbor,submarket)
                    zero+=1 
            #2.Of all the neighbors, track all those combinations which lead to ~10M SF and combine with submarket that has closest AVG BLDG SIZE
            elif neighbor.curr_N!=0 and neighbor.combinestatus()==0:
                if submarket.curr_N<10 and calc_distance(submarket.currmean,neighbor.currmean)<curr_diff:
                    print "combine flag set to 1"
                    comb_neighbor=neighbor
                    curr_diff=calc_distance(submarket.mean,neighbor.mean)
                    combine_flag=1
                    
        if combine_flag==1: 
            combine(comb_neighbor,submarket)
    i+=1
        
#GET OUTPUT 
output=pandas.DataFrame.from_dict(submarkets, orient='index') 
output['orig_inventory']=0
output['final_code']='Unchanged'
output['final_inventory']=0 
output['final_N']=0
for k,v in submarkets.iteritems(): 
    output.loc[k,'orig_inventory']=v.getInventory()
    output.loc[k,'final_code']=v.getcurrentcode()
    output.loc[k,'final_inventory']=v.getCurrentInventory()
    output.loc[k,'final_N']=v.curr_N
print zero
output.to_csv("output.csv") 
"""
codes=lambda x: x.getcode()     
track_submarkets['new_codes']=track_submarkets['new_submarket'].map(codes)
track_submarkets['Inventory']=track_submarkets['new_submarket'].map(lambda x: x.getInventory())
track_submarkets.to_csv("output.csv")


#After initial combines, go throguh track submarkets and see which submarkets are still <10 M SF
#still_small=track_submarkets['Inventory']<10000000
#print still_small 
#for submarket in 
"""