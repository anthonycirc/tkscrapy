# Tkscrapy
Tkscrapy is a small scraper in Python based on the Scrapy library as well as Tkinter for the graphical user interface (GUI)
You can use the Python version directly or the executable (linux, windows and macOs) create with cx_freeze

![Capture.png](https://cajoline.github.io/tkscrapy/capture.png)


## Installing the python version
Download the project and go to /tkscrapy and do:
```Bash
cd /tkscrapy/tkscrapy
pip freeze> requirements.txt #(to install all dependencies)
python gui.py #(to execute the script)
```

## Linux executable installation
Download the linux version in / app_desktop_exec / linux / executable
```bash
mv linux /opt/Tkscrapy
touch ~/.local/share/aplications/Tkscrapy.desktop # create a shortcut .desktop
```
Here is an example of .desktop file:
```Bash
[Desktop Entry]
Type = Application
Encoding = UTF-8
Name = Tkscrapy
How = Scraper with Tkinter GUI
Exec = /opt/Tkscrapy/launcher.sh
Icon = /opt/Tkscrapy/logo.png
Terminal = false
StartupNotify = true
```
OR
Download the .deb package for Ubuntu/Debian in / app_desktop_exec / linux / deb / tkscrapy.deb

## Windows executable installation (coming soon)

## Mac executable installation (coming soon)

# Documentation
an example of use to scrap a page
- Enter the type of output (JSON, CSV, XML)
- Reseign a valid url with the protocol (http: //)
- Add in * Parent selector * the CSS selector you want to search for example if I want to retrieve all links from the site I would do like this: ** a **
- Then in the text field I add the column accompanied by the desired value for example: ** link | a ** or ** link | a :: text ** (to have the textual content)

For more information, see the scrapy documentation for selectors [Scrapy documentation] (https://docs.scrapy.org/en/latest/)

You can follow the navigation if you want to visit several pages by checking the box * "pagination selector" *:
- ex: ** li.next to :: attr ("href") **, you just have to add the navigation link selector

see [Scrapy documentation] (https://docs.scrapy.org/en/latest/) for more information
