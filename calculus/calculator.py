#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════╗
║          CALCULUS — Advanced CLI Calculator v2.0          ║
║          Built with Python · Crafted with care            ║
╚═══════════════════════════════════════════════════════════╝
"""

import math
import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
#  ANSI COLOR PALETTE
# ─────────────────────────────────────────────

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    PRIMARY = "\033[38;5;51m"
    ACCENT  = "\033[38;5;201m"
    SUCCESS = "\033[38;5;82m"
    WARNING = "\033[38;5;220m"
    ERROR   = "\033[38;5;196m"
    MUTED   = "\033[38;5;240m"
    HEADER  = "\033[38;5;226m"

THEMES = {
    "neon":   {"PRIMARY": "\033[38;5;51m",  "ACCENT": "\033[38;5;201m", "SUCCESS": "\033[38;5;82m",  "HEADER": "\033[38;5;226m"},
    "ocean":  {"PRIMARY": "\033[38;5;39m",  "ACCENT": "\033[38;5;45m",  "SUCCESS": "\033[38;5;120m", "HEADER": "\033[38;5;159m"},
    "sunset": {"PRIMARY": "\033[38;5;208m", "ACCENT": "\033[38;5;198m", "SUCCESS": "\033[38;5;154m", "HEADER": "\033[38;5;220m"},
    "mono":   {"PRIMARY": "\033[38;5;255m", "ACCENT": "\033[38;5;250m", "SUCCESS": "\033[38;5;245m", "HEADER": "\033[38;5;231m"},
}

def apply_theme(name: str):
    t = THEMES.get(name, THEMES["neon"])
    Color.PRIMARY = t["PRIMARY"]
    Color.ACCENT  = t["ACCENT"]
    Color.SUCCESS = t["SUCCESS"]
    Color.HEADER  = t["HEADER"]


# ─────────────────────────────────────────────
#  HISTORY & MEMORY MANAGER
# ─────────────────────────────────────────────

HISTORY_FILE = Path.home() / ".calculus_history.json"

class HistoryManager:
    def __init__(self, max_entries: int = 100):
        self.entries: list[dict] = []
        self.max_entries = max_entries
        self._load()

    def _load(self):
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE) as f:
                    data = json.load(f)
                    self.entries = data.get("entries", [])[-self.max_entries:]
            except Exception:
                self.entries = []

    def save(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump({"entries": self.entries}, f, indent=2)
        except Exception:
            pass

    def add(self, expression: str, result: float):
        self.entries.append({
            "expr": expression,
            "result": result,
            "time": datetime.now().strftime("%H:%M:%S"),
        })
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)
        self.save()

    def last_result(self) -> float | None:
        return self.entries[-1]["result"] if self.entries else None

    def show(self, n: int = 10):
        recent = self.entries[-n:]
        if not recent:
            cprint("  No history yet.", Color.MUTED)
            return
        cprint(f"\n  {'#':<4} {'Time':<10} {'Expression':<30} {'Result'}", Color.HEADER + Color.BOLD)
        cprint("  " + "─" * 60, Color.MUTED)
        for i, e in enumerate(recent, 1):
            cprint(f"  {i:<4} {e['time']:<10} {e['expr']:<30} {fmt_result(e['result'])}", Color.PRIMARY)


class MemoryBank:
    def __init__(self):
        self._val: float = 0.0

    def store(self, v: float):  self._val = v
    def add(self,   v: float):  self._val += v
    def sub(self,   v: float):  self._val -= v
    def recall(self) -> float:  return self._val
    def clear(self):            self._val = 0.0

    @property
    def display(self) -> str:
        return fmt_result(self._val)


# ─────────────────────────────────────────────
#  FORMATTING HELPERS
# ─────────────────────────────────────────────

def cprint(text: str, color: str = ""):
    print(f"{color}{text}{Color.RESET}")

def fmt_result(v: float) -> str:
    if isinstance(v, complex):
        return str(v)
    if v == int(v) and abs(v) < 1e15:
        return f"{int(v):,}"
    return f"{v:.10g}"

def separator(char="─", width=62, color=None):
    cprint(f"  {char * width}", color or Color.MUTED)


# ─────────────────────────────────────────────
#  CORE MATH OPERATIONS
# ─────────────────────────────────────────────

def add(a, b):       return a + b
def subtract(a, b):  return a - b
def multiply(a, b):  return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero — the universe would implode.")
    return a / b

def power(a, b):     return a ** b

def modulo(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero.")
    return a % b

def floor_div(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot floor-divide by zero.")
    return a // b

def sqrt(a):
    if a < 0:
        raise ValueError(f"√{a} is complex — enable complex mode with 'complex on'.")
    return math.sqrt(a)

def cbrt(a):         return math.copysign(abs(a) ** (1/3), a)

def ln(a):
    if a <= 0:
        raise ValueError("ln requires a positive number.")
    return math.log(a)

def log10(a):
    if a <= 0:
        raise ValueError("log10 requires a positive number.")
    return math.log10(a)

def log2(a):
    if a <= 0:
        raise ValueError("log2 requires a positive number.")
    return math.log2(a)

def factorial(a):
    if a < 0 or a != int(a):
        raise ValueError("Factorial requires a non-negative integer.")
    return math.factorial(int(a))

def percent(a):      return a / 100

TRIG_FUNCS = {
    "sin":  math.sin,  "cos":  math.cos,  "tan":  math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
}

ANGLE_MODE = "deg"

def trig(fn_name: str, a: float) -> float:
    fn = TRIG_FUNCS[fn_name]
    if fn_name in ("sin","cos","tan") and ANGLE_MODE == "deg":
        a = math.radians(a)
    result = fn(a)
    if fn_name in ("asin","acos","atan") and ANGLE_MODE == "deg":
        result = math.degrees(result)
    return result


# ─────────────────────────────────────────────
#  SAFE EXPRESSION EVALUATOR
# ─────────────────────────────────────────────

SAFE_NAMES = {
    "pi":    math.pi,
    "e":     math.e,
    "tau":   math.tau,
    "inf":   math.inf,
    "phi":   (1 + math.sqrt(5)) / 2,
    "sqrt":  math.sqrt,
    "cbrt":  cbrt,
    "abs":   abs,
    "ceil":  math.ceil,
    "floor": math.floor,
    "round": round,
    "log":   math.log,
    "log10": math.log10,
    "log2":  math.log2,
    "ln":    math.log,
    "exp":   math.exp,
    "sin":   lambda x: math.sin(math.radians(x) if ANGLE_MODE=="deg" else x),
    "cos":   lambda x: math.cos(math.radians(x) if ANGLE_MODE=="deg" else x),
    "tan":   lambda x: math.tan(math.radians(x) if ANGLE_MODE=="deg" else x),
    "asin":  lambda x: math.degrees(math.asin(x)) if ANGLE_MODE=="deg" else math.asin(x),
    "acos":  lambda x: math.degrees(math.acos(x)) if ANGLE_MODE=="deg" else math.acos(x),
    "atan":  lambda x: math.degrees(math.atan(x)) if ANGLE_MODE=="deg" else math.atan(x),
    "atan2": math.atan2,
    "sinh":  math.sinh,
    "cosh":  math.cosh,
    "tanh":  math.tanh,
    "factorial": math.factorial,
    "gcd":   math.gcd,
    "lcm":   math.lcm,
    "comb":  math.comb,
    "perm":  math.perm,
    "hypot": math.hypot,
}

def safe_eval(expr: str, ans: float | None = None) -> float:
    expr = expr.strip()
    expr = expr.replace("^", "**")
    expr = expr.replace("×", "*").replace("÷", "/")

    if ans is not None:
        expr = expr.replace("ans", str(ans))

    expr = re.sub(r'(\d)(pi|e|tau|phi|sqrt|sin|cos|tan|log|ln|exp|abs|ceil|floor)', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)

    allowed_globals = {"__builtins__": {}}
    allowed_globals.update(SAFE_NAMES)

    try:
        result = eval(expr, allowed_globals)
        return float(result)
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero.")
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}")


# ─────────────────────────────────────────────
#  UNIT CONVERTER
# ─────────────────────────────────────────────

CONVERSIONS = {
    ("km","m"):    1000,    ("m","km"):    0.001,
    ("m","cm"):    100,     ("cm","m"):    0.01,
    ("m","mm"):    1000,    ("mm","m"):    0.001,
    ("mi","km"):   1.60934, ("km","mi"):   0.621371,
    ("ft","m"):    0.3048,  ("m","ft"):    3.28084,
    ("in","cm"):   2.54,    ("cm","in"):   0.393701,
    ("kg","g"):    1000,    ("g","kg"):    0.001,
    ("kg","lb"):   2.20462, ("lb","kg"):   0.453592,
    ("lb","oz"):   16,      ("oz","lb"):   0.0625,
    ("hr","min"):  60,      ("min","hr"):  1/60,
    ("min","sec"): 60,      ("sec","min"): 1/60,
    ("day","hr"):  24,      ("hr","day"):  1/24,
    ("kb","b"):    1024,    ("b","kb"):    1/1024,
    ("mb","kb"):   1024,    ("kb","mb"):   1/1024,
    ("gb","mb"):   1024,    ("mb","gb"):   1/1024,
    ("tb","gb"):   1024,    ("gb","tb"):   1/1024,
    ("sqm","sqft"):10.7639, ("sqft","sqm"):0.0929,
    ("acre","sqm"):4046.86, ("sqm","acre"):0.000247105,
}

def convert_units(value: float, from_u: str, to_u: str) -> float:
    from_u, to_u = from_u.lower(), to_u.lower()
    if from_u == "c" and to_u == "f": return value * 9/5 + 32
    if from_u == "f" and to_u == "c": return (value - 32) * 5/9
    if from_u == "c" and to_u == "k": return value + 273.15
    if from_u == "k" and to_u == "c": return value - 273.15
    if from_u == "f" and to_u == "k": return (value - 32) * 5/9 + 273.15
    if from_u == "k" and to_u == "f": return (value - 273.15) * 9/5 + 32
    key = (from_u, to_u)
    if key in CONVERSIONS:
        return value * CONVERSIONS[key]
    raise ValueError(f"Unknown conversion: {from_u} → {to_u}")


# ─────────────────────────────────────────────
#  DISPLAY
# ─────────────────────────────────────────────

BANNER = r"""
  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║    ██████╗ █████╗ ██╗      ██████╗██╗   ██╗██╗   ██╗███████╗║
  ║   ██╔════╝██╔══██╗██║     ██╔════╝██║   ██║██║   ██║██╔════╝║
  ║   ██║     ███████║██║     ██║     ██║   ██║██║   ██║███████╗ ║
  ║   ██║     ██╔══██║██║     ██║     ██║   ██║██║   ██║╚════██║ ║
  ║   ╚██████╗██║  ██║███████╗╚██████╗╚██████╔╝╚██████╔╝███████║ ║
  ║    ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝║
  ║                                                              ║
  ║           Advanced CLI Calculator  ·  v2.0                  ║
  ╚══════════════════════════════════════════════════════════════╝
