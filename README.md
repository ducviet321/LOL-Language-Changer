# LOL Language Changer

![Screenshot](/resources/gui.PNG)

The language can be changed now from LeagueClient but the in game champion voice are still all in english, unless use this tool.

So, enjoy changing to any of these languages:

```text
en_US: English (alternatives en_GB, en_AU)
vi_VN: Vietnamese
ja_JP: Japanese
ko_KR: Korean
zh_CN: Chinese
zh_TW: Taiwanese
es_ES: Spanish (Spain)
es_MX: Spanish (Latin America)
fr_FR: French
de_DE: German
it_IT: Italian
pl_PL: Polish
ro_RO: Romanian
el_GR: Greek
pt_BR: Portuguese
hu_HU: Hungarian
ru_RU: Russian
tr_TR: Turkish
```

# Download

[Click here to download the latest version](https://github.com/LowEQ/LOL-Language-Changer/releases/download/Beta/lol_language_changer.exe)

# Usage

## Windows

1. Make sure to open League Client first.
2. Open this program(with admin right), select language and click "Change"!

*Note* First time selecting a new language would take ~5 minutes to download it, because added logging to `.log` file to store application logs we need admin right for write and create the log file.

![Downloading German Language Pack](resources/german.png)

## Linux and macOS (Obsolete)

```bash
# Linux
./lol_language_changer.py --wineprefix /path/to/install

# macOS native install
./lol_language_changer.py

# macOS WINE install
./lol_language_changer.py --mac-wine --wineprefix /path/to/install
```

# Caveats (Obsolete)

- The Linux client may get a bit glitchy. If the Riot Games Client launches,it should be in the selected language.
If it does not let you launch the game due to a greyed out button, simply close the Riot Client and launch League of Legends.exe normally.
The game should then load and start downloading the new language.

- The Linux client may also take a few minutes to run after the Language Changer window has closed, but the language change will still apply.

# Build

`pyinstaller --noconfirm --onefile --windowed --icon "D:/Projects/LOL-Language-Changer/icon.ico" --workpath "D:/Projects/LOL-Language-Changer/build" --distpath "D:/Projects/LOL-Language-Changer/dist" --add-data "C:/Python/tcl/tcl8.6;./tcl" --add-data "C:/Python/tcl/tk8.6;./tk" "D:/Projects/LOL-Language-Changer/lol_language_changer.py"`

# License

This project is forked orginally from [Here](https://github.com/ducviet321/LOL-Language-Changer), made it working with windows only other os are not supported. feel free do changes

@TheDuckNiceRight
