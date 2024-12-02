import tkinter as tk
from tkinter import filedialog, messagebox


def browse_files(file_type: str) -> str:
    """
    Opens the file dialog for selecting a file.
    """
    root = tk.Tk()
    root.withdraw()

    if file_type == "audio":
        filename = filedialog.askopenfilename(
            title="Select Audio File", filetypes=[("Audio Files", "*.mp3;*.wav;*.aac;*.flac;*.ogg")]
        )
    elif file_type == "image":
        filename = filedialog.askopenfilename(
            title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

    if not filename:
        messagebox.showwarning("Warning", f"No {file_type} file selected.")

    return filename


def main():
    window = tk.Tk()
    window.title("(@1blckhrt) Audio and Image Merger")
    window.geometry("500x500")
    window.config(background="black", padx=20, pady=20)

    title_label = tk.Label(
        window,
        text="Audio and Image Merger",
        font=("Arial", 24),
        bg="black",
        fg="white",
    )

    audio_file_explorer_label = tk.Label(
        window,
        text="Select Audio File",
        font=("Arial", 16),
        bg="black",
        fg="white",
    )

    image_file_explorer_label = tk.Label(
        window,
        text="Select Image File",
        font=("Arial", 16),
        bg="black",
        fg="white",
    )

    get_audio_button = tk.Button(
        window,
        text="Open Audio File",
        command=lambda: browse_files("audio"),
        font=("Arial", 13),
        bg="blue",
        fg="white",
    )

    get_image_button = tk.Button(
        window,
        text="Open Image File",
        command=lambda: browse_files("image"),
        font=("Arial", 13),
        bg="blue",
        fg="white",
    )

    title_label.pack(padx=20, pady=20)
    audio_file_explorer_label.pack()
    get_audio_button.pack()
    image_file_explorer_label.pack()
    get_image_button.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
