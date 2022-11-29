################################################
# Veit Ebbers
# 10/24/2022
# Project 3
################################################

import pandas as pd
import numpy as np
import itertools

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# variables 2
λ1 = 2
λ2 = 23
λ3 = 75
μ = 101
# variables 1
#λ1 = 5
#λ2 = 2
#λ3 = 3
#μ = 12

# user input
arrivals = input("Enter number of arrivals:")
print("Number of arrivals: " + arrivals)
arrivals=int(arrivals)

debugMode = input("Debug mode? (y/n): ")
if debugMode == "y": 
    print("Debug mode is on")
elif debugMode == "n":
    print("Debug mode is off")
else :
    print("Invalid input! Please enter y or n. Debug mode is off.")


# function to generate independent exponential random variables with mean 1/μ and the size of the arrivals
def generateTimes(x,arrivals):
    return np.random.exponential(scale=1/x,size=arrivals)

serviceTimes=generateTimes(μ,arrivals)
interarrivalTimeOne=generateTimes(λ1,arrivals)
interarrivalTimeOne[0:1] = 0
interarrivalTimeTwo=generateTimes(λ2,arrivals)
interarrivalTimeTwo[0:1] = 0
interarrivalTimeThree=generateTimes(λ3,arrivals)
interarrivalTimeThree[0:1] = 0

# calculate interarrival times
def computeInterarrivals(timeOne,timeTwo,timeThree, arrivals):
    arrivalRange=np.arange(arrivals)
    arrivalArray=np.zeros(int(arrivals))
    interarrivalOne=0
    interarrivalTwo=0
    interarrivalThree=0
    
    for i,λ1,λ2,λ3 in zip(arrivalRange,timeOne,timeTwo,timeThree):
        if λ1<=λ2 and λ1<=λ3:
            interarrivalOne+=1
            arrivalRange[i]=λ1
            arrivalArray[i]=λ1
        elif λ2<=λ1 and λ2<=λ3:
            interarrivalTwo+=1
            arrivalRange[i]=λ2
            arrivalArray[i]=λ2
        elif λ3<=λ1 and λ3<=λ2:
            interarrivalThree+=1
            arrivalRange[i]=λ2
            arrivalArray[i]=λ3

    return interarrivalOne/arrivals,interarrivalTwo/arrivals,interarrivalThree/arrivals,arrivalArray

#


# return cumulative sum
def interarrivalCumSum(x):
    return np.cumsum(x)

# mesh different incoming 
percentageOne,percentageTwo,percentageThree,interarrivals= computeInterarrivals(interarrivalTimeOne,interarrivalTimeTwo,interarrivalTimeThree, arrivals)
interarrivalsCumulated=interarrivalCumSum(interarrivals)

# calculate times
def calculateTimes(serviceTimes,arrivalTime):
    
    # append extra index to arrival time
    arrivalTime= np.append(arrivalTime,[0])
    
    # append extra index to time Service Begins
    timeServiceBegins=np.zeros(np.size(serviceTimes))
    timeServiceBegins=np.append(timeServiceBegins,[0])
    
    timeServiceEnds=np.zeros(np.size(serviceTimes))
    
    # index list
    indexList=np.arange(np.size(serviceTimes))
    
    
    for i,b,c,d,e in zip(indexList, arrivalTime, timeServiceBegins, serviceTimes, timeServiceEnds):
        if i!=0:
            if arrivalTime[i]>=timeServiceEnds[i-1]:
                timeServiceBegins[i]=arrivalTime[i]
                timeServiceEnds[i]+=arrivalTime[i]+serviceTimes[i]
            elif arrivalTime[i]<=timeServiceEnds[i-1]:
                timeServiceBegins[i]=timeServiceEnds[i-1]
                timeServiceEnds[i]+=timeServiceEnds[i-1]+serviceTimes[i]
        else:
            timeServiceEnds[0]=serviceTimes[0]

    # waiting time => cut of negative values since waiting time can not be negative
    waitingTime=timeServiceBegins-arrivalTime
    waitingTime[waitingTime<0]=0
    
    # time of customer in system
    customerInSystem=timeServiceEnds-arrivalTime[:-1]
    
    # idle time of server
    # index shift up and equalizing last index
    idleTime=np.roll(timeServiceBegins[:-1],-1)-timeServiceEnds
    idleTime=np.cumsum(idleTime)
    length=np.size(idleTime)-1
    idleTime[length]=0


                
    return timeServiceBegins,timeServiceEnds,waitingTime,customerInSystem, idleTime

timeServiceBegins,timeServiceEnds,waitingTime=calculateTimes(serviceTimes,interarrivalsCumulated)

# data frame for the table
if debugMode == "y":
    df=pd.DataFrame(columns=['Customer','Interarrival time(minutes)','Arrival time on clock','Service time(minutes)','Time Service begins','Waiting time in Queue','Time service ends','Time customer in system','Idle time of server'])
    df.loc[:, 'Customer'] = np.arange(1,(np.size(serviceTimes)+1),1,dtype=int)
    df.loc[:, 'Interarrival time(minutes)'] = interarrivals
    df.loc[:, 'Arrival time on clock'] = interarrivalCumSum(interarrivals)
    df.loc[:, 'Service time(minutes)'] = serviceTimes
    df.loc[:, 'Time Service begins'] = timeServiceBegins[:-1]
    df.loc[:, 'Time service ends'] = timeServiceEnds
    df.loc[:, 'Waiting time in Queue'] = waitingTime[:-1]

    print(df.head())
    print(df.tail())
    

# print results
print("\nAverage waiting time in queue: ",np.mean(waitingTime))
print("Average time customer in system: ",np.mean(timeServiceEnds))
print("Percentage of cars arriving from road 1: ",percentageOne)
print("Percentage of cars arriving from road 2: ",percentageTwo)
print("Percentage of cars arriving from road 3: ",percentageThree)