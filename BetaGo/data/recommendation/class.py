import json
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity

# load json file
def loadFont():
    f = open("db.json", encoding='utf-8')
    setting = json.load(f)
    dict = {}
    id = {}
    count = 1
    for i in setting:
        dict[i] = setting[i]
    for i in setting.keys():
        setting[i]['id'] = count
        count += 1
    return setting
description = loadFont()

# define keyword
keyword = {'security': 1, 'data': 2, 'software': 3, 'algorithm': 4, 'application': 5, 'network': 6,
           'distributed': 7, 'IoT': 8, 'blockchain': 9, 'python': 10, 'C++': 11, 'C': 12, 'engage': 13, 'digital': 14,
           'neural': 15, 'wireless': 16, 'search': 17, 'system': 18, 'vision': 19, 'hardware':20, 'compression':21, 'machine learning': 22,'artificial':23}

# Classify the course depend on overview
dict = {}
dict_name = {}
for i in description:
    dict[i] = description[i]['overview']
    dict_name[i] = description[i]['name']
frequency = {}
cl = {}
for i in dict:
    divi = re.sub(r'[^A-Za-z0-9]+',' ',dict[i])
    divi = divi.split(' ')
    d = re.sub(r'[^A-Za-z0-9]+',' ',dict_name[i])
    d = d.split(' ')
    classy = ''

    for j in keyword:
        if j in divi or j.capitalize() in divi or (j + 's') in divi:
            if j not in classy:
                classy += j + ' '
    for j in keyword:
        if j in d or j.capitalize() in d or (j + 's') in d:
            if j not in classy:
                classy += j + ' '
    cl[i] = classy
    for j in dict:
        if j in dict[i]:
            cl[i] = cl[j]

# store category in json file
for i in description:
    description[i]['category'] = cl[i]
jsonData = json.dumps(description)
fileObject = open('course_category.json', 'w')
fileObject.write(jsonData)
fileObject.close()






