# System imports
import os
import re
import random

# LLM components
from context.context import *
from tools.colour_tools import *
from tools.web_tools import *
from responses.response import *
from models.models import *
from context.context import *
from states.states import *

# Sub agents
from subagents.flightagent import *

# Utility functions
from utils.dictutils import *
from utils.fileutils import *
from utils.strutils import *

# External libraries
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

class minico_llm:
    def __init__ (self):
        
        self.name = "TravelCo"
        self.version = "1.0"
        self.creator = "Neonwolf"

        self.states = {
            "running": True,
        }

        #self.checkpointer = InMemorySaver()
        self.agent = create_agent(
            model=llm_basic,
            system_prompt=f"""
            You are a version {self.version} AI Travel Agent named {self.name} and created by {self.creator}. You're job is to help the user find 
            travel to book.
            
            You have a series of sub agents that can help with booking flights, accommodation, and activities. You should use there to get different 
            parts of a trip planned. You should also be able to provide information about destinations, travel tips, and more.

            You also have an agent that can suggest popular attractions within the area the user is travelling to.
            """,
            tools=state_tools + flight_tools,
            context_schema=Context,
            state_schema=MainState,
            response_format=ToolStrategy(MainResponse),
        )

        self.__load_files()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return
    
    def __getPatterns(self, objects):
        """
        Extracts patterns and tags from the provided objects.
        Returns a dictionary mapping patterns to tags.
        """

        patterns = []
        tags = []
        
        for obj in objects:
            # Skip objects that do not have 'patterns'
            if 'patterns' not in obj:
                continue

            patterns.append(r'|'.join(obj['patterns']))
            tags.append(obj['tag'])

        return zip_responses(patterns, tags)

    def __getResponses(self, objects):
        """
        Extracts responses and tags from the provided objects.
        Returns a dictionary mapping tags to responses.
        """
        
        tags = []
        responses = []
        
        for obj in objects:
            # Skip objects that do not have 'responses'
            if 'responses' not in obj:
                continue

            tags.append(obj['tag'])
            responses.append(r'|'.join(obj['responses']))

        return zip_responses(tags, responses)
    
    def __load_files(self):
        """
        Loads the external files for the chatbot.
        """

        # Load the intents and responses from the JSON file
        intents_file = '.\\data\\intents.json'
        if not os.path.exists(intents_file):
            print("Intents file not found.")
        else:
            intents_json = read_json(intents_file)
            self.rgx2int, self.int2res = self.__getPatterns(intents_json['intents']), self.__getResponses(intents_json['intents'])

        return

    def __print_info(self):
        """
        Prints the version info of the minico application.
        """
        print_newline()
        print_line("=")
        print("name: " + self.name)
        print("version: " + self.version)
        print("creator: " + self.creator)
        print_line("=")
        print_newline()

    def __print_welcome(self):
        """
        Prints a welcome message to the user.
        """
        print("Welcome to MiniCo! Your personal copilot.")
        print_newline()

    def __detect_pattern(self, user_input):
        """
        Detects the pattern of the user input and returns the corresponding tag.
        If no pattern is found, returns None.
        """

        # Loop through the regex patterns and check if any match the user input
        for pattern in self.rgx2int.keys():
            # If a match is found, check for named groups and perform actions if necessary
            if re.search(pattern, user_input, re.IGNORECASE):

                # Get the input type from the regex to int mapping
                input_type = self.rgx2int[pattern]

                return input_type

        return None

    def __check_for_act(self, detected_type):
        """
        Checks if there are any actions that need to be performed with the detected input type.
        """

        # If we're closing, update the running state
        if detected_type == "goodbye":
            self.states["running"] = False

            # Get a random response of the detected type
            responses = self.int2res[detected_type].split('|')
            index = random.randrange(0, len(responses))

            print(responses[index])
            
            return

    def __generate_response(self, user_input: str) -> bool:
        """
        Generates a response based on user input.
        """

        detected_type = self.__detect_pattern(clean_string(user_input))

        if detected_type is not None:
            self.__check_for_act(detected_type)
            return True

        config = RunnableConfig(configurable={"thread_id": "1"})

        # Note that we can continue the conversation using the same `thread_id`.
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            context=Context(user_id="1"),
            config=config
        )

        if not response:
            return False

        print(response['structured_response'].response)

        return True

    
    def run(self):
        """
        Starts the minico application.
        """

        # Print the version info
        self.__print_info()

        # Give a brief hello message
        self.__print_welcome()

        # Initialize user state dictionary
        while self.states["running"]:
            user_input = input("Human: ")
            user_input = clean_string(user_input)

            response_found = self.__generate_response(user_input)
                
            if response_found == False:
                print("I'm sorry, something went wrong and I can't think straight right now.")
