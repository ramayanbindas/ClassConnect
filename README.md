# ClassConnect
ClassConnect is revolutionizing education with interactive online learning. By helping in scheduling classes, collaborate with institution, teacher and student.

```markdown
# ClassConnect - Your Virtual Classroom Solution

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

ClassConnect is a versatile virtual classroom application designed to facilitate remote learning and collaboration.
It provides a seamless platform for educators and students to connect, share resources, and engage in interactive
lessons from anywhere in the world.

### Key Highlights

- Live video conferencing for interactive classes.
- Secure user authentication and role-based access.
- File sharing, assignment submission, and grading.
- Chat rooms and discussion boards for communication.
- Responsive design for various devices and screen sizes.

## Features

- **Video Conferencing:** Conduct live video classes with multiple participants, screen sharing, and real-time interaction.

- **Authentication:** User-friendly login and registration with role-based access (teacher/student).

- **File Sharing:** Upload and share course materials, assignments, and resources.

- **Assignment Submission:** Students can submit assignments digitally, and teachers can grade them within the platform.

- **Communication:** Chat rooms, discussion boards, and private messaging for effective communication.

- **Responsive Design:** Optimized for desktop, tablet, and mobile devices.
- **Scheduling Classe:** Directly by the teacher of the institution.
- **Notice:** Upadated Notice are access directly from the institution.
- **Reminder:** Real-time update app feature allow the student to keep-up-to date along the institution.

## Getting Started

### Prerequisites

- Python 3.10.0
- Kivy Framework 2.2.1
- KivyMD (Kivy Material Design)  1.1.1
- Other project-specific dependencies (check requirements.txt)
```

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/ramayanbindas/ClassConnect.git
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Start the application:
4. Note: Before running this script make sure to uncomment out self.load_kv() code with in the file component/auth_screen.py
```code
class CreateAuth(Base):
      def __init__(self, screen_name, screenmanager, *args, **kw):
          super().__init__(screen_name, screenmanager, *args, **kw):

          self.load_kv_files("mobile_view", "tablet_view", "desktop_view")
```

   ```shell
   python ClassConnect.py
   ```
1. To run this application in hot reload mode:
2. Note: Make sure to comment out self.load_kv() code with in the file component/auth_screen.py
```code
class CreateAuth(Base):
      def __init__(self, screen_name, screenmanager, *args, **kw):
          super().__init__(screen_name, screenmanager, *args, **kw):

          # self.load_kv_files("mobile_view", "tablet_view", "desktop_view")
```
```shell
python ClassConncetHotreloader.py
```

## Usage

1. Launch the application.

2. Sign in as a teacher or student.

3. Explore the various features, including video conferencing, file sharing, and messaging.

4. Create or join virtual classrooms and enjoy a seamless learning experience.

## Contributing

We welcome contributions from the community. If you'd like to contribute to ClassConnect, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

   ```shell
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:

   ```shell
   git commit -m "Add your message here"
   ```

4. Push your changes to your fork:

   ```shell
   git push origin feature/your-feature-name
   ```

5. Create a pull request from your fork to the main repository.

6. Wait for feedback and, once approved, your changes will be merged.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```
