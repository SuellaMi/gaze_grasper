import tkinter as tk
import Arm_Controller

# Initialize window
root = tk.Tk()

# Create text output
l1 = tk.Label(root, text="Robotic Arm Controller")
l2 = tk.Label(root, text="DXL1:")
l3 = tk.Label(root, text="DXL2:")
l4 = tk.Label(root, text="DXL3:")

# Display text in GUI
l1.grid(row=0, column=0)
l2.grid(row=1, column=0)
l3.grid(row=2, column=0)
l4.grid(row=3, column=0)

# Create first entry field
# Call variablenname.get() to get the degrees
entry1 = tk.StringVar()
field1 = tk.Entry(root, textvariable=entry1)

# Create second entry field
entry2 = tk.StringVar()
field2 = tk.Entry(root, textvariable=entry2)

# Create third entry field
entry3 = tk.StringVar()
field3 = tk.Entry(root, textvariable=entry3)

# Display entry fields
field1.grid(row=1, column=1)
field2.grid(row=2, column=1)
field3.grid(row=3, column=1)

# Create OK button to start movement
MovingBtn = tk.Button(root, text="OK")
MovingBtn.grid(row=1, column=2)
# Call moving function
MovingBtn.bind('<ButtonPress-1>', Arm_Controller.start_moving)

tk.Button(root, text="Quit", command=root.destroy).grid(column=1, row=4)

# Infinite loop which can be terminated by keyboard or mouse interrupt
root.mainloop()