"""

HELP_TEXT = """
  ┌──────────────────────────────────────────────────────────┐
  │                    QUICK REFERENCE                       │
  ├──────────────────────────────────────────────────────────┤
  │  EXPRESSIONS   Type any math expression:                 │
  │    3 + 4 * 2      standard arithmetic                    │
  │    (1 + 2) ^ 3    use ^ or ** for power                  │
  │    sqrt(144)      functions with parens                  │
  │    sin(45)        trig in current angle mode             │
  │    2pi            implicit multiplication                 │
  │    ans + 1        use last result                        │
  ├──────────────────────────────────────────────────────────┤
  │  COMMANDS                                                │
  │    hist [n]        show last n history entries           │
  │    clear hist      clear all history                     │
  │    ms/m+/m-/mr/mc  memory operations                     │
  │    conv <n> <f> <t> unit conversion                      │
  │    deg / rad       angle mode                            │
  │    theme <name>    neon|ocean|sunset|mono                │
  │    cls             clear screen                          │
  │    help / ?        this help                             │
  │    exit / quit     exit                                  │
  └──────────────────────────────────────────────────────────┘
"""


# ─────────────────────────────────────────────
#  MAIN REPL
# ─────────────────────────────────────────────

def process_command(raw: str, history: HistoryManager, mem: MemoryBank) -> bool:
    global ANGLE_MODE

    line = raw.strip()
    if not line:
        return True

    lower = line.lower()

    if lower in ("exit", "quit", "q", "bye"):
        cprint("\n  Thanks for using Calculus. See you! ✓\n", Color.SUCCESS + Color.BOLD)
        return False

    if lower in ("help", "?", "h"):
        cprint(HELP_TEXT, Color.PRIMARY)
        return True

    if lower in ("cls", "clear"):
        os.system("cls" if os.name == "nt" else "clear")
        return True

    if lower.startswith("hist"):
        parts = lower.split()
        n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        history.show(n)
        return True

    if lower == "clear hist":
        history.entries.clear()
        history.save()
        cprint("  History cleared.", Color.SUCCESS)
        return True

    if lower == "mr":
        val = mem.recall()
        cprint(f"  MR  =  {Color.SUCCESS}{fmt_result(val)}{Color.RESET}", Color.PRIMARY)
        return True
    if lower == "mc":
        mem.clear()
        cprint("  Memory cleared.", Color.SUCCESS)
        return True
    if lower == "mem":
        cprint(f"  Memory  =  {Color.SUCCESS}{mem.display}{Color.RESET}", Color.PRIMARY)
        return True

    for cmd, fn in [("ms ", mem.store), ("m+ ", mem.add), ("m- ", mem.sub)]:
        if lower.startswith(cmd):
            try:
                val = safe_eval(line[len(cmd):], history.last_result())
                fn(val)
                cprint(f"  Memory  =  {Color.SUCCESS}{mem.display}{Color.RESET}", Color.PRIMARY)
            except Exception as ex:
                cprint(f"  Error: {ex}", Color.ERROR)
            return True

    if lower.startswith("conv "):
        parts = line.split()
        if len(parts) == 4:
            try:
                val = float(parts[1])
                result = convert_units(val, parts[2], parts[3])
                expr = f"{fmt_result(val)} {parts[2]} → {parts[3]}"
                cprint(f"\n  {expr}", Color.MUTED)
                cprint(f"  = {Color.SUCCESS}{Color.BOLD}{fmt_result(result)} {parts[3]}{Color.RESET}\n", Color.SUCCESS)
                history.add(expr, result)
            except Exception as ex:
                cprint(f"  Error: {ex}", Color.ERROR)
        else:
            cprint("  Usage: conv <value> <from_unit> <to_unit>", Color.WARNING)
        return True

    if lower in ("deg", "rad"):
        ANGLE_MODE = lower
        cprint(f"  Angle mode: {Color.ACCENT}{ANGLE_MODE.upper()}{Color.RESET}", Color.PRIMARY)
        return True

    if lower.startswith("theme "):
        name = lower.split()[1]
        if name in THEMES:
            apply_theme(name)
            cprint(f"  Theme: {Color.ACCENT}{name}{Color.RESET}", Color.PRIMARY)
        else:
            cprint(f"  Unknown theme. Options: {', '.join(THEMES)}", Color.WARNING)
        return True

    # Expression evaluation
    try:
        ans = history.last_result()
        result = safe_eval(line, ans)
        print()
        cprint(f"  {Color.MUTED}{line}{Color.RESET}", "")
        cprint(f"  {Color.BOLD}{'─'*40}{Color.RESET}", Color.PRIMARY)
        cprint(f"  {Color.SUCCESS}{Color.BOLD}= {fmt_result(result)}{Color.RESET}\n", "")
        history.add(line, result)
    except Exception as ex:
        cprint(f"\n  {Color.ERROR}✖  {ex}{Color.RESET}\n", "")

    return True


def status_bar(history: HistoryManager, mem: MemoryBank) -> str:
    angle  = f"{Color.ACCENT}{ANGLE_MODE.upper()}{Color.RESET}"
    memory = f"M={Color.WARNING}{mem.display}{Color.RESET}"
    ans    = history.last_result()
    last   = f"ans={Color.SUCCESS}{fmt_result(ans)}{Color.RESET}" if ans is not None else f"{Color.MUTED}no ans{Color.RESET}"
    return f"  {Color.MUTED}[{Color.RESET}{angle}{Color.MUTED}]{Color.RESET}  {memory}  {last}"


def run():
    apply_theme("neon")
    history = HistoryManager()
    mem     = MemoryBank()

    cprint(BANNER, Color.PRIMARY + Color.BOLD)
    cprint("  Type an expression, 'help' for commands, or 'exit' to quit.\n", Color.MUTED)

    while True:
        try:
            print(status_bar(history, mem))
            separator()
            user_input = input(f"  {Color.HEADER}{Color.BOLD}  ›  {Color.RESET}")
            separator()
        except (KeyboardInterrupt, EOFError):
            cprint("\n\n  Interrupted. Goodbye!\n", Color.MUTED)
            break

        if not process_command(user_input, history, mem):
            break


if __name__ == "__main__":
    run()
