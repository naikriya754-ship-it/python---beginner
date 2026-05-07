#Reverse a string without using built-in functions
def reverse_string(item):
    reverse_item = ""
    for char in item:
        reverse_item = char + reverse_item
    return reverse_item
print(reverse_string("riya"))

