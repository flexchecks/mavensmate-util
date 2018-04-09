Get-ChildItem -Include comment_utilities.py,*.sublime-keymap,*.sublime-snippet,*.tmpreferences -Recurse | ForEach-Object { 
    Copy-Item -Force -Recurse -Path $_.FullName -Destination "C:\Google Drives\spelak@flexchecks.com\FlexChecks\Development\Snippets\Sublime"
}