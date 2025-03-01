from EasyApply import EasyApply
import json
import time

if __name__ == "__main__":
	with open("config.json") as config_file:
		data = json.load(config_file)

	# flow of app
	bot = EasyApply(data)
	bot.login()
	bot.search_jobs({ "title": data["keywords"], "location": data["location"]})
	time.sleep(1)
	bot.easy_apply_filter()
	bot.other_filters()
	bot.apply_all_filters()
	time.sleep(2)
	bot.find_offers()

	while(True):
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			print("Ended script lifecycle")
			break
		except Exception as e:
			print(f"Error: Script ended with exception {e}")
			break