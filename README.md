<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br>
<div align="center">
  <a href="https://github.com/SenaThenu/StudySphere">
    <img src="https://github.com/SenaThenu/StudySphere/blob/main/readme-assets/Logo.png" alt="Logo" height="80">
  </a>

<h3 align="center">🚀 StudySphere 🚀</h3>

  <p align="center">
    ✨ Streamline your study journey with this open-source Notion template, integrating scientifically-backed techniques for maximum effectiveness. ✨
    <br>
    <a href="https://github.com/SenaThenu/StudySphere/issues">Report Bug🐞/Feature🙌</a>
  </p>
</div>

<!-- PROJECT SHIELDS -->
<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg?labelColor=003694&color=ffffff" alt="License">
  <img src="https://img.shields.io/github/contributors/SenaThenu/StudySphere?labelColor=003694&color=ffffff" alt="GitHub contributors" >
  <img src="https://img.shields.io/badge/version-1.0.0-yellow.svg?labelColor=003694&color=ffffff" alt="Version">
  <img src="https://img.shields.io/github/stars/SenaThenu/StudySphere.svg?labelColor=003694&color=ffffff" alt="Stars">
  <img src="https://img.shields.io/github/forks/SenaThenu/StudySphere.svg?labelColor=003694&color=ffffff" alt="Forks">
  <img src="https://img.shields.io/github/issues/SenaThenu/StudySphere.svg?labelColor=003694&color=ffffff" alt="Issues">
</p>


