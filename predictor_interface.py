import tkinter
from tkinter import ttk
from tkinter import messagebox
import threading
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from predictor_pipeline import stock_prediction


# Dictionary that matches company names with their abbreviations.
abbreviations = {
    "Google": "GOOG", "Apple": "AAPL", "Tesla": "TSLA", "Amazon": "AMZN",
    "Berkshire Hathaway Inc.": "BRK-B", "Johnson & Johnson": "JNJ",
    "JPMorgan Chase & Co.": "JPM","Visa Inc.": "V","Mastercard Incorporated": "MA",
    "Walmart Inc.": "WMT", "The Coca-Cola Company": "KO", "NVIDIA Corporation": "NVDA",
    "Home Depot, Inc.": "HD","Walt Disney Company": "DIS", "McDonald's Corporation": "MCD",
    "International Business Machines Corporation (IBM)": "IBM","Starbucks Corporation": "SBUX",
    "Netflix, Inc.": "NFLX", "Pfizer Inc.": "PEE", "Microsoft Corporation": "MSFT",
    "Facebook": "META", "Alibaba Group Holding Limited": "BABA"}

def comboFunction(event):
    selected_company = combo.get()
    # Changing the selected company name with abbreviation.
    selected_company = abbreviations.get(selected_company, selected_company)
    print(f"Selected company: {selected_company}")

window = tkinter.Tk()
window.title("Stock Price Predictor")
window.geometry("800x600")

# Logo
window.iconbitmap(r"spp.ico")

# Progress bar
progress_bar = ttk.Progressbar(window, mode='indeterminate')
progress_bar.pack(fill=tkinter.X, pady=10)

def predict():
    selected_company = combo.get()
    selected_company = abbreviations.get(selected_company, selected_company)
    print(f"Predicting for: {selected_company}")

    # Show the progress bar
    progress_bar.start()

    forecast_period = int(combo_forecast_period.get())

    def perform_prediction():
        try:
            df = stock_prediction(selected_company, forecast_period)
            x = df.index
            y = df['yhat']
            ax.clear()
            ax.plot(x, y, marker='o')
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.set_title(selected_company)
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Error",
                                 f"An error occurred during the prediction process: {str(e)}")

        progress_bar.stop()

    thread = threading.Thread(target=perform_prediction)
    thread.start()

title_label = ttk.Label(window, text="Stock Price Predictor", font=("Times New Roman", 20))
title_label.pack(pady=10)


combo = ttk.Combobox(window, values=["Google", "Apple", "Tesla", "Amazon",
                                     "Berkshire Hathaway Inc.", "Johnson & Johnson",
                                     "JPMorgan Chase & Co.", "Visa Inc.",
                                     "Mastercard Incorporated", "Walmart Inc.",
                                     "The Coca-Cola Company", "NVIDIA Corporation",
                                    "Home Depot, Inc.", "Walt Disney Company",
                                     "McDonald's Corporation", "International Business Machines Corporation (IBM)",
                                     "Starbucks Corporation", "Netflix, Inc.", "Pfizer Inc.",
                                     "Microsoft Corporation", "Facebook", "Alibaba Group Holding Limited"],
                     justify="center")
combo.pack(fill=tkinter.X)
combo.set("Select Company")
combo.bind("<<ComboboxSelected>>", comboFunction)

# Combobox forecast period
forecast_period_values = list(range(1, 13))
combo_forecast_period = ttk.Combobox(window, values=forecast_period_values, justify="center")
combo_forecast_period.pack(fill=tkinter.X)
combo_forecast_period.set("Select Forecast Period")

predict_button = tkinter.Button(window, text="Predict", command=predict)
predict_button.pack(fill=tkinter.X)

graph_frame = tkinter.Frame(window)
graph_frame.pack(fill=tkinter.BOTH, expand=True)

fig = plt.Figure()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

ax = fig.add_subplot(111)

toolbar = NavigationToolbar2Tk(canvas, graph_frame)
toolbar.update()
canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

created_by_label = tkinter.Label(window, text="Created by Baran Yalçın", font=("Times New Roman", 8, "italic"))
created_by_label.pack(side="bottom", anchor="se", padx=10, pady=10)

window.mainloop()