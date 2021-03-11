from bs4 import BeautifulSoup
import requests


class dllink_scraper:
    def __init__(self):
        HOMEPAGE_URL = 'https://www.gogoanime.sh'
        self.HOMEPAGE_URL = HOMEPAGE_URL

    def search(self, keyword):
        html_data = requests.get(
            f"{self.HOMEPAGE_URL}/search.html?keyword={keyword}")
        soup = BeautifulSoup(html_data.text, 'html.parser')
        a_tags = soup.find_all(attrs={"class": "items"})
        l = a_tags[0].find_all("a")
        t = a_tags[0].get_text().replace(" ", "").split("\n")
        for i in range(0, t.count('')):
            t.remove('')

        count = 1
        for t_index in range(0, len(t), 2):
            print(count, t[t_index], t[t_index+1])
            count += 1

        links = []

        for link in l:
            links.append(link["href"])

        links = list(dict.fromkeys(links))

        return links

    def get_eplinks(self, param):
        episodes = requests.get(f"{self.HOMEPAGE_URL}/{param}").text
        soup = BeautifulSoup(episodes, 'html.parser')
        epnum = soup.find_all(id="episode_page")
        n = epnum[0].find_all("a")
        nums = []

        for num in n:
            nums.append(num["ep_end"])

        e = int(nums[-1]) + 1

        ep_links = []

        for k in range(1, e):
            ep_links.append(
                f'{self.HOMEPAGE_URL}/{param.split("/")[-1]}-episode-{k}')

        return ep_links

    def get_dllink(ep_link):
        eppage = requests.get(ep_link)
        soup = BeautifulSoup(eppage.text,'html.parser')
        tags = soup.find_all(attrs={"class":"anime_video_body_cate"})

        v = tags[0].find_all("a")

        links = []

        for l in v:
            links.append(l["href"])

        dlpage = requests.get(links[-1])
        soup = BeautifulSoup(dlpage.text,'html.parser')
        
        dllinks = soup.find_all(attrs={"class": "mirror_link"})
        f_link = dllinks[0].a["href"]
        f_link = f_link.replace(" ", "%20")

        return f_link