# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

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
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)


#
# Example main menu referenced in the Start() method
# for the 'Video' prefix handler
#

def VideoMainMenu():
    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")

    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    content = XML.ElementFromURL(PRODUCTION_URL, True)
    for item in content.xpath('//div[@class="filter"]/a'):
			titleUrl = item.get('href')
			title = item.text
			dir.Append(
					Function(
						DirectoryItem(CategoryPage, title, subtitle="", summary="", thumb=R(ICON), art=R(ART)), 
						  pageUrl=BASE_URL+titleUrl)
					)
    # ... and then return the container
    return dir

def CategoryPage(sender, pageUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    dir.viewGroup = 'InfoList'
    content = XML.ElementFromURL(pageUrl, True)
    for item in content.xpath('//div[@class="column span-16 item"]'):
  		# title = item.xpath('./h1').text
			# titleUrl = item.xpath('./div[@class="column span-4"]/a').get('href')
			# thumb = item.xpath('./div[@class="column span-4"]/a/img').get('src')
			# description = item.xpath('./div[@class="column span-12"]/p').text
			# dir.Append(Function(CallbackExample, title, subtitle="", summary=decription, thumb=R(BASE_URL+thumb), art=R(ART)), 
			#		titleUrl=BASE_URL+titleUrl)
			dir.Append(Function(
				DirectoryItem(CallbackExample, "title", subtitle="subtitle", summar="summary", thumb=R(ICON), art=R(ART)),
        titleUrl="/url")
				)
    return dir

# def VideoPage(sender, titleUrl):
#    dir = MediaContainer(title2=sender.itemTitle)
#    dir.viewGroup = 'InfoList'
#    return dir

def CallbackExample(sender,titleUrl):

    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "Not implemented",
        "In real life, you'll make more than one callback,\nand you'll do something useful.\nsender.itemTitle=%s" % sender.itemTitle
    )


