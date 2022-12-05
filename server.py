
from playwright.sync_api import sync_playwright
import time
import os
import flask
from flask_cors import CORS
APP = flask.Flask(__name__)
CORS(APP)


PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch_persistent_context(
    user_data_dir="/tmp/playwright",
    headless=False,
)
PAGE = BROWSER.new_page()


def get_input_box():
    """Get the child textarea of `PromptTextarea__TextareaWrapper`"""
    return PAGE.query_selector("textarea")


def is_logged_in():
    return get_input_box() is not None


def send_message(message):
    box = get_input_box()
    box.click()
    box.fill(message)
    box.press("Enter")


def get_last_message():
    """Get the latest message"""
    page_elements = PAGE.query_selector_all(
        "div[class*='ConversationItem__Message']")
    last_element = page_elements[-1]
    return last_element.inner_text()


@APP.route("/chat", methods=["GET"])
def chat():
    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    time.sleep(10)
    for i in range(10):
        response = get_last_message()
        print(len(response))
        if len(response) > 1:  # you would be thinking why i didn't use if response. idk why but len of empty response is always 1 LMAO -_-
            break
        time.sleep(8)

    response = get_last_message()
    return response


def start_browser():
    PAGE.goto("https://chat.openai.com/")
    if not is_logged_in():
        print("Please log in to OpenAI Chat")
        print("Press enter when you're done")
        input()
    else:
        print("Logged in")
        APP.run(port=5001, threaded=False)


if __name__ == "__main__":
    start_browser()
