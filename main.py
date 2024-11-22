import re
import flet as ft
import openai
from time import sleep

# OpenAI API Key
openai.api_key = "API_KEY"

# Function to call ChatGPT API for recipe generation
def generate_recipe(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a recipe generator assistant. Provide recipes with a title, description, ingredients, and steps based on the user's prompt.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]

# Function to parse ingredients and steps using regex
def parse_recipe(content):
    # Extract ingredients using regex
    ingredients_match = re.search(r"(?i)Ingredients:(.*?)(Steps:|Directions:)", content, re.S)
    ingredients = []
    if ingredients_match:
        ingredients_raw = ingredients_match.group(1).strip()
        ingredients = re.findall(r"[-•*]?\s*(.+)", ingredients_raw)
        # Standardize the bullet format to use '-'
        ingredients = [f"{ingredient.strip()}" for ingredient in ingredients]
        ingredients[0] = f"- {ingredients[0].strip()}"

    # Extract steps using regex
    steps_match = re.search(r"(?i)(Steps|Directions):\s*(.+)", content, re.S)
    steps = []
    if steps_match:
        steps_raw = steps_match.group(2).strip()
        steps = re.split(r"\d+[.)]\s*", steps_raw)  # Split based on step numbering
        steps = [step.strip() for step in steps if step.strip()]  # Remove empty steps

    return ingredients, steps

# Flet App
def main(page: ft.Page):
    page.title = "AI-Powered Recipe Generator"
    page.scroll = "adaptive"
    page.padding = 30
    page.background_color = "#f9f9f9"  # Soft background color for the app

    # State variables
    recipe_title = ft.Text("", size=24, weight="bold", color="black", text_align="left")
    recipe_description = ft.Text("", size=16, weight="normal", color="black", text_align="left")
    ingredients_list = ft.Column()
    steps_list = ft.Column()

    # Loading Screen with Centered Text Progress
    def show_loading_screen():
        loading_text = ft.Text(
            "Generating your recipe... Please wait",
            size=18,
            weight="bold",
            color="blue",
            text_align="center",
        )
        # Center container
        progress_container = ft.Container(
            content=loading_text,
            alignment=ft.alignment.center,
            expand=True,
        )
        page.clean()
        page.add(progress_container)
        page.update()

        # Simulate progress by updating text
        loading_phrases = [
            "Analyzing your input...",
            "Fetching ingredients...",
            "Crafting steps for your recipe...",
            "Almost there...",
        ]
        for phrase in loading_phrases:
            loading_text.value = phrase
            sleep(1.5)  # Simulating loading
            page.update()

    # Generate Recipe Function
    def generate_recipe_action(e):
        user_input = recipe_input.value.strip()
        if not user_input:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please enter a recipe idea or ingredients!"))
            page.snack_bar.open = True
            page.update()
            return

        show_loading_screen()

        try:
            # Call ChatGPT to generate recipe
            result = generate_recipe(f"Generate a recipe for: {user_input}")

            # Parse ChatGPT response
            #recipe_title.value = result.split("\n")[0].strip()  # Assume the first line is the title
            #recipe_description.value = "\n".join(result.split("\n")[1:3]).strip()  # Assume description follows

            recipe_title.value = result.split("\n")[0].removeprefix("Title: ").strip()  # Remove "Title: " from the title
            recipe_description.value = "\n".join(line.removeprefix("Description: ") for line in result.split("\n")[1:3]).strip()  # Remove "Description: "

            # Extract ingredients and steps
            ingredients, steps = parse_recipe(result)

            # Display ingredients as bullet points
            ingredients_list.controls = [
                ft.Text(ingredient, size=14) for ingredient in ingredients
            ]

            # Display steps as a clean ordered list
            steps_list.controls = [
                ft.Text(f"{idx + 1}. {step.strip()}", size=14)
                for idx, step in enumerate(steps)
            ]

        except Exception as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error generating recipe: {err}"))
            page.snack_bar.open = True

        # Update the page with results
        update_result_section()
        page.update()

    # Update the results section
    def update_result_section():
        page.clean()
        hero_section()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        recipe_title,
                        ft.Divider(height=10, thickness=1, color="grey"),
                        recipe_description,
                        ft.Divider(height=10, thickness=1, color="grey"),
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [ft.Text("Ingredients", size=20, weight="bold"), ingredients_list],
                                        spacing=10,
                                    ),
                                    bgcolor="#f5f5f5",
                                    padding=20,
                                    border_radius=10,
                                    expand=1,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [ft.Text("Steps", size=20, weight="bold"), steps_list],
                                        spacing=10,
                                    ),
                                    bgcolor="#f5f5f5",
                                    padding=20,
                                    border_radius=10,
                                    expand=1,
                                ),
                            ],
                            spacing=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=20,
                ),
                padding=20,
                bgcolor="#ffffff",
                border_radius=15,
                shadow=ft.BoxShadow(
                    blur_radius=10, color="#cccccc", offset=ft.Offset(0, 5)
                ),
            )
        )

    # Hero Section
    def hero_section():
        page.clean()
        hero_title = ft.Text(
            "Meet Your Personal AI-Powered Kitchen Assistant",
            size=32,
            weight="bold",
            text_align="center",
        )
        hero_subtitle = ft.Text(
            "Simply type a recipe idea or some ingredients you have on hand, and the AI will instantly generate an all-new recipe on demand.",
            size=18,
            text_align="center",
            color="gray",
        )
        global recipe_input
        recipe_input = ft.TextField(
            label="Create a recipe for...",
            border_color="black",
            expand=True,
            height=50,
        )
        generate_button = ft.ElevatedButton(
            "Generate",
            on_click=generate_recipe_action,
            bgcolor="black",
            color="white",
            width=200,
            height=50,
        )

        # Add the Hero Section
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        hero_title,
                        hero_subtitle,
                        ft.Row([recipe_input], alignment="center"),
                        ft.Row([generate_button], alignment="center"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=40,
                bgcolor="#f0f0f0",
                border_radius=15,
            )
        )

    # Show the Hero Section initially
    hero_section()


# Run Flet app
ft.app(target=main)
