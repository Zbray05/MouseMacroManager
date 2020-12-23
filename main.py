from tkinter import *
import os
import json


def add_macros_windows(root, macro_dict):
    new_window = Toplevel(root)
    new_window.title('add a macro')

    macro_name = Label(new_window, text="Name")
    macro_name.grid(row=0, column=0)

    macro_content = Label(new_window, text="Macro")
    macro_content.grid(row=1, column=0)

    name_text = Entry(new_window)
    name_text.grid(row=0, column=1, sticky='w')

    macro = Text(new_window, height=3, width=25)
    macro.grid(row=1, column=1)

    save_macros_button = Button(new_window,
                                text='Save',
                                command=lambda: add_macro(name_text.get(),
                                                          macro.get('1.0', END),
                                                          macro_dict,
                                                          new_window))

    save_macros_button.grid(row=2, column=1)


def create_profile_window(root, profile_dict, macro_dict, converted_macro_list):
    new_window = Toplevel(root)
    new_window.title('Create new profile')

    profile_name = Label(new_window, text='Profile Name')
    profile_name.grid(row=0, column=0)

    profile_name_input = Entry(new_window)
    profile_name_input.grid(row=0, column=1)

    mouse_button1_label = Label(new_window, text="Button 1")
    mouse_button1_label.grid(row=1, column=0)

    mouse_button2_label = Label(new_window, text="Button 2")
    mouse_button2_label.grid(row=1, column=1)

    listbox_button1_mouse = Listbox(new_window, height=5, listvariable=converted_macro_list, exportselection=0)
    listbox_button1_mouse.grid(row=2, column=0)

    listbox_button2_mouse = Listbox(new_window, height=5, listvariable=converted_macro_list, exportselection=0)
    listbox_button2_mouse.grid(row=2, column=1)

    save_profile_button = Button(new_window,
                                 text="Save Profile",
                                 command=lambda: add_profile(profile_name_input.get(),
                                                             macro_dict[listbox_button1_mouse.get(ACTIVE)],
                                                             macro_dict[listbox_button2_mouse.get(ACTIVE)],
                                                             profile_dict,
                                                             new_window))
    save_profile_button.grid(row=0, column=2)


def add_macro(name, macro, macro_dict, window):
    macro_dict[name] = macro
    save_macros_json(macro_dict)
    window.destroy()


def add_profile(name, macro1, macro2, profile_dict, window):
    profile_dict[name] = [macro1, macro2]
    save_profile_json(profile_dict)
    window.destroy()


def update_message_label(label, text, color, time):
    label.config(text=text, fg=color)
    label.after(time, lambda: label.config(text=''))


def apply(profile):
    with open('C:/Users/Zach/Documents/mouse.ahk', 'w') as macro_ahk:
        macro_ahk.write(f'#SingleInstance force\nXButton1::{profile[0]}\nXButton2::{profile[1]}')
    macro_ahk.close()
    os.system('cmd /c "start C:/Users/Zach/Documents/mouse.ahk"')


def apply_handler(profile, message_label):
    try:
        apply(profile)
    except IndexError:
        update_message_label(message_label, 'Must select both', 'Red', 2000)
    else:
        update_message_label(message_label, 'Macros updated', 'Green', 2000)


def save_macros_json(macro_dict):
    json_object = json.dumps(macro_dict, indent=4)
    with open('macros.json', 'w') as outfile:
        json.dump(json_object, outfile)
    outfile.close()


def load_macros_json():
    with open('macros.json', 'r') as infile:
        macro_dict = json.loads(infile.read())
        macro_dict = json.loads(macro_dict)
        infile.close()
    return macro_dict


def retrieve_macro_data():
    macro_dict = load_macros_json()
    converted_macro_list = StringVar(value=[*macro_dict])
    return [macro_dict, converted_macro_list]


def save_profile_json(profile_dict):
    json_object = json.dumps(profile_dict, indent=4)
    with open('profiles.json', 'w') as outfile:
        json.dump(json_object, outfile)
    outfile.close()


def load_profile_json():
    with open('profiles.json', 'r') as infile:
        profile_dict = json.loads(infile.read())
        profile_dict = json.loads(profile_dict)
        infile.close()
    return profile_dict


def retrieve_profile_data():
    try:
        profile_dict = load_profile_json()
        converted_profile_list = StringVar(value=[*profile_dict])
        return [profile_dict, converted_profile_list]
    except FileNotFoundError:
        print("no profiles file found")
        return [{}, []]
    except json.decoder.JSONDecodeError:
        print("file empty")
        return [{}, []]


def main():

    window = Tk()
    window_width = 300
    window_height = 150
    window.geometry(f"{window_width}x{window_height}")

    macro_dict, converted_macro_list = retrieve_macro_data()
    profile_dict, converted_profile_list = retrieve_profile_data()

    profiles_label = Label(window, text='Profiles')
    profiles_label.grid(row=0, column=0)

    profile_listbox = Listbox(window, height=5, listvariable=converted_profile_list, exportselection=0)
    profile_listbox.grid(row=1, column=0)

    message_label = Label(text='')
    message_label.grid(row=2, column=0)

    add_macros_button = Button(text='Add Macro',
                               command=lambda: add_macros_windows(window, macro_dict))
    add_macros_button.grid(row=1, column=1, padx=10, sticky='n')

    create_profile_button = Button(text='Create Profile',
                                   command=lambda: create_profile_window(window,
                                                                         profile_dict,
                                                                         macro_dict,
                                                                         converted_macro_list))
    create_profile_button.grid(row=1, column=1, padx=10)

    apply_button = Button(text='Apply',
                          command=lambda: apply_handler(profile_dict[profile_listbox.get(ACTIVE)],
                                                        message_label))
    apply_button.grid(row=2, column=0)

    window.mainloop()


if __name__ == '__main__':
    main()
