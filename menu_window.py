import tkinter as tk
import random
from tkinter import messagebox


WINDOW_BG = "#F0FDFA"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#99F6E4"
TEXT_PRIMARY = "#134E4A"
TEXT_SECONDARY = "#0F766E"
ACCENT = "#0D9488"
ACCENT_ACTIVE = "#0F766E"
CTA_BG = "#F97316"
CTA_ACTIVE = "#EA580C"
DESCRIPTION_MESSAGES = [
    "给你挑了两道菜，先吃饭，再继续打怪。",
    "先把午饭安排明白，下午的脑子才转得更快。",
    "今天这两道看着都行，别让肚子先开始催你。",
    "吃饭这件事先别拖，挑一个顺眼的就出发。",
    "午饭先稳住，后面的活儿也会顺一点。",
    "先选个想吃的，别让今日份能量条见底。",
]


class RecommendationWindow:
    def __init__(self, dishes, on_refresh):
        self.dishes = list(dishes)
        self.on_refresh = on_refresh
        self.excluded = set()
        self.description_message = self._pick_description()
        self.root = tk.Tk()
        self.root.title("今天吃什么")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.configure(bg=WINDOW_BG)
        self.root.minsize(360, 300)

        self.container = tk.Frame(self.root, bg=WINDOW_BG, padx=20, pady=20)
        self.container.pack(fill="both", expand=True)

        self.card = tk.Frame(
            self.container,
            bg=CARD_BG,
            highlightbackground=CARD_BORDER,
            highlightthickness=1,
            padx=20,
            pady=20,
        )
        self.card.pack(fill="both", expand=True)

        self.badge_label = tk.Label(
            self.card,
            text="午餐提醒",
            bg=CARD_BG,
            fg=ACCENT,
            font=("Microsoft YaHei", 10, "bold"),
            anchor="w",
        )
        self.badge_label.pack(fill="x")

        self.title_label = tk.Label(
            self.card,
            text="今天吃什么",
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            font=("Microsoft YaHei", 18, "bold"),
            anchor="w",
        )
        self.title_label.pack(fill="x", pady=(8, 4))

        self.description_label = tk.Label(
            self.card,
            text=self.description_message,
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=("Microsoft YaHei", 10),
            anchor="w",
            justify="left",
        )
        self.description_label.pack(fill="x", pady=(0, 16))

        self.list_frame = tk.Frame(self.card, bg=CARD_BG)
        self.list_frame.pack(fill="x")
        self.dish_rows = []
        self._render_dishes()

        self.tip_label = tk.Label(
            self.card,
            text="“换一换”只会排除当前窗口已经出现过的菜。",
            bg=CARD_BG,
            fg=TEXT_SECONDARY,
            font=("Microsoft YaHei", 9),
            anchor="w",
            justify="left",
        )
        self.tip_label.pack(fill="x", pady=(16, 18))

        self.action_row = tk.Frame(self.card, bg=CARD_BG)
        self.action_row.pack(fill="x")
        self.action_row.grid_columnconfigure(0, weight=1)
        self.action_row.grid_columnconfigure(1, weight=1)

        self.refresh_button = tk.Button(
            self.action_row,
            text="换一换",
            command=self.handle_refresh,
            bg=CTA_BG,
            activebackground=CTA_ACTIVE,
            fg="#FFFFFF",
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            padx=0,
            pady=10,
            font=("Microsoft YaHei", 10, "bold"),
            cursor="hand2",
        )
        self.refresh_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.close_button = tk.Button(
            self.action_row,
            text="我再想想",
            command=self.root.destroy,
            bg="#CCFBF1",
            activebackground="#99F6E4",
            fg=TEXT_PRIMARY,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            padx=0,
            pady=10,
            font=("Microsoft YaHei", 10, "bold"),
            cursor="hand2",
        )
        self.close_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _clear_dish_rows(self):
        for row in self.dish_rows:
            row.destroy()
        self.dish_rows = []

    def _pick_description(self):
        return random.choice(DESCRIPTION_MESSAGES)

    def _render_dishes(self):
        self._clear_dish_rows()
        for index, dish in enumerate(self.dishes, start=1):
            row = tk.Frame(self.list_frame, bg="#F8FFFE", highlightbackground="#CCFBF1", highlightthickness=1, padx=12, pady=10)
            row.pack(fill="x", pady=(0, 8))

            index_label = tk.Label(
                row,
                text=f"{index:02d}",
                bg="#CCFBF1",
                fg=ACCENT_ACTIVE,
                font=("Microsoft YaHei", 9, "bold"),
                width=4,
                pady=4,
            )
            index_label.pack(side="left")

            name_label = tk.Label(
                row,
                text=dish,
                bg="#F8FFFE",
                fg=TEXT_PRIMARY,
                font=("Microsoft YaHei", 12, "bold"),
                anchor="w",
                justify="left",
            )
            name_label.pack(side="left", fill="x", expand=True, padx=(12, 0))
            self.dish_rows.append(row)

    def handle_refresh(self):
        self.excluded.update(self.dishes)
        refreshed = self.on_refresh(set(self.excluded))
        if not refreshed:
            messagebox.showinfo("今天吃什么", "菜单里的菜已经换完了。")
            return
        self.dishes = list(refreshed)
        self.description_message = self._pick_description()
        self.description_label.config(text=self.description_message)
        self._render_dishes()

    def show(self):
        self.root.mainloop()


def show_error(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()
