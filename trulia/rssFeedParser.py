import re
import operator
import feedparser

#trulia_value_path = 'entities, *integer*, title_detail, value'  
#trulia_link_path = 'entities, *integer*, link'

def extract_num_followed_by_word(text, word):
    if(re.search('\d+ '+word, text)):
        uword = re.search('\d+ '+word, text).group()
        sword = str(uword)
        sword = re.search('\d+', sword).group()
        return int(sword)



"""EXTRACT_PRICE
prices of the form $14,000 
4 steps
    1. split on space
    2. find the array-element with a '$' in it
    3. remove the '$' and ',' 
    4. and convert to int
"""
def extract_price(value):
    if(re.search('\$',value)):
        space = re.split(' ', value) 
        #space = [u'2815', u'Kensington', u'Ave,', u'Kansas', u'City,', u'MO', u'64128,', u'$24,900', u'3', u'beds,', u'2', u'baths']
        uprice = [s for s in space if '$' in s] #unicode string price
        uprice = uprice[0] #array[unicode] -> unicode string
        sprice = str(uprice) #unicode -> string price
        if('$' in sprice): 
            sprice = sprice.replace('$','')
        if(',' in sprice): 
            sprice = sprice.replace(',','')

        return int(sprice)

"""
trulia_feed_kc = 'http://www.trulia.com/rss2/for_sale/Kansas_City,MO/0-25000_price/'
trulia_feed_sf = 'http://www.trulia.com/rss2/for_sale/San_Francisco,CA/1-300000_price/'
trulia_feed_omaha = 'http://www.trulia.com/rss2/for_sale/Omaha,NE/1-25000_price/'
trulia_feeds = [trulia_feed_omaha, trulia_feed_kc]
"""
f = open('feeds')
feed_urls = f.readlines()
f.close()
houses=dict()
j=0 #feed counter

for feed_url in feed_urls:
    d = feedparser.parse(feed_url)
    print "Parsing "+feed_url
    for i in range(0, d['entries'].__len__()):
        """
        try:
            d['entries'][i]
        except IndexError:
            break
        """
        link = str(d['entries'][i]['link'])
        value = d['entries'][i]['title']
        summary = d['entries'][i]['summary']
        #value = u'2815 Kensington Ave, Kansas City, MO 64128, $24,900 3 beds, 2 baths'
        sqft = extract_num_followed_by_word(summary, 'sqft')
        beds = extract_num_followed_by_word(value, 'bed')
        baths = extract_num_followed_by_word(value, 'bath')
        price = extract_price(value)
        ratio = 0
        if(price>0 and beds>0 and baths>0):
            ratio = (beds*baths)/(price/10000.0)
        houses[j]= [ratio, sqft, price, beds, baths, link]#,link
        i+=1; j+=1

#sort houses on ratio (the first element in the value array) (high ratio is good)
homes = sorted(houses.itervalues(), key=operator.itemgetter(1), reverse=1)
homes = sorted(houses.itervalues(), key=operator.itemgetter(0), reverse=1)

f = open('homes.csv','w')
line = str()
for home in homes:
    for field in home:
        line += str(field)+', '
    f.write(line.__getslice__(0,line.__len__()-2) + '\n')
    line = ''
f.close()
