import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# -------------------- CLASS DEFINITIONS --------------------

class Applicant:
    def _init_(self, name, income, credit_score, debt):
        self.name = name
        self.income = income
        self.credit_score = credit_score
        self.debt = debt
        self.ai_score = (0.5 * credit_score) + (0.3 * income) - (0.2 * debt)

    def _repr_(self):
        return f"{self.name} (Score: {self.ai_score:.2f})"


class CreditScoringSystem:
    def _init_(self):
        self.heap = []  # (-score, applicant)

    def add_applicant(self, applicant):
        heapq.heappush(self.heap, (-applicant.ai_score, applicant))

    def get_top_applicant(self):
        if not self.heap:
            return None
        return self.heap[0][1]

    def approve_top_applicant(self):
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[1]

    def get_all_applicants(self):
        return sorted([(-score, app) for score, app in self.heap], reverse=True)


# -------------------- GUI APP --------------------

class CreditAppGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("💳 AI-Powered Credit Scoring System")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.system = CreditScoringSystem()

        # ---------- INPUT SECTION ----------
        frame_input = tk.LabelFrame(root, text="Add New Applicant", padx=10, pady=10)
        frame_input.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_input, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame_input, text="Income:").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(frame_input, text="Credit Score:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(frame_input, text="Debt:").grid(row=1, column=2, padx=5, pady=5)

        self.entry_name = tk.Entry(frame_input)
        self.entry_income = tk.Entry(frame_input)
        self.entry_credit = tk.Entry(frame_input)
        self.entry_debt = tk.Entry(frame_input)

        self.entry_name.grid(row=0, column=1)
        self.entry_income.grid(row=0, column=3)
        self.entry_credit.grid(row=1, column=1)
        self.entry_debt.grid(row=1, column=3)

        tk.Button(frame_input, text="Add Applicant", command=self.add_applicant, bg="#007bff", fg="white").grid(row=2, column=0, columnspan=4, pady=10)

        # ---------- TABLE SECTION ----------
        frame_table = tk.LabelFrame(root, text="Applicant Rankings", padx=10, pady=10)
        frame_table.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("Name", "Income", "Credit Score", "Debt", "AI Score")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)

        # ---------- BUTTONS ----------
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Show Top Applicant", command=self.show_top, bg="#28a745", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(frame_buttons, text="Approve Top Applicant", command=self.approve_top, bg="#ffc107", fg="black").grid(row=0, column=1, padx=10)
        tk.Button(frame_buttons, text="Exit", command=root.quit, bg="#dc3545", fg="white").grid(row=0, column=2, padx=10)

    # -------------------- FUNCTIONS --------------------

    def add_applicant(self):
        try:
            name = self.entry_name.get()
            income = float(self.entry_income.get())
            credit = float(self.entry_credit.get())
            debt = float(self.entry_debt.get())

            if not name:
                messagebox.showwarning("Warning", "Please enter a name.")
                return

            applicant = Applicant(name, income, credit, debt)
            self.system.add_applicant(applicant)
            self.refresh_table()

            messagebox.showinfo("Success", f"Applicant {name} added successfully! AI Score: {applicant.ai_score:.2f}")
            self.entry_name.delete(0, tk.END)
            self.entry_income.delete(0, tk.END)
            self.entry_credit.delete(0, tk.END)