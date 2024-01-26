import json



if __name__ == "__main__":
  with open("alert_configs.json", "r") as file:
    data = json.load(file)

  if data["status"] == "enabled":
    """ logic here """
