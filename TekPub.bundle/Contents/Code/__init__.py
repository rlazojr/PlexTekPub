# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import re # <-- for regular expressions

####################################################################################################

VIDEO_PREFIX = "/video/tekpub"
BASE_URL       = "http://tekpub.com"
PRODUCTION_URL = "http://tekpub.com/productions"
NAME           = L('Title')
CACHE_INTERVAL = 1800
ART            = 'art-default.jpg'
ICON           = 'icon-default.png'
DEBUG          = True

####################################################################################################

def Start():
    ## make this plugin show up in the 'Video' section
    ## in Plex. The L() function pulls the string out of the strings
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")

    dir.Append(
      Function(
        DirectoryItem(CategoryPage, "All Series", subtitle="", summary="", 
          thumb=R(ICON), art=R(ART)), 
          pageUrl=PRODUCTION_URL)
        )
    content = XML.ElementFromURL(PRODUCTION_URL, True)
    for item in content.xpath('//div[@class="filter"]/a'):
			titleUrl = item.get('href')
			title = item.text
			dir.Append(
					Function(
						DirectoryItem(CategoryPage, title, subtitle="", summary="", thumb=R(ICON), 
							art=R(ART)), 
						  pageUrl=BASE_URL+titleUrl)
					)
    # ... and then return the container
    return dir

def CategoryPage(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    dir.viewGroup = 'InfoList'
    content = XML.ElementFromURL(pageUrl, True)
    for item in content.xpath('//div[@class="column span-16 item"]'):
			title = item.xpath('./h1')[0].text
			titleUrl = item.xpath('./div[@class="column span-4"]/a')[0].get('href')
			thumb = item.xpath('./div[@class="column span-4"]/a/img')[0].get('src')
			description = item.xpath('./div[@class="column span-12"]/p')[0].text
			dir.Append(Function(
				DirectoryItem(VideoPage, title, subtitle="", summary=description, 
					thumb=BASE_URL+thumb, art=R(ART)),
        titleUrl=BASE_URL+titleUrl)
				)
    return dir

def VideoPage(sender, titleUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    dir.viewGroup = 'InfoList'
    idx = 0
    content = XML.ElementFromURL(titleUrl, True)
    slide = content.xpath('//div[@class="column span-17"]/img')[0].get('src')
    for item in content.xpath('//div[@class="item"]/h2/a'):
      title = item.text
      titleUrl = item.get('href')
      description = item.xpath('../../p')[idx].text

      # Opening the videopage at this point to find the info is going to take too much time, as we need to open pages for all the
      # videos in the list we're buidling here.
      # Instead we postpone those steps until the moment a user selects a video. For this we add an extra function that's going to
      # be called at the moment a user selects a video. In this example it's called "PlayVideo" (you can name it whatever you
      # want) and we send it the url of the video page.

      dir.Append(Function(WebVideoItem(PlayVideo, title=title, summary=description, thumb=R(ICON)), url=BASE_URL+titleUrl))

      idx = idx + 1
		
    return dir

def PlayVideo(sender, url):
    # Open the webpage containing the video
    videopage = HTTP.Request(url)

    # Find the two pieces of information we need in the webpage by using regular expressions
    # These regex things may look a bit scary at first ;)
    url  = re.search("netConnectionUrl: '(.+?)'", videopage).group(1)
    clip = re.search("clip.+?url: '(.+?)'", videopage, re.DOTALL).group(1)

    return Redirect(RTMPVideoItem(url, clip))


def CallbackExample(sender,titleUrl):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "Not implemented",
        "In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle
    )


