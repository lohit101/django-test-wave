# YTFaceless: A Django-based Reddit Video Facelift Project

YTFaceless is a Django-based web application that takes user-submitted Reddit posts and generates a personalized video clip with a voiceover, captions, and a custom image overlay. The project utilizes Python's Praw library to fetch data from Reddit, and the assemblyai library for speech-to-text transcription.

## Features

- Fetch data from Reddit and generate a personalized video clip
- Add a custom image overlay to the video clip
- Add a voiceover to the video clip
- Add captions to the video clip
- Upload the final video clip to a CDN for sharing
- Save the final video clip URL and other details to the database for future reference

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/YTFaceless.git
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Run the Django server:
```
python manage.py runserver
```

## Usage

1. Sign up or log in to the application.
2. On the dashboard, enter the desired subreddit and click "Generate Video".
3. The application will fetch data from Reddit, generate a personalized video clip, and save the final video clip URL and other details to the database for future reference.

## Contributing

Contributions are welcome! If you find any issues or have any suggestions, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.