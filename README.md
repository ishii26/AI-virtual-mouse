# Virtual Mouse using Hand Gestures

This project uses a webcam, MediaPipe, and PyAutoGUI to transform your hand gestures into real-time mouse actions such as moving the cursor, click, drag-and-drop and more - all without touching your mouse!

## Features

#### Move Cursor:

Raise your index finger and move your hand to move the mouse.

#### Left Click:

Raise both index and middle fingers close together to perform a left click.

#### Drag and Drop:

Pinch (thumb + index finger) to click and hold, then move hand to drag; release pinch to drop.

#### Right Click:

Raise only the pinky finger to perform a right click.

#### Double Click:

Tap index and middle fingers together quickly to double-click.

#### Real-time FPS Display

#### Compatible with macOS

## How It Works

- MediaPipe detects 21 hand landmarks in real-time.
- Gesture Detection logic checks which fingers are raised and calculates distances between fingertips.
- PyAutoGUI is used to move the cursor, simulate clicks and other mouse actions.
