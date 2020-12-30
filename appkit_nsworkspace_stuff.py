from AppKit import NSWorkspace

print(NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])