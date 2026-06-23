//go:build !windows

package main

import "fmt"

func showAlert(title, msg string, isError bool) {
	fmt.Printf("[%s]\n%s\n", title, msg)
}
