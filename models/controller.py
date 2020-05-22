from .gateway import WebsiteGateway


class WebsiteController:
    def __init__(self):
        self.gateway = WebsiteGateway()

    def get_last_uncrawled_website_id(self):
        return self.gateway.get_last_uncrawled_website_id()

    def get_count_of_websites(self, website_name):
        return self.gateway.get_count_of_websites(website_name)

    def add_starting_websites(self, starting_url):
        self.gateway.add_starting_websites(starting_url)

    def crawl_current_website(self, website_name):
        self.gateway.crawl_current_website(website_name)

    def add_new_websites(self, website_name):
        self.gateway.add_new_websites(website_name)
