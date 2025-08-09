Install Go


```bash
brew install go
go mod init githib.com/rootisgod/multipasser
go get github.com/rivo/tview
go run .
```

# Build a Binary

```bash
go build -o multipasser
```

## Multi Platform

```bash
GOOS=darwin GOARCH=arm64 go build -o multipasser-macos-arm64
GOOS=darwin GOARCH=amd64 go build -o multipasser-macos-amd64
GOOS=linux GOARCH=arm64 go build -o multipasser-linux-arm64
GOOS=linux GOARCH=amd64 go build -o multipasser-linux-amd64
GOOS=windows GOARCH=arm64 go build -o multipasser-windows-arm64.exe
GOOS=windows GOARCH=amd64 go build -o multipasser-windows-amd64.exe
```

# Update

To get new tview version

```bash
go get -u github.com/rivo/tview
```