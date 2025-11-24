# Obelisk AI - Configuration
# Edit these values to customize your installation

# Ollama Configuration
OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "llama3.2:latest"

# Agent Configuration
MAX_ITERATIONS = 20  # Maximum task iterations
ACTION_DELAY = 2  # Seconds between actions
ANALYSIS_TIMEOUT = 30  # Seconds for LLM analysis

# Browser Configuration
BROWSER_HEADLESS = False  # Run browser in background
BROWSER_MAXIMIZE = True  # Maximize browser window
PAGE_LOAD_TIMEOUT = 10  # Seconds to wait for page load

# Screenshot Configuration
SCREENSHOT_DIR = "screenshots"  # Directory for screenshots
SCREENSHOT_FORMAT = "PNG"  # Image format (PNG, JPEG)

# UI Configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750
THEME = "dark"  # dark or light

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "obelisk.log"
