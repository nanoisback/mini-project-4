import sys

class Passenger:
    def __init__(self, name, age, passport_id, flight = None, seat_class = None):
        self.name = name
        self.age = age
        self.passport_id = passport_id
        self.flight = flight
        self.seat = seat_class

class Flight:
    def __init__(self, flight_number, departure, destination, departure_time, aircraft_type):
        self.__id = str(ord(departure[0].lower())) + str(ord(destination[0].lower())) + str(departure_time) + str(aircraft_type[1::])
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.departure_time = departure_time
        self.aircraft_type = aircraft_type
        self.reserved_seats = 0
        if self.aircraft_type == "A320":        # seat map for A320 with 4 business seats and 180 economies
            self.business_seats = 4
            self.premium_economy_seats = 0
            self.economy_seats = 180
        elif self.aircraft_type == "A350":      # seat map for A350: 29 business, 45 prem eco and 231 eco
            self.business_seats = 29
            self.premium_economy_seats = 45
            self.economy_seats = 231
        elif self.aircraft_type == "B787":      # seat map for B787: 28 business, 35 prem eco and 211 eco
            self.business_seats = 28
            self.premium_economy_seats = 35
            self.economy_seats = 211

    def book_seat(self, seat_class):       # when book seat, the seat in correlated class -= 1 and reserved seat += 1
        if seat_class == "Business" and self.business_seats > 0:
            self.business_seats -= 1
            self.reserved_seats += 1
            return True
        elif seat_class == "Premium Economy" and self.premium_economy_seats > 0:
            self.premium_economy_seats -= 1
            self.reserved_seats += 1
            return True
        elif seat_class == "Economy" and self.economy_seats > 0:
            self.economy_seats -= 1
            self.reserved_seats += 1
            return True
        else:
            return False

    def cancel_seat(self, seat_class):
        if seat_class == "Business":
            self.business_seats += 1
            self.reserved_seats -= 1
        elif seat_class == "Premium Economy":
            self.premium_economy_seats += 1
            self.reserved_seats -= 1
        elif seat_class == "Economy":
            self.economy_seats += 1
            self.reserved_seats -= 1
    
    def get_in_id(self):    # to get internal id, this is a getter method
        return self.__id

    def __str__(self):
        return f"Flight {self.flight_number}, Departure: {self.departure}, Destination: {self.destination}, Departure Time: {self.departure_time}h, Aircraft: {self.aircraft_type}, Business seats: {self.business_seats}, Premium Economy seats: {self.premium_economy_seats}, Economy seats: {self.economy_seats}, Reserved: {self.reserved_seats}"

class Reservation(Passenger):
    def __init__(self, name, age, passport_id, flight, seat):
        super().__init__(name, age, passport_id, flight, seat)

    def confirm_reservation(self):
        if self.flight.book_seat(self.seat):
            print(f"Reservation confirmed for {self.name} on {self.flight} in {self.seat} class.")
        else:
            print(f"No available seats in {self.seat} class for {self.flight}.")

    def cancel_reservation(self):
        self.flight.cancel_seat(self.seat)
        print(f"Reservation canceled for {self.name} on flight {self.flight}.")


class AirlineSystem(Flight):
    def __init__(self):
        # flights dictionary with 2 flights inside by default
        self.flights = {'KS203': Flight('KS203', 'Ha Noi', 'Ho Chi Minh City', 16, 'A350'), 'KS402': Flight('KS402', 'Seoul Incheon', 'Da Nang', 1, 'B787')}
        self.passengers = {}

    def add_flight(self, flight_number, departure, destination, departure_time, aircraft_type):
        if flight_number in self.flights:
            print("Flight already exists.")
            return
        else:
            flight = Flight(flight_number, departure, destination, departure_time, aircraft_type)
            self.flights[flight_number] = flight
            print(flight, "has been created")

    def register_passenger(self, name, age, passport_id):
        if passport_id in self.passengers:
            print("Passenger already registered.")
            return
        passenger = Passenger(name, age, passport_id)
        self.passengers[passport_id] = passenger
        print(f"Passenger {name} registered successfully.")

    def view_flight_details(self, flight_number):
        flight = self.flights.get(flight_number)
        if flight:
            print(f"Internal ID (do not leak): {flight.get_in_id()}") # this is for airline staff so they can view internal id, using the getter method from Flight class to get the id
            print(f"Flight number: {flight.flight_number}")
            print(f"Departure: {flight.departure}")
            print(f"Arrival: {flight.destination}")
            print(f"Departure time: {flight.departure_time}h")
            print(f"Business seats left: {flight.business_seats} seats")
            print(f"Premium economy seats left: {flight.premium_economy_seats} seats")
            print(f"Economy seats left: {flight.economy_seats} seats")
            print(f"Booked seats: {flight.reserved_seats} seats")
        else:
            print("Flight not found.")

    def view_passenger_details(self, passport_id):
        passenger = self.passengers.get(passport_id)
        if passenger:
            print(f"Name: {passenger.name}")
            print(f"Age: {passenger.age}")
            print(f"Passport ID: {passenger.passport_id}")
            print(f"Flight: {passenger.flight}")
            print(f"Seat class: {passenger.seat}")
        else:
            print("Passenger not found.")

    def search_flights(self, flight_number = None, destination = None, departure = None):
        results = []
        for flight in self.flights.values():
            if (flight_number and flight.flight_number in flight_number) or (destination and flight.destination in destination) or (departure and flight.departure in departure):
                results.append(flight)
        if results:
            for flight in results:
                print(f"Flight number: {flight.flight_number}")
                print(f"Departure: {flight.departure}")
                print(f"Arrival: {flight.destination}")
                print(f"Departure time: {flight.departure_time}h")
                print(f"Business seats left: {flight.business_seats} seats")
                print(f"Premium economy seats left: {flight.premium_economy_seats} seats")
                print(f"Economy seats left: {flight.economy_seats} seats")
                print(f"Booked seats: {flight.reserved_seats} seats")
        else:
            print("No flights found")

    def cancel_flight(self, id):
        try:
            del self.flights[id]         # airline staff can delete flights. The flight will be delete out of flights dictionary
        except:
            print("Flight not found")
        else:
            print(f"Flight {id} cancelled successfully")
    
    def book(self, thing):
        self.passengers[thing.passport_id] = thing

