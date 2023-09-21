import tempfile
import subprocess
import traceback
import sys
import os
from io import StringIO
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
import langchain.agents as lc_agents
from langchain.llms import OpenAI
import logging
from datetime import datetime
from langchain.llms import OpenAI as LangChainOpenAI
import openai

from pydantic import BaseModel

from PySide6.QtWidgets import QFileDialog

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

code_prompt = ""
code_language = ""
add_prompt = None


# LLM Chains definition
# Create an OpenAI LLM model
open_ai_llm = OpenAI(temperature=0.7, max_tokens=1000)


# Memory for the conversation
memory = ConversationBufferMemory(
    input_key='code_topic', memory_key='chat_history')
# Create a chain that generates the code

class code_gen():

    def generate_code(prompt, language):
        logger = logging.getLogger(__name__)
        try:
            global code_prompt
            global code_language
            global add_prompt

            code_prompt = prompt
            code_language = language
            # print("Chain", code_chain)
            # Prompt Templates
            code_template = PromptTemplate(input_variables=['code_topic'], template='Write me code in ' + f'{code_language} language' + ' for {code_topic}')
            code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)
            # print("Prompt", code_prompt)
            # print("Language", code_language)

            generatedCode = code_chain.run(code_prompt)
            # codeLanguage = code_language
            # print(generatedCode)
            return(generatedCode)

        except Exception as e:
            
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def add_code(prompt, add, language):
        logger = logging.getLogger(__name__)
        try:
            # print("Chain", code_chain)
            # Prompt Templates
            global code_prompt
            global code_language
            global add_prompt

            code_prompt = prompt
            code_language = language
            add_prompt = add


            print("Add Prompt ", add)
            code_template = PromptTemplate(input_variables=['add_prompt', 'code_language', 'code_prompt'], template=r'Take the existing code "{add_prompt}" written in {code_language} and add the following {code_prompt}')


            code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)
            # print("Prompt", code_prompt)
            # print("add Prompt", add_prompt)

            # print("Language", code_language)
            addCode = code_chain.run(code_prompt)

            if (addCode != "None"):
                return(addCode)
            else:
                return(add_prompt)

        except Exception as e:
            
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def what_code(prompt):
        logger = logging.getLogger(__name__)
        try:
            # print("Chain", code_chain)
            # Prompt Templates
            print("Add Prompt ", add_prompt)
            code_template = PromptTemplate(input_variables=['code_topic'], template= 'what does this code do {code_topic} and in what language is it written?')
            code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)
            # print("Prompt", code_prompt)
            # print("add Prompt", add_prompt)

            # print("Language", code_language)

            whatCode = code_chain.run(code_prompt)
            codeLanguage = code_language
            # print(generatedCode)
            return(whatCode)

        except Exception as e:
            
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def improve_code(prompt, advice):
        logger = logging.getLogger(__name__)
        try:
            print("Add Prompt ", add_prompt)
            code_template = PromptTemplate(input_variables=['code_topic'], template= ' give me advice on {code_topic} for this code'+ f' {add_prompt}' )
            code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)

            adviceCode = code_chain.run(code_prompt)
            # print(generatedCode)
            return(adviceCode)

        except Exception as e:
            
            logger.error(f"Error in code generation: {traceback.format_exc()}")
        

    def generate_code(project_goals, language, project_scope, skill_level):
        # Initialize the LangChain model
        open_ai_llm = OpenAI(temperature=0.7, max_tokens=1000)
        memory = ConversationBufferMemory(input_key='code_topic', memory_key='chat_history')

        # Create a prompt that describes the code you want to generate
        prompt = f"Create a {language} project with the following goals: {project_goals}. The project should have a scope of {project_scope} and be suitable for a skill level of {skill_level}."

        # Create a PromptTemplate and LLMChain
        code_template = PromptTemplate(input_variables=[], template=prompt)  # Remove 'code_topic' from input_variables
        code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)

        # Generate the code
        generated_code = code_chain.run(prompt)

        # Ask the user for a directory to save the generated code
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")

        # Save the generated code to a file in the selected directory
        file_path = f"{folder_path}/generated_code.txt"
        with open(file_path, 'w') as file:
            file.write(generated_code)

        return file_path