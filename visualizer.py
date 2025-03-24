# Original from CarbonSheild and tyborg
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 


# Function to parse the log file and extract relevant damage data
def parse_damage_log(file_path, spot):
    # Define regex patterns for send and receive lines
    send_pattern = r"Match damage send: Id: (\d+) Type: (\w+) type: (\w+) region: (\w+) movement: (\w*) weakPoint: (\w*) amount: ([\d.]+). closest neutral corner: (\w+)"
    #receive_pattern = r"Match damage received: Id: (\d+) Type: (\w+), type: (\w+) region: (\w+) weakPoint: (\w*) movementType:(\w*) amount: ([\d.]+)"
    receive_pattern = r"Match damage received: Id: (\d+) Type: (\w+), type: (\w+) region: (\w+) weakPoint: (\w*) movementType: (\w*) amount: ([\d.]+)"
   
    split_pattern = r"Match Results: (\w+), Blue: (\d+), Red: (\d+)"
    player_pattern = r"OnPlayerJoined: \[(\d+)\] (\w+)"

    # List to store parsed data
    parsed_data = []
    players = []
    


    # Open the file and read line by line
    with open(file_path, 'r') as file:
        match_spot = -1

        for line_num, line in enumerate(file):
            if line_num < spot:
                continue
            # Try to match the "send" pattern
            send_match = re.search(send_pattern, line)
            if send_match:
                print("punch found")
                timestamp = line.split(']')[0][1:]  # Extract timestamp
                parsed_data.append({
                    'Timestamp': timestamp,
                    "who": "Opponent",
                    'Player': send_match.group(2),
                    'DamageType': send_match.group(3),
                    'Region': send_match.group(4),
                    "movement": send_match.group(5),
                    'WeakPoint': send_match.group(6) if send_match.group(6) else 'None',
                    'Amount': float(send_match.group(7)),
                    'Action': 'Send'
                })

            # Try to match the "receive" pattern
            receive_match = re.search(receive_pattern, line)
            if receive_match:
                print("punch found")
                timestamp = line.split(']')[0][1:]  # Extract timestamp
                parsed_data.append({
                    'Timestamp': timestamp,
                    "who": "You",
                    'Player': receive_match.group(2),
                    'DamageType': receive_match.group(3),
                    'Region': receive_match.group(4),
                    'WeakPoint': receive_match.group(5) if receive_match.group(5) else 'None',
                    "movement": receive_match.group(6),
                    'Amount': float(receive_match.group(7)),
                    'Action': 'Receive'
                })
            
            player = re.search(player_pattern, line)
            if player:
                print("players found")
                players.append(player.group(2))
            
            endmatch = re.search(split_pattern, line)
            if endmatch:
                match_spot = line_num
                match_re = {
                    "Line": line_num,
                    "Blue": endmatch.group(1),
                    "Red": endmatch.group(2)
                }
                break




    return (parsed_data, players, match_spot)

# Function to convert timestamp string to datetime
def convert_to_datetime(timestamp_str):
    global mintime
    return (datetime.strptime(timestamp_str, '%H:%M:%S.%f') - mintime).total_seconds()

# Function to visualize the damage over time
def plot_damage_over_time(data):
    global mintime
    # Create a DataFrame
    df = pd.DataFrame(data)
    # Convert the 'Timestamp' column to datetime
    #print(df)
    #print(df[df['who'] == "You"])
    #
    
    mintime = datetime.strptime(df['Timestamp'].min(0), '%H:%M:%S.%f')

    df['Timestamp'] = df['Timestamp'].apply(convert_to_datetime)

    # Plotting
    #fig = plt.figure(figsize=(10, 6))

    fig, ax = plt.subplots()
    
    # Plot damage over time for both Send and Receive




    for index, row in df.iterrows():

        awaysqr = [(0,4),(4,0), (4,-4), (-4,-4), (-4,0)]
        downsqr = [(0,-4),(4,0), (4,4), (-4,4), (-4,0)]

        if row['Player'] == "PlayerBlue": col = "blue"
        else: col = "red"
        if row["Region"] == "Head": 
            if row["movement"] == "MovingIntoPunch": mark = "v"
            elif row["movement"] == "MovingAwayFromPunch": mark = "^"
            else: mark = "o"
        
        else: 
            if row["movement"] == "MovingIntoPunch": mark = downsqr
            elif row["movement"] == "MovingAwayFromPunch": mark = awaysqr
            else: mark = "s"




        if row["DamageType"] == "Hit" or row["DamageType"] == "None": ax.scatter(row['Timestamp'], row['Amount'], c=col, s = 35, marker = mark)
        else: ax.scatter(row['Timestamp'], row['Amount'], c=col, edgecolors='black', s = 60, linewidths=2, marker = mark)
        
    
    fig.set_size_inches(17, 4)
    ax.grid(axis = 'y')
    ax.set_title('Damage Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Damage Amount')
    ax.legend()
    #ax.set_xticks(rotation=0)
    #ax.tight_layout()
    return fig



