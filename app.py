from flask import Flask, render_template, request, jsonify
import json
import random
import os
from collections import defaultdict

app = Flask(__name__)

# Food database with attributes for smart matching
food_db = [
    {
        "name": "Pizza",
        "mood_match": ["Happy", "Celebrating", "Lazy"],
        "diet_type": ["Veg", "Non-Veg"],  # Can have both options
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200", "₹200-300"],
        "tags": ["cheese", "comfort food", "fast food"],
        "restaurant_types": ["pizzeria", "italian", "fast food"]
    },
    {
        "name": "Biryani",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300", "₹300+"],
        "tags": ["rice", "flavorful", "festive"],
        "restaurant_types": ["north indian", "hyderabadi", "mughlai"]
    },
    {
        "name": "Burger",
        "mood_match": ["Happy", "Lazy"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200", "₹200-300"],
        "tags": ["fast food", "quick", "satisfying"],
        "restaurant_types": ["fast food", "american", "cafe"]
    },
    {
        "name": "Soup",
        "mood_match": ["Tired", "Sad"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200"],
        "tags": ["comfort food", "warm", "light"],
        "restaurant_types": ["chinese", "continental", "cafe"]
        
    },
    {
        "name": "Khichdi",
        "mood_match": ["Tired", "Sad"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild"],
        "budget_range": ["₹100-200"],
        "tags": ["comfort food", "easy to digest", "homely"],
        "restaurant_types": ["north indian", "home style", "healthy"]
        
    },
    {
        "name": "Masala Maggi",
        "mood_match": ["Tired", "Lazy"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["Under ₹100"],
        "tags": ["quick", "comfort food", "snack"],
        "restaurant_types": ["cafe", "street food", "quick bites"]
        
    },
    {
        "name": "Ice Cream",
        "mood_match": ["Sad", "Happy", "Celebrating"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild"],
        "budget_range": ["₹100-200"],
        "tags": ["dessert", "sweet", "comfort food"],
        "restaurant_types": ["dessert", "ice cream parlor", "cafe"]
        
    },
    {
        "name": "Fries",
        "mood_match": ["Sad", "Happy", "Lazy"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["Under ₹100", "₹100-200"],
        "tags": ["snack", "comfort food", "fast food"],
        "restaurant_types": ["fast food", "cafe", "american"]
        
    },
    {
        "name": "Brownie",
        "mood_match": ["Sad", "Happy", "Celebrating"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild"],
        "budget_range": ["₹100-200"],
        "tags": ["dessert", "sweet", "chocolate"],
        "restaurant_types": ["bakery", "cafe", "dessert"]
        
    },
    {
        "name": "Cake",
        "mood_match": ["Celebrating", "Happy"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild"],
        "budget_range": ["₹200-300", "₹300+"],
        "tags": ["dessert", "sweet", "celebration"],
        "restaurant_types": ["bakery", "cafe", "dessert"]
       
    },
    {
        "name": "Tandoori Platter",
        "mood_match": ["Celebrating", "Happy"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹300+"],
        "tags": ["grilled", "flavorful", "festive"],
        "restaurant_types": ["north indian", "mughlai", "punjabi"]
        
    },
    {
        "name": "Noodles",
        "mood_match": ["Celebrating", "Happy", "Lazy"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium", "Spicy"],
        "budget_range": ["₹100-200"],
        "tags": ["stir-fried", "comfort food", "quick"],
        "restaurant_types": ["chinese", "asian", "street food"]
        
    },
    {
        "name": "Wraps",
        "mood_match": ["Lazy", "Happy"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200", "₹200-300"],
        "tags": ["handy", "quick", "filling"],
        "restaurant_types": ["cafe", "fast food", "healthy"]
        
    },
    {
        "name": "Paratha",
        "mood_match": ["Lazy", "Happy"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200"],
        "tags": ["breakfast", "Indian", "filling"],
        "restaurant_types": ["north indian", "punjabi", "dhaba"]
        
    },
    {
        "name": "Momos",
        "mood_match": ["Lazy", "Happy"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium", "Spicy"],
        "budget_range": ["₹100-200"],
        "tags": ["street food", "steamed", "snack"],
        "restaurant_types": ["tibetan", "chinese", "street food"]
      
    },
    {
        "name": "Paneer Tikka",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300"],
        "tags": ["grilled", "protein", "starter"],
        "restaurant_types": ["north indian", "punjabi", "mughlai"]
        
    },
    {
        "name": "Sandwich",
        "mood_match": ["Happy", "Lazy", "Tired"],
        "diet_type": ["Veg", "Non-Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200"],
        "tags": ["quick", "light", "versatile"],
        "restaurant_types": ["cafe", "fast food", "bakery"]
      
    },
    {
        "name": "Dosa",
        "mood_match": ["Happy", "Lazy"],
        "diet_type": ["Veg"],
        "spice_level": ["Mild", "Medium"],
        "budget_range": ["₹100-200", "₹200-300"],
        "tags": ["South Indian", "crispy", "breakfast"],
        "restaurant_types": ["south indian", "udupi", "breakfast"]
      
    },
    # Added Non-Veg Options Below
    {
        "name": "Butter Chicken",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300", "₹300+"],
        "tags": ["creamy", "curry", "protein"],
        "restaurant_types": ["north indian", "punjabi", "mughlai"]
        
    },
    {
        "name": "Chicken Tikka",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300"],
        "tags": ["grilled", "protein", "starter"],
        "restaurant_types": ["north indian", "punjabi", "mughlai"]
        
    },
    {
        "name": "Fish Curry",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300", "₹300+"],
        "tags": ["seafood", "curry", "protein"],
        "restaurant_types": ["bengali", "south indian", "coastal"]
        
    },
    {
        "name": "Mutton Rogan Josh",
        "mood_match": ["Celebrating", "Happy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹300+"],
        "tags": ["curry", "rich", "festive"],
        "restaurant_types": ["north indian", "kashmiri", "mughlai"]
       
    },
    {
        "name": "Chicken Biryani",
        "mood_match": ["Happy", "Celebrating"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300", "₹300+"],
        "tags": ["rice", "flavorful", "festive"],
        "restaurant_types": ["hyderabadi", "mughlai", "north indian"]
        
    },
    {
        "name": "Mutton Biryani",
        "mood_match": ["Celebrating", "Happy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹300+"],
        "tags": ["rice", "flavorful", "festive"],
        "restaurant_types": ["hyderabadi", "mughlai", "north indian"]
        
    },
    {
        "name": "Keema Pav",
        "mood_match": ["Happy", "Lazy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹100-200", "₹200-300"],
        "tags": ["minced meat", "street food", "comfort food"],
        "restaurant_types": ["mumbai", "street food", "maharashtrian"]
        
    },
    {
        "name": "Chicken Kebab",
        "mood_match": ["Happy", "Celebrating", "Lazy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300"],
        "tags": ["grilled", "starter", "protein"],
        "restaurant_types": ["north indian", "mughlai", "bbq"]
        
    },
    {
        "name": "Fish Fry",
        "mood_match": ["Happy", "Lazy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300"],
        "tags": ["crispy", "seafood", "starter"],
        "restaurant_types": ["south indian", "bengali", "coastal"]
        
    },
    {
        "name": "Chicken 65",
        "mood_match": ["Happy", "Lazy"],
        "diet_type": ["Non-Veg"],
        "spice_level": ["Medium", "Spicy"],
        "budget_range": ["₹200-300"],
        "tags": ["crispy", "starter", "spicy"],
        "restaurant_types": ["south indian", "andhra", "tamil"]
        
    }
]

# Updated restaurant database with more Indian locations
restaurants_db = [
    {
        "name": "Pizza Paradise",
        "cuisine_types": ["pizzeria", "italian", "fast food"],
        "rating": 4.2,
        "price_range": "₹100-200",
        "location": "Koramangala"
    },
    {
        "name": "Biryani House",
        "cuisine_types": ["north indian", "hyderabadi", "mughlai"],
        "rating": 4.5,
        "price_range": "₹200-300",
        "location": "Indiranagar"
    },
    {
        "name": "Burger Junction",
        "cuisine_types": ["fast food", "american", "cafe"],
        "rating": 4.0,
        "price_range": "₹100-200",
        "location": "HSR Layout"
    },
    {
        "name": "South Indian Delight",
        "cuisine_types": ["south indian", "udupi", "breakfast"],
        "rating": 4.3,
        "price_range": "₹100-200",
        "location": "JP Nagar"
    },
    {
        "name": "Tandoori Nights",
        "cuisine_types": ["north indian", "mughlai", "punjabi"],
        "rating": 4.1,
        "price_range": "₹300+",
        "location": "MG Road"
    },
    {
        "name": "Chinese Box",
        "cuisine_types": ["chinese", "asian", "street food"],
        "rating": 3.9,
        "price_range": "₹100-200",
        "location": "Whitefield"
    },
    {
        "name": "Cafe Corner",
        "cuisine_types": ["cafe", "bakery", "dessert"],
        "rating": 4.4,
        "price_range": "₹200-300",
        "location": "Koramangala"
    },
    {
        "name": "Momo Magic",
        "cuisine_types": ["tibetan", "chinese", "street food"],
        "rating": 4.2,
        "price_range": "₹100-200",
        "location": "Indiranagar"
    },
    # Added more Indian restaurants below
    {
        "name": "Punjabi Dhaba",
        "cuisine_types": ["north indian", "punjabi", "dhaba"],
        "rating": 4.3,
        "price_range": "₹100-200",
        "location": "Marathahalli"
    },
    {
        "name": "Bengal Kitchen",
        "cuisine_types": ["bengali", "coastal", "seafood"],
        "rating": 4.4,
        "price_range": "₹200-300",
        "location": "BTM Layout"
    },
    {
        "name": "Andhra Spice",
        "cuisine_types": ["south indian", "andhra", "spicy"],
        "rating": 4.3,
        "price_range": "₹200-300",
        "location": "Electronic City"
    },
    {
        "name": "Kebab House",
        "cuisine_types": ["north indian", "mughlai", "bbq"],
        "rating": 4.5,
        "price_range": "₹200-300",
        "location": "Jayanagar"
    },
    {
        "name": "Mumbai Street Food",
        "cuisine_types": ["mumbai", "street food", "maharashtrian"],
        "rating": 4.0,
        "price_range": "₹100-200",
        "location": "Banashankari"
    },
    {
        "name": "Coastal Delights",
        "cuisine_types": ["coastal", "seafood", "south indian"],
        "rating": 4.6,
        "price_range": "₹300+",
        "location": "Malleshwaram"
    },
    {
        "name": "Delhi Darbar",
        "cuisine_types": ["north indian", "mughlai", "punjabi"],
        "rating": 4.4,
        "price_range": "₹300+",
        "location": "Bellandur"
    },
    {
        "name": "Hyderabadi House",
        "cuisine_types": ["hyderabadi", "mughlai", "biryani"],
        "rating": 4.7,
        "price_range": "₹200-300",
        "location": "Sarjapur Road"
    }
]

import random
from collections import defaultdict
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

# Scoring function to match foods based on user preferences
def get_meal_suggestions(mood, diet, spice, budget):
    scored_foods = []
    
    for food in food_db:
        score = 0
        
        # Match mood - primary factor
        if mood in food["mood_match"]:
            score += 10
        
        # Match diet preference - critical factor
        if diet == "Any" or diet in food["diet_type"]:
            score += 15
        else:
            # If diet preference doesn't match, skip this food
            continue
            
        # Match spice level
        if spice in food["spice_level"]:
            score += 7
            
        # Match budget
        if budget in food["budget_range"]:
            score += 8
            
        # Add a little randomization for variety (±2 points)
        score += random.randint(-2, 2)
        
        # Only include foods with a reasonable match score
        if score > 15:
            scored_foods.append({"name": food["name"], "score": score})
    
    # Sort by score (highest first)
    scored_foods.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top 3-5 suggestions
    num_suggestions = min(5, len(scored_foods))
    if num_suggestions == 0:
        # Fallback suggestions if no matches found
        return ["Pizza", "Sandwich", "Dosa"]
    
    return [food["name"] for food in scored_foods[:num_suggestions]]

# Function to get restaurant recommendations based on food suggestions
def get_restaurant_suggestions(food_items, user_location=None):
    food_restaurant_types = []
    
    # Get restaurant types for each food item
    for food_name in food_items:
        for food in food_db:
            if food["name"] == food_name:
                food_restaurant_types.extend(food["restaurant_types"])
    
    # Count frequency of each restaurant type
    restaurant_type_counts = defaultdict(int)
    for rest_type in food_restaurant_types:
        restaurant_type_counts[rest_type] += 1
    
    # Score restaurants based on matched cuisine types
    scored_restaurants = []
    for restaurant in restaurants_db:
        score = 0
        for cuisine in restaurant["cuisine_types"]:
            if cuisine in restaurant_type_counts:
                score += restaurant_type_counts[cuisine] * 3
        
        # Bonus for higher ratings
        score += (restaurant["rating"] - 3.5) * 5 if restaurant["rating"] > 3.5 else 0
        
        # Location match bonus (if provided)
        if user_location and restaurant["location"].lower() == user_location.lower():
            score += 8
            
        # Add some randomization
        score += random.uniform(-0.5, 0.5)
        
        if score > 0:
            scored_restaurants.append({
                "name": restaurant["name"],
                "rating": restaurant["rating"],
                "price_range": restaurant["price_range"],
                "location": restaurant["location"],
                "score": score
            })
    
    # Sort by score
    scored_restaurants.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top restaurants
    return scored_restaurants[:3]

# New function to get restaurants for a specific food item
def get_restaurants_for_food(food_name, user_location=None):
    food_restaurant_types = []
    
    # Get restaurant types for the specific food
    for food in food_db:
        if food["name"] == food_name:
            food_restaurant_types = food["restaurant_types"]
            break
    
    # Score restaurants based on matched cuisine types
    scored_restaurants = []
    for restaurant in restaurants_db:
        score = 0
        for cuisine in restaurant["cuisine_types"]:
            if cuisine in food_restaurant_types:
                score += 5
        
        # Bonus for higher ratings
        score += (restaurant["rating"] - 3.5) * 3 if restaurant["rating"] > 3.5 else 0
        
        # Location match bonus (if provided)
        if user_location and restaurant["location"].lower() == user_location.lower():
            score += 8
            
        # Add some randomization
        score += random.uniform(-0.5, 0.5)
        
        if score > 0:
            scored_restaurants.append({
                "name": restaurant["name"],
                "rating": restaurant["rating"],
                "price_range": restaurant["price_range"],
                "location": restaurant["location"],
                "score": score
            })
    
    # Sort by score
    scored_restaurants.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top restaurants for this food
    return scored_restaurants[:4]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mood = request.form["mood"]
        diet = request.form["diet"]
        spice = request.form["spice"]
        budget = request.form["budget"]
        location = request.form.get("location", "")
        
        meals = get_meal_suggestions(mood, diet, spice, budget)
        restaurants = get_restaurant_suggestions(meals, location)
        
        return render_template("index.html", meals=meals, restaurants=restaurants)
    
    return render_template("index.html", meals=None, restaurants=None)

# API endpoint to get food recommendations
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json()
    mood = data.get("mood")
    diet = data.get("diet")
    spice = data.get("spice")
    budget = data.get("budget")
    location = data.get("location", None)
    
    meals = get_meal_suggestions(mood, diet, spice, budget)
    restaurants = get_restaurant_suggestions(meals, location)
    
    return jsonify({
        "food_recommendations": meals,
        "restaurant_recommendations": restaurants
    })

# New API endpoint to get restaurants for a specific food
@app.route("/api/restaurants-for-food", methods=["GET"])
def restaurants_for_food():
    food_name = request.args.get("food")
    location = request.args.get("location", None)
    
    if not food_name:
        return jsonify({"error": "Food name is required"}), 400
    
    restaurants = get_restaurants_for_food(food_name, location)
    
    return jsonify({
        "food": food_name,
        "restaurants": restaurants
    })

if __name__ == "__main__":
    app.run(debug=True)
