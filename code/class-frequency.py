import re
import matplotlib.pyplot as plt

file_path = "/Users/andreachristou/Documents/git/kge-impact/dataset/ablation/iOf-test.txt"


q_values = {}

# Reads through the iOf-test file and finds all the Q-values.
with open(file_path, 'r') as file:
  for line in file:
    matches = re.findall(r'Q(\d+)', line)
    for match in matches:
      if match not in q_values:
        q_values[match] = 0
      q_values[match] += 1

# It sorts them.
sorted_q_values = dict(sorted(q_values.items(), key=lambda item: item[1], reverse=True))

# Top 100 used in the histogram for ease of vizualization.
top_n = 100

# Saved in a dictonary to count the unique values without the Q.
top_q_values = dict(list(sorted_q_values.items())[:top_n])

# Saved each variable count in the text file found in frequency folder.
with open("iOf-class-count.txt", "w") as f:
  f.write("Q Value Counts (All):\n")
  for q, count in q_values.items():
    f.write(f"Q{q}: {count}\n")


q_labels = ["Q" + q for q in top_q_values.keys()]
q_counts = list(top_q_values.values())

# Histogram of first 100 most frequent values.
plt.figure(figsize=(12, 6))


plt.bar(q_labels, q_counts)
plt.xlabel('Q Values')
plt.ylabel('Frequency')
plt.title(f'Top {top_n} Most Frequent Q Values')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
