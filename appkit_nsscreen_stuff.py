import AppKit
[print(screen.frame().size.width, screen.frame().size.height)
 for screen in AppKit.NSScreen.screens()]