<!-- TABLE OF CONTENTS -->
## Table of Contents 📜
- [Table of Contents 📜](#table-of-contents-)
- [About The Project 📖](#about-the-project-)
  - [Built With 🔧](#built-with-)
- [Getting Started 🚦](#getting-started-)
  - [Prerequisites 📋](#prerequisites-)
  - [Installation 🛠️](#installation-️)
- [Usage 🚀](#usage-)
  - [How the Template Works](#how-the-template-works)
  - [How the Program Works](#how-the-program-works)
- [Roadmap 🗺️](#roadmap-️)
- [Contributing 👋](#contributing-)
- [Current Contributors 🧙‍♂️](#current-contributors-️)
- [Acknowledgments \\w 💖](#acknowledgments-w-)

<!-- ABOUT THE PROJECT -->
## About The Project 📖

[![Product Screenshot][product-screenshot]](https://example.com)

Elevate your study game with this open-source Notion template—it's like having a personal study cheerleader! This template embraces the science-backed power of Active Recall and Spaced Repetition, all while adding a dash of fun with a traffic light system that guides your way. 

The best part? Our trusty `manager.py` script automates the whole process kicking your friction in the butt! It's all about working smart, not hard, in this nonprofit study revolution!

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>


### Built With 🔧

<a href="https://www.python.org/">
  <img src="https://img.shields.io/badge/Python-3570a0?style=for-the-badge&logo=python&logoColor=ffffff" alt="Python">
</a>
<a href="https://www.notion.so/">
  <img src="https://img.shields.io/badge/Notion_API-b8c7d6?style=for-the-badge&logo=notion&logoColor=000" alt="Notion API">
</a>

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>



<!-- GETTING STARTED -->
## Getting Started 🚦
Firstly, you need the StudySphere Notion Template to use the `manager.py` (unless you wanna create one outta scratch :) Download it by following this [link](https://senathenu.notion.site/2428547d9c0f45c48fa0b4018fec3e54?v=92e0d0c8a4c44bd7ba1acd1d67b7b1d0&pvs=4)!

To get started, download the code using any of the methods as shown below. (To get this, click on "Code" on the top-right)

<center>
  <img src="https://github.com/SenaThenu/StudySphere/blob/main/readme-assets/download-the-code.png" alt="Download the Code" height="300">
</center>

### Prerequisites 📋
Most importantly, you need Python installed on your computer! You can install it via [Python Official Website](https://www.python.org/)

Afterwards, to run the trusty  `manager.py` program, you need to install a package we have used to make the CLI colourful. So, open the terminal in the folder where you have the downloaded code. Then run,

`pip install -r requirements.txt`

### Installation 🛠️
Once you have got the code and all the necessary 3rd party libraries, you are pretty much done with installation.

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>



<!-- USAGE EXAMPLES -->
## Usage 🚀

### How the Template Works

Basically, it's a database where you can store your main subjects/topics (or whatever you wanna call them). To keep things simple, we call the stuff inside a database branches!

Every note you store in the database is associated with 3 Repetition Interval Columns (Rep 1, Rep 2, Rep 3) for you to store spaced repetition dates and 3 Repetition Rates columns to rate how confident you felt (green, yellow, red). Based on your ratings, the database calculates your strength for the content in that note. So, all the notes are sorted according to the strength. Then, there is a Revision Rep Column to perform revision on the notes when you have an exam ahead.

### How the Program Works

Instead of letting you to manually set spaced repetition and revision dates (which is dreadful), it automatically sets them with predefined intervals.

*Note: this just what it is capable of currently...*

Yet, as a community, especially during this Hacktoberfest, we can extend it further. We all (including you) power up this! So, why are you waiting? Go ahead... It's okay to make mistakes. We all are learning *forever!*

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>



<!-- ROADMAP -->
## Roadmap 🗺️
I have listed some unaccomplished features you can start working on. Plus, you can even add some. See, it's a non-code contribution to Hacktoberfest!

- [ ] Created a Logo ✨
- [x] Automatic Spaced Repetition Dates Setter ✨
- [x] Automatic Revision Scheduler ✨
  - [ ] Smart Revision Setter - Setting revision for notes whose strength is below a specific limit.
- [x] Flexible Parameters (Modify using settings) ✨
- [ ] Replace the fancy emojis in this readme with [3D animated fancy ones](https://emojipedia.org/microsoft-teams)

See the [open issues](https://github.com/SenaThenu/StudySphere/issues) for a full list of proposed features (and known issues).

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>


<!-- CONTRIBUTING -->
## Contributing 👋

Welcome Code Wizards! 🧙‍♂️✨ Your contributions fuel ⛽ this repo!!!
<br>
*Let's show the power 💪 of Open-Source! Power up the Hacktoberfest!*

<details>
    <summary>Why are open-source developers the sweetest folks in tech? 🍭</summary>
    <p> Because they believe in sharing not only code but also <i>smiles 😄</i> and <i>love ❤️</i> through 0s and 1s!</p>
</details>

<br>

* Ways to Contribute 🫂
  * [Open Issues](https://github.com/SenaThenu/StudySphere/issues)
  * [Update Readme](https://github.com/SenaThenu/StudySphere/blob/main/README.md)
  * [Make the Logo and the Assets Cooler](https://github.com/SenaThenu/StudySphere/tree/main/slides)
  * Introduce an ***awesome feature*** 💫
    1. Fork the Project 🍴
    2. Create your Feature Branch (`git checkout -b my_awesome_feature_branch`)
    3. Commit your Changes (`git commit -m 'Add some awesome features'`)
    4. Upstream this repository (`git remote add origin https://github.com/SenaThenu/StudySphere.git`)
    5. Push to the Main Branch of this repo (`git push origin my_awesome_feature_branch`)
    6. Open a Pull Request 🚀
    
    > If you want help with Git check out this Fireship video: [Git It!](https://www.youtube.com/watch?v=HkdAHXoRtos)

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>

## Current Contributors 🧙‍♂️

😍This wouldn't exist if it weren't for these developers! ***My Gratitude!!!*** ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
> "Even when I lose, I'm winning \
> 'Cause I give you all of me \
> And you give me all of you" \
> *~ All of Me - John Legend*

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments \w 💖

* [Documentation Template](https://github.com/othneildrew/Best-README-Template)
* [G.R.O.W. Revision Method - Cajun Koi Academy](https://www.youtube.com/watch?v=N60JDe3a0IM)

<p align="right"><a href="#readme-top">Jump to Top🔝</a></p>
