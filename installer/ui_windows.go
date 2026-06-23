//go:build windows

package main

import (
	"syscall"
	"unsafe"
)

var (
	user32      = syscall.NewLazyDLL("user32.dll")
	messageBoxW = user32.NewProc("MessageBoxW")
)

func showAlert(title, msg string, isError bool) {
	var flags uintptr = 0x40 // MB_ICONINFORMATION
	if isError {
		flags = 0x10 // MB_ICONERROR
	}
	t, _ := syscall.UTF16PtrFromString(title)
	m, _ := syscall.UTF16PtrFromString(msg)
	messageBoxW.Call(0,
		uintptr(unsafe.Pointer(m)),
		uintptr(unsafe.Pointer(t)),
		flags)
}
