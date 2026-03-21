import anthropic
import os
import json

api_key = os.getenv("CLAUDE_API_KEY")

client = anthropic.Anthropic(api_key=api_key)

#Use Claude to detect topic for analysis.py
def detect_topics(review):

    instructions = """
        You are an expert at deriving the main topics from a body of text.
        Your job is to extract topics from a google review of a Chinese restaurant.

        Allowed topics:
        - food_safety
        - cleanliness
        - food_quality
        - service
        - pricing
        - other

        Rules:
        - Return a JSON array of strings.
        - Include all topics clearly mentioned.
        - Do not include explanations.
        - Do not include any text outside the JSON.
    """

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=instructions,
        messages=[
            {"role": "user", "content": f"Review: {review}"}
        ]
    )

    topics = json.loads(message.content[0].text)
    return topics

#Use Claude to generate a response
def generate_response(analysis, reviewer_name):

    if analysis['risk']:
        risk_instructions = """
        Rules: 
        - NEVER admit fault
        - NEVER make promises
        - NEVER make up information not otherwise given

        Behavior:
        - Acknowledge their concerns
        - Encourage them to come in person to address the issue
        """
    else:
        risk_instructions = ""


    instructions = f"""
    You are an expert at drafting responses to google reviews of a Chinese restaurant.

    Rules:
    - Response should be at most 3 sentences.
    - Professional, polite, friendly tone.
    - Do not use emojis.
    - Do not invent details not otherwise mentioned in review.
    - Start every response with "Hi {reviewer_name}, " , NOTHING before this.
    - Be very general in your responses.
    
    Behavior:
    - If review is positive:
        - Thank the customer
        - Reference something they mentioned
        - Invite them back in a friendly, casual tone

    - If review is neutral:
        - Thank the customer
        - Apoligize briefly (once)
        - Encourage them to return in a friendly, casual tone

    - If review is negative:
        - Thank the customer for giving us a try
        - Apologize for the bad experience briefly
        - Acknowledge the issue briefly
        - Encourage them to return in a friendly, casual tone

    - {risk_instructions}
    """

    review_context = f"""
    Review: {analysis['review']}
    Sentiment: {analysis['sentiment']}
    Topics: {analysis['topic']}
    """

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=instructions,
        messages=[
            {"role": "user", "content": review_context}
        ]
    )

    final_response = response.content[0].text
    return final_response