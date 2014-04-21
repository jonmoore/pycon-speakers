import pandas as pd
import matplotlib.pyplot as plt
import requests
from counter import Counter
import json
import csv


class GenderHelper(object):

    def __init__(self):
        self.gender_dict = {}
        self.counter = Counter(250)
        self.count = 0

    def get_gender(self, name):
        if name not in self.gender_dict:
            self.counter.check_limit()
            url = 'http://api.genderize.io/?name=%s' %name
            response = requests.get(url).json()

            self.counter.increment()
            self.count += 1
            print self.count

            if response['gender'] is None:
                self.gender_dict[name] = 'andy'
            else:
                self.gender_dict[name] = response['gender']

        return self.gender_dict[name]
        

    def get_firstname(self, name):
            # in case the first token contains dot (e.g. Dr., Dr, D., S., etc)
            # take the next available token
            name_parts = name.split() 
            firstname = name_parts[0]
            if (firstname.find('.') != -1 or len(firstname) < 3) and len(name_parts) > 1:
                firstname = name_parts[1]
            
            # in case of french names like Jean-Paul, Jean-Sebastian, etc
            # take the second half 
            if firstname.find('-') != -1:
                firstname = firstname.split('-')[1]
            return firstname

    def correct_gender(self, gender, name):
        if gender == 'andy':
            gender_from_web = self.get_gender(self.get_firstname(name))
            
            return gender_from_web if gender_from_web is not None else 'andy'
        else:
            return gender
        

if __name__ == '__main__':
   
    with open('./ndata.csv', 'w+') as newfile:
        csvwriter = csv.writer(newfile, delimiter=',')
        with open('./data.csv', 'rb') as datafile:
            csvreader = csv.reader(datafile)
            gender_helper = GenderHelper()
            for c, g, n, i, y in csvreader:
                g = gender_helper.correct_gender(g,n)
                csvwriter.writerow([c,g,n,i,y])            