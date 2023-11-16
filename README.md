# Adaptive Code Editor (ACE)

ACE is an intelligent code editor that leverages the power of OpenAI's GPT-4 model to assist you in your coding tasks. It provides a user-friendly interface for writing, debugging, and generating code.

Setup

To set up ACE, follow these steps:

1. Ensure that Python is installed on your machine.
2. Clone the ACE repository to your local machine.
3. Install the required dependencies by running the following command in the root directory of the project:
   `pip install -r requirements.txt`
4. Set up the OpenAI API key by creating a `.env` file in the code_gen directory of the project and adding the following line:
   `OPENAI_API_KEY=<your_api_key>`

   Replace `<your_api_key>` with your actual OpenAI API key.
5. Start ACE by running the `code_editor.py` script:
   `python code_editor.py`

That's it! ACE is now set up and ready to use. Enjoy coding with the power of OpenAI's GPT-4 model!

### Features

#### Code Generation

ACE can generate new code based on your project goals and the language you're using. It uses OpenAI's GPT-4 model to understand your requirements and generate the appropriate code.

#### Code Improvement

ACE can provide advice on how to improve your existing code. It can analyze your code and suggest improvements to make it more efficient and readable.

#### Code Execution

ACE allows you to execute commands directly from the built-in terminal. You can run your code and see the output without leaving the editor.

#### Syntax Highlighting

ACE supports syntax highlighting for Python and HTML, making it easier to read and understand your code.

#### File Navigation

ACE provides a file navigation panel that allows you to easily navigate through your project's files and directories.

#### Git Integration

ACE can display the status of your Git repository, allowing you to keep track of your changes and commits.

### Usage

To start using ACE, run the code_editor.py script. This will open the ACE window where you can start coding. You can use the terminal at the bottom of the window to interact with the GPT-4 model. For example, you can type code: `<your requirements>` to generate new code, or gpt: `<your question>` to ask the model a question.

### Advanced Usage

ACE provides several advanced features for power users:

- Customizable Workspace: ACE allows you to customize your workspace according to your needs. You can choose between a basic, moderate, or advanced workspace, each providing a different set of features and tools.
- Streaming GPT Responses: ACE can stream responses from the GPT-4 model, allowing you to see the model's output as it's being generated.
- User Journeys: ACE supports user journeys, which are predefined sequences of interactions with the GPT-4 model. This allows you to automate common tasks and workflows.

### Contributing

Contributions to ACE are welcome. If you have a feature request, bug report, or proposal, please open an issue on the project's GitHub page. When submitting a pull request, please make sure your code follows the project's coding standards and include tests for any new features or bug fixes.

### License

ACE is open-source software licensed under the GPL-3.0 license. This means you are free to use, modify, and distribute the software, as long as you include the original copyright notice and disclaimers.
