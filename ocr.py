# USAGE
# python ocr.py --image images/example_01.png 
# python ocr.py --image images/example_02.png  --preprocess blur

# import the necessary packages
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import argparse
import cv2
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import csv
import datetime
import pprint

pp = pprint.PrettyPrinter(indent = 4)

btm_area = (196, 1385, 1080, 2230)
xp_area = (50, 590, 360, 663)
user_area = (385, 377, 1080, 450)

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

users = {}


onlyfiles = [f for f in listdir("images/") if isfile(join("images/", f)) and (".jpg" in f or ".png" in f)]
for img in onlyfiles:
    if ".jpg" in img:
        pre, ext = os.path.splitext("images/"+img)
        os.rename("images/"+img, pre+".png")
successCount = 0
totalCount = 0

num_screenshots = 0

onlyfiles = [f for f in listdir("images/") if isfile(join("images/", f)) and (".jpg" in f or ".png" in f)]
for img in onlyfiles:
    ocr_read_error = 0
    num_screenshots += 1
    print("working on "+img)
    
    print("images/"+img)

    # image = cv2.imread("images/"+img)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # gray = cv2.threshold(gray, 0, 255,
    #   cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    gray = Image.open("images/"+img)
    gray = gray.filter(ImageFilter.MedianFilter())

    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2)
    gray = gray.convert('1')
    
    bottom_stats = gray.crop(btm_area)
    bottom_stats.save("images/btm_"+img)

    bottom_stats = cv2.imread("images/btm_"+img)
    bottom_stats = cv2.medianBlur(bottom_stats, 3)
    cv2.imwrite("images/btm_"+img, bottom_stats)




    xp_stats = gray.crop(xp_area)
    xp_stats.save("images/xp_"+img)

    xp_stats = cv2.imread("images/xp_"+img)
    xp_stats = cv2.medianBlur(xp_stats, 5)
    cv2.imwrite("images/xp_"+img, xp_stats)




    user_stats = gray.crop(user_area)
    user_stats.save("images/user_"+img)

    user_stats = cv2.imread("images/user_"+img)
    user_stats = cv2.medianBlur(user_stats, 3)
    cv2.imwrite("images/user_"+img, user_stats)

    btm_text = pytesseract.image_to_string(Image.open("images/btm_"+img))
    xp_text = pytesseract.image_to_string(Image.open("images/xp_"+img))
    user_text = pytesseract.image_to_string(Image.open("images/user_"+img))

    if " Total power heroes" in btm_text:
        successCount = successCount + 1
    totalCount = totalCount + 1
    numbers = []
    print(btm_text)
    for line in btm_text.splitlines():
        new_num = line.replace(" ", "")
        if isInt(new_num):
            numbers.append(new_num)
        else:
            print("Error: One of the bottom read numbers was not an Integer.")
            numbers.append("n/a")
            # ocr_read_error = 1
            # break

        if len(numbers) == 10:
            break
    os.remove("images/user_"+img)
    os.remove("images/xp_"+img)
    os.remove("images/btm_"+img)
    # print(numbers)
    if ocr_read_error == 1:
        print("Error: ",img, " wasn't able to be processed correctly.")
    else:
        print(user_text)
        print(xp_text)
        print(numbers)
        print(str(len(numbers)))
        print("//////////////")

        stats = {"walkers_killed":numbers[0],
                    "humans_killed":numbers[1],
                    "missions_played":numbers[2],
                    "missions_completed":numbers[3],
                    "shots_fired":numbers[4],
                    "stash_collected":numbers[5],
                    "total_power_heroes":numbers[6],
                    "total_power_weapons":numbers[7],
                    "cards_collected":numbers[8],
                    "survivors_rescued":numbers[9]}
        # for key, value in stats.items():

        user_text = user_text.replace(" ", "")
        print(user_text, " is now being added to users")
        if user_text == "RoaI-P" or user_text == "Real-P" or user_text == "ReaI-P":
            users["Real-P"] = stats
        elif user_text == "Phoenix":
            users["Phoenix"] = stats
        elif user_text == "Knatata":
            users["Knatata"] = stats
        elif user_text == "Paladyne" or user_text == "Paladyno":
            users["Paladyne"] = stats
        elif user_text == "patolala" or user_text == "Patolala":
            users["patolala"] = stats
        elif user_text == "Chrlsklng" or user_text == "ChrisKing":
            users["ChrisKing"] = stats
        elif user_text == "rgdark2609" or user_text == "Rgdark2609":
            users["rgdark2609"] = stats
        elif user_text == "Mcleon":
            users["Mcleon"] = stats
        elif user_text == "Vorbeuler" or user_text == "Verbeuler":
            users["Verbeuler"] = stats
        elif user_text == "Player8b2":
            users["Player 8b2"] = stats
        elif user_text == "Mango" or user_text == "Mongo":
            users["Mongo"] = stats
        elif user_text == "D-Bone":
            users["D-Bone"] = stats
        elif user_text == "Syronlr" or user_text == "Syronir":
            users["Syronir"] = stats
        elif user_text == "Playerc4d" or user_text == "Player04d":
            users["Player c4d"] = stats
        elif user_text == "Wlndukolt" or user_text == "Windukeit":
            users["Windukeit"] = stats
        elif user_text == "atkh21":
            users["atkh21"] = stats
        elif user_text == "Noslca" or user_text == "Nosica":
            users["Nosica"] = stats
        elif user_text == "SCOOP":
            users["SCOOP"] = stats
        elif user_text == "Tomasz -" or user_text == "Tomasz" or "Tomasz" in user_text:
            users["Tomasz"] = stats
        elif user_text == "JenFee" or user_text == "JenFeo" or "JenFee" in user_text or user_text == "JonFoe" or user_text == "JenFoe":
            users["JenFee"] = stats
        elif user_text.lower() == "suave" or user_text.lower == "suaue" or user_text.lower == "SUBVO":
            users["Suave"] = stats
        elif user_text == "ThlerlmManne" or user_text == "ThlorlmManne":
            users["ThierImManne"] = stats
        elif user_text == "ThlerlmManne" or user_text == "suaue":
            users["ThierImManne"] = stats
        elif user_text == "Unknownhasl" or user_text == "Unknownhasi":
            users["Unknownhasi"] = stats
        else:
            users[user_text] = stats
            print("Added a new user: ", user_text)
    
