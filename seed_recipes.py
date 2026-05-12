import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flavorloop.settings')
django.setup()

from django.contrib.auth.models import User
from pages.models import Recipe, RecipeIngredient

user = User.objects.get(id=1)

recipes = [
    {
        "title": "Avocado Toast Express",
        "description": "Crispy sourdough topped with smashed avocado, cherry tomatoes, and a sprinkle of chili flakes.",
        "image_url": "https://images.unsplash.com/photo-1588137372308-15f75323ca8d?w=600",
        "prep_time_minutes": 8,
        "servings": 2,
        "difficulty": "Easy",
        "category": "Quick Meals",
        "instructions": "1. Toast the sourdough bread until golden.\n2. Mash the avocado with lime juice, salt and pepper.\n3. Spread avocado on toast.\n4. Top with halved cherry tomatoes and chili flakes.\n5. Drizzle with olive oil and serve.",
        "ingredients": [
            {"name": "Sourdough Bread", "quantity": "2 slices", "serving_qty": 100, "kcal": 250, "fat": 1.5, "carbs": 50, "protein": 9, "fiber": 2, "salt": 1.2, "sugars": 2},
            {"name": "Avocado", "quantity": "1 whole", "serving_qty": 150, "kcal": 240, "fat": 22, "carbs": 13, "protein": 3, "fiber": 10, "salt": 0.01, "sugars": 1},
            {"name": "Cherry Tomatoes", "quantity": "8 pieces", "serving_qty": 80, "kcal": 14, "fat": 0.2, "carbs": 3, "protein": 0.7, "fiber": 1, "salt": 0.04, "sugars": 2},
        ]
    },
    {
        "title": "15-Min Chicken Stir Fry",
        "description": "Quick and colorful chicken stir-fry with snap peas, bell peppers, and a savory soy-ginger sauce.",
        "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600",
        "prep_time_minutes": 15,
        "servings": 3,
        "difficulty": "Easy",
        "category": "Quick Meals",
        "instructions": "1. Slice chicken breast into thin strips.\n2. Heat oil in a wok over high heat.\n3. Stir-fry chicken until golden, about 4 minutes.\n4. Add snap peas, bell peppers, and ginger.\n5. Toss with soy sauce and sesame oil.\n6. Serve over rice.",
        "ingredients": [
            {"name": "Chicken Breast", "quantity": "400g", "serving_qty": 400, "kcal": 660, "fat": 7, "carbs": 0, "protein": 124, "fiber": 0, "salt": 0.4, "sugars": 0},
            {"name": "Bell Pepper", "quantity": "2 whole", "serving_qty": 200, "kcal": 60, "fat": 0.6, "carbs": 12, "protein": 2, "fiber": 4, "salt": 0.01, "sugars": 8},
            {"name": "Snap Peas", "quantity": "150g", "serving_qty": 150, "kcal": 63, "fat": 0.3, "carbs": 11, "protein": 4, "fiber": 4, "salt": 0.01, "sugars": 6},
        ]
    },
    {
        "title": "Mediterranean Bowl",
        "description": "Hearty grain bowl with chickpeas, roasted vegetables, hummus, and tahini dressing.",
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600",
        "prep_time_minutes": 12,
        "servings": 2,
        "difficulty": "Easy",
        "category": "Vegan",
        "instructions": "1. Cook quinoa according to package instructions.\n2. Roast sweet potato cubes at 200C for 15 minutes.\n3. Arrange quinoa, chickpeas, and roasted vegetables in bowls.\n4. Add a generous dollop of hummus.\n5. Drizzle with tahini dressing and sprinkle with sesame seeds.",
        "ingredients": [
            {"name": "Quinoa", "quantity": "200g", "serving_qty": 200, "kcal": 740, "fat": 12, "carbs": 130, "protein": 28, "fiber": 14, "salt": 0.02, "sugars": 0},
            {"name": "Chickpeas", "quantity": "300g", "serving_qty": 300, "kcal": 495, "fat": 8, "carbs": 82, "protein": 27, "fiber": 23, "salt": 0.72, "sugars": 13},
            {"name": "Sweet Potato", "quantity": "300g", "serving_qty": 300, "kcal": 261, "fat": 0.3, "carbs": 60, "protein": 5, "fiber": 9, "salt": 0.18, "sugars": 12},
        ]
    },
    {
        "title": "Black Bean Tacos",
        "description": "Spiced black bean tacos with fresh salsa, guacamole, and cilantro lime crema.",
        "image_url": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600",
        "prep_time_minutes": 14,
        "servings": 4,
        "difficulty": "Easy",
        "category": "Vegan",
        "instructions": "1. Warm black beans with cumin, chili powder, and garlic.\n2. Prepare fresh salsa with diced tomatoes, onion, and cilantro.\n3. Warm tortillas in a dry pan.\n4. Fill with beans, salsa, and guacamole.\n5. Top with fresh cilantro.",
        "ingredients": [
            {"name": "Black Beans", "quantity": "400g can", "serving_qty": 400, "kcal": 520, "fat": 2, "carbs": 95, "protein": 35, "fiber": 30, "salt": 1.8, "sugars": 3},
            {"name": "Corn Tortillas", "quantity": "8 pieces", "serving_qty": 200, "kcal": 500, "fat": 5, "carbs": 100, "protein": 12, "fiber": 10, "salt": 0.6, "sugars": 4},
            {"name": "Avocado", "quantity": "1 whole", "serving_qty": 150, "kcal": 240, "fat": 22, "carbs": 13, "protein": 3, "fiber": 10, "salt": 0.01, "sugars": 1},
        ]
    },
    {
        "title": "Tofu Buddha Bowl",
        "description": "Crispy baked tofu over mixed greens with edamame, carrots, and peanut sauce.",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600",
        "prep_time_minutes": 25,
        "servings": 2,
        "difficulty": "Medium",
        "category": "Vegan",
        "instructions": "1. Press and cube tofu, toss in cornstarch and soy sauce.\n2. Bake at 200C for 20 minutes until crispy.\n3. Prepare peanut sauce with peanut butter, soy sauce, and lime.\n4. Arrange greens, shredded carrots, and edamame in bowls.\n5. Top with crispy tofu and drizzle with peanut sauce.",
        "ingredients": [
            {"name": "Tofu", "quantity": "300g", "serving_qty": 300, "kcal": 450, "fat": 24, "carbs": 9, "protein": 45, "fiber": 3, "salt": 0.06, "sugars": 2},
            {"name": "Mixed Greens", "quantity": "150g", "serving_qty": 150, "kcal": 30, "fat": 0.5, "carbs": 4, "protein": 3, "fiber": 3, "salt": 0.15, "sugars": 1},
            {"name": "Edamame", "quantity": "150g", "serving_qty": 150, "kcal": 185, "fat": 8, "carbs": 14, "protein": 17, "fiber": 8, "salt": 0.04, "sugars": 3},
        ]
    },
    {
        "title": "Protein Power Smoothie Bowl",
        "description": "Thick banana-berry smoothie bowl topped with granola, chia seeds, and fresh fruit.",
        "image_url": "https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600",
        "prep_time_minutes": 8,
        "servings": 1,
        "difficulty": "Easy",
        "category": "High Protein",
        "instructions": "1. Blend frozen banana, mixed berries, protein powder, and almond milk until thick.\n2. Pour into a bowl.\n3. Top with granola, chia seeds, sliced banana, and berries.\n4. Drizzle with honey.",
        "ingredients": [
            {"name": "Banana", "quantity": "1 large", "serving_qty": 120, "kcal": 107, "fat": 0.4, "carbs": 27, "protein": 1.3, "fiber": 3, "salt": 0.001, "sugars": 14},
            {"name": "Mixed Berries", "quantity": "100g", "serving_qty": 100, "kcal": 50, "fat": 0.5, "carbs": 12, "protein": 1, "fiber": 5, "salt": 0.001, "sugars": 7},
            {"name": "Protein Powder", "quantity": "30g scoop", "serving_qty": 30, "kcal": 120, "fat": 1.5, "carbs": 3, "protein": 25, "fiber": 0, "salt": 0.3, "sugars": 1},
            {"name": "Granola", "quantity": "50g", "serving_qty": 50, "kcal": 225, "fat": 9, "carbs": 33, "protein": 5, "fiber": 3, "salt": 0.1, "sugars": 12},
        ]
    },
    {
        "title": "Grilled Chicken & Quinoa",
        "description": "Marinated grilled chicken breast with quinoa, broccoli, and lemon herb dressing.",
        "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=600",
        "prep_time_minutes": 30,
        "servings": 2,
        "difficulty": "Medium",
        "category": "High Protein",
        "instructions": "1. Marinate chicken in lemon juice, garlic, and herbs for 15 minutes.\n2. Grill chicken on each side for 6-7 minutes.\n3. Cook quinoa in vegetable broth.\n4. Steam broccoli until tender-crisp.\n5. Slice chicken and serve over quinoa with broccoli.\n6. Drizzle with lemon herb dressing.",
        "ingredients": [
            {"name": "Chicken Breast", "quantity": "400g", "serving_qty": 400, "kcal": 660, "fat": 7, "carbs": 0, "protein": 124, "fiber": 0, "salt": 0.4, "sugars": 0},
            {"name": "Quinoa", "quantity": "200g", "serving_qty": 200, "kcal": 740, "fat": 12, "carbs": 130, "protein": 28, "fiber": 14, "salt": 0.02, "sugars": 0},
            {"name": "Broccoli", "quantity": "200g", "serving_qty": 200, "kcal": 68, "fat": 0.7, "carbs": 14, "protein": 6, "fiber": 5, "salt": 0.07, "sugars": 3},
        ]
    },
    {
        "title": "Tuna Steak Poke Bowl",
        "description": "Fresh tuna steak cubes with sushi rice, cucumber, avocado, and soy-sesame dressing.",
        "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600",
        "prep_time_minutes": 20,
        "servings": 2,
        "difficulty": "Medium",
        "category": "High Protein",
        "instructions": "1. Cook sushi rice and season with rice vinegar.\n2. Cube fresh tuna and marinate in soy sauce and sesame oil.\n3. Slice cucumber, avocado, and radish.\n4. Arrange rice in bowls, top with tuna and vegetables.\n5. Garnish with sesame seeds and seaweed strips.",
        "ingredients": [
            {"name": "Tuna Steak", "quantity": "300g", "serving_qty": 300, "kcal": 420, "fat": 4, "carbs": 0, "protein": 90, "fiber": 0, "salt": 0.15, "sugars": 0},
            {"name": "Sushi Rice", "quantity": "300g", "serving_qty": 300, "kcal": 1050, "fat": 1, "carbs": 240, "protein": 20, "fiber": 1, "salt": 0.01, "sugars": 0},
            {"name": "Avocado", "quantity": "1 whole", "serving_qty": 150, "kcal": 240, "fat": 22, "carbs": 13, "protein": 3, "fiber": 10, "salt": 0.01, "sugars": 1},
        ]
    },
    {
        "title": "Egg White Omelette",
        "description": "Fluffy egg white omelette with spinach, mushrooms, and feta cheese.",
        "image_url": "https://images.unsplash.com/photo-1510693206972-df098062cb71?w=600",
        "prep_time_minutes": 10,
        "servings": 1,
        "difficulty": "Easy",
        "category": "High Protein",
        "instructions": "1. Whisk egg whites until frothy.\n2. Sauté mushrooms and spinach until wilted.\n3. Pour egg whites into a non-stick pan.\n4. Add vegetables and crumbled feta to one side.\n5. Fold and cook until set. Season and serve.",
        "ingredients": [
            {"name": "Egg Whites", "quantity": "150ml", "serving_qty": 150, "kcal": 78, "fat": 0.3, "carbs": 1, "protein": 17, "fiber": 0, "salt": 0.6, "sugars": 1},
            {"name": "Spinach", "quantity": "50g", "serving_qty": 50, "kcal": 12, "fat": 0.2, "carbs": 2, "protein": 1.5, "fiber": 1, "salt": 0.04, "sugars": 0.2},
            {"name": "Mushrooms", "quantity": "100g", "serving_qty": 100, "kcal": 22, "fat": 0.3, "carbs": 3, "protein": 3, "fiber": 1, "salt": 0.03, "sugars": 1},
            {"name": "Feta Cheese", "quantity": "50g", "serving_qty": 50, "kcal": 133, "fat": 11, "carbs": 2, "protein": 7, "fiber": 0, "salt": 1.8, "sugars": 2},
        ]
    },
    {
        "title": "Classic Tiramisu",
        "description": "Layered Italian dessert with espresso-soaked ladyfingers and mascarpone cream.",
        "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600",
        "prep_time_minutes": 45,
        "servings": 8,
        "difficulty": "Hard",
        "category": "Desserts",
        "instructions": "1. Brew strong espresso and let it cool.\n2. Whip mascarpone with sugar and egg yolks until smooth.\n3. Fold in whipped cream for lightness.\n4. Dip ladyfingers briefly in espresso and layer in dish.\n5. Spread mascarpone cream over ladyfingers.\n6. Repeat layers and dust with cocoa powder.\n7. Refrigerate for at least 4 hours before serving.",
        "ingredients": [
            {"name": "Mascarpone Cheese", "quantity": "500g", "serving_qty": 500, "kcal": 2150, "fat": 190, "carbs": 20, "protein": 35, "fiber": 0, "salt": 0.4, "sugars": 15},
            {"name": "Ladyfingers", "quantity": "300g", "serving_qty": 300, "kcal": 1200, "fat": 15, "carbs": 240, "protein": 30, "fiber": 3, "salt": 1.5, "sugars": 120},
            {"name": "Espresso", "quantity": "300ml", "serving_qty": 300, "kcal": 6, "fat": 0, "carbs": 0, "protein": 0.3, "fiber": 0, "salt": 0.01, "sugars": 0},
            {"name": "Cocoa Powder", "quantity": "30g", "serving_qty": 30, "kcal": 68, "fat": 4, "carbs": 17, "protein": 6, "fiber": 10, "salt": 0.01, "sugars": 0.5},
        ]
    },
    {
        "title": "Chocolate Lava Cake",
        "description": "Individual molten chocolate cakes with a gooey center, served with vanilla ice cream.",
        "image_url": "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=600",
        "prep_time_minutes": 25,
        "servings": 4,
        "difficulty": "Hard",
        "category": "Desserts",
        "instructions": "1. Melt dark chocolate and butter together.\n2. Whisk eggs and sugar until thick and pale.\n3. Fold chocolate mixture into eggs, then fold in flour.\n4. Pour into greased ramekins.\n5. Bake at 220C for exactly 12 minutes.\n6. Invert onto plates immediately and serve warm.",
        "ingredients": [
            {"name": "Dark Chocolate", "quantity": "200g", "serving_qty": 200, "kcal": 1100, "fat": 60, "carbs": 120, "protein": 14, "fiber": 14, "salt": 0.04, "sugars": 90},
            {"name": "Butter", "quantity": "100g", "serving_qty": 100, "kcal": 717, "fat": 81, "carbs": 0.1, "protein": 0.9, "fiber": 0, "salt": 0.87, "sugars": 0.1},
            {"name": "Eggs", "quantity": "3 large", "serving_qty": 150, "kcal": 230, "fat": 15, "carbs": 1.5, "protein": 19, "fiber": 0, "salt": 0.65, "sugars": 1.5},
        ]
    },
    {
        "title": "Crème Brûlée",
        "description": "Silky vanilla custard with a perfectly caramelized sugar crust.",
        "image_url": "https://images.unsplash.com/photo-1470124182917-cc6d71087de8?w=600",
        "prep_time_minutes": 60,
        "servings": 6,
        "difficulty": "Hard",
        "category": "Desserts",
        "instructions": "1. Heat cream with vanilla bean until simmering.\n2. Whisk egg yolks and sugar until pale.\n3. Slowly pour hot cream into yolks, whisking constantly.\n4. Strain and pour into ramekins.\n5. Bake in a water bath at 150C for 45 minutes.\n6. Chill for 4 hours.\n7. Sprinkle sugar on top and torch until caramelized.",
        "ingredients": [
            {"name": "Heavy Cream", "quantity": "500ml", "serving_qty": 500, "kcal": 1750, "fat": 185, "carbs": 14, "protein": 10, "fiber": 0, "salt": 0.4, "sugars": 14},
            {"name": "Egg Yolks", "quantity": "6 large", "serving_qty": 120, "kcal": 400, "fat": 32, "carbs": 4, "protein": 16, "fiber": 0, "salt": 0.08, "sugars": 4},
            {"name": "Sugar", "quantity": "100g + 6 tbsp", "serving_qty": 150, "kcal": 600, "fat": 0, "carbs": 150, "protein": 0, "fiber": 0, "salt": 0.01, "sugars": 150},
        ]
    },
    {
        "title": "Post-Workout Chicken Wrap",
        "description": "Whole wheat wrap filled with grilled chicken, Greek yogurt sauce, and fresh vegetables.",
        "image_url": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=600",
        "prep_time_minutes": 15,
        "servings": 2,
        "difficulty": "Easy",
        "category": "Fitness",
        "instructions": "1. Grill seasoned chicken breast and slice thinly.\n2. Mix Greek yogurt with lemon juice and dill.\n3. Warm whole wheat wraps.\n4. Spread yogurt sauce on wraps.\n5. Layer chicken, lettuce, cucumber, and tomato.\n6. Roll tightly and slice in half.",
        "ingredients": [
            {"name": "Chicken Breast", "quantity": "300g", "serving_qty": 300, "kcal": 495, "fat": 5, "carbs": 0, "protein": 93, "fiber": 0, "salt": 0.3, "sugars": 0},
            {"name": "Whole Wheat Wrap", "quantity": "2 large", "serving_qty": 140, "kcal": 420, "fat": 8, "carbs": 70, "protein": 14, "fiber": 8, "salt": 0.8, "sugars": 4},
            {"name": "Greek Yogurt", "quantity": "100g", "serving_qty": 100, "kcal": 97, "fat": 5, "carbs": 3.5, "protein": 17, "fiber": 0, "salt": 0.06, "sugars": 3.5},
        ]
    },
    {
        "title": "Salmon & Sweet Potato",
        "description": "Oven-baked salmon fillet with roasted sweet potato and steamed asparagus.",
        "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600",
        "prep_time_minutes": 35,
        "servings": 2,
        "difficulty": "Medium",
        "category": "Fitness",
        "instructions": "1. Preheat oven to 200C.\n2. Cut sweet potatoes into wedges, toss with olive oil, and roast for 25 minutes.\n3. Season salmon with lemon, garlic, and herbs.\n4. Bake salmon alongside sweet potatoes for 15 minutes.\n5. Steam asparagus until tender-crisp.\n6. Plate everything and drizzle with lemon juice.",
        "ingredients": [
            {"name": "Salmon Fillet", "quantity": "300g", "serving_qty": 300, "kcal": 630, "fat": 36, "carbs": 0, "protein": 66, "fiber": 0, "salt": 0.24, "sugars": 0},
            {"name": "Sweet Potato", "quantity": "400g", "serving_qty": 400, "kcal": 348, "fat": 0.4, "carbs": 80, "protein": 6, "fiber": 12, "salt": 0.24, "sugars": 16},
            {"name": "Asparagus", "quantity": "200g", "serving_qty": 200, "kcal": 44, "fat": 0.4, "carbs": 8, "protein": 4, "fiber": 4, "salt": 0.04, "sugars": 4},
        ]
    },
    {
        "title": "Protein Pancakes",
        "description": "Fluffy oatmeal protein pancakes topped with banana, berries, and a drizzle of honey.",
        "image_url": "https://images.unsplash.com/photo-1528207776546-365bb750ee9c?w=600",
        "prep_time_minutes": 15,
        "servings": 2,
        "difficulty": "Easy",
        "category": "Fitness",
        "instructions": "1. Blend oats, banana, protein powder, eggs, and milk until smooth.\n2. Heat a non-stick pan over medium heat.\n3. Pour small amounts of batter to form pancakes.\n4. Cook until bubbles form on surface, then flip.\n5. Stack and top with sliced banana, berries, and honey.",
        "ingredients": [
            {"name": "Oats", "quantity": "100g", "serving_qty": 100, "kcal": 380, "fat": 7, "carbs": 66, "protein": 13, "fiber": 10, "salt": 0.01, "sugars": 1},
            {"name": "Protein Powder", "quantity": "40g", "serving_qty": 40, "kcal": 160, "fat": 2, "carbs": 4, "protein": 33, "fiber": 0, "salt": 0.4, "sugars": 1},
            {"name": "Banana", "quantity": "1 medium", "serving_qty": 100, "kcal": 89, "fat": 0.3, "carbs": 23, "protein": 1.1, "fiber": 2.6, "salt": 0.001, "sugars": 12},
            {"name": "Eggs", "quantity": "2 large", "serving_qty": 100, "kcal": 155, "fat": 11, "carbs": 1.1, "protein": 13, "fiber": 0, "salt": 0.43, "sugars": 1.1},
        ]
    },
    {
        "title": "Garlic Butter Shrimp",
        "description": "Sizzling shrimp in garlic butter sauce with a squeeze of fresh lemon and parsley.",
        "image_url": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=600",
        "prep_time_minutes": 12,
        "servings": 3,
        "difficulty": "Easy",
        "category": "Quick Meals",
        "instructions": "1. Clean and devein shrimp.\n2. Melt butter in a large skillet over medium-high heat.\n3. Add minced garlic and cook for 30 seconds.\n4. Add shrimp and cook 2-3 minutes per side.\n5. Finish with lemon juice, red pepper flakes, and fresh parsley.",
        "ingredients": [
            {"name": "Shrimp", "quantity": "400g", "serving_qty": 400, "kcal": 400, "fat": 3, "carbs": 3, "protein": 80, "fiber": 0, "salt": 2.8, "sugars": 0},
            {"name": "Butter", "quantity": "50g", "serving_qty": 50, "kcal": 359, "fat": 41, "carbs": 0.05, "protein": 0.4, "fiber": 0, "salt": 0.44, "sugars": 0.05},
            {"name": "Garlic", "quantity": "6 cloves", "serving_qty": 30, "kcal": 45, "fat": 0.2, "carbs": 10, "protein": 1.9, "fiber": 0.6, "salt": 0.05, "sugars": 0.3},
        ]
    },
    {
        "title": "Lentil Curry",
        "description": "Rich and creamy red lentil curry with coconut milk, spinach, and warm spices.",
        "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600",
        "prep_time_minutes": 15,
        "servings": 4,
        "difficulty": "Easy",
        "category": "Vegan",
        "instructions": "1. Sauté onion, garlic, and ginger until soft.\n2. Add curry powder, cumin, and turmeric.\n3. Stir in red lentils, diced tomatoes, and coconut milk.\n4. Simmer for 15 minutes until lentils are tender.\n5. Fold in fresh spinach until wilted.\n6. Serve over basmati rice with naan bread.",
        "ingredients": [
            {"name": "Red Lentils", "quantity": "300g", "serving_qty": 300, "kcal": 1050, "fat": 4, "carbs": 180, "protein": 75, "fiber": 33, "salt": 0.18, "sugars": 6},
            {"name": "Coconut Milk", "quantity": "400ml", "serving_qty": 400, "kcal": 920, "fat": 96, "carbs": 8, "protein": 8, "fiber": 0, "salt": 0.06, "sugars": 8},
            {"name": "Diced Tomatoes", "quantity": "400g can", "serving_qty": 400, "kcal": 72, "fat": 0.8, "carbs": 16, "protein": 3, "fiber": 5, "salt": 0.8, "sugars": 10},
        ]
    },
    {
        "title": "Berry Protein Muffins",
        "description": "Moist high-protein muffins packed with mixed berries and a crunchy oat topping.",
        "image_url": "https://images.unsplash.com/photo-1607958996333-17c557248e7?w=600",
        "prep_time_minutes": 35,
        "servings": 12,
        "difficulty": "Medium",
        "category": "High Protein",
        "instructions": "1. Preheat oven to 180C.\n2. Mix protein powder, oat flour, baking powder, and salt.\n3. Whisk eggs, Greek yogurt, honey, and vanilla.\n4. Fold wet ingredients into dry, then gently fold in berries.\n5. Divide into muffin tin and top with oats.\n6. Bake for 20-22 minutes until golden.",
        "ingredients": [
            {"name": "Protein Powder", "quantity": "60g", "serving_qty": 60, "kcal": 240, "fat": 3, "carbs": 6, "protein": 50, "fiber": 0, "salt": 0.6, "sugars": 2},
            {"name": "Oat Flour", "quantity": "200g", "serving_qty": 200, "kcal": 760, "fat": 14, "carbs": 132, "protein": 26, "fiber": 20, "salt": 0.02, "sugars": 2},
            {"name": "Mixed Berries", "quantity": "200g", "serving_qty": 200, "kcal": 100, "fat": 1, "carbs": 24, "protein": 2, "fiber": 10, "salt": 0.002, "sugars": 14},
        ]
    },
    {
        "title": "Peanut Butter Energy Bites",
        "description": "No-bake energy bites with peanut butter, oats, dark chocolate chips, and honey.",
        "image_url": "https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?w=600",
        "prep_time_minutes": 10,
        "servings": 16,
        "difficulty": "Easy",
        "category": "Fitness",
        "instructions": "1. Mix rolled oats, peanut butter, honey, and flax seeds.\n2. Fold in dark chocolate chips and chia seeds.\n3. Refrigerate mixture for 15 minutes.\n4. Roll into 16 bite-sized balls.\n5. Store in the refrigerator for up to a week.",
        "ingredients": [
            {"name": "Rolled Oats", "quantity": "200g", "serving_qty": 200, "kcal": 760, "fat": 14, "carbs": 132, "protein": 26, "fiber": 20, "salt": 0.02, "sugars": 2},
            {"name": "Peanut Butter", "quantity": "150g", "serving_qty": 150, "kcal": 885, "fat": 75, "carbs": 30, "protein": 38, "fiber": 8, "salt": 0.75, "sugars": 12},
            {"name": "Dark Chocolate Chips", "quantity": "80g", "serving_qty": 80, "kcal": 440, "fat": 24, "carbs": 48, "protein": 6, "fiber": 6, "salt": 0.02, "sugars": 36},
        ]
    },
]

for recipe_data in recipes:
    r, created = Recipe.objects.get_or_create(
        title=recipe_data["title"],
        defaults={
            "owner": user,
            "description": recipe_data["description"],
            "image_url": recipe_data["image_url"],
            "prep_time_minutes": recipe_data["prep_time_minutes"],
            "servings": recipe_data["servings"],
            "difficulty": recipe_data["difficulty"],
            "category": recipe_data["category"],
            "instructions": recipe_data["instructions"],
        }
    )
    if created:
        for ing in recipe_data["ingredients"]:
            RecipeIngredient.objects.create(
                recipe=r,
                name=ing["name"],
                quantity=ing["quantity"],
                serving_qty=ing["serving_qty"],
                nutrition_kcal=ing["kcal"],
                nutrition_fat=ing["fat"],
                nutrition_carbs=ing["carbs"],
                nutrition_protein=ing["protein"],
                nutrition_fiber=ing.get("fiber", 0),
                nutrition_salt=ing.get("salt", 0),
                nutrition_sugars=ing.get("sugars", 0),
            )
        print(f"Created: {r.title}")
    else:
        print(f"Exists: {r.title}")

print(f"\nDone! Total recipes: {Recipe.objects.filter(owner=user).count()}")
