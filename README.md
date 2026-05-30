# ⚡ CALCULUS — Advanced Calculator v2.0

> A beautifully crafted calculator in two flavours: a feature-rich **Python CLI** and a stunning **web UI** — both fully functional, zero dependencies.
## 🌐 Live Demo
👉 [Open Web Calculator](https://agnuspaul.github.io/Calculator-CLI/)
---
---

## 📁 Project Structure

```
calculus/
├── 📄 calculator.py          ← Main CLI app (Python 3.10+)
├── 🧪 test_calculator.py     ← 42 unit tests — all passing ✓
├── 🌐 index.html             ← Web UI (open in browser / Live Server)
├── 📋 requirements.txt       ← No pip installs needed!
├── 📖 README.md              ← You're reading it
├── .gitignore
└── .vscode/
    ├── settings.json         ← Editor config (tabs, format-on-save)
    ├── launch.json           ← F5 to run or debug
    ├── tasks.json            ← Ctrl+Shift+B to launch
    └── extensions.json       ← Recommended extensions
```

---

## 🚀 Getting Started in VS Code

### Option A — CLI Calculator (Python)

1. Open the folder in VS Code:
   ```
   File → Open Folder → select the `calculus/` folder
   ```

2. Press **`Ctrl+Shift+B`** (or **`Cmd+Shift+B`** on Mac) to run the calculator directly.

   **Or** open the integrated terminal and type:
   ```bash
   python3 calculator.py
   ```

3. To run all 42 tests:
   ```bash
   python3 test_calculator.py
   ```
   Or press **`Ctrl+Shift+P`** → `Tasks: Run Test Task`

4. To debug: press **`F5`** and pick **"▶ Run Calculator"** or **"🧪 Run All Tests"**

### Option B — Web UI

1. Install the **Live Server** extension (recommended in `.vscode/extensions.json`)
2. Right-click `index.html` → **"Open with Live Server"**
3. Or just double-click `index.html` to open in your browser directly

---

## ✨ Features

| Feature | CLI | Web UI |
|---|:---:|:---:|
| Basic arithmetic (+, -, *, /, %) | ✅ | ✅ |
| Expression evaluator (`3*(2+sqrt(144))^2`) | ✅ | ✅ |
| 40+ math functions | ✅ | ✅ |
| Constants: π, e, τ, φ, ∞ | ✅ | ✅ |
| Implicit multiplication (`2pi`, `3(x+1)`) | ✅ | ✅ |
| `ans` — use last result | ✅ | ✅ |
| Memory bank (MS, M+, M−, MR, MC) | ✅ | ✅ |
| Persistent history (across sessions) | ✅ | ✅ |
| Unit converter (length, mass, temp, time…) | ✅ | ✅ |
| Angle mode: DEG / RAD | ✅ | ✅ |
| Color themes (neon, ocean, sunset, mono) | ✅ | ✅ |
| Keypad buttons | ❌ | ✅ |
| Quick reference panel | ❌ | ✅ |

---

## 💡 Usage Examples

```
  › 2 + 3 * 4
  = 14

  › (1 + 2) ^ 10
  = 59,049

  › sqrt(2) * pi
  = 4.442882938

  › sin(45)
  = 0.7071067812

  › factorial(12)
  = 479,001,600

  › ans / 2
  = 239,500,800

  › conv 100 c f
  = 212 f

  › ms 42
  Memory = 42

  › m+ sqrt(16)
  Memory = 46

  › hist 5
  # shows last 5 calculations
```

---

## 📋 Full Command Reference

### Arithmetic Operators
| Operator | Meaning | Example |
|---|---|---|
| `+` `-` `*` `/` | Basic arithmetic | `3 + 4` → `7` |
| `//` | Floor division | `22 // 7` → `3` |
| `%` | Modulo | `22 % 7` → `1` |
| `**` or `^` | Power | `2^10` → `1024` |

### Math Functions
`sqrt` `cbrt` `abs` `ceil` `floor` `round` `exp` `hypot`
`ln` `log` `log2` `log10`
`sin` `cos` `tan` `asin` `acos` `atan`
`sinh` `cosh` `tanh`
`factorial` `gcd` `lcm` `comb` `perm`

### Constants
`pi`  `e`  `tau`  `phi`  `inf`

### CLI Commands
| Command | Action |
|---|---|
| `hist [n]` | Last n history entries (default 10) |
| `clear hist` | Delete all history |
| `ms <expr>` | Memory Store |
| `m+ <expr>` | Memory Add |
| `m- <expr>` | Memory Subtract |
| `mr` | Memory Recall |
| `mc` | Memory Clear |
| `conv <val> <from> <to>` | Unit conversion |
| `deg` / `rad` | Angle mode toggle |
| `theme <name>` | `neon` `ocean` `sunset` `mono` |
| `cls` | Clear screen |
| `help` / `?` | Show help |
| `exit` / `q` | Quit |

### Unit Conversion Reference
| Category | Units |
|---|---|
| Length | `km` `m` `cm` `mm` `mi` `ft` `in` |
| Mass | `kg` `g` `lb` `oz` |
| Temperature | `c` `f` `k` |
| Time | `day` `hr` `min` `sec` |
| Digital | `tb` `gb` `mb` `kb` `b` |
| Area | `sqm` `sqft` `acre` |

---

## 🧪 Test Results

```
============================================================
  CALCULUS — Test Suite
============================================================

test_add ... ok
test_divide ... ok
...

Ran 42 tests in 0.003s

  ✓ All 42 tests passed!
============================================================
```

**Test coverage:**
- `TestArithmetic` — add, subtract, multiply, divide, power, modulo
- `TestAdvancedMath` — sqrt, cbrt, ln, log10, log2, factorial
- `TestSafeEval` — expressions, precedence, constants, functions, security
- `TestUnitConverter` — length, mass, temperature, time, digital
- `TestMemoryBank` — store, add, subtract, recall, clear
- `TestFormatting` — integer display, float precision, negatives

---

## 🔒 Security

The expression evaluator uses a **whitelist-only** approach — `eval()` runs with `__builtins__` disabled and only safe math functions allowed. Attempts to use `os`, `open`, `import`, or any Python builtin are blocked.

---

## ⚙️ Requirements

- **Python 3.10+** (uses `float | None` union type hints)
- **No pip installs** — pure standard library
- Any modern browser for `index.html`

---

## 📄 License

MIT — free to use, modify, and distribute.

---

*Built with Python · Crafted with care ⚡*
