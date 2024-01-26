import requests
from datetime import datetime

class Webhook:
  def __init__ (self, webhook_url, webhook_id, webhook_token):
    self.url = webhook_url
    self.id = webhook_id
    self.token = webhook_token
    self.data = {}

  def data_parser (self, message):
    today = datetime.now()

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    self.data["username"] = "TvAlert Bot"
    self.data["allowed_mentions"] = { "parse": [ "everyone "]}
    self.data["content"] = "@everyone Current Update: " + today

    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    self.data["embeds"] = []

    for item in message:
      embed_obj = {}
      embed_obj["title"] = item["exchange"] +":" + item["symbol"]
      embed_obj["description"] = """
      **SENTIMENT**: **{0}** [BUY: {1} | SELL: {2} | NEUTRAL: {3}]
      
      **OHLC** {4} {5} {6} {7}
      **VOLUME** {8}
      **RSI** {9} [*{10}*]
      """.format(
          item['summary']['RECOMMENDATION'],
          item['summary']['BUY'],
          item['summary']['SELL'],
          item['summary']['NEUTRAL'],
          item['statistics']['open'],
          item['statistics']['high'],
          item['statistics']['low'],
          item['statistics']['close'],
          item['rsi']['rsi'],
          item['rsi']['status']
          )

      if item['summary']['RECOMMENDATION'] == "SELL":
        embed_obj["color"] = 16711680 #red
      elif item['summary']['RECOMMENDATION'] == "BUY":
        embed_obj["color"] = 65280 #green
      else: 
        embed_obj["color"] = 16777215 #white

      self.data["embeds"].push(embed_obj)


  def send_notification(self):
    webhook = self.url + self.id + '/' + self.token
    result = requests.post(webhook, json = self.data)

    try:
      result.raise_for_status()
    except requests.exceptions.HTTPError as err:
      print(err)
    else:
      print("Payload delivered successfully, code {}.".format(result.status_code))
