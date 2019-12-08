import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, PostbackAction, MessageAction, MessageTemplateAction, PostbackTemplateAction, PostbackTemplateAction

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_url

load_dotenv()


# machine = TocMachine(
#     states=["user", "state1", "state2"],
#     transitions=[
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state1",
#             "conditions": "is_going_to_state1",
#         },
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state2",
#             "conditions": "is_going_to_state2",
#         },
#         {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
#     ],
#     initial="user",
#     auto_transitions=False,
#     show_conditions=True,
# )

machine = TocMachine(
    states=["user","fsm", "start", "swimmingring", "guilty", "encounter", "bad", "reriver", "save", "thousand", "greedy", "notbad", "compensate", "daughter", "happy", "ugly", "gay", "recompensate", "goodman", "gameover", "reriverfromguilty", "selfish"],
    transitions=[
        {"trigger": "advance", "source": "user", "dest": "fsm", "conditions": "is_going_to_fsm", },
        {"trigger": "advance", "source": "user", "dest": "start", "conditions": "is_going_to_start", },
        {"trigger": "advance", "source": ["start", "swimmingring"], "dest": "save", "conditions": "is_going_to_save",},
        {"trigger": "advance", "source": "start", "dest": "swimmingring", "conditions": "is_going_to_swimmingring",},
        {"trigger": "advance", "source": "swimmingring", "dest": "guilty", "conditions": "is_going_to_guilty",},
        {"trigger": "advance", "source": "guilty", "dest": "encounter", "conditions": "is_going_to_encounter",},
        {"trigger": "advance", "source": "guilty", "dest": "reriverfromguilty", "conditions": "is_going_to_reriverfromguilty",},
        {"trigger": "advance", "source": "encounter", "dest": "reriver", "conditions": "is_going_to_reriver",},
        {"trigger": "advance", "source": "encounter", "dest": "bad", "conditions": "is_going_to_bad",},
        {"trigger": "advance", "source": ["reriver", "reriverfromguilty"], "dest": "start", "conditions": "is_going_to_start",},
        {"trigger": "advance", "source": "reriver", "dest": "gameover", "conditions": "is_going_to_gameover",},
        {"trigger": "advance", "source": "save", "dest": "thousand", "conditions": "is_going_to_thousand",},
        {"trigger": "advance", "source": "thousand", "dest": "greedy", "conditions": "is_going_to_greedy",},
        {"trigger": "advance", "source": "thousand", "dest": "notbad", "conditions": "is_going_to_notbad",},
        {"trigger": "advance", "source": ["save", "recompensate"], "dest": "compensate", "conditions": "is_going_to_compensate",},
        {"trigger": "advance", "source": "compensate", "dest": "daughter", "conditions": "is_going_to_daughter",},
        {"trigger": "advance", "source": "compensate", "dest": "recompensate", "conditions": "is_going_to_recompensate",},
        {"trigger": "advance", "source": "daughter", "dest": "happy", "conditions": "is_going_to_happy",},
        {"trigger": "advance", "source": "daughter", "dest": "ugly", "conditions": "is_going_to_ugly",},
        {"trigger": "advance", "source": "daughter", "dest": "gay", "conditions": "is_going_to_gay",},
        {"trigger": "advance", "source": "recompensate", "dest": "goodman", "conditions": "is_going_to_goodman",},
        {"trigger": "advance", "source": "reriverfromguilty", "dest": "selfish", "conditions": "is_going_to_selfish",},
        {"trigger": "go_back", "source": ["fsm", "gameover", "bad", "greedy", "notbad", "happy", "ugly", "gay", "goodman", "selfish"], "dest": "user"},
        {"trigger": "advance", "source": ["user","fsm", "start", "swimmingring", "guilty", "encounter", "bad", "reriver", "save", "thousand", "greedy", "notbad", "compensate", "daughter", "happy", "ugly", "gay", "recompensate", "goodman", "gameover", "reriverfromguilty", "selfish"], "dest": "start", "conditions": "is_going_to_start",},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state == "user":
                text = "按start鍵開始遊戲\n按fsm鍵顯示狀態圖"
                btn=[
                    MessageTemplateAction(
                        label = "start",
                        text="start"
                    ),
                    MessageTemplateAction(
                        label = "fsm",
                        text="fsm"
                    )
                ]
                send_button_message(event.reply_token, text, btn)
            else:
                send_text_message(event.reply_token, "Not Entering any State")

    return "OK"

#draw fsm
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)

