from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Union, List
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    user_message: str
    system_prompt: str = Field(default="You are a helpful assistant.", example="You are a helpful assistant.")
    model: str = Field(default="gpt-3.5-turbo")
    frequency_penalty: Optional[float] = Field(default=0, ge=-2.0, le=2.0)
    logit_bias: Optional[Dict[int, float]] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = Field(default=0, ge=-2.0, le=2.0)
    response_format: Optional[Dict[str, str]] = None
    seed: Optional[int] = None
    stream: Optional[bool] = None
    temperature: Optional[float] = Field(default=1, ge=0, le=2)
    top_p: Optional[float] = Field(default=1, ge=0, le=1)


class TextChatRequest(BaseModel):
    user_text: str
    image_url: str
    model: str = Field(default="gpt-4-vision-preview")
    max_tokens: Optional[int] = None


async def async_chat_completions_create(**kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: client.chat.completions.create(**kwargs))

@app.post("/chat")
async def generate_chat_completion(request: ChatRequest):
    system_message = {"role": "system", "content": request.system_prompt}
    user_message = {"role": "user", "content": request.user_message}

    try:
        completion = await async_chat_completions_create(
            model=request.model,
            messages=[system_message, user_message],
            frequency_penalty=request.frequency_penalty,
            logit_bias=request.logit_bias,
            logprobs=request.logprobs,
            top_logprobs=request.top_logprobs,
            max_tokens=request.max_tokens,
            presence_penalty=request.presence_penalty,
            response_format=request.response_format,
            stream=request.stream,
            temperature=request.temperature,
            top_p=request.top_p,
        )
        
        completion_message = completion.choices[0].message
        
        return {
            "completion": {
                "content": completion_message.content,
                "role": completion_message.role,
                "function_call": getattr(completion_message, 'function_call', None),
                "tool_calls": getattr(completion_message, 'tool_calls', None)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/image_text_chat")
async def generate_image_text_chat_completion(request: TextChatRequest):
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": request.user_text},
            {"type": "image_url", "image_url": request.image_url}
        ]
    }]
    
    try:
        completion = await async_chat_completions_create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
        )
        
       
        completion_message = completion.choices[0].message 
        
        return {"completion": completion_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
