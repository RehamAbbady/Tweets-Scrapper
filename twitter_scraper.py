from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

class Tweet(object):
  def __init__(self, tweet_id:str,text:str,screen_name:str,user_id:str,tweet_time:str):
      self.tweet_id=tweet_id
      self.text=text
      self.screen_name=screen_name
      self.user_id=user_id
      self.tweet_time=tweet_time
 

#convert string to list
def Convert(string): 
    l = list(string.split(" ")) 
    return l

#create a function to search in twitter by keyword, and a date range(starting and ending dates)
#and then scroll to the end of the search result to get all tweets
def Search(keyword,s_date,e_date,driver):
    keyword=Convert(keyword)
    url="https://twitter.com/search?q="
    #form the search query url
    for word in keyword:
        url += "{}%20".format(word)
    url+="until%3A{}".format(e_date)
    url+="%20since%3A{}&".format(s_date)
    driver.get(url)
    print(url)
    #scroll to the end of the page
    page_height = driver.execute_script("return document.body.scrollHeight") 
    while True:
        #scroll to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #wait befor trying to scroll again
        time.sleep(5)
        page_height_new=driver.execute_script("return document.body.scrollHeight")
        #if the current page height equals the previous page height then you reached the bottom
        if page_height==page_height_new:
            break
        #assign  page height after refreshing
        page_height=page_height_new

def get_tweets(driver):
    tweet_div = driver.page_source
    #bs object represents the document as a nested data structure
    obj = BeautifulSoup(tweet_div, "html.parser")
    #find divs with class tweets
    content = obj.find_all("div", class_="tweet")
    tweets=[]
    for c in content:
            tweet_id=c['data-tweet-id']
            text = c.find("p", class_="tweet-text").getText()
            screen_name = c.find("strong", class_="fullname").getText()
            user_id=c['data-user-id']
            tweet_time = c.find(class_="tweet-timestamp")['title']
            print(tweet_time)
            t=Tweet(tweet_id,text,screen_name,user_id,tweet_time)
            tweets.append(t)

    return tweets

def to_json_file(tweets):
    for t in tweets:
        with open("tweets.json", "a") as file:
                json.dump(t.__dict__ ,file)
    


def main():
    keyword = input("please enter kewords: ") 
    s_date = input("please enter the start date in the format YYYY-MM-DD: ") 
    e_date = input("please enter the end date in the format YYYY-MM-DD: ") 
    #create a webdriver instance 
    driver = webdriver.Chrome('E:\chromedriver')
    Search(keyword,s_date,e_date,driver)
    all_tweets=get_tweets(driver)
    to_json_file(all_tweets)
   


if __name__ == "__main__":
    main()
    
