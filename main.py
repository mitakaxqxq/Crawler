import requests
from bs4 import BeautifulSoup
from db import Session
from bootstrap import bootstrap
from models.models import Website


def main():
    session = Session()
    initial_url = "https://register.start.bg"
    queue = [initial_url]
    passed = [initial_url]
    while queue:
        url = queue.pop(0)
        reader = requests.get(url)
        server = reader.headers["Server"]

        website = Website(name=url, server=server)
        session.add(website)
        session.commit()

        html_doc = reader.content
        soup = BeautifulSoup(html_doc, "html.parser")
        list_of_tags = soup.find_all("a")

        for link in list_of_tags:
            website = link.get("href")
            element = str(website)
            if ".bg" in element and (element.startswith("http") or element.startswith("https")):
                print(element)
                if element not in passed:
                    queue.append(element)
                    passed.append(element)


if __name__ == '__main__':
    bootstrap()
    main()
