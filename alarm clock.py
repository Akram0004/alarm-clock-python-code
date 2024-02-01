from tkinter import *
from tkinter import simpledialog
import datetime
import time
import winsound
from threading import Thread

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.alarms = []

        # Set background color and window size
        self.root.configure(bg="#2C3E50")
        self.root.geometry("600x600")

        # Title label
        Label(root, text="Alarm Clock", font=("Helvetica", 36, "bold"), fg="#ffffff", bg="#2C3E50").pack(pady=20)

        # Clock display
        self.clock_label = Label(root, font=("Helvetica", 48), fg="#ffffff", bg="#2C3E50")
        self.clock_label.pack()

        # Date entry
        Label(root, text="Enter Date for Alarm (YYYY-MM-DD):", font=("Helvetica", 14), fg="#ffffff", bg="#2C3E50").pack()
        self.date_entry = Entry(root, font=("Helvetica", 14))
        self.date_entry.pack()

        # Time frame
        time_frame = Frame(root, bg="#2C3E50")
        time_frame.pack(pady=(20, 0))

        # Hour dropdown
        Label(time_frame, text="Hour:", font=("Helvetica", 14), fg="#ffffff", bg="#2C3E50").grid(row=0, column=0, padx=5)
        self.hour = Spinbox(time_frame, from_=0, to=23, width=3, font=("Helvetica", 14))
        self.hour.grid(row=0, column=1)

        # Minute dropdown
        Label(time_frame, text="Minute:", font=("Helvetica", 14), fg="#ffffff", bg="#2C3E50").grid(row=0, column=2, padx=5)
        self.minute = Spinbox(time_frame, from_=0, to=59, width=3, font=("Helvetica", 14))
        self.minute.grid(row=0, column=3)

        # Second dropdown
        Label(time_frame, text="Second:", font=("Helvetica", 14), fg="#ffffff", bg="#2C3E50").grid(row=0, column=4, padx=5)
        self.second = Spinbox(time_frame, from_=0, to=59, width=3, font=("Helvetica", 14))
        self.second.grid(row=0, column=5)

        # Set alarm button
        Button(root, text="Set Alarm", font=("Helvetica", 16), command=self.set_alarm, bg="#16A085", fg="#ffffff").pack(pady=20)

        # Alarm listbox
        Label(root, text="Alarms", font=("Helvetica", 24, "bold"), fg="#ffffff", bg="#2C3E50").pack()
        self.alarm_listbox = Listbox(root, width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#333333")
        self.alarm_listbox.pack(pady=10)

        # Buttons frame
        buttons_frame = Frame(root, bg="#2C3E50")
        buttons_frame.pack()

        # Edit alarm button
        Button(buttons_frame, text="Edit Alarm", font=("Helvetica", 14), command=self.edit_alarm, bg="#2980B9", fg="#ffffff").grid(row=0, column=0, padx=5)

        # Delete alarm button
        Button(buttons_frame, text="Delete Alarm", font=("Helvetica", 14), command=self.remove_alarm, bg="#E74C3C", fg="#ffffff").grid(row=0, column=1, padx=5)

        # Snooze alarm button
        Button(buttons_frame, text="Snooze Alarm", font=("Helvetica", 14), command=self.snooze_alarm, bg="#F39C12", fg="#ffffff").grid(row=0, column=2, padx=5)

        # Update clock
        self.update_clock()

    def update_clock(self):
        # Update clock label
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)

        # Update every second
        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        # Get selected date and time
        selected_date = self.date_entry.get()
        selected_time = f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"

        # Combine date and time
        try:
            alarm_datetime = datetime.datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        # Add alarm to listbox
        self.alarm_listbox.insert(END, f"{selected_date} {selected_time}")

        # Start alarm thread
        t1 = Thread(target=self.alarm, args=(alarm_datetime,))
        t1.start()

    def alarm(self, alarm_datetime):
        # Wait for alarm time and play sound
        while True:
            current_time = datetime.datetime.now()
            if current_time >= alarm_datetime:
                print("Time to Wake up")
                winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
                self.flash_window()
                break
            time.sleep(1)

    def flash_window(self):
        # Flash the window to get user's attention
        for _ in range(3):
            self.root.iconify()
            self.root.update()
            time.sleep(0.5)
            self.root.deiconify()
            self.root.update()

    def edit_alarm(self):
        # Get selected alarm
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            selected_alarm = self.alarm_listbox.get(index)

            # Prompt user to edit alarm time
            new_time = simpledialog.askstring("Edit Alarm", "Enter new time (HH:MM:SS):", parent=self.root)
            if new_time:
                # Update alarm time in listbox
                self.alarm_listbox.delete(index)
                self.alarm_listbox.insert(index, f"{selected_alarm.split()[0]} {new_time}")

    def remove_alarm(self):
        # Remove selected alarm from listbox
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            self.alarm_listbox.delete(index)

    def snooze_alarm(self):
        # Get selected alarm
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            selected_alarm = self.alarm_listbox.get(index)

            # Prompt user to enter snooze duration
            snooze_time = simpledialog.askinteger("Snooze Alarm", "Enter snooze duration in minutes:", parent=self.root)
            if snooze_time:
                # Calculate new alarm time
                new_alarm_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_time)

                # Add snoozed alarm to listbox
                self.alarm_listbox.insert(index, f"{new_alarm_time.strftime('%Y-%m-%d %H:%M:%S')} (Snoozed)")

                # Start snoozed alarm thread
                t1 = Thread(target=self.alarm, args=(new_alarm_time,))
                t1.start()


if __name__ == "__main__":
    root = Tk()
    root.title('Alarm-Clock')
    alarm_clock = AlarmClock(root)
    root.mainloop()
