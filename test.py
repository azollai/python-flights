print("Loading...")

from typing import List
from ryanair2 import Ryanair,Flight
from datetime import date, datetime, timedelta
from enum import Enum, IntEnum
import pickle
from collections import namedtuple

DAYS_IN_A_WEEK = 7
GoodDay = namedtuple("GoodDay", ("start", "end"))
Trip = namedtuple("Trip",("start","end"))

class Day(IntEnum):
    MONDAY = 0,
    TUESDAY = 1,
    WEDNESDAY = 2,
    THURSDAY = 3,
    FRIDAY =4,
    SATURDAY = 5,
    SUNDAY = 6

ryanair = Ryanair("DKK") 
TODAY = date.today().strftime("%d-%m-%y")
GOOD_DAYS:list[GoodDay] = [
    {"start":Day.THURSDAY,"end":Day.SATURDAY},
    {"start":Day.FRIDAY,"end":Day.SATURDAY},
    {"start":Day.FRIDAY,"end":Day.SUNDAY},
    {"start":Day.SATURDAY,"end":Day.SUNDAY},
    {"start":Day.SATURDAY,"end":Day.MONDAY},
    {"start":Day.SUNDAY,"end":Day.MONDAY},
    {"start":Day.SUNDAY,"end":Day.TUESDAY},
    {"start":Day.FRIDAY,"end":Day.MONDAY},
    {"start":Day.FRIDAY,"end":Day.TUESDAY},
    {"start":Day.THURSDAY,"end":Day.SUNDAY},
    {"start":Day.THURSDAY,"end":Day.MONDAY},
]
LEAVE_HOUR = {"from":7,"to":11}
ARRIVE_BACK_HOUR ={"from":18,"to":21}

def getAllDatesBetween(start_date:date,end_date:date)->list[str]:
    delta = end_date - start_date   # returns timedelta
    dates = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates.append(day.isoformat())
    return dates

def getCheapestFlight(fro:str,to:str,dateFrom:str,dateTo:str)->list[Flight]:
    flights = ryanair.get_flights(fro,to,dateFrom,dateTo)
    if len(flights) == 0:
        return None
    flight = flights[0]
    return flight

def getAllFlights(fro:str,to:str,dates:list[date])->list[Flight]:
    _flights=[]
    for d in dates:
        flight = getCheapestFlight(fro,to,d,d)
        if flight != None:
            _flights.append(flight)
    print("")
    return _flights

def saveData(fro:str,to:str,flights:list[Flight],_date_to_use:str):
    pickle.dump(flights,open(fro+"_"+to+"_"+"flights"+_date_to_use+".dat","wb"))
def loadData(fro:str,to:str,_date_to_use:str):
    return pickle.load(open(fro+"_"+to+"_"+"flights"+_date_to_use+".dat","rb"))

def printFlights(flights:list[Flight]):
    for f in flights:
        if f != None:
            print(f.departureTime,f.price)
def printCheapFlights(flights:list[Flight],price:int):
    _flights = filter(lambda f:f!=None and f.price<price,flights)
    printFlights(_flights)

def lookUpPerfectTrips(there_flights: List[Flight],back_flights: List[Flight],good_days:list[GoodDay],leave_hour:int,arrive_back_hour:int,max_price:int)->list[Trip]:
    perfect_trips:list[Trip] = []

    for start_flight in there_flights:
        for good_day in good_days:
            if doesGoodDayMatchStartFlight(good_day,start_flight) == False:
                continue
            end_flight:Flight = getEndFlight(back_flights, start_flight, good_day)
            if end_flight == None:
                continue

            price_total_ok = start_flight.price + end_flight.price < max_price
            if price_total_ok == False:
                continue

            leave_hour_ok = start_flight.departureTime.hour < leave_hour
            if leave_hour_ok == False:
                continue

            arrive_back_hour_ok = end_flight.departureTime.hour > arrive_back_hour   
            if arrive_back_hour_ok == False:
                continue

            perfect_trips.append({"start":start_flight,"end":end_flight})
    
    return perfect_trips

def getEndFlight(back_flights:list[Flight], start_flight:Flight, good_day:GoodDay)->Flight:
     diff_in_days = getDifferenceInDays(good_day)
     end_date:datetime = (start_flight.departureTime + timedelta(days = diff_in_days))
     end_flight:Flight = None
     for f in back_flights:
        if f.departureTime.year == end_date.year and f.departureTime.month == end_date.month and f.departureTime.day == end_date.day:
            end_flight = f
     return end_flight

def doesGoodDayMatchStartFlight(good_day:GoodDay, start_flight:Flight)->bool:
    #print(good_day,start_flight)
    st=int(good_day["start"])
    wd=start_flight.departureTime.weekday()
    return st ==wd 

def getDifferenceInDays(good_day:GoodDay)->int:
    diff_in_days = good_day["end"] - good_day["start"]
    if diff_in_days < 0:
        diff_in_days += DAYS_IN_A_WEEK
    return diff_in_days

def printPerfectTrips(trips:list[Trip]):
    print("")
    print("Perfect trips:")
    for t in trips:
        printFlights([t["start"],t["end"]])
        print("")

def getFlights(fro:str, to:str, _dates:list[date], _date_to_use:str, _ingest:bool)->list[Flight]:
    flights = []
    if ingest:
        flights = getAllFlights(fro,to,_dates)
        saveData(fro,to,flights,_date_to_use)
    else:
        flights = loadData(fro,to,_date_to_use)
    return flights

dates = getAllDatesBetween(date(2023,1,1),date(2023,3,1))
FROM = "CPH"
TO = "VCE"
ingest = True
date_to_use = TODAY

there_flights = getFlights(FROM,TO,dates,date_to_use,ingest)
back_flights = getFlights(TO,FROM,dates,date_to_use,ingest)

print("THERE_FLIGHTS")
printFlights(there_flights)
print("BACK_FLIGHTS")
printFlights(back_flights)
#printCheapFlights(flights,200)
perfect_trips = lookUpPerfectTrips(there_flights,back_flights,GOOD_DAYS,20,5,600)
printPerfectTrips(perfect_trips)