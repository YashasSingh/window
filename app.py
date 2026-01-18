import sys
import signal
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtGui import QIcon

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Setup the Window
        self.setWindowTitle("TigerID Browser")
        self.resize(800, 600)
        
        # Hide the window icon
        self.setWindowIcon(QIcon())
        
        # Hide from taskbar
        self.setWindowFlags(Qt.WindowType.Tool)

        # 2. Create the Web View (The "Browser" part)
        self.browser = QWebEngineView()
        
        # Disable favicon loading to hide website icons
        settings = self.browser.page().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadIconsForPage, False)
        
        self.browser.setUrl(QUrl("https://cybersecurity-nasd.vercel.app/"))
        
        # 3. Monitor URL changes and close on target URL
        self.target_url = "https://cybersecurity-nasd.vercel.app/cybersecurity"  # Change this to your target URL
        self.browser.urlChanged.connect(self.check_url)

        # 4. Set the browser as the central widget (removes all margins/bars)
        self.setCentralWidget(self.browser)
    
    def check_url(self, url):
        """Check if the current URL matches the target URL and close if it does"""
        if url.toString() == self.target_url:
            print(f"Target URL reached: {self.target_url}")
            print("Stopping application completely...")
            QApplication.instance().quit()  # Completely exit the application
    
    def closeEvent(self, event):
        """Handle window close - hide window and reopen after 6 minutes"""
        print("Window closed. Will reopen in 6 minutes...")
        self.hide()
        
        # Set timer to reopen window after 6 minutes (360000 milliseconds)
        QTimer.singleShot(360000, self.reopen_window)
        
        # Accept the event but don't actually quit the application
        event.accept()
    
    def reopen_window(self):
        """Reopen the window after the timer expires"""
        print("Reopening window...")
        self.show()

# Run the Application
app = QApplication(sys.argv)

# Allow Ctrl+C to stop the application
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Set up a timer to let Python handle signals
timer = QTimer()
timer.timeout.connect(lambda: None)
timer.start(100)

window = SimpleBrowser()
window.show()
sys.exit(app.exec())