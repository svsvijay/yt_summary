from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    # Extract video URL from the query parameters
    video_url = request.args.get('video_url')
    
    # Extract video ID from URL
    video_id = video_url.split('watch?v=')[-1]
    
    try:
        # Attempt to fetch the transcript for the given video ID
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        
        # Fetching the actual transcript data
        transcript_data = transcript.fetch()
        return jsonify(transcript_data)
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 400
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run()

 