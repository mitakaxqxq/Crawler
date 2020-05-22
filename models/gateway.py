from .models import Website, Visits
import sqlalchemy
from sqlalchemy import desc
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('..')
from db import Base, Session


class WebsiteGateway:
    def __init__(self):
        self.db = Base()
        self.session = Session()

    def get_last_uncrawled_website_id(self):
        last_website_id = self.session.query(Visits).order_by(desc(Visits.visited_id)).first()
        return last_website_id.visited_id

    def get_count_of_websites(self, website_name):
        counter = 0
        reader = requests.get(website_name)
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

    def crawl_current_website(self, current_website_id):
        current_id = self.session.query(Visits).filter(Visits.visited_id == current_website_id).first()
        current_link = self.session.query(Website).filter(Website.website_id == current_id.visited_id).first()
        currently_visiting_id = current_id.visited_id
        reader = requests.get(str(current_link.name))
        try:
            reader.content
        except Exception:
            pass
        current_website_parent_link = self.session.query(Website.name).filter(
            Website.website_id == currently_visiting_id).first()
        if current_id.current_id == self.get_count_of_websites(current_website_parent_link.name):
            print('You have already visited all links on this website!')
            try:
                self.session.add(Visits(visited_id=current_website_id + 1, current_id=0))
                self.session.commit()
                self.session.close()
            except Exception:
                print('Already in database')
                self.session.rollback()
        else:
            self.add_new_websites(current_website_parent_link.name)
            self.session.query(Visits).filter(Visits.visited_id == current_website_id).update(
                {Visits.current_id: self.get_count_of_websites(current_website_parent_link.name)})
            self.session.commit()
            self.session.close()
            try:
                self.session.add(Visits(visited_id=current_website_id + 1, current_id=0))
                self.session.commit()
                self.session.close()
            except Exception:
                print('Already in database')
                self.session.rollback()

    def add_starting_websites(self, starting_url):
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
                    website = Website(name=element, server=server)
                    self.session.add(website)
                    self.session.commit()
                    self.session.close()
                except sqlalchemy.exc.IntegrityError:
                    print('Website already added')
                    self.session.rollback()
            if "link.php" in element and (element.startswith("http") or element.startswith("https")):
                try:
                    new_url = "https://register.start.bg" + element
                    website = Website(name=new_url, server=server)
                    self.session.add(website)
                    self.session.commit()
                    self.session.close()
                except sqlalchemy.exc.IntegrityError:
                    print('Website already added')
                    self.session.rollback()
        self.session.close()
        print('Done.')

    def add_new_websites(self, website_name):
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
                    website = Website(name=element, server=server)
                    self.session.add(website)
                    self.session.commit()
                    self.session.close()
                    queue.append(element)
                except sqlalchemy.exc.IntegrityError:
                    print('Website already added')
                    self.session.rollback()
            if "link.php" in element and (element.startswith("http") or element.startswith("https")):
                try:
                    new_url = website_name + element
                    website = Website(name=new_url, server=server)
                    self.session.add(website)
                    self.session.commit()
                    self.session.close()
                    queue.append(new_url)
                    print(new_url)
                except sqlalchemy.exc.IntegrityError:
                    print('Website already added')
                    self.session.rollback()
        self.session.close()
