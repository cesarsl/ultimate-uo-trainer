
import atexit
import ctypes
import os
import sys
import threading

PY2 = b'' == ''  # py2 check

if PY2:  # py2 import
    # tkinter
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    # configparser
    import ConfigParser as configparser
else:  # py3 import
    # tkinter
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
    # configparser
    import configparser

from py_stealth import winapi


CONFIG_FILE = 'py-hotkeys.ini'

MODS = {0x10: 'Shift', 0xA0: 'LShift', 0xA1: 'RShift', 0x11: 'Ctrl',
        0xA2: 'LCtrl', 0xA3: 'RCtrl', 0x12: 'Alt', 0xA4: 'LAlt', 0xA5: 'RAlt'}

KEYS = {0x10: 'Shift', 0xA0: 'LShift', 0xA1: 'RShift', 0x11: 'Ctrl',
        0xA2: 'LCtrl', 0xA3: 'RCtrl', 0x12: 'Alt', 0xA4: 'LAlt', 0xA5: 'RAlt',
        0x1B: 'Esc', 0x70: 'F1', 0x71: 'F2', 0x72: 'F3', 0x73: 'F4',
        0x74: 'F5', 0x75: 'F6', 0x76: 'F7', 0x77: 'F8', 0x78: 'F9',
        0x79: 'F10', 0x7A: 'F11', 0x7B: 'F12', 0x13: 'PrintScreen',
        0x91: 'ScrollLock', 0x2C: 'Pause', 0x2D: 'Insert', 0x24: 'Home',
        0x21: 'PageUp', 0x2E: 'Delete', 0x23: 'End', 0x22: 'PageDown',
        0x08: 'Backspace', 0x09: 'Tab', 0x14: 'CapsLock', 0x0D: 'Return',
        0x20: 'Space', 0x25: 'Left', 0x26: 'Up', 0x27: 'Right', 0x28: 'Down',
        0xC0: '`', 0x31: '1', 0x32: '2', 0x33: '3', 0x34: '4', 0x35: '5',
        0x36: '6', 0x37: '7', 0x38: '8', 0x39: '9', 0x30: '0', 0xBD: '-',
        0xBB: '=', 0x51: 'Q', 0x57: 'W', 0x45: 'E', 0x52: 'R', 0x54: 'T',
        0x59: 'Y', 0x55: 'U', 0x49: 'I', 0x4F: 'O', 0x50: 'P', 0xDB: '[',
        0xDD: ']', 0x41: 'A', 0x53: 'S', 0x44: 'D', 0x46: 'F', 0x47: 'G',
        0x48: 'H', 0x4A: 'J', 0x4B: 'K', 0x4C: 'L', 0xBA: ';', 0xDE: "'",
        0xDC: '\\', 0x5A: 'Z', 0x58: 'X', 0x43: 'C', 0x56: 'V', 0x42: 'B',
        0x4E: 'N', 0x4D: 'M', 0xBC: ',', 0xBE: '.', 0xBF: '/', 0x90: 'NumLock',
        0x61: 'Num1', 0x62: 'Num2', 0x63: 'Num3', 0x64: 'Num4', 0x65: 'Num5',
        0x66: 'Num6', 0x67: 'Num7', 0x68: 'Num8', 0x69: 'Num9', 0x6B: 'Num+',
        0x60: 'Num0', 0x6E: 'Num.', 0x6D: 'Num-', 0x6A: 'Num*', 0x6F: 'Num/'}

# decorators
enum_windows_proc = winapi.WNDENUMPROC
low_level_keyboard_proc = winapi.HOOKPROC


