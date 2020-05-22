import sys
from bootstrap import bootstrap
from models.controller import WebsiteController


class Application:

    @classmethod
    def build(self):
        bootstrap()
        controller = WebsiteController()
        controller.add_starting_websites(starting_url="https://register.start.bg")

    @classmethod
    def start(self):
        try:
            controller = WebsiteController()
            index = controller.get_last_uncrawled_website_id()
            while True:
                controller.crawl_current_website(index)
                index += 1
        except KeyboardInterrupt:
            pass


def main():
    command = sys.argv[1]
    if command == 'build':
        Application.build()
    elif command == 'start':
        Application.start()
    else:
        raise ValueError(f'Unkown command {command}. Valid ones are "build" and "start"!')


if __name__ == '__main__':
    main()
