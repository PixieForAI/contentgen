import json
from google import genai
from django.conf import settings
import logging

# Set up a logger for this module
logger = logging.getLogger(__name__)

def generate_campaign_content(input_content: str, org_context: str, campaign_context: str) -> dict | None:
    """
    Invokes the Gemini API to generate content for all platforms based on an input brief.

    Args:
        input_content: The user-provided content or idea.
        org_context:
        campaign_context:

    Returns:
        A dictionary containing the generated content for all fields,
        or None if an error occurs.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        logger.error("GEMINI_API_KEY is not configured in settings.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        # model_name="gemini-2.0-flash-lite"
        model_name = "gemini-2.5-flash"
        fields = {
            "linkedin_content": {"description": "Professional content for LinkedIn, business-focused and engaging for a professional audience, including relevant hashtags. Length should be 1 to 1.5 times the input content", "type": "string"},
            "x_content": {"description": "Short, punchy content for X (formerly Twitter), under 280 characters, using emojis and relevant hashtags.", "type": "string"},
            "facebook_content": {"description": "Engaging and community-focused content for Facebook, suitable for discussion, including emojis and relevant hashtags.", "type": "string"},
            "instagram_content": {"description": "Visually-driven caption for an Instagram post, including relevant hashtags and emojis.", "type": "string"},
            "youtube_content": {"description": "A detailed description for a YouTube video"},
            "quora_content": {"description": "An answer-style post for Quora, providing value and expertise on the topic. Length should be 1 to 1.5 times the input content", "type": "string"},
            "reddit_content": {"description": "A post suitable for a relevant subreddit, written in a conversational and authentic tone. Length should be 1 to 1.5 times the input content", "type": "string"},
            "blog_content": {"description": "A short-form blog post (2-3 paragraphs) that expands on the input content. Length should be 2 to 3 times the input content", "type": "string"},
            "image_prompt": {"description": "A descriptive prompt for an AI image generator to create a relevant visual.", "type": "string"},
            "video_prompt": {"description": "A descriptive prompt for an AI video generator to create a short-form video.", "type": "string"},
        }

        prompt = f"""
        You are a world-class marketing and content creation expert.
        Your task is to understand the organization and campaign contexts and generate a cohesive set of social media 
        and blog content.
        Use the input content and generate other social media content as specified in the JSON output structure below.
        Provide the output as a single, valid JSON object. 

        ORG_CONTEXT:
        ------------
        {org_context}

        CAMPAIGN_CONTEXT:
        -----------------
        {campaign_context}

        INPUT_CONTENT: 
        {input_content}

        JSON_OUTPUT_STRUCTURE:
        {{
            "linkedin_content": "{json.dumps(fields['linkedin_content'])}",
            "x_content": "{json.dumps(fields['x_content'])}",
            "facebook_content": "{json.dumps(fields['facebook_content'])}",
            "instagram_content": "{json.dumps(fields['instagram_content'])}",
            "youtube_content": "{json.dumps(fields['youtube_content'])}",
            "quora_content": "{json.dumps(fields['quora_content'])}",
            "reddit_content": "{json.dumps(fields['reddit_content'])}",
            "blog_content": "{json.dumps(fields['blog_content'])}",
            "image_prompt": "{json.dumps(fields['image_prompt'])}",
            "video_prompt": "{json.dumps(fields['video_prompt'])}",
        }}

        Ensure the output is ONLY the JSON object.
        Do not include any explanatory text, comments, or markdown formatting (like ```json) before or after the JSON object.


        """

        #response = model.generate_content(prompt)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        logger.error(f"Response: {response.text[7:-3]}")

        return json.loads(response.text[7:-3])

    except Exception as e:
        logger.error(f"An error occurred while calling the Gemini API: {e}")
        return None