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

    title_label.pack(padx=20, pady=20)

    window.mainloop()


if __name__ == "__main__":
    main()
