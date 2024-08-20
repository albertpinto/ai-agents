import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
from litellm import completion
import uvicorn

class Agent:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        # Set environment variable for OpenAI API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

    def get_response(self, prompt: str) -> str:
        try:
            # Call the LLM to get a completion
            response = completion(
                model=self.model,
                messages=[{"content": prompt, "role": "user"}]
            )
            # Extract the generated text
            result = response.choices[0].message.content
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling LiteLLM API: {str(e)}")

# Initialize the FastAPI app
app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an instance of the Agent class
agent = Agent()

@app.get("/prompt/{prompt}")
def get_prompt(prompt: str):
    """
    Get a prompt response from the OpenAI agent.
    """
    print(f"Received prompt: {prompt}")
    
    try:
        response = agent.get_response(prompt)
        print(f"Response: {response}")
        return {"prompt": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)

