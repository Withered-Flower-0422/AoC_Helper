import os
import requests
import json
import windnd
import tkinter as tk
from tkinter import Menu, filedialog, simpledialog, messagebox

from config import cfg_path
from source import src_path
from language import language

# const
VERSION = "1.2.0"
AUTHOR = "Withered Flower"
EMAIL = "2734850178@qq.com"


class AoC_Helper:
    def __init__(self):
        # create window
        self.root = tk.Tk()

        # import settings
        with open(cfg_path["settings"], "r") as f:
            settings = json.load(f)
            self.language = settings["language"]
            self.last_window_pos_x, self.last_window_pos_y = (
                settings["last_window_pos"]
                if settings["last_window_pos"] is not None
                else (
                    self.root.winfo_screenwidth() // 2 - 150,
                    self.root.winfo_screenheight() // 2 - 200,
                )
            )

        # window basic setting
        self.root.title(self.lang("AoC Helper"))
        self.root.geometry(f"300x320+{self.last_window_pos_x}+{self.last_window_pos_y}")
        self.root.resizable(False, False)
        self.root.iconbitmap(src_path["icon"])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        windnd.hook_dropfiles(self.root, self.set_path)

        # create menu
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # create settings menu
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(
            label=self.lang("Set Path"), command=self.set_path
        )
        self.settings_menu.add_command(
            label=self.lang("Set Cookies"),
            command=lambda: os.startfile(cfg_path["cookies"]),
        )
        self.menu_bar.add_cascade(label=self.lang("Settings"), menu=self.settings_menu)

        # create tools menu
        self.tools_menu = Menu(self.menu_bar, tearoff=0)
        self.tools_menu.add_command(
            label=self.lang("Create New AoC"), command=self.create_new_aoc
        )
        self.menu_bar.add_cascade(label=self.lang("Tools"), menu=self.tools_menu)

        # create language menu
        self.lang_menu = Menu(self.menu_bar, tearoff=0)
        self.lang_menu.add_command(
            label=self.lang("English"),
            command=lambda: self.set_language("en"),
        )
        self.lang_menu.add_command(
            label=self.lang("Chinese"),
            command=lambda: self.set_language("zh"),
        )
        self.menu_bar.add_cascade(label=self.lang("Language"), menu=self.lang_menu)

        # create help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(
            label=self.lang("About"),
            command=lambda: messagebox.showinfo(
                self.lang("About"),
                f"{self.lang("Version")}: {VERSION}\n{self.lang("Author")}: {AUTHOR}\n{self.lang("Email")}: {EMAIL}",
            ),
        )
        self.menu_bar.add_cascade(label=self.lang("Help"), menu=self.help_menu)

        # create curernt path lable
        self.cur_path_lable = tk.Label(self.root)
        self.cur_path_lable.pack(pady=20)

        # create buttons
        self.create_new_day_btn = tk.Button(
            self.root,
            text=self.lang("Create New Day"),
            command=self.create_new_day,
            width=20,
        )
        self.create_new_day_btn.pack(pady=10)

        self.create_newest_p1_btn = tk.Button(
            self.root,
            text=self.lang("Open Newest Part 1"),
            command=lambda: self.open_newest(1),
            width=20,
        )
        self.create_newest_p1_btn.pack(pady=10)

        self.create_part2_btn = tk.Button(
            self.root,
            text=self.lang("Create Part 2"),
            command=self.create_part2,
            width=20,
        )
        self.create_part2_btn.pack(pady=10)

        self.create_newest_p2_btn = tk.Button(
            self.root,
            text=self.lang("Open Newest Part 2"),
            command=lambda: self.open_newest(2),
            width=20,
        )
        self.create_newest_p2_btn.pack(pady=10)

        # create version lable
        self.ver_lable = tk.Label(self.root, text=f"Ver. {VERSION}")
        self.ver_lable.pack(pady=10)

        # load path
        self.load_path()

    def lang(self, s):
        if s not in language or self.language == "en":
            return s
        return language[s][self.language]

    def load_path(self):
        with open(cfg_path["path"], "r") as f:
            self.cur_path = f.read()
        if not os.path.isdir(self.cur_path):
            self.cur_path = ""
            with open(cfg_path["path"], "w") as f:
                f.write("")
        if self.cur_path:
            if len(self.cur_path) <= 30:
                cur_path_text = self.cur_path
            else:
                cur_path_text = self.cur_path[:3] + "..." + self.cur_path[-25:]
        else:
            cur_path_text = "Not Set"
        self.cur_path_lable.config(text=f"{self.lang("Current Path")}: {cur_path_text}")

    def set_path(self, folder_selected=None):
        if folder_selected is None:
            while True:
                folder_selected = filedialog.askdirectory(
                    title=self.lang("Select AoC Folder")
                )
                if not folder_selected:
                    return
                aoc = folder_selected[-7:-4]
                year = folder_selected[-4:]
                if not (aoc == "aoc" and year.isdigit() and int(year) >= 2015):
                    messagebox.showerror(
                        self.lang("Error"),
                        self.lang(
                            'Invalid folder.\nFolder name should be "aoc" with valid year followed.'
                        ),
                    )
                    continue
                with open(cfg_path["path"], "w") as f:
                    f.write(folder_selected)
                self.load_path()
                break
        else:
            folder_selected = folder_selected[0].decode("utf-8")
            aoc = folder_selected[-7:-4]
            year = folder_selected[-4:]
            if not (aoc == "aoc" and year.isdigit() and int(year) >= 2015):
                messagebox.showerror(
                    self.lang("Error"),
                    self.lang(
                        'Invalid folder.\nFolder name should be "aoc" with valid year followed.'
                    ),
                )
                return
            with open(cfg_path["path"], "w") as f:
                f.write(folder_selected)
            self.load_path()

    def set_language(self, lang):
        self.language = lang
        messagebox.showinfo(
            self.lang("Success"),
            self.lang("Language changed.\nEffective at next startup."),
        )

    def on_closing(self):
        with open(cfg_path["settings"], "w") as f:
            f.write(
                json.dumps(
                    {
                        "language": self.language,
                        "last_window_pos": (
                            self.root.winfo_x(),
                            self.root.winfo_y(),
                        ),
                    },
                    indent=4,
                )
            )
        self.root.destroy()

    def is_cur_path_valid(self):
        if self.cur_path:
            return True
        else:
            messagebox.showerror(
                self.lang("Error"), self.lang("Please set the path first.")
            )
            return False

    def open_newest(self, part):
        if not self.is_cur_path_valid():
            return
        day_list = [x for x in os.listdir(self.cur_path) if x.startswith("day")]
        if not day_list:
            messagebox.showerror(self.lang("Error"), self.lang("No day found."))
            return
        path = os.path.join(self.cur_path, day_list[-1], f"part{part}.js")
        if not os.path.isfile(path):
            messagebox.showerror(
                self.lang("Error"),
                self.lang(f'No "part{part}.js" found in the last day.'),
            )
            return
        os.startfile(path)

    def create_new_aoc(self) -> None:
        folder_selected = filedialog.askdirectory(title=self.lang("Where to Create"))
        if not folder_selected:
            return
        while True:
            year = simpledialog.askstring(
                self.lang("Year"), self.lang("Enter the year of the AoC challenge:")
            )
            if year is None:
                return
            if not (len(year) == 4 and year.isdigit() and int(year) >= 2015):
                messagebox.showerror(
                    self.lang("Error"), self.lang("Invalid year.\nPlease try again.")
                )
                continue
            folder_name = f"aoc{year}"
            path = os.path.join(folder_selected, folder_name)
            if os.path.exists(path):
                messagebox.showerror(
                    self.lang("Error"),
                    f"{folder_name} " + self.lang("already exists.\nPlease try again."),
                )
                continue
            break
        os.mkdir(path)
        with open(os.path.join(path, ".gitignore"), "w") as f:
            f.write("*\n\n!/**/\n!*.js\n!*.md\n!*.gitignore\n")
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(
                f"# AoC-{year}-js\nMy [Advent of Code](https://adventofcode.com/{year}) solutions in JavaScript."
            )
        with open(cfg_path["path"], "w") as f:
            f.write(path)
        self.load_path()

    def create_new_day(self) -> None:
        if not self.is_cur_path_valid():
            return
        with open(cfg_path["cookies"], "r") as f:
            try:
                cookies = json.load(f)
            except:  # noqa: E722
                cookies = {}
        if not cookies:
            messagebox.showerror(self.lang("Error"), self.lang("Incorrect cookies."))
            return

        next_day = (
            len([x for x in os.listdir(self.cur_path) if x.startswith("day")]) + 1
        )
        if next_day > 25:
            messagebox.showerror(self.lang("Error"), self.lang("25 puzzles reached."))
            return
        url = f"https://adventofcode.com/{self.cur_path[-4:]}/day/{next_day}/input"
        response = requests.get(url=url, cookies=cookies)

        if response.status_code == 200:
            folder_name = "day" + "0" * (next_day < 10) + str(next_day)
            path = os.path.join(self.cur_path, folder_name)
            os.mkdir(path)
            with open(os.path.join(path, "part1.js"), "w") as f:
                f.write(
                    "const data = require('fs').readFileSync(require('path').join(__dirname, 0 ? 'puzzle.txt' : 'example.txt'), 'utf8')\n\n"
                )
            with open(os.path.join(path, "puzzle.txt"), "w") as f:
                f.write(response.text.strip())
            with open(os.path.join(path, "example.txt"), "w") as f:
                pass
            messagebox.showinfo(
                self.lang("Success"), self.lang("New day created successfully!")
            )
            os.startfile(os.path.join(path, "example.txt"))
        else:
            messagebox.showerror(
                self.lang("Error"),
                self.lang(
                    "Failed to retrieve the webpage.\nPlease recheck your cookies or the puzzle is not available yet."
                ),
            )

    def create_part2(self) -> None:
        if not self.is_cur_path_valid():
            return
        for day in [x for x in os.listdir(self.cur_path) if x.startswith("day")]:
            path1 = os.path.join(self.cur_path, day, "part1.js")
            if not os.path.isfile(path1):
                with open(path1, "w") as f:
                    f.write(
                        "const data = require('fs').readFileSync(require('path').join(__dirname, 0 ? 'puzzle.txt' : 'example.txt'), 'utf8')\n\n"
                    )
            path2 = os.path.join(self.cur_path, day, "part2.js")
            if os.path.isfile(path2):
                continue
            with open(path1, "r") as f:
                code = f.read()
            with open(path2, "w") as f:
                f.write(code)


if __name__ == "__main__":
    AoC_Helper().root.mainloop()
