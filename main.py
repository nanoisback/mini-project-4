import sys
flight_data = {}    # store flight data
aircraft_types = ["A320", "A350", "B787"]
passenger_storage = {}  # store passenger data: name, age, passport id, flight, seat

class Flight:
    def __init__(self, id, public_id, departure, destination, departure_time, aircraft):
        self.__id = id
        self.public = public_id
        self.depart = departure
        self.des = destination
        self.time = departure_time
        self.type = aircraft

    def __str__(self):
        return (f"Flight {self.__id} has been created with public ID: {self.public}, departure: {self.depart}, arrival: {self.des}, departure time: {self.time}h, aircraft: {self.type}")
    
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
        return flight_data[keyword]             # search by public id
    
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
        if self.passport in passenger_storage and self.pub_id in flight_data:
            print(f"Passenger {self.name}, passport: {self.passport}, confirm to book seat in {self.seat} class on flight {self.pub_id}")
            if inp == "Confirm":                            # if user confirm, proceed to change data in fligh data and passenger data
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

                passenger_storage[self.passport].extend([self.pub_id, self.seat])
            else:
                pass
        else:
            print("Passenger or flight does not exist")
    
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
        
        elif self.passport in passenger_storage and len(passenger_storage[self.passport]) < 4:  # error handle: cancel while not booked seat
            print("Passenger currently does not have booked seat")
        
        else:
            print("Passenger not found")

class AirlineSystem:
    def __init__(self):
        pass
    
    def add_flight(self, id, public_id, departure, destination, departure_time, aircraft):
        ad = Flight(id, public_id, departure, destination, departure_time, aircraft)
        print(ad)
        ad.store()
    
    def view_flight_details(self, flight_number):
        if flight_number in flight_data:
            print(Search(flight_number, id))
        else:
            print("Flight not found")
    
    def view_passenger_details(self, passport_number):
        if passport_number in passenger_storage:
            print(passenger_storage[passport_number])
        else:
            print("Passenger not found")
    
    def cancel_flight(self, id):
        flight_data.pop(id)


system = AirlineSystem()        # front-end
while True:
    print("\nKS Airlines Reservation System")   # choices
    print("1. Add Flight")
    print("2. Register Passenger")
    print("3. Book Seat")
    print("4. Cancel Reservation")
    print("5. View Flight Details")
    print("6. View Passenger Details")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("Logging in airline management system...")
        internal_id = input("Enter internal id: ")
        flight_number = input("Enter public id: ")
        departure = input("Enter departure: ")
        destination = input("Enter destination: ")
        departure_time = input("Enter departure time: ")
        aircraft = input("Enter aircraft type: ")
        if aircraft != "A320" and aircraft != "A350" and aircraft != "B787":    # error handle: wrong aircraft choice
            print("Aircraft type error")
        else:
            system.add_flight(internal_id, flight_number, departure, destination, departure_time, aircraft)

    elif choice == '2':
        name = input("Enter passenger name: ")
        age = input("Enter passenger age: ")
        passport_number = input("Enter passport number: ")
        passenger = Passenger(name, age, passport_number)
        passenger.store()
        print("Passenger registered successfully!")

    elif choice == '3':
        flight_number = input("Enter flight number: ")
        passport_number = input("Enter passenger passport number: ")
        name = input("Enter your name: ")
        seat_class = input("Enter your seat class (Business, Premium economy, Economy): ")
        if seat_class != "Business" and seat_class != "Premium economy" and seat_class != "Economy":    # error handle: wrong seat choice
            print('Invalid seat choice!')
        else:
            re = Reservation(name, passport_number, seat_class, flight_number)
            re.confirm_action(input("Please make sure you want to book a seat: 'Confirm' or 'Cancel': "))

    elif choice == '4':
        flight_number = input("Enter flight number: ")
        passport_number = input("Enter passenger passport number: ")
        name = input("Enter your name: ")
        seat_class = input("Enter your seat class: ")
        if seat_class != "Business" and seat_class != "Premium economy" and seat_class != "Economy":
            print('Invalid seat choice!')
        else:
            ca = Reservation(name, passport_number, seat_class, flight_number)
            ca.cancel()

    elif choice == '5':
        print("Logging in airline management system...")
        flight_number = input("Enter flight number: ")
        system.view_flight_details(flight_number)

    elif choice == '6':
        print("Logging in airline management system...")
        passport = input("Enter passenger's passport number: ")
        system.view_passenger_details(passport)

    elif choice == '7':
        print("Exiting the system. Goodbye!")
        sys.exit()

    else:
        print("Invalid choice. Please try again.")  # just in case someone input 8 9 10 or so