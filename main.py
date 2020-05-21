import requests
import sys
from bs4 import BeautifulSoup
from db import session
from bootstrap import bootstrap
from models.models import Website, Visits
import sqlalchemy


def crawl_current_website(current_website_id):
    current_id = session.query(Visits).filter(Visits.visited_id == current_website_id).first()
    current_link = session.query(Website).filter(Website.website_id == current_id.visited_id).first()
    print(current_id.visited_id, current_id.current_id)
    print(current_link.website_id, current_link.name, current_link.server, current_link.parent_id)
    currently_visiting_id = current_id.visited_id
    reader = requests.get(str(current_link.name))
    try:
        html_doc = reader.content
    except Exception:
        pass
    current_website_parent_link = session.query(Website.name).filter(
        Website.website_id == currently_visiting_id).first()
    if current_id.current_id == get_count_of_websites(current_website_parent_link.name):
        print('You have already visited all links on this website!')
        try:
            session.add(Visits(visited_id=current_website_id+1, current_id=0))
            session.commit()
        except Exception: 
            print('Already in database')
            session.rollback()
    else:
        list_of_added_sites = add_new_websites(current_website_parent_link.name, current_website_id)
        session.query(Visits).filter(Visits.visited_id == current_website_id).update(
        {Visits.current_id: currently_visiting_id + get_count_of_websites(current_website_parent_link.name)})
        session.commit()
        try:
            session.add(Visits(visited_id=current_website_id+1, current_id=0))
            session.commit()
        except Exception: 
            print('Already in database')
            session.rollback()


def add_starting_websites(starting_url, queue):
    bootstrap()
    reader = requests.get(starting_url)
    server = reader.headers["Server"]

    html_doc = reader.content
    soup = BeautifulSoup(html_doc, "html.parser")
    list_of_tags = soup.find_all("a")

    for link in list_of_tags:
        website = link.get("href")
        element = str(website)
        if ".bg" in element and (element.startswith("http") or element.startswith("https")):
            print(element)
            try:
                website = Website(name=element, server=server, parent_id=0)
                session.add(website)
                session.commit()
                queue.append(element)
            except sqlalchemy.exc.IntegrityError:
                print('Website already added')
                session.rollback()
        if "link.php" in element and (element.startswith("http") or element.startswith("https")):
            try:
                new_url = "https://register.start.bg" + element
                website = Website(name=new_url, server=server, parent_id=0)
                session.add(website)
                session.commit()
                queue.append(element)
            except sqlalchemy.exc.IntegrityError:
                print('Website already added')
                session.rollback()
    session.close()
    print('Done.')
    return queue


def get_count_of_websites(website_name):
    counter = 0
    reader = requests.get(website_name)
    server = reader.headers["Server"]
    html_doc = reader.content
    soup = BeautifulSoup(html_doc, "html.parser")
    list_of_tags = soup.find_all("a")

    for link in list_of_tags:
        website = link.get("href")
        element = str(website)
        if ".bg" in element and (element.startswith("http") or element.startswith("https")):
            counter += 1
        if "link.php" in element and (element.startswith("http") or element.startswith("https")):
            counter += 1
    return counter

def add_new_websites(website_name, website_parent_id):
    print(website_name)
    queue = []
    reader = requests.get(website_name)
    server = reader.headers["Server"]
    html_doc = reader.content
    soup = BeautifulSoup(html_doc, "html.parser")
    list_of_tags = soup.find_all("a")

    for link in list_of_tags:
        website = link.get("href")
        element = str(website)
        if ".bg" in element and (element.startswith("http") or element.startswith("https")):
            print(element)
            try:
                website = Website(name=element, server=server, parent_id=website_parent_id)
                session.add(website)
                session.commit()
                queue.append(element)
            except sqlalchemy.exc.IntegrityError:
                print('Website already added')
                session.rollback()
        if "link.php" in element and (element.startswith("http") or element.startswith("https")):
            try:
                new_url = website_name + element
                website = Website(name=new_url, server=server, parent_id=website_parent_id)
                session.add(website)
                session.commit()
                queue.append(new_url)
                print(new_url)
            except sqlalchemy.exc.IntegrityError:
                print('Website already added')
                session.rollback()
    session.close()


def main():
    command = sys.argv[1]
    if command == 'build':
        add_starting_websites("https://register.start.bg", [])
    elif command == 'start':
        try:
            index = 1
            while True:
                crawl_current_website(index)
                index += 1
        except KeyboardInterrupt:
            session.commit()
            session.close()
    else:
        raise ValueError(f'Unkown command {command}. Valid ones are "build" and "start"!')


if __name__ == '__main__':
    bootstrap()
    main()
