import json
import re
from openai import AzureOpenAI
from ai_recruiter import (
    extract_text_from_pdf,
    get_embedding,
    search_candidates,
    evaluate_candidate,
)

import os
from dotenv import load_dotenv
load_dotenv()

chat_client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_CHAT_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_key=os.getenv("AZURE_OPENAI_CHAT_KEY"),
    api_version="2024-12-01-preview",
)

# Tool Wrappers
def tool_extract_text_from_pdf(file_path):
    return {"text": extract_text_from_pdf(file_path)}

def tool_get_embedding(text):
    return {"embedding": get_embedding(text)}

def tool_search_candidates(job_description_text, k=5):
    candidates = search_candidates(job_description_text, k)
    return {"candidates": candidates}

def tool_evaluate_candidate(job_description, candidate_name, candidate_text):
    eval_result = evaluate_candidate(job_description, candidate_name, candidate_text)
    score = extract_match_score(eval_result)
    return {
        "evaluation": eval_result,
        "score": score,
        "name": candidate_name
    }

def extract_match_score(text):
    match = re.search(r"Match Score: (\d+)/10", text)
    return int(match.group(1)) if match else 0

# Autonomous Recruiter Agent
def run_autonomous_recruiter_agent(job_description):
    messages = [
        {"role": "system", "content": (
            "You are an autonomous AI recruiter. You can use tools to extract, embed, search, and evaluate candidates.\n"
            "Your task is to find and justify the best candidate(s) for a job description. Think step-by-step. "
            "Use the tools below. Stop when you're confident."
        )},
        {"role": "user", "content": job_description}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_text_from_pdf",
                "description": "Extracts text from a PDF file at a given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string"},
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_embedding",
                "description": "Generates an embedding from a text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                    },
                    "required": ["text"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_candidates",
                "description": "Search candidates using a job description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_description_text": {"type": "string"},
                        "k": {"type": "integer", "default": 5}
                    },
                    "required": ["job_description_text"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "evaluate_candidate",
                "description": "Evaluate a candidate against a job description.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_description": {"type": "string"},
                        "candidate_name": {"type": "string"},
                        "candidate_text": {"type": "string"},
                    },
                    "required": ["job_description", "candidate_name", "candidate_text"]
                }
            }
        }
    ]

    for _ in range(10):
        response = chat_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        msg = response.choices[0].message

        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_messages = []

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if name == "extract_text_from_pdf":
                    result = tool_extract_text_from_pdf(**args)
                elif name == "get_embedding":
                    result = tool_get_embedding(**args)
                elif name == "search_candidates":
                    result = tool_search_candidates(**args)
                elif name == "evaluate_candidate":
                    result = tool_evaluate_candidate(**args)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": json.dumps(result)
                })

            # Append both the tool_calls message and the tool responses
            messages.append(msg)
            messages.extend(tool_messages)

        else:
            return msg.content  # Final output

    return "Agent stopped after 10 steps without a conclusion."