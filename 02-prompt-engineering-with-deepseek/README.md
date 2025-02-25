# Setup

1. Create virtual environment: `python3 -m venv --prompt prompteng venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

# Usage

1. Rent the RTX 4090 GPU at [Neuralrack](https://neuralrack.ai).
2. Choose "Container Mode" -> "Recommended Recipes" -> "DeepSeekR1-32b".
3. Memorize the IP address of the rented instances
4. Run the app substituting the `<ip_address>`
    ```bash
    LLM_SERVER_IP_ADDRESS=<ip_address> python app.py
    ```
