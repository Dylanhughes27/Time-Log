import os
import datetime
import json
import os
import time
import sys
import msvcrt


class TimeLogger:
    def __init__(self):
        t = datetime.datetime.now()
        self.project_path = ''
        self.finished_project_path = ''
        self.prompts = []
        self.finished_prompts = []
        self.year = t.year
        self.month = t.month
        self.day = t.day
        self.military_hour = t.hour
        self.times_for_day = {}
        self.time_keep = {}
        self.new_user_input = ''
        if self.military_hour > 12:
            self.hour = self.military_hour - 12
        else:
            self.hour = self.military_hour
        self.minute = t.minute
        if self.minute < 10:
            self.real_minute = '0' + str(t.minute)
        else:
            self.real_minute = self.minute
        self.date = str(self.month) + '_' + str(self.day) + '_' + str(self.year)
        self.time = str(self.hour) + ":" + str(self.real_minute)
        self.user_input = ''
        self.new_input = ''

        if self.military_hour == 8 and self.minute < 30:
            self.times_for_day = {
                '8:00': '',
                '8:30': '',
                '9:00': '',
                '9:30': '',
                '10:00': '',
                '10:30': '',
                '11:00': '',
                '11:30': '',
                '12:00': '',
                '12:30': '',
                '1:00': '',
                '1:30': '',
                '2:00': '',
                '2:30': '',
                '3:00': '',
                '3:30': '',
                '4:00': '',
                '4:30': '',
                '5:00': ''
            }
            self.save_time(1)
            self.save_time(2)

    def display_prompts(self, n):
        if n == 1:
            print(self.time + "\n")
            print('  (0)..........FINISHED FOLDER\n')
            for i in range(len(self.prompts) - 1):
                print("  (%s)..........%s\n" % (str(i+1), self.prompts[i][:-4]))
        elif n == 2:
            print(self.time + '\n')
            for i in range(len(self.finished_prompts)):
                print("  (%s)..........%s\n" % (str(i+1), self.finished_prompts[i][:-4]))

    def get_user_input(self):
        start_time = time.time()
        sys.stdout.write('What have you been working on? ')
        sys.stdout.flush()
        self.user_input = ''
        while True:
            if msvcrt.kbhit():
                byte_arr = msvcrt.getche()
                if ord(byte_arr) == 13:  # enter_key
                    break
                elif ord(byte_arr) == 8:  # backspace
                    l = len(self.user_input) - 1
                    self.user_input = self.user_input[0:l]
                elif ord(byte_arr) >= 32:  # space_char
                    self.user_input += "".join(map(chr, byte_arr))
            if len(self.user_input) == 0 and (time.time() - start_time) > 60 * 60 * 29:
                print("timing out, using default value.")
                self.user_input = "Away from desk"
                break
        if self.user_input == '0':
            self.display_prompts(2)
            self.get_new_user_input()

    def get_new_user_input(self):
        self.new_user_input = input("\nWhat have you been working on? ")

    def set_project_path(self, path):
        self.project_path = path
        self.prompts = os.listdir(self.project_path)
        self.finished_project_path = self.project_path + '\\FINISHED'
        self.finished_prompts = os.listdir(self.finished_project_path)

    def save_time(self, n):
        if n == 1:
            with open('times_for_day.json', 'w') as f_obj:
                json.dump(self.times_for_day, f_obj, indent=4)
        elif n == 2:
            with open('time_keep.json', 'w') as f_obj:
                json.dump(self.time_keep, f_obj, indent=4)

    def load_time(self, n):
        if n == 1:
            with open('times_for_day.json') as f_obj:
                self.times_for_day = json.load(f_obj)
        elif n == 2:
            with open('time_keep.json') as f_obj:
                self.time_keep = json.load(f_obj)

    def set_time_key(self):
        if len(self.user_input) < 3:
            if self.user_input == '':
                self.times_for_day[self.time] = "None"
                print("\n\nYou have been working on " + self.times_for_day[self.time])
                input()
                if "None" in self.time_keep.keys():
                    self.time_keep["None"] += .5
                else:
                    self.time_keep["None"] = 5
            elif self.user_input == '0':
                self.times_for_day[self.time] = self.finished_prompts[int(self.new_user_input) - 1][:-4]
                print("\n\nYou have been working on " + self.times_for_day[self.time])
                input()
                if self.finished_prompts[int(self.new_user_input) - 1][:-4] in self.time_keep.keys():
                    self.time_keep[self.finished_prompts[int(self.new_user_input) - 1][:-4]] += .5
                else:
                    self.time_keep[self.finished_prompts[int(self.new_user_input) - 1][:-4]] = .5
            else:
                self.times_for_day[self.time] = self.prompts[int(self.user_input) - 1][:-4]
                print("\n\nYou have been working on " + self.times_for_day[self.time])
                input()
                if self.prompts[int(self.user_input) - 1][:-4] in self.time_keep.keys():
                    self.time_keep[self.prompts[int(self.user_input) - 1][:-4]] += .5
                else:
                    self.time_keep[self.prompts[int(self.user_input) - 1][:-4]] = .5
        else:
            self.times_for_day[self.time] = self.user_input
            print('\nYou have been working on ' + self.times_for_day[self.time])
            input()
            if self.user_input in self.time_keep.keys():
                self.time_keep[self.user_input] += .5
            else:
                self.time_keep[self.user_input] = .5

    def print_to_final_time_sheet(self, final_time_sheet):
        if self.military_hour == 20:
            with open(final_time_sheet) as f:
                data = f.readlines()
            text = open(final_time_sheet, "w")
            text.write(self.date + ":\n\n")
            text.close()
            text = open(final_time_sheet, "a")
            for key, value in self.time_keep.items():
                text.write(key + '\t\t' + str(value) + ' hours' + '\n\n')
            for i in data:
                text.write(i)

    def print_to_daily_sheet(self, path_to_folder):
        text = open(path_to_folder + '\\' + self.date + '.txt', 'w+')
        text.write(self.date + '\n\n')
        for key, value in self.times_for_day.items():
            text.write(key + '\t\t\t' + value + '\n\n')

    def run_time_logger(self, project_path, final_time_sheet, path_to_folder):
        self.load_time(1)
        self.load_time(2)
        self.set_project_path(project_path)
        self.display_prompts(1)
        self.get_user_input()
        self.set_time_key()
        self.print_to_final_time_sheet(final_time_sheet)
        self.print_to_daily_sheet(path_to_folder)
        self.save_time(1)
        self.save_time(2)
