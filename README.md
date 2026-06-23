# Zoom — неофіційний переклад інтерфейсу українською

> [English version below](#zoom--unofficial-ukrainian-ui-translation)

Цей репозиторій містить неофіційний переклад інтерфейсу **Zoom** українською мовою (uk\_UA).

**Актуально для версії:** Zoom 7.1.0 (3715)

---

## Про переклад

Перекладено елементи інтерфейсу клієнтського застосунку Zoom — кнопки, меню, підказки, повідомлення тощо. **Частина інтерфейсу залишається англійською** — це рядки, що формуються на серверах Zoom і не входять до локального файлу перекладу (наприклад, деякі сповіщення, вміст, що генерується AI, та окремі елементи веб-інтерфейсу).

Переклад виконано з використанням **Claude Haiku** як допоміжного інструменту та вичитано мною вручну. Попри це, помилки можливі. Якщо ви помітили неточність або маєте пропозиції — будь ласка, зв'яжіться зі мною: **github@grabovska.com**

Оригінальні рядки інтерфейсу є власністю Zoom Video Communications, Inc. Я не претендую на жодні права щодо оригінального тексту.

---

## Встановлення

> ⚠️ **Переклад не зберігається після оновлення Zoom.** Після кожного оновлення застосунку файл перекладу перезаписується, і його потрібно встановити знову.

### Linux

```bash
sudo cp uk.qm /opt/zoom/translations/uk.qm
```

Або скористайтеся скриптом:

```bash
bash install.sh
```

Перезапустіть Zoom.

---

### macOS

```bash
bash install.sh
```

Скрипт автоматично знайде потрібний файл усередині `/Applications/zoom.us.app` і замінить його. Перезапустіть Zoom.

---

### Windows

Відкрийте PowerShell і виконайте:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

Або замініть файл вручну. Зазвичай він знаходиться за одним із таких шляхів:

```
%APPDATA%\Zoom\bin\translations\uk.qm
C:\Program Files\Zoom\bin\translations\uk.qm
```

Перезапустіть Zoom.

---

## Повторне встановлення після оновлення

Після кожного оновлення Zoom просто повторіть команду встановлення для вашої ОС. Файли перекладу в цьому репозиторії оновлюватимуться при виході нових версій Zoom.

---

---

# Zoom — Unofficial Ukrainian UI Translation

This repository contains an **unofficial Ukrainian (uk\_UA) translation** of the Zoom desktop client interface.

**Tested with:** Zoom 7.1.0 (3715)

---

## About

The translation covers the local client UI — buttons, menus, tooltips, dialog messages, etc. **Some parts of the interface remain in English** because they are rendered server-side by Zoom and are not part of the local translation file (this includes certain notifications, AI-generated content, and some web-based UI elements).

The translation was produced with the assistance of **Claude Haiku** and proofread by me. As I am human, I may have missed something — if you spot an error or have a suggestion, please feel free to reach out: **github@grabovska.com**

The original UI strings are the property of Zoom Video Communications, Inc. I make no claim over the original text.

---

## Installation

> ⚠️ **The translation does not survive Zoom updates.** Each Zoom upgrade overwrites the translation file, so you will need to reinstall it after every update.

### Linux

```bash
sudo cp uk.qm /opt/zoom/translations/uk.qm
```

Or use the included script:

```bash
bash install.sh
```

Restart Zoom.

---

### macOS

```bash
bash install.sh
```

The script will automatically locate `uk.qm` inside `/Applications/zoom.us.app` and replace it. Restart Zoom.

---

### Windows

Open PowerShell and run:

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

Or replace the file manually. It is typically found at one of:

```
%APPDATA%\Zoom\bin\translations\uk.qm
C:\Program Files\Zoom\bin\translations\uk.qm
```

Restart Zoom.

---

## Reinstalling after a Zoom update

After each Zoom update, simply re-run the install command for your OS. Translation files in this repository will be updated as new Zoom versions are released.

---

## License

Installation scripts: [MIT](https://opensource.org/licenses/MIT)

Original Zoom UI strings © Zoom Video Communications, Inc. All rights reserved.
