import tkinter as tk
import music_controller
import threading
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Global variables for UI elements
root = None
song_label = None
btn_pause = None
play_counts = {}  # Dictionary to track song plays


def update_song_label():
    if music_controller.songs and 0 <= music_controller.current_index < len(music_controller.songs):
        song_name = music_controller.songs[music_controller.current_index][0]
        song_label.config(text=song_name)
    else:
        song_label.config(text="No Song Playing")


def update_pause_button():
    if btn_pause:
        btn_pause.config(text="⏸️" if not music_controller.is_paused else "▶️")


def force_update_ui():
    update_song_label()
    update_pause_button()


def update_play_count():
    """Fixed version that properly accesses the songs list"""
    if music_controller.songs and 0 <= music_controller.current_index < len(music_controller.songs):
        song_name = music_controller.songs[music_controller.current_index][0]
        play_counts[song_name] = play_counts.get(song_name, 0) + 1


def play_current_song():
    music_controller.playMusic()
    update_play_count()
    force_update_ui()


def toggle_pause_resume():
    music_controller.pause()
    force_update_ui()


def next_song():
    music_controller.play_next()
    update_play_count()
    force_update_ui()


def prev_song():
    music_controller.play_previous()
    update_play_count()
    force_update_ui()


def pause_or_resume():
    toggle_pause_resume()
    force_update_ui()


def start_gesture_control():
    def run_gesture():
        import gesture_control
        gesture_control.GestureController().run()

    gesture_thread = threading.Thread(target=run_gesture, daemon=True)
    gesture_thread.start()


def show_play_statistics():
    if not play_counts:
        print("No songs played yet!")
        return

    # Filter and sort songs by play count (descending)
    filtered_data = {k: v for k, v in sorted(play_counts.items(),
                                             key=lambda item: item[1], reverse=True) if v > 0}

    if not filtered_data:
        print("No songs have been played yet!")
        return

    songs = list(filtered_data.keys())
    counts = list(filtered_data.values())

    # Create figure with dark theme
    plt.figure(figsize=(10, 8), facecolor='#121212')
    ax = plt.gca()
    ax.set_facecolor('#1E1E1E')

    # Create pie chart with improved settings
    wedges, texts, autotexts = plt.pie(
        counts,
        labels=songs,
        autopct=lambda p: f'{p:.1f}% ({int(p / 100 * sum(counts))} plays)',
        startangle=90,
        colors=plt.cm.tab20.colors,
        textprops={'color': 'white', 'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': '#121212'}
    )

    # Style adjustments
    plt.setp(autotexts, size=10, weight="bold")
    plt.title(f'Song Play Statistics\nTotal Plays: {sum(counts)}',
              color='white', fontsize=14, pad=20)

    # Add interactive legend
    legend = plt.legend(
        wedges,
        [f"{song}: {count} plays" for song, count in zip(songs, counts)],
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        facecolor='#1E1E1E',
        edgecolor='white',
        fontsize=10,
        labelcolor='white'
    )

    plt.tight_layout()
    plt.show()


def start_app():
    global root, song_label, btn_pause
    
    # Initialize window
    root = tk.Tk()
    root.title("🎵 Music Player")
    root.geometry("800x600")

    # ✅ Load background image AFTER initializing root
    image = Image.open("C:/Users/VANSHIKA/OneDrive/Desktop/study/python/MusicPlayer/bg.jpg")
    image = image.resize((800, 600))  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(image)

    # ✅ Create label with image and place it behind everything
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference!
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    # Song display
    song_label = tk.Label(root, text="No Song Playing",
                          font=("Arial", 24), fg="white", bg="#081C26")
    song_label.pack(pady=50)

    # Control buttons
    controls_frame = tk.Frame(root,bg="#081C26")
    controls_frame.pack()

    # Control buttons
    btn_prev = tk.Button(controls_frame, text="⏮", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0, command=prev_song)
    btn_play = tk.Button(controls_frame, text="▶", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0, command=play_current_song)
    btn_pause = tk.Button(controls_frame, text="⏸️", font=("Arial", 30),
                          fg="white", bg="#1DB954", bd=0, command=pause_or_resume)
    btn_next = tk.Button(controls_frame, text="⏭", font=("Arial", 30),
                         fg="white", bg="#1DB954", bd=0, command=next_song)

    # Layout buttons
    btn_prev.grid(row=0, column=0, padx=20)
    btn_play.grid(row=0, column=1, padx=20)
    btn_pause.grid(row=0, column=2, padx=20)
    btn_next.grid(row=0, column=3, padx=20)

    # Additional buttons
    btn_gesture = tk.Button(controls_frame, text="👆 Gesture Control",
                            font=("Arial", 14), fg="white", bg="#1DB954",
                            command=start_gesture_control)
    btn_gesture.grid(row=1, columnspan=4, pady=20)

    btn_stats = tk.Button(controls_frame, text="📈 Show Stats",
                          font=("Arial", 14), fg="white", bg="#1DB954",
                          command=show_play_statistics)
    btn_stats.grid(row=2, columnspan=4, pady=20)

    # Status bar
    status_label = tk.Label(root, text=f"🎵 {len(music_controller.songs)} songs loaded",
                            font=("Arial", 12), fg="grey", bg="#121212")
    status_label.pack(side="bottom", pady=10)

    def update_ui():
        update_song_label()
        update_pause_button()
        root.after(100, update_ui)

    update_ui()
    root.mainloop()


if __name__ == "__main__":
    start_app()