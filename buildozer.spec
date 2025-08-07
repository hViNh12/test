[app]

title = KivyCarScore
package.name = kivycar
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,mp3,xls,xlsx
version = 1.0

requirements = python3,kivy,pandas,gtts,openpyxl

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

# Optional icons
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
