import requests
from bs4 import BeautifulSoup


def main():
    initial_url = "https://register.start.bg"
    queue = [initial_url]
    passed = [initial_url]
    while queue:
        url = queue.pop(0)
        reader = requests.get(url)
        html_doc = reader.content
        soup = BeautifulSoup(html_doc, "html.parser")
        list_of_tags = soup.find_all("a")

        for link in list_of_tags:
            website = link.get("href")
            element = str(website)
            if element.find(".bg") and (element.startswith("http") or element.startswith("https")):
                print(element)
                if element not in passed:
                    queue.append(element)
                    passed.append(element)

        reader = requests.get(url)


if __name__ == '__main__':
    main()
