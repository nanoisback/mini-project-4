import random
flight_data = {}
aircraft_types = ["A320", "A350", "B787"]
passenger_storage = {}

class Flight:
    def __init__(self, id, public_id, departure, destination, departure_time, aircraft):
        self.__id = id
        self.public = public_id
        self.depart = departure
        self.des = destination
        self.time = departure_time
        self.type = aircraft

    def __str__(self):
        return (f"Flight {self.__id} has been created, departure: {self.depart}, arrival: {self.des}, departure time: {self.time}, aircraft: {self.type}")
    
    def store(self):
        if self.type == "A320":
            flight_data[self.public] = [self.public, self.depart, self.des, self.time, 4, 0, 180, 0] # 4 business, 0 prem eco, 180 economy, 0 reserved
        elif self.type == "A350":
            flight_data[self.public] = [self.public, self.depart, self.des, self.time, 29, 45, 231, 0] # 29 business, 45 prem economy, 231 economy, 0 reserved
        else:
            flight_data[self.public] = [self.public, self.depart, self.des, self.time, 28, 35, 211, 0] # 28 business, 35 prem economy, 211 economy, 0 reserved
    
class Passenger:
    def __init__(self, name, age, passport_id): # input passenger info
        self.name = name
        self.age = age
        self.__pass = passport_id

    def store(self):
        passenger_storage[self.__pass] = [self.name, self.age]

def Search(keyword, kind):    # use keyword to search for flight, might be anything in flight's info
    if keyword not in flight_data:
        return "No flight found"
    
    elif kind == "id":
        # search by public id
        return flight_data[keyword]
    
    elif kind == "departure":
        for i in flight_data:
            if flight_data[i][1] == keyword:    # search by departure place
                return flight_data[i]
            
    elif kind == "arrival":
        for i in flight_data:
            if flight_data[i][2] == keyword:    # search by destination
                return flight_data[i]
    
    elif kind == "departure time":
        for i in flight_data:
            if flight_data[i][3] == keyword:    # search by departure time
                return flight_data[i]

class Reservation:
    def __init__(self, name, passport, seat_class, flight_pub_id):
        self.name = name
        self.passport = passport
        self.pub_id = flight_pub_id
        self.seat = seat_class
        
    def confirm_action(self, inp):
        if self.passport in passenger_storage:
            print(f"Passenger {self.name}, passport: {self.passport}, confirm to book seat in {self.seat} class on flight {self.pub_id}")
            if inp == "Confirm":
                if self.seat == "Business":
                    if flight_data[self.pub_id][-4] > 0:
                        flight_data[self.pub_id][-4] -= 1
                        flight_data[self.pub_id][-1] += 1
                        print("Seat booked")
                    else:
                        print("No seat in class available")

                elif self.seat == "Premium economy":
                    if flight_data[self.pub_id][-3] > 0:
                        flight_data[self.pub_id][-3] -= 1
                        flight_data[self.pub_id][-1] += 1
                        print("Seat booked")
                    else:
                        print("No seat in class available")

                elif self.seat == "Economy":
                    if flight_data[self.pub_id][-2] > 0:
                        flight_data[self.pub_id][-2] -= 1
                        flight_data[self.pub_id][-1] += 1
                        print("Seat booked")
                    else:
                        print("No seat in class available")

                passenger_storage[self.passport] = [Passenger.name, Passenger.age, self.pub_id, self.seat]
            else:
                pass
        else:
            print("Passenger does not exist")
            pass
    
    def cancel(self):
        if self.passport in passenger_storage and len(passenger_storage[self.passport]) == 4:
            print(f"Passenger {self.name}, passport: {self.passport}, cancel seat in {self.seat} class on flight {self.pub_id}")
            if self.seat == "Business":
                flight_data[self.pub_id][-4] += 1
                flight_data[self.pub_id][-1] -= 1
                print("Seat released")

            elif self.seat == "Premium economy":
                flight_data[self.pub_id][-3] += 1
                flight_data[self.pub_id][-1] -= 1
                print("Seat released")

            elif self.seat == "Economy":
                flight_data[self.pub_id][-2] += 1
                flight_data[self.pub_id][-1] -= 1
                print("Seat released")

            passenger_storage[self.passport] = [Passenger.name, Passenger.age]
        
        elif self.passport in passenger_storage and len(passenger_storage[self.passport]) < 4:
            print("Passenger currently does not have booked seat")
        
        else:
            print("Passenger not found")
    