# Zoom — неофіційний переклад інтерфейсу українською

> [English version below](#zoom--unofficial-ukrainian-ui-translation)

Цей репозиторій містить неофіційний переклад інтерфейсу **Zoom** українською мовою (uk\_UA).

**Актуально для версії:** Zoom 7.1.0 (3715)

---
## Присвята
Переклад виконано для моєї мами, яка не розуміє англійської, а інтерфейсом мовою країни-ворога неприємно користуватись з очевидних причин. 

---

## Як це працює

Zoom не має вбудованої підтримки украïнської мови у своєму клієнті для Linux, macOS і Windows — тому переклад реалізовано через заміну файлу російського перекладу (`ru.qm`) українським текстом. Після встановлення вам потрібно обрати в налаштуваннях Zoom мову **русский** — саме тоді інтерфейс відображатиметься **українською**.

**Частина інтерфейсу залишається англійською або російською** — це рядки, що формуються на серверах Zoom і не входять до локального файлу перекладу (наприклад, деякі системні сповіщення, вміст, що генерується AI, та окремі елементи веб-інтерфейсу).

---

## Встановлення

> ⚠️ **Переклад не зберігається після оновлення Zoom.** Після кожного оновлення застосунку файл перекладу перезаписується оригінальним російським перекладом, і його потрібно встановити знову.

### Windows

Завантажте і запустіть **[zoom-ua-installer.exe](https://github.com/polymatheiia/zoom-ua/raw/main/zoom-ua-installer.exe)** — він автоматично знайде Zoom і встановить переклад. Після запуску перезапустіть Zoom.

Якщо exe не спрацював, можна скористатися PowerShell-скриптом (для досвідчених користувачів):

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

### Linux

**Одна команда через curl:**

```bash
sudo curl -fsSL https://raw.githubusercontent.com/polymatheiia/zoom-ua/main/ru.qm \
    -o /opt/zoom/translations/ru.qm
```

Або клонуйте репозиторій і запустіть скрипт:

```bash
git clone https://github.com/polymatheiia/zoom-ua.git
cd zoom-ua
bash install.sh
```

---

### macOS

**Одна команда через curl:**

```bash
curl -fsSL https://raw.githubusercontent.com/polymatheiia/zoom-ua/main/ru.qm \
    -o "$(find /Applications/zoom.us.app -name ru.qm 2>/dev/null | head -1)"
```

Або клонуйте репозиторій і запустіть скрипт:

```bash
git clone https://github.com/polymatheiia/zoom-ua.git
cd zoom-ua
bash install.sh
```

---

## Після встановлення

Перезапустіть Zoom, потім змініть мову інтерфейсу:

**Windows:**
1. Клацніть правою кнопкою на іконці Zoom у системному треї (правий нижній кут екрана)
2. Наведіть на **Switch Languages**
3. Оберіть **русский** — Zoom перезапуститься українською

**macOS:**
1. Клацніть правою кнопкою (або option+клік) на іконці Zoom у Dock
2. Наведіть на **Switch Languages**
3. Оберіть **русский** — Zoom перезапуститься українською

**Linux:**
1. Клацніть правою кнопкою на іконці Zoom у верхньому правому куті екрана активностей
2. Натисніть **Switch Languages**
3. Оберіть **русский** — Zoom перезапуститься українською

---

## Після оновлення Zoom

Просто повторіть встановлення для вашої ОС — нічого більше не потрібно.

---

## Авторство та відповідальність

Переклад виконано з використанням **Claude Haiku** як допоміжного інструменту та вичитано мною вручну. Попри це, помилки можливі — я всього лиш людина, а тексту там таки багато. Якщо ви помітили неточність або маєте пропозиції, будь ласка, напишіть мені: **github@grabovska.com**

Оригінальні рядки інтерфейсу є власністю Zoom Video Communications, Inc. Я не претендую на жодні права щодо оригінального тексту.

---
---

# Zoom — Unofficial Ukrainian UI Translation

This repository contains an **unofficial Ukrainian (uk\_UA) translation** of the Zoom desktop client interface.

**Tested with:** Zoom 7.1.0 (3715)

---

## How it works

Zoom does not have built-in Ukrainian language support in its desktop client. The translation works by **replacing the russian translation file** (`ru.qm`) with Ukrainian text. After installation, set Zoom's display language to **Русский** — the interface will then appear in Ukrainian.

**Some parts of the interface remain in English** — these are strings generated server-side by Zoom and not included in the local translation file (certain system notifications, AI-generated content, and some web-based UI elements).

---

## Installation

> ⚠️ **The translation does not survive Zoom updates.** Each Zoom upgrade overwrites the translation file with the original russian translation. Reinstall after every update.

### Windows

Download and run **[zoom-ua-installer.exe](https://github.com/polymatheiia/zoom-ua/raw/main/zoom-ua-installer.exe)** — it will automatically find Zoom and install the translation. Restart Zoom afterwards.

If the exe doesn't work, use the PowerShell script (for advanced users):

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

### Linux

**One-liner with curl:**

```bash
sudo curl -fsSL https://raw.githubusercontent.com/polymatheiia/zoom-ua/main/ru.qm \
    -o /opt/zoom/translations/ru.qm
```

Or clone the repo and run the script:

```bash
git clone https://github.com/polymatheiia/zoom-ua.git
cd zoom-ua
bash install.sh
```

---

### macOS

**One-liner with curl:**

```bash
curl -fsSL https://raw.githubusercontent.com/polymatheiia/zoom-ua/main/ru.qm \
    -o "$(find /Applications/zoom.us.app -name ru.qm 2>/dev/null | head -1)"
```

Or clone the repo and run the script:

```bash
git clone https://github.com/polymatheiia/zoom-ua.git
cd zoom-ua
bash install.sh
```

---

## After installation

Restart Zoom, then switch the display language:

**Windows:**
1. Right-click the Zoom icon in the system tray (bottom-right corner)
2. Hover over **Switch Languages**
3. Select **русский** — Zoom will restart in Ukrainian

**macOS:**
1. Right-click (or option-click) the Zoom icon in the Dock
2. Hover over **Switch Languages**
3. Select **русский** — Zoom will restart in Ukrainian

**Linux:**
1. Right-click the Zoom icon in the top-right corner of the Activities screen
2. Click **Switch Languages**
3. Select **русский** — Zoom will restart in Ukrainian

---

## After a Zoom update

Simply repeat the installation step for your OS — that's all.

---

## Credits and disclaimer

The translation was produced with the assistance of **Claude Haiku** and proofread by me. As I am just a mere human, I may have missed something. If you spot an error or have a suggestion, please reach out: **github@grabovska.com**

The original UI strings are the property of Zoom Video Communications, Inc. I make no claim over the original text.

---

## License

Installer and scripts: [MIT](https://opensource.org/licenses/MIT)  
Original Zoom UI strings © Zoom Video Communications, Inc. All rights reserved.
