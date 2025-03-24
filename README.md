# MBM-Clock (Mind Before Machine)

A productivity tool that helps you manage your approach to problem-solving with a focus on using your own thinking before resorting to AI assistance.

![Screenshot 2025-03-24 205302](https://github.com/user-attachments/assets/ae9a9383-7588-42e7-a024-eb477d81443b)

## Overview

Mind Before Machine is a customizable multi-phase timer application that helps you structure your problem-solving process by encouraging thoughtful engagement with challenges before turning to AI tools. This approach promotes deeper learning, better retention, and more creative solutions.

## Philosophy

When faced with a problem, it's tempting to immediately ask an LLM (Large Language Model) like ChatGPT, Claude, or other AI assistants for solutions. However, this can:

- Limit your own skill development
- Reduce critical thinking practice
- Create dependency on AI tools
- Decrease long-term knowledge retention

Mind Before Machine encourages a balanced approach: **think first, then enhance with AI**. By dedicating structured time to your own thought process before consulting AI tools, you build stronger cognitive skills while still benefiting from AI assistance when needed.

## Features

- **Multi-phase Timer**: Configure multiple timed phases for different stages of your problem-solving process
- **Always-on-top Display**: Timer stays visible while you work
- **Task Tracking**: Name and track your tasks
- **History Management**: Review completed tasks and their outcomes
- **Phase Accountability**: Records whether you completed each phase legitimately or "cheated" by skipping ahead
- **Customizable UI**: Adjust timer size and appearance
- **Cross-platform**: Works on Windows, macOS, and Linux

## How It Works

**Demo:**
https://github.com/user-attachments/assets/384bbc4d-cc35-456d-b418-b7a01305494d



1. **Start a new task**: Name your current challenge/problem
2. **Configure phases**: Set up multiple timed phases (e.g., "Think", "Research", "Plan", "Implement", "AI Assist")
3. **Work through each phase**: The timer keeps you accountable to spending dedicated time in each stage
4. **Complete or advance**: When a phase timer completes, decide whether to move to the next phase or complete the entire task
5. **Review history**: Track your progress and see how you've improved your independent problem-solving skills

## Recommended Workflow

A suggested workflow might be:

1. **Phase 1 (15-30 min)**: Think about the problem independently, without any external resources
2. **Phase 2 (15-30 min)**: Research and explore relevant documentation/resources
3. **Phase 3 (10-15 min)**: Implement a solution attempt based on your own understanding
4. **Phase 4 (10-15 min)**: Leverage AI assistance to enhance or correct your solution

This structure ensures you develop your own thinking skills while still benefiting from AI capabilities.

## Installation 

### Option 1: Using the Windows Executable

If you've built the executable using the instructions in the "Building from Source" section:

1. Navigate to the `dist/Mind_Before_Machine` directory
2. Run `MBM Clock.exe`

### Option 2: Running from Source

#### Prerequisites

- Python 3.6+
- PyQt5

#### Dependencies

```
pip install PyQt5
```

For Windows users, you may also need:
```
pip install pywin32
```

#### Running the Application

Clone the repository:
```
git clone https://github.com/nunichego/MBM-Clock.git
cd MBM-Clock
```

Run the application:
```
python main.py
```

## Usage Guide

### Main Timer Window

- **Timer Display**: Shows remaining time for current phase
- **Settings Button**: Configure timer appearance and phases
- **Notes Button**: View task history and manage phases
- **Close Button**: Exit the application

The timer window can be moved by clicking and dragging. Buttons auto-hide after a few seconds and reappear when you click the timer.

### Settings

- **Timer Size**: Adjust the size of the timer display
- **Number of Phases**: Configure how many phases your task has
- **Phase Names**: Give meaningful names to each phase
- **Phase Duration**: Set the time for each phase

### Notes and History

- **Task History**: View completed tasks and their status
- **Phase Details**: See the details of each phase completion
- **Task Management**: Start new tasks or complete current ones

## Building from Source

### Building a Windows Executable

The application includes a dedicated build script to create a Windows executable:

1. Install the required dependencies:
```
pip install pyinstaller pillow
```

2. Run the build script:
```
python build_app.py
```

This will:
- Create an icon file if needed
- Clean previous build directories
- Run PyInstaller with the optimized spec file
- Copy necessary resources to the build directory

The executable will be created in the `dist/Mind_Before_Machine` directory.

### Alternative Manual Build

You can also build the executable manually using PyInstaller:

```
pip install pyinstaller
pyinstaller timer_app.spec
```

Or for a simple build without the spec file:

```
pyinstaller --name="MBM Clock" --windowed --icon=resources/icons/icon.ico main.py
```

## License

This project is licensed under GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## Acknowledgments

- Inspired by the Pomodoro Technique and other time management methods
- Designed to promote mindful use of AI assistance tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/feature`)
5. Open a Pull Request
