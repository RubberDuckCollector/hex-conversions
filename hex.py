import csv
import math
import time
import pandas
import datetime
from random import randint

# TODO: add unlimited mode
# TODO: add username inside quiz()

def write_to_csv(csv_file_name, field_names_list):
    # field_names_list must be in the order of [play_num, correct, maximum, elapsed_time, date_and_time_played]

    # record game data with csv
        with open(csv_file_name, "r") as f: # if there are no previous records:
            lines = f.readline()
            if len(lines) == 0:
                with open(csv_file_name, "w") as f: # write first game data
                    fieldnames = ["play num", "score/10", "difficulty (max range)", "time (sec)", "date and time played"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)

                    writer.writeheader() # put the field names in the file
                    writer.writerow({"play num": field_names_list[0], "score/10": field_names_list[1], "difficulty (max range)": field_names_list[2], "time (sec)": field_names_list[3], "date and time played": field_names_list[4]})
            else:
                # all subsequent game data written with this code
                # field names are already in the file so game data is appended
                with open(csv_file_name, "a") as f:
                    fieldnames = ["play num", "score/10", "difficulty (max range)", "time (sec)", "date and time played"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerow({"play num": field_names_list[0], "score/10": field_names_list[1], "difficulty (max range)": field_names_list[2], "time (sec)": field_names_list[3], "date and time played": field_names_list[4]})

def quiz(mode, maximum):
    num_of_questions = 10
    correct = 0
    if mode == 1: # game is hex to decimal
        start = time.time()
        print("Time start")
        for i in range(0, num_of_questions):
            try:
                num = randint(0, maximum)
                user_answer = int(input(f"What is {hex(num)} in decimal? "))
                if user_answer == num:
                    print("Correct")
                    correct += 1
                else:
                    print(f"Incorrect\nCorrect answer is {num}")
            except ValueError:
                print(f"You didn't enter a decimal number, incorrect\nCorrect answer is {num}")
        end = time.time()
        elapsed_time = end - start
        elapsed_time = math.floor(elapsed_time * 1000) / 1000
        print(f"You got {correct}/{num_of_questions} correct.")
        print(f"You took: {elapsed_time} seconds. Your game data is being recorded.")

        # get time then date played
        time_played = time.localtime()
        time_played = time.strftime("%H:%M:%S", time_played)
        today = datetime.date.today()

        date_played = today.strftime("%B %d, %Y")
        date_and_time_played = date_played + " at " + time_played

        # find game num
        # this should be the number of the game just played
        with open("hex_to_decimal_play_num.txt", "r") as f:
            game_num = f.readline()
            if len(game_num) == 0: # if this is the first game
                with open("hex_to_decimal_play_num.txt", "w") as f:
                    f.write("2") # write 2, because next game should be #2
                    play_num = 1 # if the file has no number, the game just played should be #1
            else:
                play_num = int(game_num)

                # the next game num is written to the file because next game,
                # the code will read it straight away.
                # e.g: user plays game 2, code reads 2, then code increments to game 3.
                # game 3 is ready for next time
                next_play = play_num + 1
                with open("hex_to_decimal_play_num.txt", "w") as f:
                    f.write(str(next_play))

        write_to_csv("hex_to_decimal_scores.csv", [play_num, correct, maximum, elapsed_time, date_and_time_played])

    elif mode == 2: # game is decimal to hex (answer in hex)
        start = time.time()
        print("Time start")
        for i in range(0, num_of_questions):
            num = randint(0, maximum)
            user_answer = input(f"What is {str(num)} in hex? 0x").lower()
            user_answer = "0x" + user_answer
            # this boolean evaluation will work because hex() returns a str
            # therefore here i am comparing 2 strings
            if user_answer == hex(num):
                print("Correct")
                correct += 1
            else:
                print(f"Incorrect\nCorrect answer is {hex(num)}")
        end = time.time()
        elapsed_time = end - start
        elapsed_time = math.floor(elapsed_time * 1000) / 1000
        print(f"You got {correct}/{num_of_questions} correct.")
        print(f"You took: {elapsed_time} seconds. Your game data is being recorded.")

        # get time then date played
        time_played = time.localtime()
        time_played = time.strftime("%H:%M:%S", time_played)
        today = datetime.date.today()

        date_played = today.strftime("%B %d, %Y")
        date_and_time_played = date_played + " at " + time_played

        # find game num
        # this should be the number of the game just played
        with open("decimal_to_hex_play_num.txt", "r") as f:
            game_num = f.readline()
            if len(game_num) == 0: # if this is the first game
                with open("decimal_to_hex_play_num.txt", "w") as f:
                    f.write("2") # write 2, because next game should be #2
                    play_num = 1 # if the file has no number, the game just played should be #1
            else:
                play_num = int(game_num)

                # the next game num is written to the file because next game,
                # the code will read it straight away.
                # e.g: user plays game 2, code reads 2, then code increments to game 3.
                # game 3 is ready for next time
                next_play = play_num + 1
                with open("decimal_to_hex_play_num.txt", "w") as f:
                    f.write(str(next_play))

        write_to_csv("decimal_to_hex_scores.csv", [play_num, correct, maximum, elapsed_time, date_and_time_played])

def main():

    data = []

    while True:
        choice_1 = int(input("Choose mode (Enter the number inside the square [] brackets):\nHex to decimal [1]\nDecimal to hex [2]\nSee scores [3]\nHelp [4]\n> "))
        if choice_1 == 1:
            data.append(1)
            break
        elif choice_1 == 2:
            data.append(2)
            break
        elif choice_1 == 3:
            while True:
                try:
                    scores = int(input("See scores of:\nHex to decimal [1]\nDecimal to hex [2]\n> "))
                    if scores == 1:
                        dataframe = pandas.read_csv('hex_to_decimal_scores.csv')
                        print(dataframe)
                        return
                    elif scores == 2:
                        dataframe = pandas.read_csv('decimal_to_hex_scores.csv')
                        print(dataframe)
                        return
                    else:
                        print(f"{scores} is not a valid number.")
                except pandas.errors.EmptyDataError: # this will be thrown if the csv file is empty
                    print("You don't have any game data yet. Practise some number conversions!")
                    return
            break
        elif choice_1 == 4:
            print("Welcome to help. This will outline your experience with the game.\nTo start with, you'll choose whether you convert hexadecimal numbers (base-16) to decimal numbers (base-10) [in these square brackets].\n")
            print("Then, you select your difficulty. Since you are asked to convert random numbers on the spot, each difficulty has a certian pool of numbers to choose from.")
            print("There are 5 difficulties. 1 is easiest, 5 is hardest. Difficulty 1 can only ask you to convert numbers between 0 and 16 inclusive.")
            print("Don't worry about the '0x' prefix. It's what computers use to signify a number in base-16. The game handles this for you so you don't have to enter it")
            print("Each subsequent difficulty doubles the possible numbers. (2: 32, 3: 64....)")
            print("Some data about your game is tracked:\n\tThe nth time you have played\n\tYour score out of 10\n\tThe game's difficulty\n\tHow long you took\n\tThe date and time of your game.")
            print("When you finish a game, this data is stored in csv and text files.")
            print("You can see this data on the first screen.\n")
        else:
            print(f"{choice_1} is not a valid number.")

    while True:
        choice_2 = int(input("Choose dificulty:\nEasy (0-16) [1]\nMedium (0-32) [2]\nHard (0-64) [3]\nVery hard (0-128) [4]\nVery very hard (0-256) [5]\n> "))
        if choice_2 == 1:
            data.append(16)
            break
        elif choice_2 == 2:
            data.append(32)
            break
        elif choice_2 == 3:
            data.append(64)
            break
        elif choice_2 == 4:
            data.append(128)
            break
        elif choice_2 == 5:
            data.append(256)
            break
        else:
            print(f"{choice_2} is not a valid number.")

    quiz(data[0], data[1])


if __name__ == '__main__':
    main()