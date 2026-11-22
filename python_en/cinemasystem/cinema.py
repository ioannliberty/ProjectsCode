class Hall:
    # cinema hall class
    def __init__(self, code: int, name: str, rows: int, columns: int, price: float, description: str):
        self._code = code
        self._name = name
        self._rows = rows
        self._columns = columns
        self._price = price
        self._description = description

    # getters for safe field access
    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def price(self):
        return self._price

    def get_info(self):
        return (self._code, self._name, (self._rows, self._columns), self._price, self._description)


class Film:
    # film class
    def __init__(self, code: int, name: str, description: str):
        self._code = code
        self._name = name
        self._description = description

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    def get_info(self):
        return (self._code, self._name, self._description)


class Schedule:
    # screening schedule class
    def __init__(self, code: int, film_code: int, hall_code: int, date_time: str):
        self._code = code
        self._film_code = film_code
        self._hall_code = hall_code
        self._date_time = date_time

    @property
    def code(self):
        return self._code

    @property
    def film_code(self):
        return self._film_code

    @property
    def hall_code(self):
        return self._hall_code

    @property
    def date_time(self):
        return self._date_time

    def get_info(self):
        return (self._code, self._film_code, self._hall_code, self._date_time)


class Tiket:
    # ticket class
    def __init__(self, schedule_code: int, seats: list, cost: float):
        self._schedule_code = schedule_code
        self._seats = seats
        self._cost = cost

    @property
    def schedule_code(self):
        return self._schedule_code

    @property
    def seats(self):
        return self._seats

    @property
    def cost(self):
        return self._cost

    def get_info(self):
        return (self._schedule_code, self._seats, self._cost)


class Cinema:
    # main cinema class
    def __init__(self):
        self._halls = {}
        self._films = {}
        self._film_schedule = {}
        self._tikets = []

    def add_hall(self, hall: Hall):
        self._halls[hall.code] = hall

    def add_film(self, film: Film):
        self._films[film.code] = film

    def add_schedule(self, schedule: Schedule):
        self._film_schedule[schedule.code] = schedule

    def get_free_tikets_by_schedule(self, code: int):
        # check that the screening exists
        if code not in self._film_schedule:
            return []

        schedule = self._film_schedule[code]
        hall = self._halls[schedule.hall_code]

        # build the list of all seats in the hall
        all_sets = []
        for r in range(hall.rows):
            for c in range(hall.columns):
                all_sets.append((r, c))

        # find all tickets already bought for this screening
        schedule_tikets = filter(lambda t: t.schedule_code == code, self._tikets)

        # remove taken seats from the free list
        for tiket in schedule_tikets:
            for s in tiket.seats:
                if s in all_sets:
                    all_sets.remove(s)

        return all_sets

    def register_tiket(self, schedule_code: int, seats: list):
        schedule = self._film_schedule[schedule_code]
        hall = self._halls[schedule.hall_code]

        # calculate the cost and create the ticket
        cost = len(seats) * hall.price
        tiket = Tiket(schedule_code, seats, cost)
        self._tikets.append(tiket)
        return tiket

    # show all available films
    def show_all_films(self):
        print("\n=== AVAILABLE FILMS ===")
        if not self._films:
            print("No films yet.")
            return
        for film in self._films.values():
            code, name, desc = film.get_info()
            print(f"Code: {code} | Title: \"{name}\" — {desc}")

    # show all screenings by film code
    def show_schedules_by_film(self, film_code: int):
        if film_code not in self._films:
            print(f"\nError: film with code {film_code} not found.")
            return

        film = self._films[film_code]
        print(f"\n=== SCREENINGS FOR \"{film.name}\" ===")
        found = False
        for schedule in self._film_schedule.values():
            if schedule.film_code == film_code:
                hall = self._halls[schedule.hall_code]
                free_count = len(self.get_free_tikets_by_schedule(schedule.code))
                print(
                    f"Screening code: {schedule.code} | Time: {schedule.date_time} | "
                    f"Hall: {hall.name} | Price: {hall.price} UAH | Free seats: {free_count}"
                )
                found = True

        if not found:
            print("No screenings for this film yet.")

    # show all bought tickets
    def show_all_tikets(self):
        print("\n=== ALL BOUGHT TICKETS ===")
        if not self._tikets:
            print("No tickets bought yet.")
            return

        for idx, tiket in enumerate(self._tikets, start=1):
            schedule = self._film_schedule[tiket.schedule_code]
            film = self._films[schedule.film_code]
            hall = self._halls[schedule.hall_code]
            print(
                f"Ticket #{idx} | Screening #{tiket.schedule_code} (\"{film.name}\", {schedule.date_time}, "
                f"Hall: {hall.name}) | Seats: {tiket.seats} | Total: {tiket.cost} UAH"
            )

    # show bought tickets by screening code
    def show_tikets_by_schedule(self, schedule_code: int):
        if schedule_code not in self._film_schedule:
            print(f"\nError: screening with code {schedule_code} not found.")
            return

        schedule = self._film_schedule[schedule_code]
        film = self._films[schedule.film_code]
        print(f"\n=== BOUGHT TICKETS FOR SCREENING #{schedule_code} (\"{film.name}\", {schedule.date_time}) ===")

        schedule_tikets = [t for t in self._tikets if t.schedule_code == schedule_code]
        if not schedule_tikets:
            print("No tickets bought for this screening yet.")
            return

        for idx, tiket in enumerate(schedule_tikets, start=1):
            print(f"Ticket #{idx} | Seats: {tiket.seats} | Total: {tiket.cost} UAH")


