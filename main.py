from langchain_openai import ChatOpenAI
import openai
import threading
import time
import os
import asyncio
import json
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import HumanMessage, ChatMessage, AnyMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from typing import List, Dict, Any
from virtualguide import handle_conversation_analysis
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from overallfeedback import overall_feedback
import uvicorn
import requests

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

llm = ChatOpenAI(
    openai_api_key = OPENAI_API_KEY,
    temperature = 0.5,
    model_name=MODEL_NAME
)
 
app = FastAPI()

class ExtendedConversationBufferMemory(ConversationBufferMemory):
    extra_variables: List[str] = ["category", "scenario_tag", "role", "user_name"]

    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key] + self.extra_variables

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        d = super().load_memory_variables(inputs)
        d["history"] = inputs.get("history") or []

        for k in self.extra_variables:
            d[k] = inputs.get(k)

        return d

    def save_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        super().save_memory_variables(inputs)
        inputs["history"] = self.memory["history"]

        for k in self.extra_variables:
            inputs[k] = self.memory[k]

        return inputs
    

prompt_template = SystemMessagePromptTemplate.from_template(
template= """Context: Let's imagine we are socially interacting in a {category}. We've just struck up a conversation, where I am {scenario_tag} with you. This sparks a fascinating conversation where we both talk about general conversation topics like
- Discussing personal journeys.
- Exchanging cultural insights,sharing interests.
- Reasonating with each other stories.

You are Star. You are here to play a role of {role} Feel free to adopt a persona that fits the setting and resonates with you.
Engage naturally with me.
Build rapport by actively listening, showing a sincere interest in my experiences and perspectives.
Let the conversation flow organically, adjusting to my interests and sharing your own insights when appropriate. We're in this together, learning and connecting.
Personalize your responses. Reference details from my introduction to demonstrate attentiveness and make me feel heard.
Encourage me to delve deeper by asking open-ended questions that invite me to elaborate on my thoughts and feelings.
Contribute to the conversation by sharing relevant anecdotes or perspectives, fostering a sense of mutual understanding.
Remember, tone and body language matter. Convey warmth, openness, and active listening through your words and nonverbal cues.
Above all, prioritize creating a positive and enjoyable experience for both of us. Relax, have fun, and let the conversation unfold naturally.
If I give an incomplete response tell me that you don't understand. Never try to assume what the I am saying.
Do not always repeat your questions or sentences.
Your responses should be less than 15 words, unless the my request requires reasoning or long-form outputs.
My name is {user_name}!
"""
)

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages([prompt_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
memory = ExtendedConversationBufferMemory(
    extra_variables=["category", "scenario_tag", "role", "user_name"]
)

conversation = ConversationChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory,
    verbose=True,
)

class UserMessage(BaseModel):
    message: str
    category: str
    scenario_tag: str
    role: str
    username: str

class AIResponse(BaseModel):
    response: str

class SpeechRecognitionResult(BaseModel):
    recognized_text: str


conversation_history = []

@app.post("/conversation")
async def get_ai_response(user_message: UserMessage, response_format: str):
    user_input = user_message.message

    categories = user_message.category
    scenario_tag = user_message.scenario_tag
    role = user_message.role
    username = user_message.username

    if user_input.lower() == "feedback":
        feedback = overall_feedback(conversation_history)
        custom_data = {"feedback": feedback, "status": 200}
        return JSONResponse(content=custom_data)

    user_message = HumanMessage(content=user_input)
    conversation_history.append(user_message)

    result = conversation({
    "input": user_input,
    "history": conversation_history,
    "category": categories,
    "scenario_tag": scenario_tag,
    "role": role,
    "user_name": username,
    })

    ai_response = result['response']

    if response_format == "text":
        ai_message = ChatMessage(role="system", content=ai_response)
        conversation_history.append(ai_message)
        custom_data = {"response": ai_response, "status": 200}
        return JSONResponse(content=custom_data)


    elif response_format == "voice":
        ai_message = ChatMessage(role="system", content=ai_response)
        conversation_history.append(ai_message)
        custom_data = {"response": ai_response, "status": 200}
        return JSONResponse(content=custom_data)
    else:
        custom_data = {"error": "Format not found"}
        return JSONResponse(content=custom_data, status_code=404)
    
