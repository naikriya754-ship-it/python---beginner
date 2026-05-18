#Write a function that counts how many times a word appears in a sentence.
def count_word(sentence,word):
    words = sentence.split()
    return words.count(word)

sentence = "hello world hello everyone hello"
word = "hello"

print(count_word(sentence,word))