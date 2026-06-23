# Zoom — неофіційний переклад інтерфейсу українською

> [English version below](#zoom--unofficial-ukrainian-ui-translation)

Цей репозиторій містить неофіційний переклад інтерфейсу **Zoom** українською мовою (uk\_UA).

**Актуально для версії:** Zoom 7.1.0 (3715)

---

## Як це працює

Zoom не має вбудованої підтримки украïнської мови у своєму клієнті для Linux, macOS і Windows — тому переклад реалізовано через заміну файлу **russian** перекладу (`ru.qm`) українським текстом. Після встановлення вам потрібно обрати в налаштуваннях Zoom мову **Русский** — саме тоді інтерфейс відображатиметься українською.

**Частина інтерфейсу залишається англійською** — це рядки, що формуються на серверах Zoom і не входять до локального файлу перекладу (наприклад, деякі системні сповіщення, вміст, що генерується AI, та окремі елементи веб-інтерфейсу).

---

## Встановлення

> ⚠️ **Переклад не зберігається після оновлення Zoom.** Після кожного оновлення застосунку файл перекладу перезаписується оригінальним russian перекладом, і його потрібно встановити знову.

### Windows

Завантажте і запустіть **[zoom-ua-installer.exe](zoom-ua-installer.exe)** — він автоматично знайде Zoom і встановить переклад. Після запуску перезапустіть Zoom.

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

1. Перезапустіть Zoom
2. Відкрийте **Налаштування → Загальне → Мова** і оберіть **Русский**
3. Інтерфейс перемкнеться на українську

---

## Після оновлення Zoom

Просто повторіть встановлення для вашої ОС — нічого більше не потрібно.

---

## Авторство та відповідальність

Переклад виконано з використанням **Claude Haiku** як допоміжного інструменту та вичитано мною вручну. Попри це, помилки можливі — я людина. Якщо ви помітили неточність або маєте пропозиції, будь ласка, напишіть: **github@grabovska.com**

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

Download and run **[zoom-ua-installer.exe](zoom-ua-installer.exe)** — it will automatically find Zoom and install the translation. Restart Zoom afterwards.

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

1. Restart Zoom
2. Go to **Settings → General → Language** and select **Русский**
3. The interface will switch to Ukrainian

---

## After a Zoom update

Simply repeat the installation step for your OS — that's all.

---

## Credits and disclaimer

The translation was produced with the assistance of **Claude Haiku** and proofread by me. As I am human, I may have missed something. If you spot an error or have a suggestion, please reach out: **github@grabovska.com**

The original UI strings are the property of Zoom Video Communications, Inc. I make no claim over the original text.

---

## License

Installer and scripts: [MIT](https://opensource.org/licenses/MIT)  
Original Zoom UI strings © Zoom Video Communications, Inc. All rights reserved.