system = AirlineSystem()

while True:
    print("\nTeam 13 Reservation System")
    print("1. Add Flight")
    print("2. Register Passenger")
    print("3. View Flight Details")
    print("4. View Passenger Details")
    print("5. Make Reservation")
    print("6. Cancel Reservation")
    print("7. Search Flights")
    print("8. Cancel Flight")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("Logging in airline management system...")
        flight_number = input("Enter flight number: ").upper()
        departure = input("Enter departure location: ").capitalize()
        destination = input("Enter destination: ").capitalize()
        departure_time = input("Enter departure time: ")
        aircraft_type = input("Enter aircraft type (A320/A350/B787): ").upper()
        
        try:
            departure_time = int(departure_time)
        except:
            print("Time format error")
            departure_time = 25

        
        if aircraft_type != "A320" and aircraft_type != "A350" and aircraft_type != "B787":    # error handle: wrong aircraft choice
            print("Aircraft type error")
        
        elif departure_time < 0 or departure_time > 24:
            print("Please enter time from 0 to 24")
        
        else:
            system.add_flight(flight_number, departure, destination, departure_time, aircraft_type)

    elif choice == '2':
        name = input("Enter passenger name: ")
        age = int(input("Enter passenger age: "))
        passport_id = input("Enter passport ID: ")
        system.register_passenger(name, age, passport_id)

    elif choice == '3':
        print("Logging in airline management system...")
        flight_number = input("Enter flight number: ").upper()
        system.view_flight_details(flight_number)

    elif choice == '4':
        print("Logging in airline management system...")
        passport_id = input("Enter passenger passport ID: ")
        system.view_passenger_details(passport_id)

    elif choice == '5':
        passport_id = input("Enter passenger passport ID: ")
        flight_number = input("Enter flight number: ").upper()
        seat_class = input("Enter seat class (Business/Premium Economy/Economy): ").capitalize()
        passenger = system.passengers.get(passport_id)
        flight = system.flights.get(flight_number)
        if passenger and flight:
            reservation = Reservation(passenger.name, passenger.age, passenger.passport_id, flight, seat_class)
            system.book(reservation)
            reservation.confirm_reservation()
        else:
            print("Passenger or flight not found.")

    elif choice == '6':
        passport_id = input("Enter passenger passport ID: ")
        flight_number = input("Enter flight number: ").upper()
        seat_class = input("Enter seat class (Business/Premium Economy/Economy): ")
        passenger = system.passengers.get(passport_id)
        flight = system.flights.get(flight_number)
        if passenger and flight:
            reservation = Reservation(passenger.name, passenger.age, passenger.passport_id, flight, seat_class)
            reservation.cancel_reservation()
        else:
            print("Passenger or flight not found.")

    elif choice == '7':
        print("Search Flights by:")
        print("1. Flight Number")
        print("2. Destination")
        print("3. Departure")
        search_choice = input("Enter your choice: ")
        if search_choice == '1':
            flight_number = input("Enter flight number: ").upper()
            system.search_flights(flight_number = flight_number)
        elif search_choice == '2':
            destination = input("Enter destination: ").capitalize()
            system.search_flights(destination = destination)
        elif search_choice == '3':
            departure = input("Enter departure location: ").capitalize()
            system.search_flights(departure = departure)
        else:
            print("Invalid choice.")

    elif choice == '8':
        print('Logging in airline management system...')
        id = input("Enter flight number: ").upper()
        system.cancel_flight(id)

    elif choice == '9':
        print("Exiting the system. Goodbye!")
        sys.exit()

    else:
        print("Invalid choice. Please try again.")
