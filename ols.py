from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from task_breakdown import task_breakdown
from task_processor import task_processor

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import uuid

## internal stuff
from model_context import get_watsonx_predictor

class LLMRequest(BaseModel):
    query: str

app = FastAPI()

def get_suid():
    return str(uuid.uuid4().hex)

@app.get("/healthz")
def read_root():
    return {"status": "1"}

@app.post("/ols")
def ols_request(llm_request: LLMRequest):
    # generate a unique UUID for the request:
    conversation = get_suid()

    logging.info(conversation + ' New conversation')

    # TODO: some kind of logging module that includes the conversation automatically?
    logging.info(conversation + ' Incoming request: ' + llm_request.query)


    #task_list, referenced_documents = task_breakdown(conversation, llm_request.query)

    task_list = ['1. Define the minimum and maximum cluster size using the ClusterAutoscaler object',
    '2. Define the MachineSet to be autoscaled and the minimum and maximum size using the MachineAutoscaler object']
    task_processor(conversation, task_list, llm_request.query)

    return task_list

@app.post("/base_llm_completion")
def base_llm_completion(llm_request: LLMRequest):
    conversation = get_suid()

    logging.info(conversation + ' New conversation')

    logging.info(conversation + ' Incoming request: ' + llm_request.query)
    bare_llm = get_watsonx_predictor(model="ibm/granite-13b-instruct-v1")

    response = bare_llm.complete(llm_request.query)

    logging.info(conversation + ' Model returned: ' + response.text)

    return {'request':llm_request.query, 'response':response}
