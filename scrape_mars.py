import requests
import json
import GetOldTweets3 as got
import pandas as pd

def scrape_data():

    api = 'https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #Twitter arguments
    username = 'MarsWxReport'
    num_tweets = 1

    #Mars caracteristics
    url = 'https://space-facts.com/mars/'

    s = requests.Session()

    #Get img and data from https://mars.nasa.gov
    response_api = s.get(api)
    json_data = json.loads(response_api.text)

    #Get tweets from @MarsWxReport
    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(num_tweets)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

    #Get Diameter, Mass, etc. from https://space-facts.com/mars/
    mars_html_table = pd.read_html(url)
    mars_df = mars_html_table[0]

    main_img = 'https://mars.nasa.gov' + json_data['items'][0]['main_image']
    title = json_data['items'][0]['title']
    paragraph = json_data['items'][0]['description']
    mars_climate = user_tweets[0][1]
    #table
    mars_table = mars_df.values.tolist()

    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"}]

    data = {
        'main_img':main_img,
        'title':title,
        'paragraph':paragraph,
        'mars_climate':mars_climate,
        'mars_table':mars_table,
        'hemisphere_img_urls':hemisphere_image_urls
    }

    return data