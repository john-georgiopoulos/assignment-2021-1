import csv
import re
import sys
import string
import sre_yield
import pprint

# Create a list consisting of the CSV values
cross_words = []
solution = []
with open(sys.argv[1], 'r') as laughs:
    csv_reader = csv.reader(laughs)
    for row in csv_reader:
        cross_words.append(row)
cross_words.sort(key=lambda x: int(x[0]))

# Make a list with each element containing an individual dot as a letter
for i in range(0, len(cross_words)):
    cross_words[i][1] = list(cross_words[i][1])

for x in cross_words:
    solution.append(x[1])
#print('Solution = ', solution)

# Find the length of the longest word that can be written in the crossword
length_count = 0
for i in range(0, len(cross_words)):
    if length_count < len(cross_words[i][1]):
        length_count = len(cross_words[i][1])

# Open txt file and find all the Regular Expressions and then filter them and store only the ones that can be written
myfile = open(sys.argv[2], 'r+')
lines = myfile.read().splitlines()
regular_expressions = []
content = []
for line in lines:
    temp = list(sre_yield.AllStrings(line, max_count=5, charset=string.ascii_uppercase))
    regex = []
    content.append(line.strip())
    for x in temp:
        if len(x) <= length_count:
           regex.append(x)
    regular_expressions.append(regex)

# print('Starting Reg. Exp. = ', regular_expressions)
# print('Starting Cross = ', cross_words)
# print('Content =', content)


def solve_crossword(cross_words, regular_expressions):
    # Checks the common letters of each word and replaces the blanks with the correct letters
    for x in cross_words:
        if len(x[1]) != x[1].count('.'):
            for i in range(0, len(x)):
                if i != 0 and i % 2 == 0:
                    for j in range(0, len(cross_words[int(x[i])])):
                        if j % 2 == 0 and j != 0 and int(cross_words[int(x[i])][j]) == int(x[0]):
                            if cross_words[int(x[i])][1][int(x[i+1])] != x[1][int(cross_words[int(x[i])][j+1])]:
                                cross_words[int(x[i])][1][int(x[i+1])] = x[1][int(cross_words[int(x[i])][j+1])]
    #print('Updated Cross = ', cross_words)

    # Calculate the ratio of know letter to word length and update the solutions list
    letters_to_dots_ratio = []
    for i in range(0, len(cross_words)):
        letters_to_dots_ratio.append((len(cross_words[i][1]) - cross_words[i][1].count('.'))/len(cross_words[i][1]))

    # Find the biggest letters to dots ratio, which is used to determine the next spot of the crossword that will be filled
    bigger_ratio = 0
    index_of_word_to_be_inserted = 100
    for i in range(0, len(cross_words)):
        if letters_to_dots_ratio[i] > bigger_ratio and letters_to_dots_ratio[i] < 1:
            bigger_ratio = letters_to_dots_ratio[i]
            index_of_word_to_be_inserted = i
        if solution[i] != cross_words[i][1]:
            solution[i] = cross_words[i][1]
    # print('Bigger ratio = ', bigger_ratio)
    # print('index = ', index_of_word_to_be_inserted)

    # Find the correct word to enter in the current spot
    nonBlanks = len(cross_words[index_of_word_to_be_inserted][1]) - cross_words[index_of_word_to_be_inserted][1].count('.')
    #print('nonBlanks = ', nonBlanks)
    matching_words = []
    for k in range(0, len(regular_expressions)):
        for word in regular_expressions[k]:
            letter_check = 0
            match_check = 0
            if len(word) == len(cross_words[index_of_word_to_be_inserted][1]):
                for letter in word:
                    if letter == cross_words[index_of_word_to_be_inserted][1][letter_check]:
                        match_check += 1
                    letter_check += 1
                if match_check == nonBlanks:
                    #print('Matching word = ', word)
                    matching_words.append(word)
            for match in matching_words:
                for i in range(0, len(match)):
                    cross_words[index_of_word_to_be_inserted][1][i] = match[i]
            solution[index_of_word_to_be_inserted] = (cross_words[index_of_word_to_be_inserted][1])
    for i in range(0, len(solution)):
        if solution[i].count('.') == 0:
            for j in range(0, len(regular_expressions)):
                for k in range(0, len(regular_expressions[j])):
                    if solution[i] == list(regular_expressions[j][k]):
                        print(i, ' ', content[j], ' ', solution[i])



    # print('Cross = ', cross_words)
    # print('Updated Reg. Expr. = ', regular_expressions)
    # print('Solution = ', solution)

for i in range(0, 1):
    solve_crossword(cross_words, regular_expressions)
