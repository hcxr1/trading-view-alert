# trading-view-alert

This is a webhook implementation that returns Trading View Analysis to discord.


## How to Use
1. Install the necessary dependencies:
`pip install -r requirements.txt`

2. Setup the environment parameters using terminal:
```
export WEBHOOK_ID=<YOUR DISCORD WEBHOOK ID>
export WEBHOOK_TOKEN=<YOUR DISCORD WEBHOOK TOKEN>
```

3. To Run the program:
`python main.py`


## Configuration
Before Running the program, please setup the `alert_configs.json` in the configs directory.
```
{
 status: enable/disable the current config
 interval: scheduler interval period
 data: market parameters and analysis
}
```
