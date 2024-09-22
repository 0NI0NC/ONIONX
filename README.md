# ONION[X] - Natural Language to C Code Compiler

## Overview

ONION[X] is a powerful web application that transforms natural language input into advanced C code using an innovative language model. This tool is designed to help developers and enthusiasts quickly generate, compile, and execute C code based on user-defined tasks.

## Features

- **Natural Language Processing:** Convert simple human language into complex C code.
- **Code Compilation and Execution:** Compile and run generated C code directly from the app.
- **Downloadable Output:** Save generated C code as a file for further use.
- **User-Friendly Interface:** Simple and intuitive UI built with Streamlit.

## Requirements

- Python 3.8+
- Streamlit
- SQLAlchemy
- LangChain
- Groq API
- DuckDuckGo Search

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ONION-X.git
   cd ONION-X
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   - Create a `.env` file in the root directory and add your `GROQ_API_KEY`:

     ```plaintext
     GROQ_API_KEY=your_api_key
     ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

## Usage

- Enter your task in the text area provided and click "Submit."
- The application will generate the C code, compile it, and display the execution output.
- You can download the generated C code using the provided button.

## About the Technology

ONION[X] uses:
- **LangChain** for handling natural language processing and agent creation.
- **Streamlit** for creating a responsive web interface.
- **DuckDuckGo Search** for enhancing information retrieval.
- **SQLAlchemy** for managing chat history.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the GNU 3.0 License. See the LICENSE file for more details.

## Acknowledgements

Thanks to all the contributors and the open-source community for making this project possible!
