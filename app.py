from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models import *
import re
import time
import psycopg2
import os
import random, string

app = Flask(__name__)

line_bot_api = LineBotApi('TF2ePPHGZTmQqyl54Z3VuXJmSiBX14Ve30bZN0fW+2P18EzZfqzRl17OD4rze7T6bQL5I0d4ZnfT5x7tQhc9KrzcoOO5nDcUx0pWVOTIWVTW3zahPsu/6gKfmBvsMnkIxaYJyNDa7pn/RlU6VMLfeQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('76f179b94445ec17830a92626c4ef3af')

def db():
    connection = psycopg2.connect(user="hjvxjowozpvmdd",
                                        password="4875bff3a2a56be7716c9878e0b726c502751eb6dff873062360ea1763f376a1",
                                        host="ec2-107-22-241-205.compute-1.amazonaws.com",
                                        port="5432",
                                        database="dd4bln8ufum5ac")
    cursor = connection.cursor()
    return cursor
cursor = db()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#建立rechmenu
@app.route("/richmenu", methods=["GET"])
def rich_menu():
    #creat rich menu
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=1200, height=405),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=URIAction(label='Go to line.me', uri='https://line.me'))]   
    )          
        #action=URIAction(label='Go to line.me', uri='https://line.me'))]   
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(rich_menu_id)

    #set_rich_menu_image
    content_type = "image/jpeg"
    with open('72890300_520706825417159_8288948115734528000_n.jpg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)

    # 
    #line_bot_api.set_default_rich_menu(rich_menu_id)
    
    #get_default_rich_menu
    # line_bot_api.get_default_rich_menu()
    return 'OK', 200

#刪除richmenu
@app.route("/richmenu/<id123>", methods=["POST"])
def drich_menu(id123):
    rich_menu_id = id123
    #delete rich menu
    line_bot_api.delete_rich_menu(rich_menu_id)
 
    return 'OK', 200
#時刻表
def buttons_message11():
    message = TemplateSendMessage(
        alt_text='查詢時刻表',
        template=ButtonsTemplate(
            title="查詢時刻表",
            text="請問要查詢哪一個",
            actions=[
                MessageTemplateAction(
                    label="營業日期",
                    text="查詢營業日期"
                ),
                MessageTemplateAction(
                    label="班次",
                    text="查詢班次"
                )
            ]
        )
    )
    return message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id  
    if 'essaim880913' in msg:
        rich_menu_id = 'richmenu-2cee31ae90f88cb370e04f9efe1ce952'
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
    if '574983261' in msg:
        rich_menu_id = 'richmenu-ed75132381729538800fc4ee274be208'
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        print(rich_menu.rich_menu_id)
    if '查詢時刻表' == msg:
        message = buttons_message11()
        line_bot_api.reply_message(event.reply_token, message)
    if '查詢營業日期' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://imgur.com/HVn3HTo.jpg',
        preview_image_url='https://imgur.com/Osi6gUd.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    if '查詢班次' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://imgur.com/fUlpm2P.jpg',
        preview_image_url='https://imgur.com/MCWyo68.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    if '聯絡資訊' == msg:
        ddd = TextSendMessage(text='Fb：XXXXXX\nGmail：XXXXXX@gmail.com\n電話：02—XXXX XXXX')
        line_bot_api.reply_message(event.reply_token, ddd)
    if '註冊' in msg:
        msg = re.sub('註冊：','',msg) #註冊：王小明 男 都經三 abc@gmail.com 09xxxxxxxx
        msg = msg.split()
        name = msg[0]
        sex = msg[1]
        level = msg[2]
        gmail = msg[3]
        phone = msg[4]
        poolOfChars  = string.ascii_letters + string.digits
        random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])
        code = random_codes(poolOfChars, 6)
        try:
            cursor.execute(f'INSERT INTO "public"."info" ("uid","name","gmail","department_level","invitation_code","invitation","phone")'+f"VALUES ('{user_id}','{name}','{gmail},'{level}','{code}','1',{phone},{sex});")
            cursor.execute("COMMIT")
        except:
            # print('fail')
            cursor.execute("ROLLBACK")
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)