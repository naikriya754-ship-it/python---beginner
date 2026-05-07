#Take time in minutes as input and convert it into hours and remaining minutes.
min = int(input("enter a number:"))
hours = min//60
remaining_min = min%60
print(f"{hours}  hours and {remaining_min} minute")