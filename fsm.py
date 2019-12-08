from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ButtonsTemplate, PostbackAction, MessageAction, MessageTemplateAction, PostbackTemplateAction, PostbackTemplateAction
from utils import send_text_message, send_button_message, send_image_url


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    # def is_going_to_user(self, event):
    #     text = event.message.text
    #     return True
    # def on_enter_user(self, event):
    #     print("I'm entering start")
    #     text = "接下來將為你呈現一個小小的道德測驗\n按下按鈕開始"
    #     reply_token = event.reply_token
    #     btn=[
    #         MessageTemplateAction(
    #             label = "Start",
    #             text="Start"
    #         )
    #     ]
    #     send_button_message(reply_token, text, btn)
    def is_going_to_fsm(self, event):
        text = event.message.text
        return (text.lower() == "fsm" or text.lower() == "fsm ")
    
    def on_enter_fsm(self, event):
        print("I'm entering fsm")
        reply_token = event.reply_token
        img_url = "https://toc-chatbot.herokuapp.com/show-fsm"
        send_image_url(reply_token, img_url)
        self.go_back()
    
    def is_going_to_start(self, event):
        text = event.message.text
        return (text.lower() == "start" or text == "我願意" or text.lower() == "start " or text.lower() == "restart" or text.lower() == "restart ")
    
    def on_enter_start(self, event):
        print("I'm entering start")

        text = "有一天當你走在路上，看到一個老爺爺掉進河裡，請問你會怎麼做?"
        reply_token = event.reply_token
        btn=[
            MessageTemplateAction(
                label = "跳下去救他",
                text="跳下去救他"
            ),
            MessageTemplateAction(
                label = "我不會游泳沒辦法救",
                text="我不會游泳沒辦法救"
            )
        ]
        send_button_message(reply_token, text, btn)

    def is_going_to_swimmingring(self, event):
        text = event.message.text
        return text == "我不會游泳沒辦法救"

    def on_enter_swimmingring(self, event):
        print("I'm entering swimmingring")
        text = "但是旁邊剛好有游泳圈欸，你確定不救?"
        btn=[
            MessageTemplateAction(
                label = "當然救",
                text="當然救"
            ),
            MessageTemplateAction(
                label = "有急事，應該會有人救吧",
                text="有急事，應該會有人救吧"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
        

    def is_going_to_guilty(self, event):
        text = event.message.text
        return text == "有急事，應該會有人救吧"

    def on_enter_guilty(self, event):
        print("I'm entering guilty")
        text = "結果看到新聞報導那位老爺爺溺死在河中請問你會愧疚嗎"
        btn=[
            MessageTemplateAction(
                label = "當然會愧疚",
                text="當然會愧疚"
            ),
            MessageTemplateAction(
                label = "雖然他死了，但不是我的錯",
                text="雖然他死了，但不是我的錯"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)

    def is_going_to_encounter(self, event):
        text = event.message.text
        return text == "雖然他死了，但不是我的錯"
    
    def on_enter_encounter(self, event):
        print("I'm entering encounter")
        text = "過了幾天去河邊玩，不小心掉進去河裡，但路過的人也都不救你，你會恨他們嗎?"
        btn=[
            MessageTemplateAction(
                label = "當然會恨",
                text="當然會恨"
            ),
            MessageTemplateAction(
                label = "我不會恨他們",
                text="我不會恨他們"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)

    def is_going_to_bad(self, event):
        text = event.message.text
        return text == "當然會恨"
    
    def on_enter_bad(self, event):
        print("I'm entering bad")
        text = "可是你當初也是這樣啊~(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_reriverfromguilty(self, event):
        text = event.message.text
        return text == "當然會愧疚"

    def on_enter_reriverfromguilty(self, event):
        print("I'm entering reriverfromguilty")
        text = "如果可以重來你還願意嗎"
        btn=[
            MessageTemplateAction(
                label = "我願意",
                text="我願意"
            ),
            MessageTemplateAction(
                label = "還是算了",
                text="還是算了"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
    
    def is_going_to_selfish(self, event):
        text = event.message.text
        return text == "還是算了"

    def on_enter_selfish(self, event):
        print("I'm entering selfish")
        text = "你是個自私的人，丟個游泳圈有那麼難嗎(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_reriver(self, event):
        text = event.message.text
        return text == "我不會恨他們"

    def on_enter_reriver(self, event):
        print("I'm entering reriver")
        text = "如果可以重來你還願意嗎"
        btn=[
            MessageTemplateAction(
                label = "我願意",
                text="我願意"
            ),
            MessageTemplateAction(
                label = "還是算了",
                text="還是算了"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
        
    def is_going_to_gameover(self, event):
        text = event.message.text
        return text == "還是算了"

    def on_enter_gameover(self, event):
        print("I'm entering gameover")
        text = "隨後慢慢沉入河裡(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_save(self, event):
        text = event.message.text
        return (text == "跳下去救他" or text == "當然救")

    def on_enter_save(self, event):
        print("I'm entering save")
        text = "將老爺爺救起來後，老爺爺決定給你一筆錢是否接受"
        btn=[
            MessageTemplateAction(
                label = "竟然你都這麼說了\n(默默伸手)",
                text="竟然你都這麼說了(默默伸手)"
            ),
            MessageTemplateAction(
                label = "我幫助你並不是為了錢",
                text="我幫助你並不是為了錢"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)

    def is_going_to_thousand(self, event):
        text = event.message.text
        return text == "竟然你都這麼說了(默默伸手)"

    def on_enter_thousand(self, event):
        print("I'm entering thousand")
        text = "結果老爺爺給你一千塊!!"
        btn=[
            MessageTemplateAction(
                label = "太少了，要再多一點",
                text="太少了，要再多一點"
            ),
            MessageTemplateAction(
                label = "收起來說謝謝",
                text="收起來說謝謝"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
    
    def is_going_to_greedy(self, event):
        text = event.message.text
        return text == "太少了，要再多一點"

    def on_enter_greedy(self, event):
        print("I'm entering greedy")
        text = "被老爺爺打，說你這個貪心的人(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()

    def is_going_to_notbad(self, event):
        text = event.message.text
        return text == "收起來說謝謝"

    def on_enter_notbad(self, event):
        print("I'm entering notbad")
        text = "恭喜你救了人也得到回報(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_compensate(self, event):
        text = event.message.text
        return text == "我幫助你並不是為了錢" or text == "是，我想脫魯"

    def on_enter_compensate(self, event):
        print("I'm entering compensate")
        text = "不然我給你其他補償?"
        btn=[
            MessageTemplateAction(
                label = "好啊",
                text="好啊"
            ),
            MessageTemplateAction(
                label = "沒關係不用",
                text="沒關係不用"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
        
    def is_going_to_recompensate(self, event):
        text = event.message.text
        return text == "沒關係不用"

    def on_enter_recompensate(self, event):
        print("I'm entering recompensate")
        text = "結果聽說她女兒貌美如花，是否想重新選擇?"
        btn=[
            MessageTemplateAction(
                label = "是，我想脫魯",
                text="是，我想脫魯"
            ),
            MessageTemplateAction(
                label = "否",
                text="否"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)

    def is_going_to_goodman(self, event):
        text = event.message.text
        return text == "否"

    def on_enter_goodman(self, event):
        print("I'm entering goodman")
        text = "你是個不求回報的大善人(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_daughter(self, event):
        text = event.message.text
        return text == "好啊"

    def on_enter_daughter(self, event):
        print("I'm entering daughter")
        text = "我決定將我貌美如花的女兒許配給你"
        btn=[
            MessageTemplateAction(
                label = "謝謝岳父大人",
                text="謝謝岳父大人"
            ),
            MessageTemplateAction(
                label = "我先看看你女兒",
                text="我先看看你女兒"
            ),
            MessageTemplateAction(
                label = "不用了，因為我是gay",
                text="不用了，因為我是gay"
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token, text, btn)
    
    def is_going_to_happy(self, event):
        text = event.message.text
        return text == "謝謝岳父大人"

    def on_enter_happy(self, event):
        print("I'm entering happy")
        text = "從此以後和老婆過著幸福快樂的生活(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()

    def is_going_to_ugly(self, event):
        text = event.message.text
        return text == "我先看看你女兒"

    def on_enter_ugly(self, event):
        print("I'm entering ugly")
        text = "結果發現他女兒真的是如花(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()
    
    def is_going_to_gay(self, event):
        text = event.message.text
        return text == "不用了，因為我是gay"

    def on_enter_gay(self, event):
        print("I'm entering ugly")
        text = "老爺爺以飛快的速度逃離現場(遊戲結束)"
        reply_token = event.reply_token
        send_text_message(reply_token, text)
        self.go_back()

    # def is_going_to_state3(self, event):
    #     text = event.message.text
    #     return text.lower() == "go to state3"

    # def on_enter_state3(self, event):
    #     print("I'm entering state3")

    #     reply_token = event.reply_token
    #     send_text_message(reply_token, "Trigger state3")
    #     self.go_back()

