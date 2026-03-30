"""
Chess - Main Menu
Python / tkinter version

Run:    python chess_menu.py

chess.jpg must be in the same folder.

Requires: Python 3.8+  (tkinter is included in the standard library)
          Pillow  ->  pip install Pillow
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


PUZZLE_JAR = "main.py"

# ── palette (R, G, B) or hex strings ──────────────────────────────────────────
C_BG        = "#0a0c12"
C_CARD      = (20,  24,  36)
C_CARD_HOV  = (32,  38,  58)
C_GOLD      = "#d4af37"
C_GOLD_LT   = "#ffd75a"
C_GOLD_DIM  = "#644f14"
C_TXT       = "#e1dccd"
C_TXT2      = "#969898"  # slightly brighter for readability on canvas
C_MUTED     = "#505362"
C_BLUE      = "#508cd2"
C_BORDER    = (50,  55,  75)
C_BRD_GOLD  = (90,  72,  22)
C_GREEN     = "#50c878"
C_WARN      = "#d26446"
C_VIGNETTE  = (0, 0, 0, 150)   # RGBA

# ── fonts (tkinter font tuples: (family, size, style)) ────────────────────────
F_DISP  = lambda s: ("Georgia",   s, "bold")
F_BODY  = lambda s: ("Helvetica", s, "normal")
F_BOLD  = lambda s: ("Helvetica", s, "bold")

def rgb(r, g, b):
    """Convert (r,g,b) tuple to hex colour string."""
    return f"#{r:02x}{g:02x}{b:02x}"

def blend(base_rgb, alpha):
    """Blend an RGB tuple with the background at the given alpha (0-255)."""
    bg = (10, 12, 18)
    a = alpha / 255
    r = int(base_rgb[0] * a + bg[0] * (1 - a))
    g = int(base_rgb[1] * a + bg[1] * (1 - a))
    b = int(base_rgb[2] * a + bg[2] * (1 - a))
    return f"#{r:02x}{g:02x}{b:02x}"


# ── helper: draw a rounded rectangle on a canvas ──────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    """Draw a filled rounded rectangle. Returns list of canvas item ids."""
    items = []
    items.append(canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="pieslice", **kwargs))
    items.append(canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="pieslice", **kwargs))
    items.append(canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="pieslice", **kwargs))
    items.append(canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="pieslice", **kwargs))
    items.append(canvas.create_rectangle(x1+r, y1, x2-r, y2, **kwargs))
    items.append(canvas.create_rectangle(x1, y1+r, x2, y2-r, **kwargs))
    return items

def rounded_rect_outline(canvas, x1, y1, x2, y2, r, color, width=1):
    """Draw just the outline of a rounded rectangle."""
    canvas.create_arc(x1,     y1,     x1+2*r, y1+2*r, start=90,  extent=90,  style="arc", outline=color, width=width)
    canvas.create_arc(x2-2*r, y1,     x2,     y1+2*r, start=0,   extent=90,  style="arc", outline=color, width=width)
    canvas.create_arc(x1,     y2-2*r, x1+2*r, y2,     start=180, extent=90,  style="arc", outline=color, width=width)
    canvas.create_arc(x2-2*r, y2-2*r, x2,     y2,     start=270, extent=90,  style="arc", outline=color, width=width)
    canvas.create_line(x1+r, y1,     x2-r, y1,     fill=color, width=width)
    canvas.create_line(x1+r, y2,     x2-r, y2,     fill=color, width=width)
    canvas.create_line(x1,   y1+r,   x1,   y2-r,   fill=color, width=width)
    canvas.create_line(x2,   y1+r,   x2,   y2-r,   fill=color, width=width)


# ==============================================================================
#  STYLED BUTTON  (drawn on a Canvas so we get rounded corners + hover)
# ==============================================================================
class StyledButton(tk.Canvas):
    PRIMARY = "primary"
    GHOST   = "ghost"

    def __init__(self, parent, text, style=PRIMARY, command=None, width=160, height=44):
        super().__init__(parent, width=width, height=height,
                         bg=C_BG, highlightthickness=0, bd=0)
        self.text    = text
        self.style   = style
        self.command = command
        self._heightov    = False
        self._prs    = False
        self._width      = width
        self._height      = height

        self.bind("<Enter>",          self._on_enter)
        self.bind("<Leave>",          self._on_leave)
        self.bind("<ButtonPress-1>",  self._on_press)
        self.bind("<ButtonRelease-1>",self._on_release)
        self.config(cursor="hand2")
        self._draw()

    def _draw(self):
        self.delete("all")
        w, h = self._width, self._height
        r = 10

        if self.style == self.PRIMARY:
            if self._prs:
                fill = C_GOLD_DIM
            elif self._heightov:
                fill = C_GOLD_LT
            else:
                fill = C_GOLD
            rounded_rect(self, 1, 1, w-1, h-1, r, fill=fill, outline="")
            # subtle top highlight
            rounded_rect(self, 2, 2, w-2, h//2, r-2, fill="#ffffff", outline="")
            self.itemconfig("all", stipple="gray25") if self._prs else None
            # redraw solid shapes last so stipple doesn't affect them badly
            self.delete("all")
            rounded_rect(self, 1, 1, w-1, h-1, r, fill=fill, outline="")
            self.create_text(w//2, h//2, text=self.text,
                             font=F_BOLD(13), fill=C_BG, anchor="center")
        else:  # GHOST
            bg_col = blend(C_CARD_HOV, 235) if self._heightov else blend(C_CARD, 220)
            brd    = C_GOLD if self._heightov else rgb(*C_BORDER)
            rounded_rect(self, 1, 1, w-1, h-1, r, fill=bg_col, outline="")
            rounded_rect_outline(self, 1, 1, w-1, h-1, r, brd, width=1)
            self.create_text(w//2, h//2, text=self.text,
                             font=F_BOLD(13), fill=C_TXT, anchor="center")

    def _on_enter(self, _):   self._heightov = True;  self._draw()
    def _on_leave(self, _):   self._heightov = False; self._draw()
    def _on_press(self, _):   self._prs = True;  self._draw()
    def _on_release(self, _):
        self._prs = False; self._draw()
        if self.command:
            self.command()


# ==============================================================================
#  GAME CARD  (Canvas-drawn card with title, description, status, button)
# ==============================================================================
class GameCard(tk.Frame):
    def __init__(self, parent, title, desc, btn_label, jar_path, accent):
        super().__init__(parent, bg=C_BG)
        self._accent    = accent
        self._jar       = jar_path
        self._title_txt = title
        self._desc_txt  = desc
        self._btn_lbl   = btn_label
        self._jar_found = os.path.isfile(jar_path)

        self._normal_bg = blend(C_CARD, 210)
        self._heightover_bg  = blend(C_CARD_HOV, 230)
        self._current_bg = self._normal_bg

        self._build()
        self._bind_hover(self)

    def _build(self):
        # Outer canvas for the rounded card background
        self.card_canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0, bd=0)
        self.card_canvas.pack(fill="both", expand=True)

        # Inner frame sits on top of the canvas
        self.inner = tk.Frame(self.card_canvas, bg=self._normal_bg)
        self.card_canvas.create_window(0, 0, anchor="nw", window=self.inner, tags="inner_win")

        self.inner.columnconfigure(0, weight=1)

        # Title
        self.title_lbl = tk.Label(self.inner, text=self._title_txt,
                                   font=F_DISP(16), fg=self._accent,
                                   bg=self._normal_bg, anchor="w")
        self.title_lbl.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 0))

        # Separator
        sep = tk.Frame(self.inner, height=1, bg=rgb(*C_BORDER))
        sep.grid(row=1, column=0, sticky="ew", padx=24, pady=(10, 0))

        # Description
        self.desc_lbl = tk.Label(self.inner, text=self._desc_txt,
                                  font=F_BODY(12), fg=C_TXT2,
                                  bg=self._normal_bg,
                                  wraplength=260, justify="left", anchor="nw")
        self.desc_lbl.grid(row=2, column=0, sticky="ew", padx=24, pady=(10, 0))

        # Status
        status_txt   = "Ready" if self._jar_found else f"File not found: {self._jar}"
        status_color = C_GREEN if self._jar_found else C_WARN
        self.status_lbl = tk.Label(self.inner, text=status_txt,
                                    font=F_BODY(10), fg=status_color,
                                    bg=self._normal_bg, anchor="w")
        self.status_lbl.grid(row=3, column=0, sticky="ew", padx=24, pady=(8, 0))

        # Spacer
        spacer = tk.Frame(self.inner, bg=self._normal_bg, height=16)
        spacer.grid(row=4, column=0)

        # Button
        self.btn = StyledButton(self.inner, self._btn_lbl,
                                style=StyledButton.PRIMARY,
                                command=self._launch,
                                width=150, height=42)
        self.btn.grid(row=5, column=0, sticky="w", padx=24, pady=(0, 22))

        # Draw the rounded card frame when geometry is known
        self.card_canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_hover(self.inner)
        self._bind_hover(self.title_lbl)
        self._bind_hover(self.desc_lbl)
        self._bind_hover(self.status_lbl)
        self._bind_hover(spacer)

    def _on_canvas_configure(self, event):
        w, h = event.width, event.height
        self.card_canvas.delete("card_bg")
        rounded_rect(self.card_canvas, 1, 1, w-1, h-1, 14,
                     fill=self._current_bg, outline="", tags="card_bg")
        rounded_rect_outline(self.card_canvas, 1, 1, w-1, h-1, 14,
                              rgb(*C_BORDER), width=1)
        self.card_canvas.tag_lower("card_bg")
        # resize the inner frame window to fill the card
        self.card_canvas.itemconfig("inner_win", width=w, height=h)
        self.inner.configure(width=w, height=h)

    def _bind_hover(self, widget):
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")

    def _on_enter(self, _):
        self._current_bg = self._heightover_bg
        self._refresh_bg()
        w = self.card_canvas.winfo_width()
        h = self.card_canvas.winfo_height()
        if w > 1:
            self.card_canvas.delete("card_bg")
            rounded_rect(self.card_canvas, 1, 1, w-1, h-1, 14,
                         fill=self._heightover_bg, outline="", tags="card_bg")
            rounded_rect_outline(self.card_canvas, 1, 1, w-1, h-1, 14,
                                  rgb(*C_BORDER), width=1)
            self.card_canvas.tag_lower("card_bg")

    def _on_leave(self, _):
        self._current_bg = self._normal_bg
        self._refresh_bg()
        w = self.card_canvas.winfo_width()
        h = self.card_canvas.winfo_height()
        if w > 1:
            self.card_canvas.delete("card_bg")
            rounded_rect(self.card_canvas, 1, 1, w-1, h-1, 14,
                         fill=self._normal_bg, outline="", tags="card_bg")
            rounded_rect_outline(self.card_canvas, 1, 1, w-1, h-1, 14,
                                  rgb(*C_BORDER), width=1)
            self.card_canvas.tag_lower("card_bg")

    def _refresh_bg(self):
        bg = self._current_bg
        for w in (self.inner, self.title_lbl, self.desc_lbl,
                  self.status_lbl):
            w.configure(bg=bg)

    def _launch(self):
        if not os.path.isfile(self._jar):
            messagebox.showwarning(
                f"{self._title_txt} - Not Found",
                f"Game file not found at:\n  {self._jar}\n\n"
                f"Place your game file at that path and try again."
            )
            return
        try:
            subprocess.Popen([sys.executable, os.path.abspath(self._jar)])
        except Exception as ex:
            messagebox.showerror("Launch Error",
                                 f"Could not launch the game:\n{ex}")


# ==============================================================================
#  MAIN WINDOW
# ==============================================================================
class ChessMenu(tk.Tk):

    WIN_W = 900
    WIN_H = 620

    def __init__(self, img_path="chess.jpg"):
        super().__init__()
        self.title("Chess")
        self.configure(bg=C_BG)
        self.geometry(f"{self.WIN_W}x{self.WIN_H}")
        self.minsize(720, 500)
        self._center()

        self._bg_photo  = None   # keep reference so GC doesn't collect it
        self._bg_image  = None   # PIL Image

        # Load background image
        if PIL_AVAILABLE and os.path.isfile(img_path):
            try:
                self._bg_image = Image.open(img_path)
            except Exception as e:
                print(f"Could not load image: {e}")

        self._build()
        self.bind("<Configure>", self._on_resize)

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - self.WIN_W) // 2
        y  = (sh - self.WIN_H) // 2
        self.geometry(f"{self.WIN_W}x{self.WIN_H}+{x}+{y}")

    # ── BUILD UI ──────────────────────────────────────────────────────────────
    def _build(self):
        # Root canvas: fills the whole window, paints bg image + all UI
        self.canvas = tk.Canvas(self, bg=C_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ── HEADER ────────────────────────────────────────────────────────────
        header_frame = tk.Frame(self.canvas, bg=C_BG)
        self.canvas.create_window(0, 0, anchor="nw",
                                   window=header_frame, tags="header_win")

        logo_bg = blend(C_CARD, 185)
        logo_pill = tk.Frame(header_frame, bg=logo_bg,
                              padx=18, pady=8)
        logo_pill.pack(side="left", padx=(32, 0), pady=(24, 0))

        logo_lbl = tk.Label(logo_pill, text="Chess",
                             font=F_DISP(17), fg=C_GOLD, bg=logo_bg)
        logo_lbl.pack()

        # ── CENTRE CONTENT ────────────────────────────────────────────────────
        centre_frame = tk.Frame(self.canvas, bg=C_BG)
        self.canvas.create_window(0, 0, anchor="nw",
                                   window=centre_frame, tags="centre_win")

        # Title block
        title_bg = blend((8, 10, 18), 160)
        title_block = tk.Frame(centre_frame, bg=title_bg, padx=40, pady=20)
        title_block.pack(pady=(0, 0))

        tk.Label(title_block, text="Welcome to Chess",
                 font=F_DISP(34), fg=C_TXT, bg=title_bg).pack()
        tk.Label(title_block, text="Select a game mode to begin",
                 font=F_BODY(15), fg=C_TXT2, bg=title_bg).pack(pady=(6, 0))

        # Game cards row
        cards_frame = tk.Frame(centre_frame, bg=C_BG)
        cards_frame.pack(pady=(32, 0))

        self.chess_card = GameCard(
            cards_frame,
            title     = "Classic Chess",
            desc      = "Play a full chess match using standard FIDE rules against your opponent. (PLEASE USE THE JAVA VERSION)",
            btn_label = "Play Now",
            jar_path  = "Null",
            accent    = C_GOLD
        )
        self.chess_card.pack(side="left", padx=(0, 12), fill="both", expand=True)
        self.chess_card.configure(width=330, height=240)

        self.puzzle_card = GameCard(
            cards_frame,
            title     = "Chess Puzzles",
            desc      = "Train your tactical vision by solving carefully crafted chess puzzles. The puzzles will run in console",
            btn_label = "Solve Puzzles",
            jar_path  = PUZZLE_JAR,
            accent    = C_BLUE
        )
        self.puzzle_card.pack(side="left", padx=(12, 0), fill="both", expand=True)
        self.puzzle_card.configure(width=330, height=240)

        # ── FOOTER ────────────────────────────────────────────────────────────
        footer_frame = tk.Frame(self.canvas, bg=C_BG)
        self.canvas.create_window(0, 0, anchor="nw",
                                   window=footer_frame, tags="footer_win")



        # store refs
        self._heighteader_frame = header_frame
        self._centre_frame = centre_frame
        self._footer_frame = footer_frame

        # draw image + reposition elements now
        self.after(10, self._redraw)

    # ── BACKGROUND + LAYOUT ──────────────────────────────────────────────────
    def _on_resize(self, event):
        if event.widget is self:
            self.after_idle(self._redraw)

    def _redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return

        self.canvas.delete("bg")

        # 1. Dark background fill
        self.canvas.create_rectangle(0, 0, w, h, fill=C_BG, outline="", tags="bg")

        # 2. Background image (cover-fit)
        if self._bg_image and PIL_AVAILABLE:
            img = self._bg_image
            ir  = img.width / img.height
            pr  = w / h
            if ir > pr:
                dh = h; dw = int(h * ir); dx = (w - dw) // 2; dy = 0
            else:
                dw = w; dh = int(w / ir); dx = 0; dy = (h - dh) // 2

            resized = img.resize((dw, dh), Image.LANCZOS)

    
            overlay = Image.new("RGBA", (dw, dh), (0, 0, 0, 150))
            base    = resized.convert("RGBA")
            composited = Image.alpha_composite(base, overlay).convert("RGB")


            cx = max(0, -dx); cy = max(0, -dy)
            cropped = composited.crop((cx, cy, cx + w, cy + h))

            self._bg_photo = ImageTk.PhotoImage(cropped)
            self.canvas.create_image(0, 0, anchor="nw",
                                      image=self._bg_photo, tags="bg")

        # Bring UI windows above background
        self.canvas.tag_raise("header_win")
        self.canvas.tag_raise("centre_win")
        self.canvas.tag_raise("footer_win")

        # 3. Position header (top-left)
        self.canvas.coords("header_win", 0, 0)

        # 4. Position centre (vertically and horizontally centred)
        self._centre_frame.update_idletasks()
        cw = self._centre_frame.winfo_reqwidth()
        ch = self._centre_frame.winfo_reqheight()
        cx = (w - cw) // 2
        cy = max(60, (h - ch) // 2)
        self.canvas.coords("centre_win", cx, cy)


if __name__ == "__main__":
    if not PIL_AVAILABLE:
        print("Warning: Pillow not installed. Background image will not show.")
        print("Install with:  pip install Pillow")

    app = ChessMenu("chess.jpg")
    app.mainloop()
