import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import os

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def transcribe():
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showerror("error", "please select a file to transcribe!")
        return
    try:
        model_name = model_var.get()
        model = whisper.load_model(model_name)
        
        status_label.config(text="transcribing... please wait")
        root.update()
        
        result = model.transcribe(file_path)
       
        output_format = output_var.get()
        output_file = f"{os.path.splitext(file_path)[0]}.{output_format}"
        
        with open(output_file, "w", encoding="utf-8") as f:
            if output_format == "txt":
                f.write(result["text"])
            elif output_format == "srt":
                segments = result["segments"]
                for i, segment in enumerate(segments):
                    f.write(f"{i+1}\n")
                    start_time = format_time(segment["start"])
                    end_time = format_time(segment["end"])
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text'].strip()}\n\n")
        
        status_label.config(text="ready")
        messagebox.showinfo("success", f"transcription complete! saved to {output_file}")
    
    except Exception as e:
        status_label.config(text="ready")
        messagebox.showerror("error", f"an error occurred: {str(e)}")


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio/Video Files", "*.mp4;*.mp3;*.mkv;*.wav")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

root = tk.Tk()
root.title("whisper transcript")
root.geometry("500x350")
main_frame = tk.Frame(root, padx=20, pady=10)
main_frame.pack(fill=tk.BOTH, expand=False)
file_frame = tk.Frame(main_frame)
file_frame.pack(fill=tk.X, pady=10)
file_path_label = tk.Label(file_frame, text="select video/audio file:")
file_path_label.pack(anchor=tk.W)
file_path_entry = tk.Entry(file_frame, width=40)
file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)
browse_button = tk.Button(file_frame, text="browse", command=browse_file)
browse_button.pack(side=tk.RIGHT, padx=5)
model_frame = tk.Frame(main_frame)
model_frame.pack(fill=tk.X, pady=10)
model_var = tk.StringVar(root)
model_var.set("base")  
model_label = tk.Label(model_frame, text="select whisper model:")
model_label.pack(anchor=tk.W)
model_menu = tk.OptionMenu(model_frame, model_var, "tiny", "base", "small", "medium", "large")
model_menu.pack(fill=tk.X, pady=5)
output_frame = tk.Frame(main_frame)
output_frame.pack(fill=tk.X, pady=10)
output_var = tk.StringVar(root)
output_var.set("txt")  
output_label = tk.Label(output_frame, text="select output format:")
output_label.pack(anchor=tk.W)
output_menu = tk.OptionMenu(output_frame, output_var, "txt", "srt")
output_menu.pack(fill=tk.X, pady=5)
status_label = tk.Label(main_frame, text="ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)
transcribe_button = tk.Button(button_frame, text="transcribe", command=transcribe, width=15, height=2)
transcribe_button.pack()


root.mainloop()
