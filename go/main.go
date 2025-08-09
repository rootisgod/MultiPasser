package main

import (
	"github.com/rivo/tview"
)

func main() {
	app := tview.NewApplication()
	textView := tview.NewTextView().
		SetText("Welcome to tview!\nPress Ctrl+C to exit").
		SetTextAlign(tview.AlignCenter)

	if err := app.SetRoot(textView, true).Run(); err != nil {
		panic(err)
	}
}