class HotkeysApp:
    def __init__(self):
        for value in MODS.values():
            setattr(self, value, False)
        self.switch_bind = None
        self.module = None
        self.vk_codes = None
        self.threads = []
        self.binds = {}
        self.hwnd = None
        # tk
        root = tk.Tk()
        root.geometry('400x200')
        root.title('py-hotkeys')
        root.resizable(0, 0)
        self.root = root
        # widgets
        # choose script sector
        file_label = ttk.LabelFrame(root, text='Choose a script file')
        file_label.pack(fill=tk.X, ipadx=3, padx=1)
        path_entry = ttk.Entry(file_label)
        path_entry.pack(fill=tk.X, side=tk.LEFT, expand=1, padx=3)
        path_entry.bind('<Return>', self.load_file)
        self.path_entry = path_entry
        browse = ttk.Button(file_label, text='Browse', command=self.load_file)
        browse.pack(side=tk.RIGHT)
        # hotkeys sector
        hk_label = ttk.LabelFrame(root, text='Bind your hot keys')
        hk_label.pack(fill=tk.BOTH, ipadx=3, ipady=1, padx=1)
        hk_listbox = tk.Listbox(hk_label)
        hk_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.hk_listbox = hk_listbox
        hk_scrollbar = ttk.Scrollbar(hk_label, command=hk_listbox.yview)
        hk_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        hk_listbox.config(yscrollcommand=hk_scrollbar)
        # buttons sector
        hk_frame = ttk.Frame(hk_label)
        hk_frame.pack(side=tk.RIGHT, fill=tk.Y)
        hk_entry = ttk.Entry(hk_frame, justify=tk.CENTER)
        hk_entry.insert(0, 'Press a key')
        hk_entry.bind('<Key>', self.get_key_codes)
        hk_entry.pack(side=tk.TOP, pady=1, padx=1, fill=tk.X)
        self.hk_entry = hk_entry
        cmd_entry = ttk.Entry(hk_frame, justify=tk.CENTER)
        cmd_entry.insert(0, 'Print your command')
        cmd_entry.bind('<1>', lambda event: event.widget.delete(0, tk.END))
        cmd_entry.pack(side=tk.TOP, pady=1, padx=1, fill=tk.X)
        self.cmd_entry = cmd_entry
        bt_frame = ttk.Frame(hk_frame)
        bt_frame.pack(side=tk.TOP)
        add = ttk.Button(bt_frame, text='Add', command=self.add_hotkey)
        add.pack(side=tk.LEFT)
        clear = ttk.Button(bt_frame, text='Clear', command=self.clear_hotkey)
        clear.pack(side=tk.RIGHT)
        # other staff sector
        oth_label = ttk.LabelFrame(hk_frame, text="Other useless staff")
        oth_label.pack(side=tk.TOP, fill=tk.X)
        switch_entry = ttk.Entry(oth_label, justify=tk.CENTER)
        switch_entry.insert(0, 'On/Off hotkey')
        switch_entry.bind('<Key>', self.get_key_codes)
        switch_entry.pack(side=tk.TOP, fill=tk.X)
        self.switch_entry = switch_entry
        check_frame = ttk.Frame(hk_frame)
        check_frame.pack(side=tk.TOP, fill=tk.X, padx=10)
        self.var_ontop = tk.BooleanVar()
        check_ontop = ttk.Checkbutton(check_frame, text='OnTop',
                                      command=self.ontop_switch,
                                      variable=self.var_ontop)
        check_ontop.pack(side=tk.LEFT)
        self.check_ontop = check_ontop
        self.var_switch = tk.BooleanVar()
        check_switch = ttk.Checkbutton(check_frame, text='Enable',
                                       command=self.on_off_switch,
                                       variable=self.var_switch)
        check_switch.pack(side=tk.RIGHT)
        self.check_switch = check_switch
        # launch manager
        self.hooks_manager()
        self.config = self.load_cfg()

    def load_file(self, event=None):
        if event is not None:  # called by the path_entry
            path = event.windget.get()
        else:  # called by the Browse button
            path = filedialog.askopenfilename(filetypes=[('Python files',
                                                          '*.py;*.pyw')])
        if not os.path.exists(path):
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, 'Can not find your file')
            return
        # import module and save/load to config
        self.import_module(path)
        self.add_cfg('main', 'module', path)

    def import_module(self, path):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        if directory not in sys.path:
            # TODO: maybe the append method will be better
            sys.path.insert(0, directory)
        self.module = __import__(filename.rpartition('.')[0])
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, filename + ' was successfully loaded')

    def get_key_codes(self, event):
        if event.type == '2':  # key pressed
            if event.keycode in (16, 17, 18):  # mods
                return 'break'
            vk_codes = [k for k, v in MODS.items() if getattr(self, v)]
            vk_codes.sort()
            vk_codes.append(event.keycode)
            if event.widget is self.hk_entry:
                self.vk_codes = tuple(vk_codes)
            if event.widget is self.switch_entry:
                self.switch_bind = vk_codes
                value = ' '.join([str(c) for c in vk_codes])
                self.add_cfg('main', 'on/off bind', value)
            text = '+'.join([KEYS[code] for code in vk_codes])
            event.widget.delete(0, tk.END)
            event.widget.insert(0, text)
        return 'break'

    def add_cfg(self, section, option, value):
        self.config[section][option] = value
        with open(CONFIG_FILE, 'w') as file:
            self.config.write(file)

    def load_cfg(self):
        config = configparser.ConfigParser()
        config.add_section('main')
        config.add_section('binds')
        for path in sys.path:
            fullpath = os.path.join(path, CONFIG_FILE)
            if os.path.exists(fullpath):
                break
        if config.read(fullpath):
            try:  # on/off switcher bind
                codes = [int(x) for x in config['main']['on/off bind'].split()]
                self.switch_bind = codes
                self.switch_entry.delete(0, tk.END)
                text = '+'.join([KEYS[code] for code in codes])
                self.switch_entry.insert(0, text)
            except KeyError:
                pass
            try:  # on/off switcher
                self.var_switch.set(config.getboolean('main', 'on/off'))
            except configparser.NoOptionError:
                pass
            try:  # load script
                self.import_module(config['main']['module'])
            except KeyError:
                return config
            for codes in config['binds']:
                vkc = tuple([int(x) for x in codes.split()])
                names = '+'.join([KEYS[c] for c in vkc])
                self.add_hotkey(hotkey=(vkc, names, config['binds'][codes]))
        return config

    def add_hotkey(self, hotkey=None):
        if hotkey is not None:
            vk_codes, names, function = hotkey
        else:
            vk_codes = self.vk_codes
            names = self.hk_entry.get()
            function = self.cmd_entry.get()
        if self.module is None:
            return winapi.MessageBox(0, 'Choose a script file', 'Error', 0)
        if vk_codes is None:
            return winapi.MessageBox(0, 'Specify a keyboard key', 'Error', 0)
        if not hasattr(self.module, function):
            error = 'Can not find ' + function + ' at ' + self.module.__name__
            return winapi.MessageBox(0, error, 'Error', 0)
        if not callable(getattr(self.module, function)):
            error = 'The selected object must be callable.'
            return winapi.MessageBox(0, error, 'Error', 0)
        if vk_codes in self.binds.keys():
            error = 'The selected key is already bound.'
            return winapi.MessageBox(0, error, 'Error', 0)
        self.binds[vk_codes] = getattr(self.module, function)
        # save to .ini
        value = ' '.join([str(c) for c in vk_codes])
        if hotkey is None:  # not from a config
            self.add_cfg('binds', value, function)
        # put to the listbox
        codes = ('{} ' * len(vk_codes)).format(*vk_codes)
        self.hk_listbox.insert(0, names + ' => ' + function + ' |' + codes)
        self.hk_entry.delete(0, tk.END)
        self.hk_entry.insert(0, 'Press a key')
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, 'Print your command')
        self.vk_codes = None

    def clear_hotkey(self):
        try:
            index = self.hk_listbox.curselection()[0]
        except IndexError:
            return
        line = self.hk_listbox.get(index)
        str_codes = ' '.join(line.split('|')[-1].split()).strip()
        codes = [int(x) for x in str_codes.split()]
        del self.binds[tuple(codes)]
        del self.config['binds'][str_codes]
        self.hk_listbox.delete(index)
        self.add_cfg('main', 'dummy', 'dummy')  # save .ini file

    def ontop_switch(self):
        @enum_windows_proc
        def enum_windows_handler(hwnd, lparam):
            buffer = ctypes.c_ulong()
            winapi.GetWindowThreadProcessId(hwnd, ctypes.byref(buffer))
            if pid == buffer.value:
                if winapi.IsWindowVisible(hwnd):
                    self.hwnd = hwnd
                    return 0
            return 1

        if self.hwnd is None:
            pid = winapi.GetCurrentProcessId()
            winapi.EnumWindows(enum_windows_handler, 0)
        var = self.var_ontop.get()
        value = winapi.HWND_TOPMOST if var else winapi.HWND_NOTOPMOST
        winapi.SetWindowPos(self.hwnd, value, 0, 0, 0, 0,
                            winapi.SWP_NOMOVE | winapi.SWP_NOSIZE)

    def on_off_switch(self):
        self.add_cfg('main', 'on/off', str(self.var_switch.get()))

    def hooks_manager(self):
        @low_level_keyboard_proc
        def hook_handler(code, wparam, lparam):
            vk_code = winapi.KBDLLHOOK.from_address(lparam).vkCode
            # mods
            if vk_code in MODS.keys():
                if wparam in (winapi.WM_KEYDOWN, winapi.WM_SYSKEYDOWN):  # press
                    setattr(self, MODS[vk_code], True)
                elif wparam in (winapi.WM_KEYUP, winapi.WM_SYSKEYUP):  # release
                    setattr(self, MODS[vk_code], False)
                else:
                    error = 'Unknown hook type ' + str(wparam)
                    winapi.MessageBox(0, error, 'Error', 0)
                    exit()
            # keys
            elif wparam in (winapi.WM_KEYDOWN, winapi.WM_SYSKEYDOWN):  # press
                if vk_code not in KEYS.keys():
                    error = 'Unknown key code ' + str(wparam)
                    winapi.MessageBox(0, error, 'Error', 0)
                    return winapi.CallNextHookEx(0, code, wparam, lparam)
                buffer = ctypes.create_unicode_buffer('', 255)
                winapi.GetClassName(winapi.GetForegroundWindow(), buffer, 255)
                if buffer.value == 'Ultima Online':
                    codes = [k for k, v in MODS.items() if getattr(self, v)]
                    codes.sort()
                    codes.append(vk_code)
                    if codes == self.switch_bind:
                        self.var_switch.set(not self.var_switch.get())
                        self.on_off_switch()
                    if self.var_switch.get():
                        try:
                            method = self.binds[tuple(codes)]
                            t = threading.Thread(target=method)
                            t.start()
                            self.threads.append(t)
                        except KeyError:
                            pass
            for index, thread in enumerate(self.threads):
                if not thread.is_alive:
                    thread.join()
                    del self.threads[index]
            return winapi.CallNextHookEx(0, code, wparam, lparam)

        def register():
            hook_id = winapi.SetWindowsHookEx(winapi.WH_KEYBOARD_LL,
                                              hook_handler,
                                              ctypes.c_void_p(), 0)
            if not hook_id:
                winapi.MessageBox(0, 'Can not register a hook.', 'Error', 0)
                exit()
            atexit.register(winapi.UnhookWindowsHookEx, hook_id)

            msg = winapi.MSG()
            while 1:
                winapi.GetMessage(msg, None, 0, 0)
                winapi.TranslateMessage(msg)
                winapi.DispatchMessage(msg)

        t = threading.Thread(target=register, daemon=True)
        t.start()


def main():
    application = HotkeysApp()
    application.root.mainloop()


if __name__ == '__main__':
    main()
