import os
import tkinter
from tkinter import filedialog, Label, Entry, Button, OptionMenu, StringVar, Checkbutton, BooleanVar
from tkinter.messagebox import showinfo, showerror
import pandas as pd
import main_plot
from idlelib.tooltip import Hovertip

if __name__ == '__main__':

    root = tkinter.Tk()
    root.title('Wind Rose Plot')
    Label(root, text="CSV file with Wind speed and direction:").grid(row=1, column=1, sticky=tkinter.E)

    sv_path = StringVar()
    txt_path = Entry(root, textvariable=sv_path, width=50)
    txt_path.grid(row=2, columnspan=2)

    options = ['']
    sv_dir = StringVar(root)
    #list_val.set(dir_options[1])  # default value

    def locate_click():
        path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("txt files", "*.csv"), ("all files", "*.*")))
        if os.path.isfile(path):
            sv_path.set(path)
            update_dropdowns(path)
        # showinfo(title='Selected Files', message=path)


    Button(root, text="Locate", command=locate_click).grid(row=1, column=2)
    Label(root, text="Wind direction field name:").grid(row=3, column=1, sticky=tkinter.E)
    listbox_dir = OptionMenu(root, sv_dir, *options)
    listbox_dir.grid(row=3, column=2)

    sv_speed = StringVar(root)
    Label(root, text="Speed field name:").grid(row=4, column=1, sticky=tkinter.E)
    listbox_speed = OptionMenu(root, sv_speed, *options)
    listbox_speed.grid(row=4, column=2)

    var_use_percent = BooleanVar()
    Checkbutton(root, text='Use percentage on spokes', variable=var_use_percent, onvalue=1, offvalue=0)\
        .grid(row=5, columnspan=2)

    var_use_box = BooleanVar()
    Checkbutton(root, text='Use box instead of bar', variable=var_use_box, onvalue=1, offvalue=0)\
        .grid(row=6, columnspan=2)

    Label(root, text="Radii:").grid(row=7, column=1, sticky=tkinter.E)
    sv_radii = StringVar(root)
    txt_radii = Entry(root, textvariable=sv_radii)
    txt_radii.grid(row=7, column=2)
    Hovertip(txt_radii, 'Comma separated list of numbers.\n'
                        'This is used to overwrite the grid. Default is 5 devisions on your data.')

    Label(root, text="Bins:")\
        .grid(row=8, column=1, sticky=tkinter.E)
    sv_bins = StringVar(root)
    txt_bins = Entry(root, textvariable=sv_bins)
    txt_bins.grid(row=8, column=2)
    Hovertip(txt_bins, 'Either an integer or a comma separated list of numbers.')

    sv_title = StringVar(root)
    Label(root, text="title:").grid(row=9, column=1, sticky=tkinter.E)
    Entry(root, textvariable=sv_title).grid(row=9, column=2)

    def update_dropdowns(path):
        try:
            file = pd.read_csv(open(path, 'r'), iterator=True)
            fields = [col for col in file.get_chunk(1)]
            update_dropdowns_with_column_names(fields)
        except Exception as ex:
            showerror(title='Failed to read csv file', message=ex)

    def path_enter_handler(event):
        path = sv_path.get()
        update_dropdowns(path)

    def update_dropdowns_with_column_names(fields):
        # now update the lists:
        menu = listbox_dir["menu"]
        menu.delete(0, "end")
        found_match = False
        for v in fields:
            menu.add_command(label=v,
                             command=lambda value=v: sv_dir.set(value))
            if 'dir' in v.lower():
                found_match = True
                sv_dir.set(v)

        if not found_match:
            sv_dir.set(fields[0])

        found_match = False
        menu = listbox_speed["menu"]
        menu.delete(0, "end")
        for v in fields:
            menu.add_command(label=v,
                             command=lambda value=v: sv_speed.set(value))
            if 'speed' in v.lower():
                found_match = True
                sv_speed.set(v)

        if not found_match:
            sv_speed.set(fields[1])

    txt_path.bind('<Return>', path_enter_handler)

    def plot_click():
        path = sv_path.get()
        if not os.path.isfile(path):
            showerror(title='Invalid path', message='You have specified an invalid path')
            return
        dir_field_name = sv_dir.get()
        speed_field_name = sv_speed.get()
        use_percent = var_use_percent.get()
        use_box = var_use_box.get()
        bins = None
        bins_str = sv_bins.get()
        if ',' in bins_str:
            bins = [float(v) for v in bins_str.split(',')]
        elif bins_str.isnumeric():
            bins = int(bins_str)

        if dir_field_name == '' or speed_field_name == '':
            update_dropdowns(path)
            dir_field_name = sv_dir.get()
            speed_field_name = sv_speed.get()

        if dir_field_name == '' or speed_field_name == '':
            showerror(title='Select Field Names', message='You must select the wind speed and direction field names')

        radii = None
        radii_str = sv_radii.get()
        if ',' in radii_str:
            radii = [float(v) for v in radii_str.split(',')]
        title = sv_title.get()
        main_plot.plot(path, dir_field_name=dir_field_name, speed_field_name=speed_field_name,
                       use_percent=use_percent, use_box=use_box, bins=bins, radii=radii,
                       title=title)


    btn_plot = Button(root, text="Plot", command=plot_click).grid(row=10, columnspan=2)

    root.mainloop()
