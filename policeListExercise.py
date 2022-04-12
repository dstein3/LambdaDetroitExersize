import csv
import json
from functools import reduce


csvfile = open('911_Calls_for_Service_(Last_30_Days) (2).csv')
#lines = csvfile.read().splitlines()
lines = csv.DictReader(csvfile)

#sublines = lines[0:99]
#print(sublines)

#dictlist = []

#rest = 100
#while rest > 0:
#    dictlist.append({})
#    rest = rest - 1

#for line in range(0,99):
    #dictlist[line]['X']=(sublines[line].split(','))[0]
    #dictlist[line]['Y']=(sublines[line].split(','))[1]
    #dictlist[line]['incident_id']=(sublines[line].split(','))[2]
    #dictlist[line]['agency']=(sublines[line].split(','))[3]
    #dictlist[line]['incident_adress']=(sublines[line].split(','))[4]
    #dictlist[line]['zip_code']=(sublines[line].split(','))[5]
    #dictlist[line]['dispatchtime']=(sublines[line].split(','))[15]
    #dictlist[line]['totalresponsetime']=(sublines[line].split(','))[17]
    #dictlist[line]['totaltime']=(sublines[line].split(','))[19]
    #dictlist[line]['neighborhood']=(sublines[line].split(','))[20]

#list2 = map(lambda c: c.get('totalresponsetime'), dictlist)
#print(list2)



filtered_911_calls = list(filter(lambda x: x['zip_code'] != '' and x['neighborhood'] != '' and x['dispatchtime'] and x['totalresponsetime'] and x['totaltime'], lines))
total_response_time = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['totalresponsetime'].replace(' ','')) , filtered_911_calls, 0)
avg_total_response_time = total_response_time/len(filtered_911_calls)
print(avg_total_response_time)
sum_dispatchtime = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['dispatchtime'].replace(' ','')) , filtered_911_calls, 0)
avg_dispatchtime = sum_dispatchtime/len(filtered_911_calls)
print(avg_dispatchtime)
sum_totaltime = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['totaltime'].replace(' ','')) , filtered_911_calls, 0)
avg_totaltime = sum_totaltime/len(filtered_911_calls)
print(avg_dispatchtime)

#filtered by neighborhood

neighList = ['Airport Sub','Arden Park','Aviation Sub','Bagley','Belle Isle','Belmont','Berg-Lahser','Bethune Community','Blackstone Park','Boyston Edison','Boynton','Brewster Homes','Brightmoor','Brush Park','Buffalo Charles','Butler','Cadillac Community','Cadillac Heights','Campau/Banglatown','Carbon Works','Castle Rouge','Central Southwest','Chadsey Condon','Chalfonte','Chandler Park','Chandler-Park Chalmers','Claytown','College Park','Conant Gardens','Conner Creek','Conner Creek Industrial','Core City','Corktown','Cornerstone Village','Crary/St Marys','Cultural Center']

def filter_neigh(data, neighborhood):
    return list(filter(lambda x: x['neighborhood'] == neighborhood, data))

def avgDispatch(baseData,neighborhood):
    data = filter_neigh(baseData,neighborhood)
    sum_dispatchtime = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['dispatchtime'].replace(' ','')) , data, 0)
    denominator = len(data)
    if denominator == 0:
        denominator = 1
    return sum_dispatchtime/denominator

def avgTotalResponse(baseData,neighborhood):
    data = filter_neigh(baseData,neighborhood)
    sum_dispatchtime = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['totalresponsetime'].replace(' ','')) , data, 0)
    denominator = len(data)
    if denominator == 0:
        denominator = 1
    return sum_dispatchtime/denominator

def avgTotalTime(baseData,neighborhood):
    data = filter_neigh(baseData, neighborhood)
    sum_dispatchtime = reduce(lambda responsetime1, responsetime2: responsetime1 + float(responsetime2['totaltime'].replace(' ','')) , data, 0)
    denominator = len(data)
    if denominator == 0:
        denominator = 1
    return sum_dispatchtime/denominator

#i need a list of dictionaries for each neighborhood, has to have all three averages as item paris and also must have a name

avgList = []

rest = 36
while rest > 0:
    avgList.append({})
    rest = rest - 1

dislist = (list(map(lambda x: avgDispatch(filtered_911_calls,x), neighList)))
reslist = (list(map(lambda x: avgTotalResponse(filtered_911_calls,x), neighList)))
totlist = (list(map(lambda x: avgTotalTime(filtered_911_calls,x), neighList)))

for id in range(0,36):
    avgList[id]['name']=neighList[id]
    avgList[id]['avgDispatchTime']=dislist[id]
    avgList[id]['avgTotalResponseTime']=reslist[id]
    avgList[id]['avgTotalTime']=totlist[id]
    avgList[id]['totalPopulation']=639111

jsonFile = json.dumps(avgList)
print(jsonFile)

#each entry of the list is one line
