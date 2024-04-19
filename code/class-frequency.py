import os
import re
import matplotlib.pyplot as plt

input_path = "../dataset/ablation"
output_path = "../graph-metrics"
show_plot = False
top_n = 100	# To be usd for top-n to plot and display in analysis

def instanceOf_analysis(show_plot=False):
	count_of_objects = dict()

	with open(os.path.join(input_path, "iOf-test.txt"), 'r') as file:
		lines = [ line for line in file.readlines() ]
		for line in lines:
			s, p, o = line.split('\t')
			o = o.strip()
			if o not in count_of_objects:
				count_of_objects[o] = 0
			count_of_objects[o] += 1

	sorted_values = dict(sorted(count_of_objects.items(), key=lambda item: item[1], reverse=True))

	with open(os.path.join(output_path, "typing-count.txt"), "w") as f:
		f.write("Entity Typing Value Counts (All):\n")
		for q, count in sorted_values.items(): # Write sorted explicit typing counts to file
			f.write(f"{q}: {count}\n")

	if(show_plot):
		# Histogram of first 100 most frequent values.
		top_n_values = dict(list(sorted_values.items())[:top_n])
		q_labels = [q for q in top_n_values.keys()]
		q_counts = list(top_n_values.values())

		plt.figure(figsize=(12, 6))
		plt.bar(q_labels, q_counts)
		plt.xlabel('Explicit Typings')
		plt.ylabel('Frequency')
		plt.title(f'Top {top_n} Most Frequent Explicit Typings')
		plt.xticks(rotation=90)
		plt.tight_layout()
		plt.show()

def subClassOf_analysis(show_plot=False):
	count_of_objects = dict()

	with open(os.path.join(input_path, "sco-test.txt"), 'r') as file:
		lines = [ line for line in file.readlines() ]
		for line in lines:
			s, p, o = line.split('\t')
			o = o.strip()
			if o not in count_of_objects:
				count_of_objects[o] = 0
			count_of_objects[o] += 1
	
	sorted_values = dict(sorted(count_of_objects.items(), key=lambda item: item[1], reverse=True))

	with open(os.path.join(output_path, "subclass-count.txt"), "w") as f:
		f.write("Subclass Value Counts (All):\n")
		for q, count in sorted_values.items(): # Write sorted explicit typing counts to file
			f.write(f"{q}: {count}\n")

	if(show_plot):
		# Histogram of first 100 most frequent values.
		top_n_values = dict(list(sorted_values.items())[:top_n])
		q_labels = [q for q in top_n_values.keys()]
		q_counts = list(top_n_values.values())

		plt.figure(figsize=(12, 6))
		plt.bar(q_labels, q_counts)
		plt.xlabel('Explicit Typings')
		plt.ylabel('Frequency')
		plt.title(f'Top {top_n} Most Frequent Explicit Typings')
		plt.xticks(rotation=90)
		plt.tight_layout()
		plt.show()


if __name__ == "__main__":
	instanceOf_analysis(show_plot)
	subClassOf_analysis(show_plot)