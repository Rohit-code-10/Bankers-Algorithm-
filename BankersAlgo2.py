import tkinter as tk
from tkinter import messagebox
import time
import threading

class BankersVisual:
    def __init__(self, root):  # ✅ Corrected: use __init__ instead of _init_
        self.root = root
        self.root.title("Banker's Algorithm - Visual Interactive Demo")
        self.root.geometry("950x700")
        self.root.configure(bg="#f2f2f2")

        title = tk.Label(self.root, text="Banker's Algorithm - Visual Interactive Demo",
                         font=("Helvetica", 18, "bold"), bg="#f2f2f2", fg="#222")
        title.pack(pady=10)

        # Input area
        input_frame = tk.Frame(self.root, bg="#f2f2f2")
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Processes:", bg="#f2f2f2").grid(row=0, column=0)
        self.proc_entry = tk.Entry(input_frame, width=5)
        self.proc_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Resources:", bg="#f2f2f2").grid(row=0, column=2, padx=10)
        self.res_entry = tk.Entry(input_frame, width=5)
        self.res_entry.grid(row=0, column=3)

        tk.Button(input_frame, text="Next", command=self.make_tables, bg="#4CAF50", fg="white").grid(row=0, column=4, padx=10)

        self.table_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.table_frame.pack(pady=10)

        # Visualization canvas
        self.canvas = tk.Canvas(self.root, width=900, height=300, bg="white",
                                highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=20)

        # Output text area
        self.output_text = tk.Text(self.root, width=110, height=10, wrap="word", bg="#f9f9f9")
        self.output_text.pack(pady=10)

    def make_tables(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            self.n = int(self.proc_entry.get())
            self.m = int(self.res_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for processes/resources.")
            return

        # Labels
        tk.Label(self.table_frame, text="Allocation Matrix").grid(row=0, column=0, columnspan=self.m)
        tk.Label(self.table_frame, text="Max Matrix").grid(row=0, column=self.m+1, columnspan=self.m)
        tk.Label(self.table_frame, text="Available").grid(row=0, column=2*self.m+2, columnspan=self.m)

        self.alloc_entries, self.max_entries, self.avail_entries = [], [], []

        # Allocation and Max matrices
        for i in range(self.n):
            row_alloc = []
            for j in range(self.m):
                e = tk.Entry(self.table_frame, width=4)
                e.grid(row=i+1, column=j)
                row_alloc.append(e)
            self.alloc_entries.append(row_alloc)

            row_max = []
            for j in range(self.m):
                e = tk.Entry(self.table_frame, width=4)
                e.grid(row=i+1, column=j+self.m+1)
                row_max.append(e)
            self.max_entries.append(row_max)

        # Available vector
        for j in range(self.m):
            e = tk.Entry(self.table_frame, width=4)
            e.grid(row=1, column=j+2*self.m+2)
            self.avail_entries.append(e)

        # Run button
        tk.Button(self.table_frame, text="Run Visual Demo", command=self.run_visual,
                  bg="#2196F3", fg="white").grid(row=self.n+2, column=0, columnspan=3, pady=10)

    def run_visual(self):
        try:
            alloc = [[int(e.get()) for e in row] for row in self.alloc_entries]
            max_need = [[int(e.get()) for e in row] for row in self.max_entries]
            avail = [int(e.get()) for e in self.avail_entries]
        except ValueError:
            messagebox.showerror("Error", "Fill all entries with integers.")
            return

        need = [[max_need[i][j] - alloc[i][j] for j in range(self.m)] for i in range(self.n)]
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Need Matrix: {need}\n\n")

        # Clear previous visualization
        self.canvas.delete("all")
        self.process_nodes = []

        # Draw process nodes
        for i in range(self.n):
            x, y = 100 + i * 150, 100
            rect = self.canvas.create_oval(x, y, x+70, y+70, fill="#ffb347", outline="black")
            text = self.canvas.create_text(x+35, y+35, text=f"P{i}", font=("Helvetica", 12, "bold"))
            self.process_nodes.append((rect, text))

        # Run Banker’s algorithm in a separate thread
        threading.Thread(target=self.run_bankers_visual, args=(alloc, need, avail), daemon=True).start()

    def run_bankers_visual(self, alloc, need, avail):
        n, m = self.n, self.m
        finish = [False]*n
        work = avail[:]
        safe_seq = []

        time.sleep(1)
        for step in range(n):
            allocated = False
            for i in range(n):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                    self.highlight_process(i, "green")
                    self.output_text.insert(tk.END, f"Process P{i} can execute. Work={work}\n")
                    self.output_text.see(tk.END)
                    time.sleep(1.5)

                    for j in range(m):
                        work[j] += alloc[i][j]
                    safe_seq.append(f"P{i}")
                    finish[i] = True
                    allocated = True
                    self.highlight_process(i, "lightgreen")
                    time.sleep(1)
                    break
            if not allocated:
                break

        if len(safe_seq) == n:
            self.output_text.insert(tk.END, f"\n✅ System is in SAFE STATE.\nSafe Sequence: {' -> '.join(safe_seq)}\n")
        else:
            self.output_text.insert(tk.END, "\n❌ Deadlock detected. System is NOT safe.\n")

    def highlight_process(self, index, color):
        rect, _ = self.process_nodes[index]
        self.canvas.itemconfig(rect, fill=color)
        self.canvas.update()

if __name__ == "__main__":  # ✅ Corrected main guard
    root = tk.Tk()
    app = BankersVisual(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox  # ✅ Corrected: import messagebox