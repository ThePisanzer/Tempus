#一个 Bug 是 Bug ，一堆 Bug 是 Debug ；能跑起来的叫 Feature ，跑不起来的叫 Debug ，跑起来了但不知所云的叫玄学，而你的 Debugger 妈妈能把“不知为何能跑”改成“不知为何跑不起来”的，如果你乱动，那么本来能跑的也跑不起来了，这叫 Release ，你盯着日志它不复现，你一去倒水它就崩，这叫 Heisenbug ，稳定复现，像玻尔模型一样老实的叫 Bohrbug ，你不看代码它有问题，一看代码它又好像正常的叫 Schrödinbug ，像混沌分形的，你修一个角，它炸一片的叫 Mandelbug~
#早期 Harvard Mark II 计算机里发现过一只飞蛾，被贴在本子上写着 “First actual case of bug being found”
#Debugger 就是去除 Bug 的东西——只不过去除方式是先制造一个更确定的 Bug ~awa


#一个扁平深色风格的桌面时钟，支持透明度、置顶、全屏、毫秒显示切换。

import datetime
import customtkinter as ctk
import sys
import os

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

BG = "#1a1a1a"
PANEL = "#252525"
TEXT_PRIMARY = "#e0e0e0"
TEXT_SECONDARY = "#888888"
ACCENT = "#0a84ff"


class ClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tempus")

        try:
            self.root.iconbitmap(resource_path("tempus_icon.ico"))
        except Exception:
            pass

        self.root.overrideredirect(True)
        self.root.geometry("600x100")
        self.root.minsize(480, 320)
        self.root.configure(fg_color=BG)
        self.root.attributes("-alpha", 0.95)

        self._fullscreen = False
        self.show_ms = True

        #主容器
        container = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
        container.pack(fill="both", expand=True, padx=24, pady=20)

        #日期行
        self.date_label = ctk.CTkLabel(
            container, text="",
            font=("Microsoft YaHei", 28, "bold"),
            text_color=TEXT_SECONDARY
        )
        self.date_label.pack(pady=(10, 0))

        self.date_label.bind("<Button-1>", self._start_move)
        self.date_label.bind("<B1-Motion>", self._do_move)

        #时间+毫秒同一行，底部对齐
        time_row = ctk.CTkFrame(container, fg_color=BG)
        time_row.pack(pady=(10, 0))

        self.clock_label = ctk.CTkLabel(
            time_row, text="00:00:00",
            font=("Consolas", 72, "bold"),
            text_color="#ffffff"
        )
        self.clock_label.pack(side="left", anchor="s")

        self.clock_label.bind("<Button-1>", self._start_move)
        self.clock_label.bind("<B1-Motion>", self._do_move)

        self.ms_label = ctk.CTkLabel(
            time_row, text=".000",
            font=("Consolas", 72, "bold"),
            text_color="#888888"
        )
        self.ms_label.pack(side="left", anchor="s", padx=(6, 0))

        self.ms_label.bind("<Button-1>", self._start_move)
        self.ms_label.bind("<B1-Motion>", self._do_move)

        #底部控制栏
        control_bar = ctk.CTkFrame(container, fg_color=BG, corner_radius=0)
        control_bar.pack(side="bottom", fill="x")

        ctk.CTkLabel(
            control_bar, text="Opacity",
            font=("Segoe UI", 11), text_color=TEXT_SECONDARY
        ).pack(side="left", padx=(0, 8))

        self.opacity_var = ctk.DoubleVar(value=0.95)
        ctk.CTkSlider(
            control_bar, from_=0.3, to=1.0,
            variable=self.opacity_var,
            command=self._on_opacity_change,
            width=140, height=16,
            button_color=ACCENT, progress_color=ACCENT
        ).pack(side="left", padx=(0, 8))

        self.opacity_label = ctk.CTkLabel(
            control_bar, text="95%",
            font=("Segoe UI", 10), text_color=TEXT_SECONDARY, width=40
        )
        self.opacity_label.pack(side="left", padx=(0, 15))

        self.topmost_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(
            control_bar, text="Always on Top",
            variable=self.topmost_var,
            command=self._toggle_topmost,
            font=("Segoe UI", 11),
            text_color=TEXT_PRIMARY,
            progress_color=ACCENT,
            button_color=TEXT_PRIMARY,
            button_hover_color=TEXT_PRIMARY,
            width=140
        ).pack(side="left", padx=(0, 15))

        self.ms_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            control_bar, text="Show ms",
            variable=self.ms_var,
            command=self._toggle_ms,
            font=("Segoe UI", 11),
            text_color=TEXT_PRIMARY,
            progress_color=ACCENT,
            button_color=TEXT_PRIMARY,
            button_hover_color=TEXT_PRIMARY,
            width=110
        ).pack(side="left")

        #快捷键
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self.on_escape())
        self.root.bind("<space>", lambda e: self._toggle_ms())

        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now()
        self.clock_label.configure(text=now.strftime("%H:%M:%S"))
        self.date_label.configure(
            text=now.strftime("%Y-%m-%d") + "  " + WEEKDAYS[now.weekday()]
        )
        if self.show_ms:
            self.ms_label.configure(text=f".{now.microsecond // 1000:03d}")
        else:
            self.ms_label.configure(text="")
        self.root.after(10, self.update_clock)

    def _on_opacity_change(self, value):
        try:
            v = float(value)
            self.root.attributes("-alpha", v)
            self.opacity_label.configure(text=f"{int(v * 100)}%")
        except Exception:
            pass

    def _toggle_topmost(self):
        try:
            self.root.attributes("-topmost", self.topmost_var.get())
        except Exception:
            pass

    def _toggle_ms(self):
        self.show_ms = not self.show_ms
        self.ms_var.set(self.show_ms)

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        self.root.attributes("-fullscreen", self._fullscreen)

    def on_escape(self):
        if self._fullscreen:
            self._fullscreen = False
            self.root.attributes("-fullscreen", False)
        else:
            self.root.destroy()

    def _start_move(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_move(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")


def main():
    root = ctk.CTk()
    app = ClockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()