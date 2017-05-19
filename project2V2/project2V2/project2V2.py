# -*- coding: utf-8 -*-
print("####################### Please Hold I am Training (This will take some time) ##################")

import json
import re
import numpy as np
from matplotlib import style 
style.use("ggplot")
from sklearn.cluster import  MiniBatchKMeans
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer as CVEC
import matplotlib.pyplot as plt
from matplotlib import style 
style.use("ggplot")



file="yummly.json"

with open(file,encoding='utf-8') as data_file:
    data=json.loads(data_file.read())

t1=data[0:] #20000

cuisine=re.findall(r'\'cuisine\': \'(.*?)\'',str(t1))
cuisine=re.sub(r'[\'|\"|\[|\]]','',str(cuisine))
cuisine=cuisine.split(",")
strip_cus=[]
for n in cuisine:
    strip_cus.append(n.strip())
cuisine=strip_cus

IDnumber=re.findall(r'\'id\': (.*?)[,|}]',str(t1)) #some times have to use } and sometimes ,
IDnumber=re.sub(r'[\'|\"|\[|\]]','',str(IDnumber))
IDnumber=IDnumber.split(",")

#print(IDnumber)

ID_hold=[]
for IDs in IDnumber:
    ID_hold.append(int(IDs))
IDnumber=ID_hold

ingredients_list=[]

for food in t1:
    #ingredients=[]
    ingredients=re.findall(r'\'ingredients\': (.*?)\]',str(food))
    ingredients=re.sub(r'[\'|\"|\[|\]]','',str(ingredients))
    ingredients=re.sub(r'-',' ',str(ingredients)) ################Have to also remove these from input strings
    ingredients=ingredients.split(",")
    strip_ing=[]    
    for n in ingredients:
        strip_ing.append(n.strip())
    ingredients_list.append(strip_ing)

############################################################

how_many_sampled=1000

cuisines=[]
for x in cuisine:
    if x not in cuisines:
        cuisines.append(x)


Cus=[]
I=[]
In=[]
for x in cuisines:
    nth=0
    List_cus=[]
    List_ID=[]
    List_In=[]
    for y in cuisine:
        
        if y==x:
            List_cus.append(cuisine[nth])
            List_ID.append(IDnumber[nth])
            List_In.append(ingredients_list[nth])            
        nth +=1
    for c in (List_cus[:how_many_sampled]):
        Cus.append(c)
    for i in (List_ID[:how_many_sampled]):
        I.append(i)
    for Ing in (List_In[:how_many_sampled]):
        In.append(Ing)

#==============================================================================
# for x in cuisines:
#     print(Cus.count(x))
#==============================================================================
    
IDnumber=I
cuisine=Cus
ingredients_list=In 
    
        
        
#########################################################################3        

   

IDS=[]
Long_ing=[]
values=[]
cuisine_Type=[]
nth=0
for sublists in ingredients_list:
    for item in sublists:
        Long_ing.append(item)
        IDS.append(IDnumber[nth])
        cuisine_Type.append(cuisine[nth])
        values.append(1)
    nth +=1



ty=[]
for i in Long_ing:
    ty.append(re.sub(r'(?<=[A-Z,a-z])[\s|-](?=[A-Z,a-z])','UQUQ',i))
Long_ing=ty
ty=[]



vectorizer=CVEC( max_df=.20,min_df=.001) #change to .1 later , min_df=.001 
CVEC_fit=vectorizer.fit_transform(Long_ing)

Long_ing=[]
for i in vectorizer.get_feature_names():
    Long_ing.append(re.sub(r'uquq',' ',i))
    
print("Identified obscure frequent ingredients:" + str(len(Long_ing)) )    #+ str(Long_ing)

genid=[]
for ilist in ingredients_list:
    ingx=[]
    for ing in Long_ing:
        if ing in ilist:
            ingx.append(1)
        else:
            ingx.append(0)
    genid.append(ingx)


clf=svm.SVC(gamma='auto')
x,y=genid,cuisine
clf.fit(x,y)

print("####################### I am Finished Let's Go ##################")


#####################Start inputs here

def predict_food(user_Ingredients):
    
    input_x=user_Ingredients         
        
    
    ingredients=re.sub(r'[\'|\"|\[|\]]','',str(input_x))
    ingredients=re.sub(r'-',' ',str(ingredients)) ################Have to also remove these from input strings
    ingredients=ingredients.split(",")
    strip_ing=[]    
    for n in ingredients:
        strip_ing.append(n.strip())
          
      
    input_x=strip_ing  


    
    #######create the binary
    input_id=[]
    for ing in Long_ing:
        if ing in input_x:
            input_id.append(1)
        else:
            input_id.append(0)
    

    p=np.array(input_id)
    p=p.reshape(1,-1)
    The_result=clf.predict(p)
    
    print('I think it is',re.sub(r'[\[|\'|\]|\s]','',str(The_result)))
    
    to_cluster=genid#[]
    numb=0
    like_food=IDnumber
#==============================================================================
#     for food in cuisine:
#         if food ==The_result:
#             to_cluster.append(genid[numb])
#             like_food.append(IDnumber[numb])
#             
#         numb +=1
#==============================================================================
    
      
    cuisine.append(The_result)
    to_cluster.append(input_id)
    like_food.append(999999999)
    
    Number_Clusters=21
    
        
    mbk=MiniBatchKMeans(init='k-means++', n_clusters=Number_Clusters,
                            n_init=20, max_no_improvement=30, verbose=0,random_state=5)
                            
    feature=np.array(to_cluster)
        
        
    mbk.fit(feature) 
        
    labels=mbk.predict(feature) 
    
    
    look_for=labels[-1]
    
    
    nth=0
    similar_foods=[]
    cuisine_in_cluster=[]
    for item in labels:
        if item == look_for:
            similar_foods.append(like_food[nth])
            cuisine_in_cluster.append(cuisine[nth])
        nth +=1
    
    print("Some similar foods:",similar_foods[0:5])
    #print(cuisine_in_cluster[0:5])
    #print(len(labels))
    #print(len(cuisine))
    
    objects=[]
    for x in cuisine_in_cluster:
        if x not in objects:
            objects.append(x)
            
    performance=[]
    for x in objects:
        performance.append(cuisine_in_cluster.count(x))
    
    y_pos = np.arange(len(objects))
    
    plt.bar(y_pos, performance,align='center')
    plt.xticks(y_pos, objects, rotation=90)
    plt.ylabel('Count')
    plt.title('Cuisines in Clusters')
    plt.show()
    

def user_program():

    user_Ingredients=[]
    user_input="a"
    while user_input != "Exit":
        print("Exit=Exit List=Enter List of Ingredients")
        user_input=input()
        if user_input == "List":
            print("Example input: Flour, water, egg")
            user_Ingredients=input()
            user_Ingredients=user_Ingredients.split(",")
            hold_x=[]
            for n in user_Ingredients:
                hold_x.append(n.strip().lower())
            user_Ingredients=hold_x
            predict_food(user_Ingredients)





