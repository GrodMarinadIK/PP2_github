### 🎨 PyPaint: Feature-Rich Drawing Application

A versatile 2D drawing application built using Python and Pygame. 
This project features a variety of geometric tools, custom drawing modes, and a robust history system (Undo) to provide a smooth creative experience.

---

### 🚀 Key Features
- Geometric Shapes: Dedicated tools for drawing rectangles, squares, circles, right triangles, equilateral triangles, and rhombuses.
- Advanced Brush System: Smooth line drawing algorithm to prevent "dotted" lines during fast mouse movements.
- Functional Tools: Fill Tool: Stack-based flood fill algorithm to avoid recursion depth issues.
- Text Tool: Dynamic text placement on the canvas.
- Eraser: Adjustable size for precise corrections.
- User Experience: Undo System: Integrated history buffer (Ctrl+Z) to revert accidental strokes.
- Save Function: Export your masterpiece as a PNG file directly from the app (Ctrl+S).
- Interactive Menu: A top-bar UI for quick selection of tools, colors, and brush sizes.

---

### 🛠 Tech Stack
- Language: Python 3.10+
- Library: pygame (Graphics and Event handling)
- Algorithms: - Bresenham-like interpolation for smooth lines.
    - Iterative Flood Fill for the paint bucket tool.

---

### 📂 Project Structure
```
Paint/
├── assets/        # Icons and images for the UI
├── paint.py       # Main application loop and UI rendering
├── tools.py       # Mathematical logic for drawing shapes and fill algorithms
└── screenshots/   # (Optional) Visual demos of the app
```

---

### 🎮 How to Use

| Controls          | ActionKey / Input             |
| :---              | :---                          |
| Draw              | Left Mouse Button (Hold)      |
| Change Brush Size | 1 through 6                   |
| Undo Last Action  | Ctrl + Z                      |
| Save Image        | Ctrl + S                      |
| Select Tool/Color | Click buttons in the top menu |

---

### Installation:
1) Install the required dependency:
```Bash
pip install pygame
```
2) Run the application:
```Bash
python paint.py
```

---

### 📐 Mathematical Logic
The `tools.py` module contains custom logic for shape rendering. Unlike standard rectangles, shapes like the **Equilateral Triangle** and **Rhombus** are calculated dynamically based on the starting mouse position and current cursor coordinates to ensure proper geometric proportions.

---

### 👤 Author
Zhanspayev Miruansani (GrodMarinad2k)

First-year Undergraduate at KBTU (Computer Systems and Software)




