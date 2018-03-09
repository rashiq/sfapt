import requests
from bs4 import BeautifulSoup
import subprocess


def scrape():
  headers = {
      'Origin': 'https://www.sfcorporaterentals.com',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6,la;q=0.5',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Accept': '*/*',
      'Referer': 'https://www.sfcorporaterentals.com/property/the-mission-studio-1508/',
      'X-Requested-With': 'XMLHttpRequest',
      'Connection': 'keep-alive',
  }

  # 1521072000
  data = [
      ('action', 'wpia_changeDay'),
      ('calendarDirection', 'jump'),
      ('totalCalendars', '5'),
      ('currentTimestamp', '1531612800'),
      ('calendarHistory', '1'),
      ('showLegend', 'no'),
      ('showDropdown', '1'),
      ('showWeekNumbers', 'no'),
      ('calendarLanguage', 'en'),
      ('weekStart', '1'),
      ('jump', 'no'),
      ('calendarID', '49'),
  ]

  response = requests.post(
    'https://www.sfcorporaterentals.com/wp-admin/admin-ajax.php',
    headers=headers,
    data=data
  )

  if response.status_code == 200:
    response = response.text
  else:
    send_email(body="You got blocked m8!")

  soup = BeautifulSoup(response, "html.parser")


  booked = soup.select('li.status-booked')

  if len(booked):
    send_email(body='There are some new bookings!')


def send_email(body):
  command = \
      """curl 172.18.0.1:1235
    -H "Content-Type: application/json"
    -d '{"subject": "SF Corp Apartments", "body": "{body}"}'
  """.format(body=body)
  subprocess.call([command], shell=True)


if __name__ == '__main__':
  scrape()