package main

import (
	_ "embed"
	"fmt"
	"os"
	"path/filepath"
)

//go:embed ru.qm
var translation []byte

func main() {
	dest, err := findDest()
	if err != nil {
		showAlert("Помилка / Error",
			"Не вдалося знайти Zoom на цьому комп'ютері.\n"+
				"Could not find Zoom on this computer.\n\n"+
				err.Error(),
			true)
		os.Exit(1)
	}

	if err := os.WriteFile(dest, translation, 0644); err != nil {
		showAlert("Помилка / Error",
			"Не вдалося записати файл:\nCould not write file:\n\n"+
				err.Error(),
			true)
		os.Exit(1)
	}

	showAlert("Готово / Done",
		"✓ Переклад встановлено успішно!\n"+
			"✓ Translation installed successfully!\n\n"+
			dest+"\n\n"+
			"Перезапустіть Zoom і оберіть мову:\n"+
			"Restart Zoom and set language:\n"+
			"Settings → General → Language → Русский",
		false)
}

func findDest() (string, error) {
	candidates := []string{
		filepath.Join(os.Getenv("APPDATA"), "Zoom", "bin", "translations", "ru.qm"),
		filepath.Join(os.Getenv("ProgramFiles"), "Zoom", "bin", "translations", "ru.qm"),
	}
	if p := os.Getenv("ProgramFiles(x86)"); p != "" {
		candidates = append(candidates, filepath.Join(p, "Zoom", "bin", "translations", "ru.qm"))
	}
	for _, p := range candidates {
		if _, err := os.Stat(p); err == nil {
			return p, nil
		}
	}
	tried := ""
	for _, p := range candidates {
		tried += "\n  " + p
	}
	return "", fmt.Errorf("searched:%s", tried)
}
