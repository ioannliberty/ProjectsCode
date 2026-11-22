# Cinema System

A small console app for managing a cinema: browse films, check screenings, buy tickets and view sales. Everything is kept in memory, so data resets on every run.

## Run

Requires Python 3 and no external dependencies.

```bash
python3 cinema.py
```

## Menu

| # | Action |
|---|--------|
| 1 | Show all available films |
| 2 | Show screenings of a film by film code (with hall, price and free seats) |
| 3 | Choose a screening and buy tickets |
| 4 | Show all bought tickets |
| 5 | Show bought tickets for one screening |
| 0 | Exit |

### Buying tickets

1. Enter a screening code from the list.
2. The app prints free seats as `(row, seat)` pairs. Numbering starts from 0.
3. Enter how many tickets you want.
4. Enter each seat as two numbers separated by a space, for example `0 1`.

The total is `number of seats * hall price`. Taken seats can't be bought twice.

## Structure

All code lives in `cinema.py`:

- `Hall` – hall with code, name, rows, columns, ticket price and description
- `Film` – film with code, name and description
- `Schedule` – screening: links a film to a hall at a given time
- `Tiket` – bought ticket: screening code, seats and total cost
- `Cinema` – holds halls, films, schedule and tickets, and has the show/buy methods
- `init_cinema()` – fills the cinema with demo data
- `main()` – console menu loop

## Demo data

- 5 halls: Red (IMAX), Blue, Green, VIP hall, Small art hall
- 5 films: Dune: Part Two, Oppenheimer, Inside Out 2, Interstellar, Inception
- 10 screenings with codes 101–110

To change the data, edit `init_cinema()`.
