# Crawler

This is a project that creates a histogram of the server software that runs bulgarian webpages (that end in .bg)

# Requirements

Before you can use this web crawler you need to install the packages in the requirements.txt file. You can do this with:

```
pip install -r requirements.txt
```

# Usage

After you have installed the packages, follow these steps:

1. Open a terminal
2. Navigate to the __Crawler__ directory
3. Run ```python main.py build```
- This command will create the __websites.db__ in the folder of the project.
4. Run ```python main.py start```
- This command will start the crawler, starting from https://register.start.bg/

# Program explanation

We have the following tables:
#### Websites
website_id  |  name  |  server  |
----------- | ------ | -------- |
1  |  https://register.start.bg/  |  Apache/2.2.15 (CentOS)  |
2  |  http://www.ibg.bg/  |  Apache/2.2.15 (CentOS)  |

#### Visits
visited_id  |  current_id  |
----------- | ------ |
1  |  0  |

In the table __Websites__, the __website_id__ column shows its id, the __name__ column shows the URL of the website and the __server__ column shows the server hosting the website.

In the table __Visits__ the __visited_id__ column shows the current website we are at and the __current_id__ shows the current link of the website we are at.

Our program uses BFS logic when traversing through the URLs that are in a given webpage. We start from our current webpage, find all URLs that are found in it, and then continue with the same steps with the first URL of our found.

Thanks to the __Visits__ table we know if we have visited all the links in a given webpage. If not, our program will continue from the last URL it was at. Example for a stopped crawler program is using the __Ctrl+C__ key combination and then starting the program again.
