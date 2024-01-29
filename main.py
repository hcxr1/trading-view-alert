import os
import json
import time
import schedule
from analysis.analysis import TvAnalysis
from webhook.webhook import Webhook

def read_configs():
  """ Read configs json """
  with open("configs/alert_configs.json", "r") as file:
    data = json.load(file)
  return data


def generate_notification(result):
  """ Generate Notification to Discord """
  webhook_id = os.environ.get("WEBHOOK_ID")
  webhook_token = os.environ.get("WEBHOOK_TOKEN")
  discord_webhook = Webhook(webhook_id, webhook_token)
  discord_webhook.data_parser(result)
  discord_webhook.send_notification()

def analyze_data(data):
  """ Analyze data based on configs """
  if data["status"] == "enabled":
    for item in data["data"]:
        result_obj = {}
        analyzer = TvAnalysis(
                item["symbol"],
                item["screener"],
                item["exchange"],
                item["period"]
            )

        result_obj["symbol"] = item["symbol"]
        result_obj["exchange"] = item["exchange"]

        if item["show_summary"] == True:
            result_obj["summary"] = analyzer.get_summary()

        if item["show_summary_breakdown"] == True:
            result_obj["summary_breakdown"] = analyzer.get_summary_breakdown()

        if item["show_statistics"] == True:
            result_obj["statistics"] = analyzer.get_statistics()

        if item["analysis"]["rsi_analysis"] == True:
            result_obj["rsi"] = analyzer.rsi_analysis()

        if item["analysis"]["moving_average_analysis"] == True:
            result_obj["ma"] = analyzer.moving_average_analysis()

        if item["analysis"]["macd_analysis"] == True:
            result_obj["macd"] = analyzer.macd_analysis()

        generate_notification(result_obj)

def run(data):
  analyze_data(data)
  print(schedule.get_jobs())     

def init():
  """ Run Tasks """
  data = read_configs()
  # define scheduler
  for item in data:
     if item["interval"] == "1h":
       schedule.every().hour.do(run, data = item)
     elif item["interval"] == "4h":
       schedule.every(4).hours.do(run, data = item)
     elif item["interval"] == "1d":
       schedule.every().day.do(run, data = item)
     elif item["interval"] == "1W":
       schedule.every().week.do(run, data = item)
  


if __name__ == "__main__":
  init()
  print("+-+-+-+-+-+-+-+-+-+-+-+-+ TvAlert Bot Started +-+-+-+-+-+-+-+-+-+-+-+-+")
  print(schedule.get_jobs())
  
  while 1:
    schedule.run_pending()
    time.sleep(1)

