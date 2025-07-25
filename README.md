# SmartMusicPlayer
# 🎵 Smart Music Player with Hand Gesture Recognition

A smart music player application that integrates **real-time hand gesture recognition** to control audio playback. This system offers an intuitive and contactless method of controlling music using **computer vision**, a **graphical user interface (GUI)**, and **database-backed personalization**.

---

## 🔧 Features

- 🎮 **Gesture-based control** using a webcam (Play/Pause, Next, Previous)
- 🖥️ **User-friendly GUI** built with Tkinter for manual control and feedback
- 📊 **Listening statistics** with pie charts using Matplotlib
- 📁 **MySQL database** integration for playlist and history tracking
- ⚙️ **Multithreaded architecture** for smooth real-time performance

---

## ✋ Hand Gesture Mapping

| Gesture      | Action           |
|--------------|------------------|
| ✊ Fist (0 fingers)  | Toggle Play/Pause |
| ☝️ One Finger        | Previous Track    |
| ✌️ Two Fingers       | Next Track        |

> Includes a cooldown mechanism to avoid repeated triggers from a single gesture.

---

## 🧩 Module-wise Description

### 1. Gesture Recognition Module
- **Tech Used**: OpenCV + MediaPipe
- **Purpose**: Detects hand gestures from webcam input
- **Highlights**:
  - Real-time gesture recognition
  - Cooldown handling for stable input processing

### 2. Music Control Module
- **Tech Used**: `pygame.mixer`
- **Purpose**: Plays, pauses, and skips audio tracks
- **Integration**: Works with both gesture recognition and GUI controls

### 3. Database Management Module
- **Tech Used**: MySQL
- **Purpose**: Stores song metadata and play history
- **Highlights**:
  - Logs each song with a timestamp
  - Enables personalized user experience

### 4. Graphical User Interface (GUI) Module
- **Tech Used**: Tkinter
- **Purpose**: Provides manual music controls and playback info
- **UI Components**:
  - Song display area
  - Play/Pause, Next, Previous buttons
  - Status bar with song count

### 5. Multithreading Module
- **Tech Used**: Python `threading`
- **Purpose**: Runs gesture recognition and GUI in parallel threads
- **Benefit**: Ensures smooth, non-blocking user interaction

### 6. Visualization Module
- **Tech Used**: Matplotlib
- **Purpose**: Displays listening analytics (play count)
- **Output**: Interactive pie chart of song plays

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- MySQL Server
- Webcam
- Recommended: Virtual environment

### Install Dependencies

```bash
pip install opencv-python mediapipe pygame matplotlib mysql-connector-python