# print("////////")
# pp.pprint("users")

walkers_killed_table = []
humans_killed_table = []
missions_played_table = []
missions_completed_table = []
shots_fired_table = []
stash_collected_table = []
total_power_heroes_table = []
total_power_weapons_table = []
cards_collected_table = []
survivors_rescued_table = []

stat_tables = {"walkers_killed_table":walkers_killed_table,
                "humans_killed_table":humans_killed_table,
                "missions_played_table":missions_played_table,
                "missions_completed_table":missions_completed_table,
                "shots_fired_table":shots_fired_table,
                "stash_collected_table":stash_collected_table,
                "total_power_heroes_table":total_power_heroes_table,
                "total_power_weapons_table":total_power_weapons_table,
                "cards_collected_table":cards_collected_table,
                "survivors_rescued_table":survivors_rescued_table}
# stat_tables = [walkers_killed_table,
#                 humans_killed_table,
#                 missions_played_table,
#                 missions_completed_table,
#                 shots_fired_table,
#                 stash_collected_table,
#                 total_power_heroes_table,
#                 total_power_weapons_table,
#                 cards_collected_table,
#                 survivors_rescued_table]

num_cols = 0
with open("StatTables/WalkersKilled.csv", mode="r") as walkers_killed:
    csv_reader = csv.reader(walkers_killed, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            # This accounts for the header line
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            # Non-Header line
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["walkers_killed"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            walkers_killed_table.append(row)
            line_count += 1


with open("StatTables/HumansKilled.csv", mode="r") as humans_killed:
    csv_reader = csv.reader(humans_killed, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["humans_killed"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            print("//////////")
            # pp.pprint(users)
            # pp.pprint(row)
            humans_killed_table.append(row)
            line_count += 1


with open("StatTables/MissionsPlayed.csv", mode="r") as missions_played:
    csv_reader = csv.reader(missions_played, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["missions_played"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            missions_played_table.append(row)
            line_count += 1


with open("StatTables/MissionsCompleted.csv", mode="r") as missions_completed:
    csv_reader = csv.reader(missions_completed, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["missions_completed"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            missions_completed_table.append(row)
            line_count += 1


with open("StatTables/ShotsFired.csv", mode="r") as shots_fired:
    csv_reader = csv.reader(shots_fired, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["shots_fired"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            shots_fired_table.append(row)
            line_count += 1

with open("StatTables/StashCollected.csv", mode="r") as stash_collected:
    csv_reader = csv.reader(stash_collected, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["stash_collected"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            stash_collected_table.append(row)
            line_count += 1


with open("StatTables/TotalPowerHeroes.csv", mode="r") as total_power_heroes:
    csv_reader = csv.reader(total_power_heroes, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["total_power_heroes"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            total_power_heroes_table.append(row)
            line_count += 1


with open("StatTables/TotalPowerWeapons.csv", mode="r") as total_power_weapons:
    csv_reader = csv.reader(total_power_weapons, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["total_power_weapons"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            total_power_weapons_table.append(row)
            line_count += 1


with open("StatTables/CardsCollected.csv", mode="r") as cards_collected:
    csv_reader = csv.reader(cards_collected, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["cards_collected"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
            # pp.pprint(row)
            cards_collected_table.append(row)
            line_count += 1


with open("StatTables/SurvivorsRescued.csv", mode="r") as survivors_rescued:
    csv_reader = csv.reader(survivors_rescued, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if row != None:
            if line_count == 0:
                row.append(datetime.date.today().strftime("%B %d, %Y"))
                num_cols = len(row)
            else:
                if row[0] in users.keys():
                    row.append(users[row[0]]["survivors_rescued"])
                    # If this clause is not triggered then the user no longer exists in the group
                else:
                    print("User '"+row[0]+"' appears to not be in the group any longer or no screenshot for them was provided. Check OCR.")
                    row.append("n/a")
                # Here we delete the user from the users dict so the leftover ones are the ones that don't exist in the table yet
                if row[0] in list(users.keys()):
                    del users[row[0]]
                    # print("Removed "+row[0]+ " from users")
            # pp.pprint(row)
            survivors_rescued_table.append(row)
            line_count += 1
print("These are the users that weren't even in the table yet and need to be added at the current run.")       
# pp.pprint(users)
# for stat_table in stat_tables:
for new_user in users.keys():
    print("Adding new user ", new_user)
    new_row = [new_user]
    for i in range(1, num_cols-1):
        new_row.append("n/a")
        print("n/a appended")

    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["walkers_killed"])
    stat_tables["walkers_killed_table"].append(new_row_temp)
    
    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["humans_killed"])
    stat_tables["humans_killed_table"].append(new_row_temp)

    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["missions_played"])
    stat_tables["missions_played_table"].append(new_row_temp)
    
    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["missions_completed"])
    print("Adding row to missions_completed_table ")
    print(new_row_temp)
    stat_tables["missions_completed_table"].append(new_row_temp)

    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["shots_fired"])
    stat_tables["shots_fired_table"].append(new_row_temp)
    
    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["stash_collected"])
    stat_tables["stash_collected_table"].append(new_row_temp)

    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["total_power_heroes"])
    stat_tables["total_power_heroes_table"].append(new_row_temp)
    
    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["total_power_weapons"])
    stat_tables["total_power_weapons_table"].append(new_row_temp)

    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["cards_collected"])
    stat_tables["cards_collected_table"].append(new_row_temp)
    
    new_row_temp = new_row.copy()
    new_row_temp.append(users[new_user]["survivors_rescued"])
    stat_tables["survivors_rescued_table"].append(new_row_temp)
    


# for key, stat_table in stat_tables.items():
#     # pp.pprint(stat_table)
#     stat_table.pop()

with open("StatTables/WalkersKilled.csv", mode="w") as walkers_killed:
    csv_writer = csv.writer(walkers_killed, delimiter=';')
    line_count = 0
    for row in walkers_killed_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/HumansKilled.csv", mode="w") as humans_killed:
    csv_writer = csv.writer(humans_killed, delimiter=';')
    line_count = 0
    for row in humans_killed_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/MissionsPlayed.csv", mode="w") as missions_played:
    csv_writer = csv.writer(missions_played, delimiter=';')
    line_count = 0
    for row in missions_played_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/MissionsCompleted.csv", mode="w") as missions_completed:
    csv_writer = csv.writer(missions_completed, delimiter=';')
    line_count = 0
    for row in missions_completed_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/ShotsFired.csv", mode="w") as shots_fired:
    csv_writer = csv.writer(shots_fired, delimiter=';')
    line_count = 0
    for row in shots_fired_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/StashCollected.csv", mode="w") as stash_collected:
    csv_writer = csv.writer(stash_collected, delimiter=';')
    line_count = 0
    for row in stash_collected_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/TotalPowerHeroes.csv", mode="w") as total_power_heroes:
    csv_writer = csv.writer(total_power_heroes, delimiter=';')
    line_count = 0
    for row in total_power_heroes_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/TotalPowerWeapons.csv", mode="w") as total_power_weapons:
    csv_writer = csv.writer(total_power_weapons, delimiter=';')
    line_count = 0
    for row in total_power_weapons_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/CardsCollected.csv", mode="w") as cards_collected:
    csv_writer = csv.writer(cards_collected, delimiter=';')
    line_count = 0
    for row in cards_collected_table:
        if row != None:
            csv_writer.writerow(row)

with open("StatTables/SurvivorsRescued.csv", mode="w") as survivors_rescued:
    csv_writer = csv.writer(survivors_rescued, delimiter=';')
    line_count = 0
    for row in survivors_rescued_table:
        if row != None:
            csv_writer.writerow(row)

print("NUM SCREENSHOTS: ",num_screenshots)