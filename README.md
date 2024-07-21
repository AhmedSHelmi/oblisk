# Oblisk

Oblisk is a simple web automation script runner based on Selenium WebDriver. It allows you to automate browser actions using a custom scripting language with commands similar to SQL. You can input commands through an external `.obl` file, via the command line, or from a URL.

## Out of the box Features

- Navigate to URLs
- Click elements
- Input text into elements
- Wait for elements
- Extract text from elements
- Press Enter or Tab keys in elements

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (make sure the ChromeDriver version matches your Chrome browser version)

## Installation

1. Clone the repository or download the `Oblisk.py` file.
2. Install the required Python packages using pip:

   ```sh
   pip install selenium requests
   ```

3. Make sure `chromedriver` is in your PATH or place it in the same directory as `Oblisk.py`.

## Usage

You can use Oblisk in three different ways:

### 1. From an External File

Create a `.obl` file with your commands. Here is an example `script.obl` file:

```obl
NAVIGATE TO 'https://example.com/login'
INPUT 'testuser' INTO element WHERE id='username'
INPUT 'password123' INTO element WHERE id='password'
CLICK element WHERE id='submit'
WAIT FOR element WHERE id='welcome-message' TIMEOUT 10 SECONDS
EXTRACT text FROM element WHERE id='welcome-message' INTO welcome_text
PRESS ENTER IN element WHERE id='username'
PRESS TAB IN element WHERE id='username'
```

Run the script using the following command:

```sh
python Oblisk.py --file path/to/script.obl
```

### 2. From Command Line

Pass the commands as a single string, separated by semicolons or new lines:

```sh
python Oblisk.py --cmd "NAVIGATE TO 'https://example.com/login'; INPUT 'testuser' INTO element WHERE id='username'; INPUT 'password123' INTO element WHERE id='password'; CLICK element WHERE id='submit'"
```

### 3. From a URL

Provide a URL that contains the commands in plain text:

```sh
python Oblisk.py --url "https://example.com/commands.txt"
```

## Command Reference

- `NAVIGATE TO '<url>'`: Navigates to the specified URL.
- `CLICK element WHERE <selector_type>='<value>'`: Clicks the element identified by the selector.
- `INPUT '<text>' INTO element WHERE <selector_type>='<value>'`: Inputs the specified text into the element.
- `WAIT FOR element WHERE <selector_type>='<value>' TIMEOUT <seconds>`: Waits for the element to appear within the specified timeout.
- `EXTRACT text FROM element WHERE <selector_type>='<value>' INTO <variable_name>`: Extracts text from the element and stores it in the specified variable.
- `PRESS ENTER IN element WHERE <selector_type>='<value>'`: Presses the Enter key in the specified element.
- `PRESS TAB IN element WHERE <selector_type>='<value>'`: Presses the Tab key in the specified element.

## Adding New Commands

To add a new command, follow these steps:

1. **Define the Command Method**: Create a new method in the `WebAutomation` class to handle the new command. The method should accept a list of arguments.

   ```python
   def new_command(self, args):
       # Your implementation here
       pass
   ```

2. **Log the Command**: Add logging to the new command method.

   ```python
   def new_command(self, args):
       self.log_command('new_command', args)
       # Your implementation here
       pass
   ```

3. **Update the Commands Dictionary**: Add the new command to the `commands` dictionary in the `__init__` method of the `WebAutomation` class.

   ```python
   self.commands = {
       'navigate to': self.navigate_to,
       'click element where': self.click_element,
       'input into element where': self.input_text,
       'wait for element where': self.wait_for_element,
       'extract text from element where': self.extract_text,
       'press enter in element where': self.press_enter_key,
       'press tab in element where': self.press_tab_key,
       'new command': self.new_command  # Add your new command here
   }
   ```

4. **Parse the Command**: Ensure that the `parse_command` method can recognize and execute the new command.

   ```python
   def parse_command(self, command):
       command = command.strip().lower()
       for key in self.commands:
           if command.startswith(key):
               args = re.findall(r'\'(.*?)\'', command[len(key):])
               self.commands[key](args)
               return
       raise ValueError(f"Unsupported command: {command}")
   ```

### Example

Here is an example usage:

```sh
python Oblisk.py --file example.obl
```

Where `example.obl` contains:

```obl
NAVIGATE TO 'https://example.com/login'
INPUT 'user' INTO element WHERE id='username'
INPUT 'pass' INTO element WHERE id='password'
CLICK element WHERE id='submit'
WAIT FOR element WHERE id='dashboard' TIMEOUT 10 SECONDS
EXTRACT text FROM element WHERE id='welcome-message' INTO welcome_text
```

## License

This project is licensed under the MIT License.