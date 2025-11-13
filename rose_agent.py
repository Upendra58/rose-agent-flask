import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

#Initialize the Gemini Client
# it automatically looks for gemini api key environment vaiable

# try:
#     client=genai.Client()
#     print("Rose brain is initialized")

#     #sample test to confirm connection
#     response = client.models.generate_content(
#         model='gemini-2.5-flash',
#         contents='Return the word "READY" in all caps.'

#     )
#     print(f"Connnection test reult: {response.text.strip()}")

# except Exception as e:
#     print(f"Initialization failed. check your API Key or network: {e}")

# rose_agent.py (Add this to the very bottom)


#----Pydantic Schema for Roadmap Precision (DSA/ML conenction)---
class SubTask(BaseModel):
    """Defines a single, concise, actionable step in the Roadmap."""
    action: str=Field(description="The concise, actionable step.")

class  CoreConcept(BaseModel):
    """Defines a main section of the roadmap (Level 1 in the outline)."""
    core_concept: str = Field(description="The main topic or core concept.")
    time_estimate: str = Field(description="Estimated time in hours or days (e.g., '4 hours', '2 days').")
    sub_tasks: list[SubTask]

class RoadmapOutput(BaseModel):
    """The final, validated structure for the entire roadmap."""
    topic_name: str = Field(description="A concise, professional title for the study plan.")
    roadmap_structure: list[CoreConcept]

#---Tool 1: roadmap planner-----
def create_roadmap(topic:str)-> RoadmapOutput:
    """
    TOOL KEYWORDS: Roadmap, structure, plan

    Generates a structured, multi-level learning or project roadmap based on the user's provided topic. 
    The output MUST strictly adhere to the defined Pydantic RoadmapOutput schema.

    Input:
        topic (str): The specific subject or goal the user wants a plan for (e.g., 'Introduction to Neural Networks').
    
    Returns:
        RoadmapOutput: A Pydantic object representing the structured learning plan.
    """
    # In a real application, this function would call the LLM to generate the content.
    # We leave the body empty for now as the orchestrator handles the LLM call.
    pass

def write_blog(topic: str, roadmap_json: RoadmapOutput) -> str:
    """
    TOOL KEYWORDS: write, article, post

    Generates a professional long-form blog post based on the provided topic and structured outline.
    The output MUST adhere to the Concise persona constraints.

    Input:
        topic (str): The original subject of the content.
        roadmap_json (RoadmapOutput): The structured outline from the create_roadmap tool.

    Output Constraints:
        The Introduction and the Conclusion MUST be a maximum of **three sentences each**. 
    """
    pass


# --- Tool 3: Image Generator Tool ---
def generate_image_prompt(topic: str) -> str:
    """
    TOOL KEYWORDS: image, photo, art

    Generates a professional, highly detailed image generation prompt based on the provided topic.
    The output MUST adhere to the Precision-Focused visual constraints.

    Input:
        topic (str): The original subject for the image.

    Output Constraints:
        The prompt MUST include a **Style**, a **Composition/Shot Type**, and an **Emotional Descriptor** for visual precision.
    """
    pass

def retrieve_past_work(query: str, top_k: int = 3) -> list[str]:
    """
    TOOL KEYWORDS: history, context, remember

    Performs a semantic search against Rose's long-term memory archive.
    Used to retrieve past work that is relevant to the current query.

    Input:
        query (str): The specific question or topic being asked by the user.
        top_k (int): The number of most relevant documents to retrieve.

    Returns:
        list[str]: A list of past documents to inform the current response.
    """
    pass

# rose_agent_orchestrator continued...

# rose_agent.py (REPLACE YOUR EXISTING run_rose_agent FUNCTION)

def run_rose_agent(user_prompt: str):
    """Executes the sequential agent logic for Rose based on keyword intent."""
    client = genai.Client()
    final_output = {}

    # Check 1: Intent Classification (Roadmap)
    if any(keyword in user_prompt.lower() for keyword in ["roadmap", "structure", "plan"]):
        print("\n[ROSE]: Intent confirmed. Generating Roadmap structure...")
        
        # --- 1. Execute Roadmap Generation (Forced Generation with Pydantic Schema Prompt) ---
        # We prompt the model to generate the content *directly* in the structured format.
        roadmap_output_text = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are the Professional Content Agent. Using the **RoadmapOutput Pydantic schema structure**, generate a detailed study roadmap for the topic: '{user_prompt}' Ensure the content is professional and detailed.",
        ).text
        final_output['Roadmap'] = roadmap_output_text

        # --- Sequential Check 2: Blog ---
        if any(keyword in user_prompt.lower() for keyword in ["write", "article", "post"]):
            print("[ROSE]: Generating Blog content...")
            
            # Pass the generated roadmap text as context for the blog post
            blog_post_text = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"You are the Professional Content Agent. Using this roadmap structure: '{roadmap_output_text}', write a professional blog post. Remember the 3-sentence intro/conclusion rule. Topic: '{user_prompt}'",
            ).text
            final_output['Blog'] = blog_post_text

            # --- Sequential Check 3: Image ---
            if any(keyword in user_prompt.lower() for keyword in ["image", "photo", "art"]):
                print("[ROSE]: Generating Image Prompt...")
                image_prompt_text = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"You are the Professional Content Agent. Generate a professional,**RETURN ONLY THE IMAGE POST.** highly detailed image prompt for the topic: '{user_prompt}'. It MUST include Style, Composition, and Emotional Descriptor.",
                ).text
                final_output['Image Prompt'] = image_prompt_text
        
    return final_output


# Rerun the previous command with your correct, new API key!


# Final Implementation is complete!
if __name__ == "__main__":
    import sys

    print("Welcome to Rose Agent Chat! Type your prompt below (type 'exit' to quit).")

    client = genai.Client()  # Make sure API key/environment is configured

    while True:
        user_prompt = input("\nYou: ")
        if user_prompt.lower().strip() in ("exit", "quit"):
            print("Goodbye! 👋")
            break

        try:
            results = run_rose_agent(user_prompt)
            print("\nRose Agent:")
            if results:
                for key, value in results.items():
                    print(f"\n[{key}]")
                    print(f"{value[:1000]}")  # Print more chars if you wish
            else:
                print("No output generated or error occurred.")
        except Exception as e:
            print(f"Error: {e}")
