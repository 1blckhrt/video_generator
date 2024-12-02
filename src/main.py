import tkinter as tk


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

    title_label.pack(padx=20, pady=20)
    audio_file_explorer_label.pack()
    image_file_explorer_label.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
