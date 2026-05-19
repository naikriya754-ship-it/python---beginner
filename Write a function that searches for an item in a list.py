#Write a function that searches for an item in a list.
def search_item(items,target):
    return target in items

fruits = ["banana","grapes","watermelon"]

print(search_item(fruits,"banana"))
print(search_item(fruits,"kiwi"))