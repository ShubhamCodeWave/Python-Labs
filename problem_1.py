#S = "apple banana apple orange banana apple"
S = input("enter a string: ")

words = S.split()

word_count = {}

for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

for word in word_count:
    print(f"{word} {word_count[word]}")