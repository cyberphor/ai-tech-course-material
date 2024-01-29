# TODO 1: Define the `pretty_print_int` function
def pretty_print_int(number: int) -> str:
    return f"{number:,}"

print(pretty_print_int(1000))
print(pretty_print_int(5))
print(pretty_print_int(547475874))
print(pretty_print_int(-84989))
print(pretty_print_int(999))

# TODO 2: Define the `pretty_print_dollars` function
def pretty_print_dollars(number: int|float) -> str:
    if number >= 0:
        return f"${number:,.2f}"
    else:
        return f"-${abs(number):,.2f}"

print(pretty_print_dollars(1000.0))
print(pretty_print_dollars(5.99))
print(pretty_print_dollars(547475874))
print(pretty_print_dollars(-84989))
print(pretty_print_dollars(999.50))

# TODO 3: Define the `make_field` function
def make_field(content: str|int|float, length: int) -> str:
    pad = length - 2
    field = '| ' + str(content)[:pad].rjust(pad) + ' |'
    return field

print(make_field(1000, 7))
print(make_field("year", 8))
print(make_field("world", 5))

# TODO 4: Define the `make_line` function
def make_line(length: int):
    return "+" + ("-" * length) + "+"

# TODO 5: Define the `simulate_infection` function
from math import ceil
def simulate_infection(population: int, initial_infected: int, r_number: float):
    day = 1
    infected = initial_infected
    deceased = 0
    while population > 0:
        print(day, population)
        deceased = infected
        population = population - deceased
        infected = ceil(infected * r_number)
        day = day + 1
    print(day, 0)

simulate_infection(1000000, 1000, 1.1)

# ------------------------------------------- #
# day | population | deceased | infected      |
# ------------------------------------------- #
# 1   | 1000000    | 0        | 1000          | 1000000 - 1000
# 2   |  999000    | 1000     | 1100          |  999000 - 1100
# 3   |  997900    | 2100     | 1210          |  997900 - 1210
# 4   |  996690    | 3310     | 1331          |  996690 - 1331
# 5   |  995359    | 4641     | 1464.1 (1465) |

# TODO 6: Define the `compound_interest` function
from math import e
def compound_interest(init_principal: float, acc_rate: float, acc_cmp_freq: int, years: int):
    if acc_cmp_freq == 0:
        return init_principal * e ** (acc_rate * years)
    else:
        return init_principal * (1 + acc_rate / acc_cmp_freq) ** (acc_cmp_freq * years)

print(compound_interest(10000.00, 0.025, 12, 4))
print(compound_interest(10000.00, 0.025, 0, 4))

from math import e
def compound_interest(init_principal: float, acc_rate: float, acc_cmp_freq: int, years: int):
    if acc_cmp_freq == 0:
        return init_principal * e ** (acc_rate * years)
    else:
        return init_principal * (1 + acc_rate / acc_cmp_freq) ** (acc_cmp_freq * years)

# TODO 7: Define the `simulate_account_balance` function
def simulate_account_balance(init_principal: float, acc_rate: float, acc_cmp_freq: int, setup_fee: float, years: int):
    init_principal -= setup_fee
    for year in range(2, (years + 2), 2):
        balance = compound_interest(init_principal, acc_rate, acc_cmp_freq, year)
        print(year, round(balance, 2))

simulate_account_balance(10000.00, 0.025, 12, 25.00, 10)

# 2 10485.88
# 4 11022.93
# 6 11587.49
# 8 12180.96
# 10 12804.82

from math import ceil

def make_line(length: int):
    return "+" + ("-" * length) + "+"

def make_field(content: str|int|float, length: int) -> str:
    pad = length - 2
    field = '| ' + str(content)[:pad].rjust(pad) + ' |'
    return field

def pretty_print_int(number: int) -> str:
    return f"{number:,}"

# TODO 8: Define the `simulate_infection_pp` function
def simulate_infection_pp(population: int, initial_infected: int, r_number: float):
    day = 1
    infected = initial_infected
    deceased = 0
    print(make_line(5) + make_line(12))
    print(make_field("Day", 5) + make_field("Population", 12))
    print(make_line(5) + make_line(12))
    while population > 0:
        print(make_field(day, 5) + make_field(pretty_print_int(population), 12))
        deceased = infected
        population = population - deceased
        infected = ceil(infected * r_number)
        day = day + 1
    print(make_field(day, 5) + make_field(0, 12))
    print(make_line(5) + make_line(12))

simulate_infection_pp(1000000, 1000, 1.1)

from math import e

def make_line(length: int):
    return "+" + ("-" * length) + "+"

def make_field(content: str|int|float, length: int) -> str:
    pad = length - 2
    field = '| ' + str(content)[:pad].rjust(pad) + ' |'
    return field

def pretty_print_dollars(number: int|float) -> str:
    if number >= 0:
        return f"${number:,.2f}"
    else:
        return f"-${abs(number):,.2f}"

def compound_interest(init_principal: float, acc_rate: float, acc_cmp_freq: int, years: int):
    if acc_cmp_freq == 0:
        return init_principal * e ** (acc_rate * years)
    else:
        return init_principal * (1 + acc_rate / acc_cmp_freq) ** (acc_cmp_freq * years)

def print_two_col_report(col1_name: str, col1_cell_size: str, col2_name: str, col2_cell_size: str, data: list):
    # print row headers
    print(
        (make_line(col1_cell_size) + make_line(col2_cell_size)),
        (make_field(col1_name, col1_cell_size) + make_field(col2_name, col2_cell_size)),
        (make_line(col1_cell_size) + make_line(col2_cell_size)),
        sep = "\n"
    )
    # print rows
    for line in data:
        cell1 = list(line.keys())[0]
        cell2 = list(line.values())[0]
        print(make_field(cell1, col1_cell_size) + make_field(cell2, col2_cell_size))
    # print row footer
    print(make_line(col1_cell_size) + make_line(col2_cell_size))

# TODO 9: Place your code for `simulate_account_balance_pp` here
def simulate_account_balance_pp(init_principal: float, acc_rate: float, acc_cmp_freq: int, setup_fee: float, years: int):
    init_principal -= setup_fee
    report = []
    for year in range(2, (years + 1), 2):
        balance = round(compound_interest(init_principal, acc_rate, acc_cmp_freq, year), 2)
        pretty_balance = pretty_print_dollars(balance)
        report.append({year: pretty_balance})
    col1_cell_size = 6
    col2_cell_size = len(str(list(report[-1].values())[0])) + 2 # for spaces
    print_two_col_report(
        col1_name = "Year",
        col1_cell_size = col1_cell_size,
        col2_name = "Balance",
        col2_cell_size = col2_cell_size,
        data = report
    )

simulate_account_balance_pp(10000.00, 0.025, 12, 25.00, 10)
simulate_account_balance_pp(100000.00, 0.022, 0, 10.0, 15)