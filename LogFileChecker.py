"""Creates a GUI for parsing out meta log data for recording from Bruker Skyscan 1173 log files."""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdlg
from pathlib import Path
import pandas as pd


class MainWindow(tk.Tk):
    """class representing the overall gui window"""

    def __init__(self):
        super().__init__()
        self.title("Log File Checker")
        # self.geometry("1250x780+20+20")
        self.target_archive_file = ""
        self.target_dir = ""
        self.data_dict = {}
        self.sheet_name = "Sheet1"

        # Title Frame
        title_frame = ttk.Frame(
            master=self,
        )
        title_frame.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W + tk.E)
        title_frame.columnconfigure(0, weight=1)

        # Main Title
        self.main_title_label = ttk.Label(
            master=title_frame,
            text="Log File Check Tool",
            relief=tk.FLAT,
            font=("Times New Roman", 18, "bold"),
        )
        self.main_title_label.grid(
            row=0, column=0, columnspan=4, rowspan=1, ipadx=5, pady=0, sticky=tk.S
        )

        # Version Label
        self.version_title_label = ttk.Label(
            master=title_frame,
            text="v1.0.0",
            font=("Times New Roman", 8, "italic"),
        )
        self.version_title_label.grid(
            row=1, column=0, columnspan=4, rowspan=1, padx=0, pady=0, sticky=tk.N
        )

        # Separate Title from Rest of Application
        sep_1 = ttk.Separator(master=self, orient="horizontal")
        sep_1.grid(row=1, column=0, sticky="nesw")

        # Start Frame
        start_frame = ttk.Frame(
            master=self,
        )
        start_frame.grid(
            column=0, row=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )
        start_frame.columnconfigure(1, weight=1)
        self.select_archive_file_button = ttk.Button(
            master=start_frame,
            text="Select Archive File",
            command=self.select_archive_file,
        )
        self.select_archive_file_button.grid(
            row=0, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )

        self.select_archive_label_frame = ttk.LabelFrame(
            master=start_frame,
            text="Selected Archive File",
            height=2,
        )
        self.select_archive_file_label = ttk.Label(
            master=self.select_archive_label_frame,
            text="",
            width=130,
            anchor=tk.W,
        )
        self.select_archive_label_frame.grid(
            row=0, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )
        self.select_archive_file_label.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.N + tk.W + tk.E,
        )

        self.archivefilekeep_yesno = tk.IntVar()
        self.keep_archive_file_checkbutton = ttk.Checkbutton(
            master=start_frame,
            text="Keep when reset?",
            onvalue=1,
            offvalue=0,
            variable=self.archivefilekeep_yesno,
        )
        self.keep_archive_file_checkbutton.grid(
            row=0,
            column=6,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.W + tk.N + tk.S,
        )
        self.archivefilekeep_yesno.set(value=0)

        self.select_folders_button = ttk.Button(
            master=start_frame,
            text="Select Data Folder(s)",
            command=self.select_folders,
        )
        self.select_folders_button.grid(
            row=1, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )
        self.select_folders_label_frame = ttk.LabelFrame(
            master=start_frame,
            text="Selected Folder(s)",
            height=2,
        )
        self.select_folders_label = ttk.Label(
            master=self.select_folders_label_frame,
            text="",
            width=130,
        )
        self.select_folders_label_frame.grid(
            row=1, column=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )
        self.select_folders_label.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.N + tk.W + tk.E,
        )
        self.one_or_many_frame = ttk.LabelFrame(
            master=start_frame,
            text="One or Many",
            height=2,
        )
        self.one_or_many_frame.grid(
            column=6, row=1, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W + tk.E
        )
        self.one_or_many_var = tk.IntVar()

        self.one_folder = ttk.Radiobutton(
            master=self.one_or_many_frame,
            text="One Folder",
            variable=self.one_or_many_var,
            value=0,
        )
        self.many_folder = ttk.Radiobutton(
            master=self.one_or_many_frame,
            text="Many Folders",
            variable=self.one_or_many_var,
            value=1,
        )
        self.one_folder.grid(
            row=0, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W
        )
        self.many_folder.grid(
            row=1, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.W
        )
        self.one_or_many_var.set(1)
        self.check_files_button = ttk.Button(
            master=start_frame,
            text="Check for Log Files",
            command=self.check_log_files,
        )
        self.check_files_button.grid(
            row=2, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.E + tk.W
        )

        # Separate Inputs from Display Portion of App
        sep_2 = ttk.Separator(master=self, orient="horizontal")
        sep_2.grid(row=2, column=0, sticky="nesw")

        input_frame = ttk.Frame(
            master=self,
        )
        input_frame.grid(
            column=0,
            row=2,
            columnspan=1,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.W + tk.E + tk.N + tk.S,
        )

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)
        input_frame.columnconfigure(3, weight=1)
        input_frame.columnconfigure(4, weight=1)

        self.empty_folders_label = ttk.Label(
            master=input_frame,
            text="Empty Folders",
            font=("Times New Roman", 9, "bold underline"),
        )
        self.empty_folders_label.grid(
            row=0, column=0, columnspan=2, rowspan=1, padx=5, pady=0, sticky=tk.W + tk.S
        )
        self.empty_folders_textvar = tk.StringVar()
        self.empty_folders_display = tk.Listbox(
            master=input_frame, listvariable=self.empty_folders_textvar, width=35
        )
        self.empty_folders_display.grid(
            row=1,
            column=0,
            columnspan=2,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.W + tk.N + tk.E,
        )
        self.empty_folders_textvar.set(value="")

        self.log_files_in_archive_label = ttk.Label(
            master=input_frame,
            text="Log Files in Archive",
            font=("Times New Roman", 9, "bold underline"),
        )
        self.log_files_in_archive_label.grid(
            row=0, column=2, columnspan=2, rowspan=1, padx=5, pady=0, sticky=tk.W + tk.S
        )
        self.log_files_in_archive_textvar = tk.StringVar()
        self.log_files_in_archive_display = tk.Listbox(
            master=input_frame, listvariable=self.log_files_in_archive_textvar, width=35
        )
        self.log_files_in_archive_display.grid(
            row=1,
            column=2,
            columnspan=2,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.W + tk.N + tk.E,
        )
        self.log_files_in_archive_textvar.set(value="")

        self.log_files_not_in_archive_label = ttk.Label(
            master=input_frame,
            text="Log Files NOT in Archive",
            font=("Times New Roman", 9, "bold underline"),
        )
        self.log_files_not_in_archive_label.grid(
            row=0, column=4, columnspan=2, rowspan=1, padx=5, pady=0, sticky=tk.W + tk.S
        )
        self.log_files_not_in_archive_textvar = tk.StringVar()
        self.log_files_not_in_archive_display = tk.Listbox(
            master=input_frame,
            listvariable=self.log_files_not_in_archive_textvar,
            width=35,
        )
        self.log_files_not_in_archive_display.grid(
            row=1,
            column=4,
            columnspan=2,
            rowspan=1,
            padx=5,
            pady=5,
            sticky=tk.W + tk.N + tk.E,
        )
        self.log_files_not_in_archive_textvar.set(value="")

        output_frame = ttk.Frame(
            master=self,
        )
        output_frame.grid(
            column=0, row=4, columnspan=1, rowspan=1, padx=5, pady=5, sticky=tk.E
        )

        self.reset_clear_button = ttk.Button(
            master=output_frame,
            text="Reset / Clear",
            command=self.reset_gui,
        )
        self.reset_clear_button.grid(
            row=2, column=1, columnspan=1, rowspan=2, padx=5, pady=5, sticky=tk.E
        )

    ## Functions for Buttons

    # Select the Archive File to compare log file names to
    def select_archive_file(self):
        """opens a file dialog asking the user to select an
        archive file where the data will be referenced to"""
        selected_destination_file = fdlg.askopenfilename()
        self.select_archive_file_label.configure(text=str(selected_destination_file))
        self.target_archive_file = selected_destination_file

    # Select the folder that either contains log files or folders with log files in them
    def select_folders(self):
        """opens a file dialog asking the user to select folders
        from which log files will be referenced"""
        target_dir = str(fdlg.askdirectory())
        self.select_folders_label.configure(text=str(target_dir))
        self.target_dir = target_dir

    # Check to see if log files read in appear in the archive file
    def check_log_files(self):
        """Check log files to display which ones need to be logged and which do not."""
        log_extension = ".log"
        log_file_list = []
        sub_dir_list = []
        empty_list = []
        in_archive_list = []
        not_in_archive_list = []
        # If an archive file was selected
        if self.target_archive_file != "":
            # If a directory was selected
            if self.target_dir != "":
                directory_path = Path(self.target_dir)
                folder_contents = os.listdir(directory_path)
                # If the selected directory has its own log files
                if int(self.one_or_many_var.get()) == 0:
                    if not folder_contents:
                        empty_list.append(directory_path)
                    else:
                        for each_file_or_folder in folder_contents:
                            # current_file = Path(self.target_dir,each_file_or_folder)
                            if Path(each_file_or_folder).suffix == log_extension:
                                log_file_list.append(
                                    Path(self.target_dir, each_file_or_folder)
                                )
                            else:
                                pass
                # If the selected directory has other subdirectories with their own log files
                elif int(self.one_or_many_var.get()) == 1:
                    sub_dir_list = [x for x in directory_path.iterdir() if x.is_dir()]
                    if len(sub_dir_list) != 0:
                        for each_sub_dir in sub_dir_list:
                            sub_folder_contents = os.listdir(each_sub_dir)
                            if not sub_folder_contents:
                                empty_list.append(str(each_sub_dir.stem))
                            else:
                                for each_file_or_folder in sub_folder_contents:
                                    if (
                                        Path(each_file_or_folder).suffix
                                        == log_extension
                                    ):
                                        log_file_list.append(
                                            Path(self.target_dir, each_file_or_folder)
                                        )
                                    else:
                                        pass
                    else:
                        print(
                            "No Subdirectories identified in directory. Please fix and try again."
                        )
                archive_file = Path(self.target_archive_file)
                wb = pd.read_excel(archive_file, sheet_name=self.sheet_name)
                for each_log_file in log_file_list:
                    if each_log_file.stem in wb.Filename.values:
                        in_archive_list.append(each_log_file.stem)
                    else:
                        not_in_archive_list.append(each_log_file.stem)
                for each_item in empty_list:
                    self.empty_folders_display.insert(tk.END, each_item)
                for each_item in in_archive_list:
                    self.log_files_in_archive_display.insert(tk.END, each_item)
                for each_item in not_in_archive_list:
                    self.log_files_not_in_archive_display.insert(tk.END, each_item)

            else:
                print(
                    "A targeted directory needs to be selected. Please select one and try again."
                )
        else:
            print(
                "An Archive File needs to be selected. Please select one and try again."
            )

    # Reset GUI for subsequent use in checking more log files
    def reset_gui(self):
        """Reset GUI for subsequent use"""
        if int(self.archivefilekeep_yesno.get()) == 0:
            self.select_archive_file_label.configure(text="")
        self.select_folders_label.configure(text="")
        self.empty_folders_display.delete(0, tk.END)
        self.log_files_in_archive_display.delete(0, tk.END)
        self.log_files_not_in_archive_display.delete(0, tk.END)


if __name__ == "__main__":
    root = MainWindow()  # Create a MainWindow Object labeled root
    root.mainloop()  # Run root through the mainloop
