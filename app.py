from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__, static_folder="static")

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        print(f"Získaná URL: {url}")  

        ydl_opts = {
    'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s", 
    'format': 'bv+ba/b',
    'merge_output_format': 'mp4',  
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4', 
    }]
}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        print(f"Staženo do: {file_path}")  
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Chyba při stahování: {str(e)}")
        return f"<h1>Chyba při stahování videa:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
