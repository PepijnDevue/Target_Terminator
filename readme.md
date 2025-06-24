# Target Terminator

## Installation
1. Make sure you have uv installed:
   ```bash
   pip install uv
   ```
2. Open terminal in root of the project and run:
   ```bash
   uv init
   uv sync
   ```

## Usage
1. Open terminal in root of the project and run:
   ```bash
   uv run main.py
   ```
2. Enter mode:
    - `k`: Play as plane with keyboard
    - `h`: Let AI play using UI
    - `empty input`: Let AI train without UI

The AI will automatically save its progress and load it next time you run the game. (pretrained)