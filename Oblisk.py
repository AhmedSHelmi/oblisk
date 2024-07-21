import logging
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.commands = {
            'navigate to': self.navigate_to,
            'click element where': self.click_element,
            'input into element where': self.input_text,
            'wait for element where': self.wait_for_element,
            'extract text from element where': self.extract_text,
            'press enter in element where': self.press_enter_key,
            'press tab in element where': self.press_tab_key
        }

    def log_command(self, command, args):
        logging.info(f"Executing command: {command} with arguments: {args}")

    def navigate_to(self, args):
        self.log_command('navigate_to', args)
        url = args[0]
        self.driver.get(url)
        logging.info(f"Navigated to {url}")

    def click_element(self, args):
        self.log_command('click_element', args)
        selector_type, value = args
        element = self.find_element(selector_type, value)
        element.click()
        logging.info(f"Clicked element with {selector_type}='{value}'")

    def input_text(self, args):
        self.log_command('input_text', args)
        text, selector_type, value = args
        element = self.find_element(selector_type, value)
        element.send_keys(text)
        logging.info(f"Inputted text '{text}' into element with {selector_type}='{value}'")

    def press_key(self, selector_type, value, key):
        self.log_command(f'press_key: {key}', [selector_type, value])
        element = self.find_element(selector_type, value)
        element.send_keys(key)
        logging.info(f"Pressed key '{key}' in element with {selector_type}='{value}'")

    def press_enter_key(self, args):
        self.press_key(args[0], args[1], Keys.ENTER)

    def press_tab_key(self, args):
        self.press_key(args[0], args[1], Keys.TAB)

    def wait_for_element(self, args):
        self.log_command('wait_for_element', args)
        selector_type, value, timeout = args
        end_time = time.time() + int(timeout)
        while time.time() < end_time:
            try:
                if self.find_element(selector_type, value):
                    logging.info(f"Element with {selector_type}='{value}' found")
                    return True
            except:
                pass
            time.sleep(1)
        logging.error(f"Timeout waiting for element with {selector_type}='{value}'")
        raise Exception(f"Timeout waiting for element {value}")

    def extract_text(self, args):
        self.log_command('extract_text', args)
        selector_type, value = args
        element = self.find_element(selector_type, value)
        text = element.text
        logging.info(f"Extracted text '{text}' from element with {selector_type}='{value}'")
        return text

    def find_element(self, selector_type, value):
        if selector_type == 'id':
            return self.driver.find_element(By.ID, value)
        elif selector_type == 'class':
            return self.driver.find_element(By.CLASS_NAME, value)
        elif selector_type == 'name':
            return self.driver.find_element(By.NAME, value)
        else:
            raise ValueError(f"Unsupported selector type: {selector_type}")

    def parse_command(self, command):
        command = command.strip().lower()
        for key in self.commands:
            if command.startswith(key):
                args = re.findall(r'\'(.*?)\'', command[len(key):])
                self.commands[key](args)
                return
        raise ValueError(f"Unsupported command: {command}")

    def parse_script(self, script):
        # Split commands by new line or semicolon
        commands = re.split(r'[;\n]', script.strip())
        for command in commands:
            if command.strip():  # Ensure the command is not empty
                self.parse_command(command)

    def run_from_file(self, file_path):
        if not file_path.endswith('.obl'):
            raise ValueError("File must have a .obl extension")
        with open(file_path, 'r') as file:
            script = file.read()
        self.parse_script(script)

    def run_from_command_line(self, command_line_script):
        self.parse_script(command_line_script)

    def run_from_url(self, url):
        response = requests.get(url)
        script = response.text
        self.parse_script(script)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    web_automation = WebAutomation(driver)

    if len(sys.argv) > 1:
        input_type = sys.argv[1]
        if input_type == '--file':
            file_path = sys.argv[2]
            web_automation.run_from_file(file_path)
        elif input_type == '--cmd':
            command_line_script = sys.argv[2]
            web_automation.run_from_command_line(command_line_script)
        elif input_type == '--url':
            url = sys.argv[2]
            web_automation.run_from_url(url)
        else:
            print("Invalid input type. Use --file, --cmd, or --url.")
    else:
        print("No input provided. Use --file, --cmd, or --url.")

    driver.quit()
