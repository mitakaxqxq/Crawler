import sys
from bootstrap import bootstrap
from models.controller import WebsiteController
from utils import draw_chart_by_dictionary


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

    @classmethod
    def show(self):
        choice = input('Do you want to see chart? (y/n)')
        if choice == 'y':
            draw_chart_by_dictionary()
        else:
            print('Goodbye!')


def main():
    command = sys.argv[1]
    if command == 'build':
        Application.build()
    elif command == 'start':
        Application.start()
    elif command == 'show':
        Application.show()
    else:
        raise ValueError(f'Unkown command {command}. Valid ones are "build" and "start"!')


if __name__ == '__main__':
    main()
