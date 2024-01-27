import os
import json
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

        if item["show_statistics"] == True:
            result_obj["statistics"] = analyzer.get_statistics()

        if item["analysis"]["rsi_analysis"] == True:
            result_obj["rsi"] = analyzer.rsi_analysis()

        if item["analysis"]["moving_average_analysis"] == True:
            result_obj["ma"] = analyzer.moving_average_analysis()

        if item["analysis"]["macd_analysis"] == True:
            result_obj["macd"] = analyzer.macd_analysis()

        generate_notification(result_obj)

@repeat(every().hour)
def run():
  """ Run Tasks """
  data = read_configs()
  analyze_data(data)

if __name__ == "__main__":

  while 1:
    schedule.run_pending()
    time.sleep(1)

