import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageOps


def browse_files(file_type: str) -> str:
    """
    Opens the file dialog for selecting a file.
    :param file_type: Type of file to select (audio or image)
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


def ensure_16_9_aspect_ratio(image_path: str, output_path: str) -> str:
    """
    Ensures the image has a 16:9 aspect ratio by resizing or padding it,
    and ensures both dimensions are divisible by 2.
    :param image_path: Path to the input image
    :param output_path: Path to save the adjusted image
    :return: Path to the adjusted image
    """
    with Image.open(image_path) as img:
        width, height = img.size
        target_ratio = 16 / 9

        current_ratio = width / height

        if abs(current_ratio - target_ratio) < 0.01:
            img = ensure_even_dimensions(img)
            img.save(output_path)
            return output_path

        if current_ratio > target_ratio:
            new_height = int(width / target_ratio)
            img = ImageOps.pad(img, (width, new_height), color=(0, 0, 0))
        else:
            new_width = int(height * target_ratio)
            img = ImageOps.pad(img, (new_width, height), color=(0, 0, 0))

        img = ensure_even_dimensions(img)

        img.save(output_path)
        return output_path


def ensure_even_dimensions(img) -> Image:
    """
    Ensures both width and height are divisible by 2.
    :param img: PIL Image object
    :return: Adjusted image
    """
    width, height = img.size

    # Adjust width if not divisible by 2
    if width % 2 != 0:
        width -= 1

    # Adjust height if not divisible by 2
    if height % 2 != 0:
        height -= 1

    return img.resize((width, height))


def get_output_path() -> str:
    """
    Prompts the user for the output file path.
    :return: Path to save the output video
    """
    root = tk.Tk()
    root.withdraw()

    output_path = filedialog.asksaveasfilename(
        title="Save Output Video", defaultextension=".mp4", filetypes=[("MP4 Video", "*.mp4")]
    )

    if not output_path:
        messagebox.showwarning("Warning", "No output file selected.")

    return output_path


def combine_audio_image(audio_path: str, image_path: str, output_path: str) -> None:
    """
    Combines an image with audio to create a video using ffmpeg.
    :param image_path: Path to the image file
    :param audio_path: Path to the audio file
    :param output_path: Path to save the output video
    """

    try:
        if not audio_path or not image_path:
            messagebox.showwarning("Warning", "Please select both an audio and image file.")
            return

        command = [
            "ffmpeg",
            "-loop",
            "1",  # Loop the image
            "-i",
            image_path,  # Input image
            "-i",
            audio_path,  # Input audio
            "-c:v",
            "libx264",  # Encode video using H.264 codec
            "-tune",
            "stillimage",  # Optimize for still images
            "-c:a",
            "aac",  # Encode audio in AAC format
            "-b:a",
            "192k",  # Audio bitrate
            "-pix_fmt",
            "yuv420p",  # Pixel format for wide compatibility
            "-shortest",  # Match the duration to the audio
            output_path,
        ]

        subprocess.run(command, check=True)
        messagebox.showinfo("Success", f"Output saved to: {output_path}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Please check that you have ffmpeg installed. An error occurred: {e}")


def remove_adjusted_image(image_path: str) -> None:
    """
    Removes the adjusted image file if it exists.
    :param image_path: Path to the adjusted image file
    """
    try:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def main() -> None:
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

    audio_path = tk.StringVar()
    image_path = tk.StringVar()

    def set_audio_path():
        audio_path.set(browse_files("audio"))
        audio_path_label.config(text=audio_path.get())

    def set_image_path():
        image_path.set(browse_files("image"))
        image_path_label.config(text=image_path.get())

    get_audio_button = tk.Button(
        window,
        text="Open Audio File",
        command=set_audio_path,
        font=("Arial", 13),
        bg="blue",
        fg="white",
    )

    get_image_button = tk.Button(
        window,
        text="Open Image File",
        command=set_image_path,
        font=("Arial", 13),
        bg="blue",
        fg="white",
    )

    def combine_and_cleanup() -> None:
        if not audio_path.get() or not image_path.get():
            messagebox.showwarning("Warning", "Please select both an audio and image file.")
            return

        adjusted_image_path = ensure_16_9_aspect_ratio(image_path.get(), "adjusted_image.png")
        combine_audio_image(
            audio_path=audio_path.get(),
            image_path=adjusted_image_path,
            output_path=get_output_path(),
        )
        remove_adjusted_image(adjusted_image_path)

    combine_button = tk.Button(
        window,
        text="Combine Audio and Image",
        command=combine_and_cleanup,
        font=("Arial", 13),
        bg="green",
        fg="white",
    )

    audio_path_label = tk.Label(
        window,
        text="",
        font=("Arial", 12),
        bg="black",
        fg="white",
    )

    image_path_label = tk.Label(
        window,
        text="",
        font=("Arial", 12),
        bg="black",
        fg="white",
    )

    title_label.pack(padx=20, pady=20)
    audio_file_explorer_label.pack()
    get_audio_button.pack()
    audio_path_label.pack()
    image_file_explorer_label.pack()
    get_image_button.pack()
    image_path_label.pack()
    combine_button.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
else:
    print("This script is not meant to be imported.")
    exit(1)
