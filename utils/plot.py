import matplotlib.pyplot as plt

def plot_G(data, title="Graph", xlabel="Timeline", ylabel="Value"):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Timestamp'], data['Value'], marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()
