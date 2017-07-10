import codecs
from selenium import webdriver
from bs4 import BeautifulSoup
from slackclient import SlackClient

def get_book_title(url):
	driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 550)
	driver.get(url)
	response = driver.page_source.encode('utf-8')
	driver.quit()
	html_str = str(response)
	soup = BeautifulSoup(html_str, "html.parser")
	title = soup.find('div', 'dotd-title')
	children = title.findChildren()
	for child in children:
		return child.contents

def clean_string(title):
	clean = str(title[0])
	clean = bytes(clean, 'utf-8').decode('unicode_escape').strip()
	return clean

def deploy_bot(url, title):
	SLACK_BOT_TOKEN =''
	BOT_NAME = 'packtbot'
	slack_client = SlackClient(SLACK_BOT_TOKEN)
	message = get_message(url,title)
	if slack_client.rtm_connect():
		slack_client.api_call("chat.postMessage", channel='random',
			text=message, as_user=True)
	else:
		print('Connection failed\n')

def get_message(url, title):
	message = 'Todays free book is {0} \n'.format(title)
	message += 'Browse over to {0} to claim it!\n'.format(url)
	return message

def main():
	url='https://www.packtpub.com/packt/offers/free-learning'
	title = get_book_title(url)
	title = clean_string(title)
	deploy_bot(url,title)


if __name__ == "__main__":
	main()