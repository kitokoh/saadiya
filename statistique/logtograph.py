import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.data = self.parse_log()

    def parse_log(self):
        log_entries = []
        with open(self.log_file, 'r') as file:
            for line in file:
                # Regex to extract timestamp and message
                match = re.match(r"(\S+ \S+) - \S+ - INFO - (.+)", line)
                if match:
                    timestamp_str, message = match.groups()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                    log_entries.append((timestamp, message))
        return pd.DataFrame(log_entries, columns=['timestamp', 'message'])

    def count_posts(self):
        # Count occurrences of "post done"
        post_done_count = self.data[self.data['message'].str.contains('post done')].shape[0]
        return post_done_count

    def analyze_hashtags(self):
        # Extract hashtags from messages
        hashtags = []
        for message in self.data['message']:
            hashtags.extend(re.findall(r'#\w+', message))
        hashtag_counts = pd.Series(hashtags).value_counts()
        return hashtag_counts

    def plot_data(self):
        hashtag_counts = self.analyze_hashtags()
        plt.figure(figsize=(10, 6))
        hashtag_counts[:10].plot(kind='bar', color='skyblue')
        plt.title('Top 10 Hashtags')
        plt.xlabel('Hashtags')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    log_analyzer = LogAnalyzer('path/to/your/log.txt')
    print("Total 'post done' count:", log_analyzer.count_posts())
    log_analyzer.plot_data()
