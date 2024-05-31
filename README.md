# 🚀 Open Source Project Finder 🌟

Welcome to the Open Source Project Finder! This Flask-based web application helps you discover open source projects where you can contribute based on your skills.

## Features

🔍 Search for repositories based on your skills  
🌟 Filter repositories with at least 100 stars  
📅 Find repositories with recently opened issues (within a month timeframe)

## Usage

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Add Your github token to line 15 of app.py file, you can create a token here https://github.com/settings/tokens
   ```
   GITHUB_TOKEN = "your github token here"
   ```




3. Run the Flask application:
    ```bash
    flask run
    ```

3. Access the application in your web browser at `http://localhost:5000`.

4. Enter your skills in the search bar and hit enter to get a list of relevant repositories.

## Contributing

🎉 Contributions are welcome! Feel free to open an issue or submit a pull request.

## Credits

🙌 This project was created by Goutham N using Flask and the GitHub API.

## License

📝 This project is free to be tinkered with.
