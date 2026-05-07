#Take a number of days as input and convert it into years, months, and days approximately
number_days = int(input("enter a number of days:"))
years = number_days // 365
remaining_days = number_days % 365
months = remaining_days // 30
days = remaining_days % 30
print(f"{years} years {months} months {days} days")
