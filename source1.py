import tkinter as tk
from tkinter import scrolledtext
import http.client
import json

def fetch_lyrics():
    song = song_entry.get()
    artist = artist_entry.get()
    if song and artist:
        conn = http.client.HTTPSConnection("api.lyrics.ovh")
        url = f"/v1/{artist}/{song}"
        conn.request("GET", url)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read().decode()
            try:
                lyrics_data = json.loads(data)
                lyrics = lyrics_data.get('lyrics', 'Lyrics not found.')
            except json.JSONDecodeError:
                lyrics = "Error decoding the response."
        else:
            lyrics = f"Error: {response.status} {response.reason}"
        conn.close()
    else:
        lyrics = "Please enter both song title and artist name."
    
    lyrics_display.delete(1.0, tk.END)  # Clear previous lyrics
    lyrics_display.insert(tk.END, lyrics)

# Create the main window
root = tk.Tk()
root.title("Lyrics Extractor")

# Create and place widgets
tk.Label(root, text="Song Title:").pack(pady=5)
song_entry = tk.Entry(root, width=50)
song_entry.pack(pady=5)

tk.Label(root, text="Artist Name:").pack(pady=5)
artist_entry = tk.Entry(root, width=50)
artist_entry.pack(pady=5)

tk.Button(root, text="Get Lyrics", command=fetch_lyrics).pack(pady=10)

lyrics_display = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
lyrics_display.pack(pady=10)

# Run the GUI event loop
root.mainloop()
