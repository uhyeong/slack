import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from layer.common.utils import init_event


init_event()
# Install the Slack app and get xoxb- token in advance
app = App(
  token=os.environ.get('SLACK_BOT_TOKEN', None),
  signing_secret=os.environ.get('SLACK_SIGNING_SECRET', None)
)

@app.message("hello")
def message_hello(message, say):
  say(f"Hey there <@{message['user']}>!")

# Listens to incoming messages that contain "hello"
@app.message("show button")
def message_hello(message, say):
  # say() sends a message to the channel where the event was triggered
  say(
    # blocks 사용법 
    # https://api.slack.com/reference/block-kit/blocks
    blocks=[
      {
        "type": "section",
        "text": {
          "type": "mrkdwn", 
          "text": f"Hi~ <@{message['user']}>!"
        },
        "accessory": {
          "type": "button",
          "text": {
            "type": "plain_text", 
            "text": "Click Me"
          },
          "action_id": "button_click"
        }
      },
      {
			"type": "context",
			"elements": [
				{
					"type": "image",
					"image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
					"alt_text": "cute cat"
				},
				{
					"type": "mrkdwn",
					"text": "*Cat* has approved this message."
				}
			]
		},
		{
			"type": "input",
			"element": {
				"type": "multi_users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users",
					"emoji": True
				},
				"action_id": "multi_users_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Label",
				"emoji": True
			}
		}
    ],
    text=f"Hey there <@{message['user']}>!"
  )

@app.action("button_click")
def action_button_click(body, ack, say):
  # Acknowledge the action
  ack()
  say(f"<@{body['user']['id']}> clicked the button")


if __name__ == "__main__":
  SocketModeHandler(app, os.environ.get('SLACK_APP_TOKEN', None)).start()
