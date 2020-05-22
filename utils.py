from models.models import Website
from db import Session
import datetime
import matplotlib.pyplot as plt


def get_dict_of_info():
    new_dict = {'hour': 0, 'two hours': 0, 'six hours': 0, 'twelve hours': 0, 'day': 0}
    session = Session()
    information = session.query(Website).filter(Website.created_at.ilike("%2020-%")).all()
    for website in information:
        date_of_creation = website.created_at
        time_of_creation = datetime.datetime.strptime(date_of_creation, '%Y-%m-%d %H:%M:%S.%f')
        time_for_hour = str(datetime.datetime.now() - datetime.timedelta(hours=1))
        time_for_two_hours = str(datetime.datetime.now() - datetime.timedelta(hours=2))
        time_for_six_hours = str(datetime.datetime.now() - datetime.timedelta(hours=6))
        time_for_twelve_hours = str(datetime.datetime.now() - datetime.timedelta(hours=12))
        time_for_day = str(datetime.datetime.now() - datetime.timedelta(hours=24))
        if time_for_hour <= str(time_of_creation.date()) + str(time_of_creation.time()):
            new_dict['hour'] += 1
        if time_for_two_hours <= str(time_of_creation.date()) + str(time_of_creation.time()):
            new_dict['two hours'] += 1
        if time_for_six_hours[0] <= str(time_of_creation.date()) + str(time_of_creation.time()):
            new_dict['six hours'] += 1
        if time_for_twelve_hours[0] <= str(time_of_creation.date()) + str(time_of_creation.time()):
            new_dict['twelve hours'] += 1
        if time_for_day[0] <= str(time_of_creation.date()) + str(time_of_creation.time()):
            new_dict['day'] += 1
    return new_dict
    session.close()


def draw_chart_by_dictionary():
    my_dict = get_dict_of_info()
    keys = my_dict.keys()
    values = my_dict.values()
    plt.suptitle('Crawled websites for the past time')
    plt.bar(keys, values)
    plt.savefig('crawled_websites.png', dpi=400)
    plt.show()
