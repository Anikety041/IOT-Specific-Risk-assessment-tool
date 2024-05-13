import tkinter as tk
from tkinter import messagebox
import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatIntelligence:
    """
    Fetches threat intelligence data from real sources and analyzes risks.
    """
    def __init__(self):
        self.threat_data = []

    def fetch_threat_data(self, url):
        """
        Fetches threat intelligence data from the specified URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.threat_data = response.json().get('data', [])
            logger.info(f"Failed to fetch threat data from {url}")
            return True
        except requests.RequestException :
            logger.info(f"Failed to fetch threat data {url}")
            return False

    def analyze_risks(self):
        """
        Analyzes threat data and identifies risks.
        """
        high_risk_threshold = 7  # Example threshold for high-risk severity
        high_risk_threats = []
        for threat in self.threat_data:
            if threat.get('severity', 0) >= high_risk_threshold:
                high_risk_threats.append(threat)
        return high_risk_threats

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Threat Intelligence and Risk Analysis")
        self.geometry("400x200")
        
        self.threat_intel = ThreatIntelligence()
        
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self, text="Enter URL:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(self, width=40)
        self.url_entry.pack(pady=5)

        self.fetch_data_button = tk.Button(self, text="Fetch Threat Data", command=self.fetch_data)
        self.fetch_data_button.pack(pady=5)

        self.analyze_button = tk.Button(self, text="Analyze Risks", command=self.analyze_risks)
        self.analyze_button.pack(pady=5)

        self.exit_button = tk.Button(self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=5)

    def fetch_data(self):
        url = self.url_entry.get()
        if url:
            if self.threat_intel.fetch_threat_data(url):
                messagebox.showinfo("Info", "Threat data fetched successfully.")
            else:
                messagebox.showerror("Info", "Failed to fetch threat data.")
        else:
            messagebox.showerror("Error", "Please enter a URL.")

    def analyze_risks(self):
        high_risk_threats = self.threat_intel.analyze_risks()
        if high_risk_threats:
            messagebox.showwarning("Warning", f"High risk threats identified: {high_risk_threats}")
        else:
            messagebox.showinfo("Info", "No high risk threats found.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
