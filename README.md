
# AI-Powered Recipe Generator

This is a user-friendly, AI-driven recipe generator that allows you to create recipes based on your ideas or available ingredients. Powered by OpenAI's GPT-3.5 Turbo model, the app provides recipes with a title, description, ingredients, and step-by-step instructions.

## Features

- **AI-Generated Recipes**: Generate creative and unique recipes by simply providing a prompt or list of ingredients.
- **Elegant UI**: A clean and modern interface designed with Flet for seamless user interaction.
- **Dynamic Parsing**: Extracts and formats ingredients and steps from the AI response for easy readability.
- **Responsive Design**: Adaptable layout that works across devices.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/coderalnaim/DishGenie.git
   cd DishGenie
   ```

2. Install dependencies:

   ```bash
   pip install requirements.txt
   ```

3. Set up your OpenAI API key:
   - Replace `"API_KEY"` in the script with your actual OpenAI API key.

4. Run the app:

   ```bash
   python main.py
   ```

## How to Use

1. Launch the app.
2. Enter your recipe idea or a list of ingredients in the input box.
3. Click the "Generate" button.
4. View the generated recipe with a title, description, ingredients, and steps.

## Code Highlights

### Key Functions

- **`generate_recipe(prompt)`**: Calls the OpenAI ChatGPT API to generate a recipe.
- **`parse_recipe(content)`**: Parses the recipe content using regex to separate ingredients and steps.
- **`generate_recipe_action(e)`**: Handles the generation process and updates the UI.

### Design

The app uses Flet to create a visually appealing and responsive UI. The design emphasizes clarity, ease of use, and accessibility.

## Requirements

- Python 3.7 or later
- Flet
- OpenAI Python client library

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [OpenAI](https://openai.com) for the GPT-3.5 Turbo model.
- [Flet](https://flet.dev) for the UI framework.

---

Feel free to fork and contribute to this project!
