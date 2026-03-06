import fitparse
import pandas as pd
import numpy as np
from datetime import timedelta


class Activity:
    def __init__(self, file_path):
        self.file_path = file_path
        self.fitfile = fitparse.FitFile(file_path)
        self.data = self._parse_fit()
        self.date = self.data["timestamp"].iloc[0]
        self.type = self._detect_type()
        self.duration_min = len(self.data) / 60  # Assuming 1s recording
        self.avg_hr = (
            self.data["heart_rate"].mean()
            if "heart_rate" in self.data.columns
            else None
        )

    def __repr__(self):
        return f"<Activity type={self.type} date={self.date} duration={self.duration_min:.2f} min>"

    def __dict__(self):
        return {
            "type": self.type,
            "date": self.date,
            "duration_min": self.duration_min,
            # "data": self.data.to_dict(orient='list')
        }

    def _parse_fit(self):
        # Extracts timestamp and heart_rate (and speed/power if available)
        records = []
        for record in self.fitfile.get_messages("record"):
            records.append(record.get_values())
        return pd.DataFrame(records)

    def calculate_trimp(self, hr_rest=60, hr_max=190, gender="male"):
        """Calculates TRIMP using the Edwards method (Zone-based) or Banister."""
        if "heart_rate" not in self.data.columns:
            return 0

        hrr = (self.avg_hr - hr_rest) / (hr_max - hr_rest)

        # Banister's Formula constants
        k = 1.92 if gender == "male" else 1.67
        trimp = self.duration_min * hrr * (0.64 * np.exp(k * hrr))
        return trimp

    def estimate_vo2max(self):
        """Standard Jack Daniels / Cooper variant for running."""
        if self.type != "running" or "heart_rate" not in self.data.columns:
            return None
        # Simplified: (15 * HRmax / HRrest) - very rough!
        # Better: Use heart rate vs pace correlation
        # and adjust by elevation if available.
        return 0  # Logic for pace/HR ratio goes here

    def _detect_type(self):
        # Logic to parse the 'sport' message in FIT file
        return "running"
