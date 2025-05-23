import tkinter as tk
from datetime import datetime
from tkinter.filedialog import asksaveasfilename
from subtitle_maker import make_subtitle

window = tk.Tk()
window.title("Subtitle Generator")
window.wm_geometry("500x310")
window.wm_minsize(width=500, height=200)
panels = []  # list of lists: [panel, jp_entry, jp_reading, en_pos (optionsmenu), en_pos (stringvar), en_entry]
title_panel = tk.Frame(window, pady=1, padx=15)
panel_holder = tk.Frame(window, pady=1, padx=15)
title_panel.pack()
panel_holder.pack()

# Title panel to label each column
tk.Label(title_panel, text="#").pack(side="left")

japanese = tk.Label(title_panel, text="Japanese",   width=18)
furigana = tk.Label(title_panel, text="Furigana",   width=10)
english = tk.Label(title_panel, text="English",     width=17)
padding = tk.Label(title_panel,                     width=4)
en_pos = tk.Label(title_panel, text="EN>JP",        width=10)

japanese.pack(side="left")
furigana.pack(side="left")
english.pack(side="right")
padding.pack(side="left")
en_pos.pack(side="right")

title_panel.pack(pady=5)


def update_dropdowns():
    for _, _, _, menu, var, _ in panels:
        menu["menu"].delete(0, "end")

        for i in range(len(panels)):
            choice = str(i + 1)
            menu['menu'].add_command(label=choice, command=tk._setit(var, choice))


def remove_input_frame():
    if len(panels) < 2: return

    last_frame = panels[-1]
    old_panel = last_frame[0]
    old_panel.pack_forget()
    panels.remove(last_frame)

    update_dropdowns()


def add_input_frame():
    new_panel = tk.Frame(panel_holder)

    tk.Label(new_panel, text=str(len(panels)+1)+".").pack(side="left")

    jp_entry = tk.Entry(new_panel)
    jp_entry.pack(side="left", padx=10)

    jp_reading = tk.Entry(new_panel, width=7)
    jp_reading.pack(side="left", padx=10)

    tk.Label(new_panel, text=" ").pack(side="left", padx=20)

    en_entry = tk.Entry(new_panel)
    en_entry.pack(side="right", padx=10)

    en_var = tk.StringVar()
    en_var.set("1")
    en_pos_options = tk.OptionMenu(new_panel, en_var, *[str(i+1) for i in range(len(panels) + 1)])
    en_pos_options.pack(side="right")

    panels.append([new_panel, jp_entry, jp_reading, en_pos_options, en_var, en_entry])
    new_panel.pack(pady=5)

    update_dropdowns()


def generate_caption():
    full_jp = ""
    full_en = ""

    for _, jp_entry, jp_reading, _, en_pos, en_entry in panels:
        full_jp += f"{jp_entry.get()}({jp_reading.get()})|"
        full_en += f"({en_pos.get()}){en_entry.get()}|"

    print("full_en", full_en[:-1])
    print("full jp:", full_jp[:-1])

    output_location = asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], initialfile=datetime.today().strftime("%m-%d-%y %I%M%p.png"))
    print("output:", output_location)
    make_subtitle(full_jp[:-1], full_en[:-1], output_location)


# submit button
tk.Button(window, text="Generate!", command=generate_caption).pack(side="bottom", pady=15)

# add and remove buttons
button_pack = {"side": "left", "padx": 15}
add_rem_frame = tk.Frame(window)
tk.Button(add_rem_frame, text="+ Add", command=add_input_frame).pack(**button_pack)
tk.Button(add_rem_frame, text="- Delete", command=remove_input_frame).pack(**button_pack)
add_rem_frame.pack(side="bottom")

add_input_frame()

tk.mainloop()
