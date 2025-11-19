#generates food combinations
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
from typing import List, Dict

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def generate_prompt(menu_items: List[str], preferences: List[str]) -> str:
    """Generate the prompt for Gemini API"""
    
    # Convert preferences to dietary constraints
    constraints = ""
    if "vegetarian" in preferences:
        constraints += "- Exclude meat, poultry, and fish\n"
    if "vegan" in preferences:
        constraints += "- Exclude all animal products (meat, dairy, eggs)\n"
    if "gluten-free" in preferences:
        constraints += "- Avoid items with wheat, barley, rye\n"
    if "high-protein" in preferences:
        constraints += "- Prioritize high-protein items in all combinations\n"
    if "low-carb" in preferences:
        constraints += "- Minimize bread, pasta, rice, and starchy items\n"

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
    return prompt

def generate_combinations(menu_items: List[str], preferences: List[str]) -> List[Dict]:
    """Generate meal combinations using Gemini API"""
    
    try:
        prompt = generate_prompt(menu_items, preferences)
        
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.9,
                'max_output_tokens': 2048,
            }
        )
        
        # Parse JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        combinations = json.loads(response_text.strip())
        
        return combinations
    
    except Exception as e:
        print(f"Error generating combinations: {e}")
        # Return fallback combinations
        return [
            {
                "name": "Error Loading Combinations",
                "items": menu_items[:3],
                "category": "Fallback",
                "description": "Could not generate AI combinations. Here are some menu items."
            }
        ]