def punchData(dlist):
    Table = []
    tsum = dlist["Amount"].shape[0]
    dsum = sum(dlist["Amount"])
    hsum = dlist[dlist['DamageType'] != "None"].shape[0]
    Table.append({
        "reigon": "Total",
        "weakpoint": "",
        "punches": tsum,
        "punchperc": "",
        "Hittotal": hsum,
        "Hitperc": "",
        "damage": dsum,
        "damagepercent": ""
        })
    print(tsum)
    print(dsum)
    for reigon in ["Head", "Body"]:
        
        if reigon == "Head":
            hlist = dlist[dlist["Region"] == "Head"]
        else: hlist = dlist[dlist["Region"] != "Head"]

        rpsum = hlist["Amount"].shape[0]
        print(hlist['DamageType'] != "None")
        rhsum = hlist[hlist['DamageType'] != "None"].shape[0]

        rdsum = sum(hlist["Amount"])
        Table.append({
        "reigon": reigon,
        "weakpoint": "Total",
        "punches": rpsum,
        "punchperc": rpsum/tsum,
        "Hittotal": rhsum,
        "Hitperc": rhsum/hsum,
        "damage": rdsum,
        "damagepercent": rdsum/dsum
        })

        for wp in hlist["Region"].unique():
            
            wblist = hlist[hlist["WeakPoint"] == "None"]
            wlist = wblist[wblist["Region"] == wp]
            
            wpsum = wlist.shape[0]
            wdsum = sum(wlist["Amount"])
            whsum = wlist[wlist['DamageType'] != "None"].shape[0]
            if wp == "Shoulder": 
                print(wlist)
                print(wlist['DamageType'] != "None")
            Table.append({
            "reigon": "",
            "weakpoint": wp,
            "punches": wpsum,
            "punchperc": wpsum/tsum,
            "Hittotal": whsum,
            "Hitperc": whsum/hsum,
            "damage": wdsum,
            "damagepercent": wdsum/dsum
        })
        
        #print(hlist["WeakPoint"])
        for wp in hlist[hlist["WeakPoint"] != "None"]["WeakPoint"].unique():
            wlist = hlist[hlist["WeakPoint"] == wp]
            wpsum = wlist.shape[0]
            wdsum = sum(wlist["Amount"])
            whsum = wlist[wlist['DamageType'] != "None"].shape[0]
            Table.append({
            "reigon": "",
            "weakpoint": wp,
            "punches": wpsum,
            "punchperc": wpsum/tsum,
            "Hittotal": whsum,
            "Hitperc": whsum/hsum,
            "damage": wdsum,
            "damagepercent": wdsum/dsum
        })

    return Table

# Function to display the data as a table
def display_table(data, title):
    df = pd.DataFrame(data)
    print()
    print(title)
    print(df.to_string(index=False))

def display_tabletk(data, window):
    tk.Label(window, text = "Spot").grid(row = 0, column = 0)
    tk.Label(window, text = "Weak").grid(row = 0, column = 1)
    tk.Label(window, text = "Punch").grid(row = 0, column = 2)
    tk.Label(window, text = "Perc").grid(row = 0, column = 3)
    tk.Label(window, text = "Hit").grid(row = 0, column = 4)
    tk.Label(window, text = "Perc").grid(row = 0, column = 5)
    tk.Label(window, text = "Damage").grid(row = 0, column = 6)
    tk.Label(window, text = "perc").grid(row = 0, column = 7)
    df = pd.DataFrame(data)
    for ind, row in df.iterrows():

        if row["reigon"] != "": bold = 1
        else: bold = 0
        for i in range(0, 8):
            val = row.iloc[i]
            if type(val) != str: s = str(round(val, 2))
            else: s = val
            if bold: tk.Label(window, text = s, font=('Ariel', 11, 'bold')).grid(row = ind+1, column = i)
            else: tk.Label(window, text = s, font = ('Ariel', 9)).grid(row = ind+1, column = i)

def die(win):
    win.quit()


def dogui(damage_data, players):
    root = tk.Tk(className="MatchData")
    root.geometry("1250x700")
    
    # Allow resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    
    # Scrollable frame for tables
    def create_scrollable_frame(master, row, column):
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, sticky="nsew")
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return scrollable_frame

    # Main frames
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    root.rowconfigure(1, weight=3)

    # Opponent and player names
    if len(players) < 1:
        players.append("opponent")
    yc = "red" if damage_data[0]["Player"] == "PlayerRed" else "blue"
    oc = "blue" if yc == "red" else "red"

    tk.Label(root, text="You", fg=yc, font=("Ariel", 24)).grid(row=0, column=0)
    oppname = ttk.Combobox(root, values=players, font=("Ariel", 24), state="readonly", foreground=oc)
    oppname.current(0)
    oppname.grid(row=0, column=1)

    butt = tk.Button(root, text="Next", command=lambda: die(root))
    butt.grid(row=0, column=3)

    # Damage Data
    yourp = punchData(pd.DataFrame(damage_data)[pd.DataFrame(damage_data)["who"] == "You"])
    opponentp = punchData(pd.DataFrame(damage_data)[pd.DataFrame(damage_data)["who"] == "Opponent"])

    # Display Plot
    fig = plot_damage_over_time(damage_data)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Display Your Data
    your_table_frame = create_scrollable_frame(root, 2, 0)
    display_tabletk(yourp, your_table_frame)

    # Display Opponent Data
    opp_table_frame = create_scrollable_frame(root, 2, 1)
    display_tabletk(opponentp, opp_table_frame)

    root.mainloop()
    return 1
    




# Main function to execute the program
def main():
    file_path = filedialog.askopenfilename()
    nextspot = 0
    flag = 1
    while flag:
        damagenums, players, nextspot = parse_damage_log(file_path, nextspot+3)
        if nextspot == -1:
            break
        print(players)
        print(nextspot)
        flag = dogui(damagenums, players)



    

# Run the main function
if __name__ == "__main__":
    main()
   