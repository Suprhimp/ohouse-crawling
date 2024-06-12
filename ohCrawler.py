from ohImgDownload import ohImgDownload
import urllib.request
from ohLinkFinder import ohLinkFinder

save_path ='livingroom-sofatable'

def ohCrawler(toSearch: str, howMany: int):
    linkSet = ohLinkFinder(toSearch, howMany)
    # for i, link in enumerate(linkSet):
    #     pad = '0'
    #     n = 3

    #     saveName = str(i).rjust(n, pad)
        # ohImgDownload(link, save_path+'/'+saveName + '.jpg')
        # urllib.request.urlretrieve(link,  save_path+'/'+saveName + '.jpg')
        

ohCrawler('10150001', 300)