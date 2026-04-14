# Mickey's Clock

An analog clock application featuring Mickey Mouse hands, synchronized with your system's real-time data.

## Features
- **Real-time Sync**: Uses the `datetime` module for 100% accurate timekeeping.
- **Pivot Rotation**: Custom math implementation to rotate hands around Mickey's "wrists".
- **Semi-transparent Hands**: Tinted and transparent layers for a modern "glassy" look.
- **Smooth Animation**: 60 FPS update rate for fluid second-hand movement.

## Implementation Details
The project is split into two parts:
- `clock.py`: Handles the trigonometric calculations for hand angles.
- `main.py`: Handles the rendering pipeline and hand transformations.