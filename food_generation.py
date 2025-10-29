#generates food combinations
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

def processData(location):
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)


    prompt = (
    "You are a creative dining assistant for Rutgers University dining halls. Your task is to generate appealing meal combinations from available menu items."
    "AVAILABLE MENU ITEMS:"
    + menu_items +
    "DIETARY PREFERENCES:" + preferences +
    "Generate 8 diverse meal combinations using ONLY the items listed above. Follow these guidelines:"
    "1. **Balanced Combo**: A nutritionally balanced plate with protein, carbs, and vegetables"
    "2. **High Protein Focus**: Maximize protein content while keeping it tasty"
    "3. **Comfort Food**: A satisfying, indulgent combination"
    "4. **Light & Fresh**: A lighter option that's still filling"
    "5. **Creative Fusion**: An unexpected but delicious pairing"

    "For each combination:"
    "- Use 3-5 items from the menu"
    "- Give it a catchy name (e.g., Power Athlete Bowl, Midnight Study Session Plate)"
    "- Consider taste, texture, and variety"
    + dietary_constraints + 
    "Return your response as a JSON array with this exact structure:"
    "["
    "  {"
    "    name: Combination Name,"
    "    items: [item1, item2, item3],"
    "    category: Balanced Combo,"
    "    description: Why this works"
    "  }"
    "]"
    "Be creative but practical - these should be meals students would actually want to eat!"
    )


    reddit_file = client.files.upload(file="output.txt")


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = [reddit_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema= list[Recommendation],
            thinking_config=types.ThinkingConfig(thinking_budget=-1)
        ),
    )

    client.close()
    return response.text 