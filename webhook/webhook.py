import requests
from datetime import datetime

class Webhook:
  def __init__ (self, webhook_id, webhook_token):
    self.url = "https://discord.com/api/webhooks/"
    self.id = webhook_id
    self.token = webhook_token
    self.data = {}

  def data_parser (self, message):
    today = datetime.now().strftime("%a %d %b %Y, %H:%M")

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    self.data["username"] = "TvAlert Bot"
    self.data["allowed_mentions"] = { "parse": [ "everyone "]}
    self.data["content"] = "@everyone **" + message["exchange"] + ":" + message["symbol"] + "** Update: " + today

    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    self.data["embeds"] = []
    embed_obj = {}
    temp = ""

    if "summary" in message.keys():
        temp += "**SENTIMENT**: **{0}** [BUY: {1} | SELL: {2} | NEUTRAL: {3}]\n".format(
          message['summary']['RECOMMENDATION'],
          message['summary']['BUY'],
          message['summary']['SELL'],
          message['summary']['NEUTRAL'],
            )

    if "statistics" in message.keys():
        temp += "**OHLC** {0} {1} {2} {3}\n**VOLUME** {4}\n".format(
                    message['statistics']['open'],
                    message['statistics']['high'],
                    message['statistics']['low'],
                    message['statistics']['close'],
                    message['statistics']['volume']
            )

    if "rsi" in message.keys():
        temp += "**RSI** {0} [*{1}*]\n".format(
                    message['rsi']['rsi'],
                    message['rsi']['status']
            )

    embed_obj["description"] = temp

    if message['summary']['RECOMMENDATION'] == "SELL":
        embed_obj["color"] = 16711680 #red
    elif message['summary']['RECOMMENDATION'] == "BUY":
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