# fill the cinema with data
def init_cinema() -> Cinema:
    cinema = Cinema()

    # 5 halls with different sizes and prices
    cinema.add_hall(Hall(1, "Red (IMAX)", 5, 6, 250.0, "Big screen and surround sound"))
    cinema.add_hall(Hall(2, "Blue", 4, 5, 160.0, "Standard comfortable hall"))
    cinema.add_hall(Hall(3, "Green", 4, 4, 140.0, "Cozy hall for family viewing"))
    cinema.add_hall(Hall(4, "VIP hall", 2, 4, 400.0, "Recliner seats and table service"))
    cinema.add_hall(Hall(5, "Small art hall", 3, 4, 120.0, "Hall for arthouse cinema"))

    # 5 films
    cinema.add_film(Film(1, "Dune: Part Two", "Science fiction epic"))
    cinema.add_film(Film(2, "Oppenheimer", "Historical biographical drama"))
    cinema.add_film(Film(3, "Inside Out 2", "Animated comedy for the whole family"))
    cinema.add_film(Film(4, "Interstellar", "Space adventure about time and space"))
    cinema.add_film(Film(5, "Inception", "Sci-fi thriller about dreams"))

    # 10 screenings
    cinema.add_schedule(Schedule(101, 1, 1, "12:00"))
    cinema.add_schedule(Schedule(102, 1, 4, "19:30"))
    cinema.add_schedule(Schedule(103, 2, 2, "14:15"))
    cinema.add_schedule(Schedule(104, 2, 1, "21:00"))
    cinema.add_schedule(Schedule(105, 3, 3, "10:30"))
    cinema.add_schedule(Schedule(106, 3, 2, "16:45"))
    cinema.add_schedule(Schedule(107, 4, 1, "15:20"))
    cinema.add_schedule(Schedule(108, 4, 4, "22:00"))
    cinema.add_schedule(Schedule(109, 5, 5, "13:00"))
    cinema.add_schedule(Schedule(110, 5, 5, "18:10"))

    return cinema


# command line interface
def main():
    cinema = init_cinema()

    while True:
        print("\n" + "=" * 40)
        print("CINEMA MENU")
        print("1. Show all available films")
        print("2. Show screenings by film code")
        print("3. Choose a screening and buy tickets")
        print("4. Show all bought tickets")
        print("5. Show bought tickets by screening code")
        print("0. Exit")
        print("=" * 40)

        choice = input("Choose an action (0-5): ").strip()

        if choice == "1":
            cinema.show_all_films()

        elif choice == "2":
            cinema.show_all_films()
            try:
                film_code = int(input("\nEnter film code: "))
                cinema.show_schedules_by_film(film_code)
            except ValueError:
                print("Error: enter an integer (film code).")

        elif choice == "3":
            # show all screenings to make choosing easier
            print("\n=== ALL AVAILABLE SCREENINGS ===")
            for s in cinema._film_schedule.values():
                film = cinema._films[s.film_code]
                hall = cinema._halls[s.hall_code]
                print(f"Screening code: {s.code} | \"{film.name}\" | Time: {s.date_time} | Hall: {hall.name} ({hall.price} UAH)")

            try:
                schedule_code = int(input("\nEnter screening code to book: "))
                if schedule_code not in cinema._film_schedule:
                    print("No screening with this code.")
                    continue

                free_seats = cinema.get_free_tikets_by_schedule(schedule_code)
                if not free_seats:
                    print("Sorry, all seats for this screening are sold out.")
                    continue

                print(f"\nFree seats (row, seat): {free_seats}")
                count = int(input("How many tickets do you want to buy? "))
                if count <= 0 or count > len(free_seats):
                    print("Invalid number of tickets.")
                    continue

                selected_seats = []
                for i in range(count):
                    while True:
                        raw = input(f"Enter row and seat for ticket #{i + 1} separated by space (example: 0 1): ")
                        parts = raw.split()
                        if len(parts) != 2:
                            print("Enter two numbers separated by space!")
                            continue

                        seat = (int(parts[0]), int(parts[1]))
                        if seat in free_seats and seat not in selected_seats:
                            selected_seats.append(seat)
                            break
                        else:
                            print("This seat is taken, already selected or does not exist. Try another one.")

                tiket = cinema.register_tiket(schedule_code, selected_seats)
                print(f"\nSuccess! Ticket issued. Seats: {tiket.seats}, to pay: {tiket.cost} UAH.")

            except ValueError:
                print("Input error: use integers only.")

        elif choice == "4":
            cinema.show_all_tikets()

        elif choice == "5":
            try:
                schedule_code = int(input("Enter screening code: "))
                cinema.show_tikets_by_schedule(schedule_code)
            except ValueError:
                print("Error: enter an integer (screening code).")

        elif choice == "0":
            print("Thank you for using the cinema system! See you.")
            break

        else:
            print("Unknown command. Choose an option from 0 to 5.")


if __name__ == "__main__":
    main()
