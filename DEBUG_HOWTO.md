# Debug Guide for paperless-ngx-postprocessor

This guide explains how to debug the postprocessor, including VS Code debugging setup and all configuration files.

## Table of Contents

1. [Quick Start](#quick-start)
2. [VS Code Configuration Files](#vs-code-configuration-files)
3. [Debugging Methods](#debugging-methods)
4. [AI Model Recommendations](#ai-model-recommendations)
5. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker container running with paperless-ngx
- VS Code with Python extension installed
- `debugpy` installed in the container's virtual environment

### Install debugpy (if not already installed)

```bash
docker exec paperless-ngx-postprocessor-paperless-ngx-1 \
  bash -c "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && pip install debugpy"
```

### Start Debugging

1. Open the project in VS Code
2. Set breakpoints in your code (e.g., `post_consume_script.py` or `paperlessngx_postprocessor/ai.py`)
3. Press `F5` and select **"Debug post_consume_script.py (Docker)"**
4. Enter a document ID when prompted (default: 1)
5. The debugger will attach and breakpoints will be hit

## VS Code Configuration Files

The `.vscode` folder contains all necessary configuration files for debugging. Here's what each file does:

### `.vscode/launch.json`

This file defines the debug configurations available in VS Code.

**Configuration: "Python-Debugger: Aktuelle Datei"**
- Type: `debugpy` (launch)
- Purpose: Debug the currently open Python file locally
- Use case: Quick debugging of individual scripts outside the container

**Configuration: "Debug post_consume_script.py (Docker)"**
- Type: `debugpy` (attach)
- Host: `localhost`
- Port: `5678`
- Path mappings: Maps local workspace to `/usr/src/paperless-ngx-postprocessor` in the container
- Pre-launch task: Automatically starts the script in the container with debugpy
- Post-debug task: Stops the script after debugging
- `justMyCode: false`: Allows debugging into library code

**How it works:**
1. The pre-launch task (`Start Debug Container Script`) starts the script in the container with `PNGX_POSTPROCESSOR_DEBUG=true`
2. The script waits for the debugger to attach on port 5678
3. VS Code connects to the debugger
4. Breakpoints become active
5. After debugging, the post-debug task stops the script

### `.vscode/tasks.json`

This file defines VS Code tasks that can be run before/after debugging or manually.

**Task: "Start Debug Container Script"**
- Type: Shell command
- Purpose: Starts `post_consume_script.py` in the Docker container with debugpy enabled
- Environment variables:
  - `PNGX_POSTPROCESSOR_DEBUG=true`: Enables debugpy in the script
  - `DOCUMENT_ID=${input:documentId}`: Prompts for document ID (default: 1)
- Background task: Runs in the background so VS Code can attach the debugger
- Auto-detects container name by searching for containers matching `paperless.*paperless-ngx`

**Task: "Stop Container Script"**
- Type: Shell command
- Purpose: Stops the running script in the container after debugging
- Uses `pkill` to terminate the Python process gracefully

**Task: "Get Container Name"**
- Type: Shell command
- Purpose: Utility task to find the correct container name
- Returns the first container matching the pattern

**Input: "documentId"**
- Type: Prompt string
- Description: Document ID to process
- Default: "1"

### `.vscode/run_in_container.py`

Helper script that runs `post_consume_script.py` in the Docker container. This script is used by VS Code tasks and can also be run manually.

**Features:**
- Auto-detects the container name by searching for containers matching `paperless.*paperless-ngx`
- Falls back to default name if auto-detection fails
- Uses `DOCUMENT_ID` environment variable (defaults to "1")
- Activates the virtual environment before running the script
- Prints the command being executed for transparency

**Usage:**
```bash
export DOCUMENT_ID=123
python3 .vscode/run_in_container.py
```

### `.vscode/settings.json`

VS Code workspace settings for Python development.

**Settings:**
- `python.defaultInterpreterPath`: Points to the local virtual environment
- `python.terminal.activateEnvironment`: Automatically activates the virtual environment in VS Code terminals

**Note:** These settings are for local development. The actual execution happens in the Docker container's virtual environment.

## Debugging Methods

### Method 1: VS Code Debugging (Recommended)

This is the easiest and most feature-rich debugging method.

**Steps:**
1. Set breakpoints in your code by clicking in the gutter next to line numbers
2. Press `F5` or go to Run → Start Debugging
3. Select **"Debug post_consume_script.py (Docker)"**
4. Enter a document ID when prompted
5. The script starts in the container and waits for the debugger
6. VS Code automatically connects
7. Use the debug toolbar to:
   - Continue (F5)
   - Step Over (F10)
   - Step Into (F11)
   - Step Out (Shift+F11)
   - Restart (Ctrl+Shift+F5)
   - Stop (Shift+F5)

**Advantages:**
- Visual breakpoints
- Variable inspection
- Call stack navigation
- Watch expressions
- Debug console for interactive evaluation

### Method 2: Manual Container Execution

Run the script manually in the container for quick testing.

```bash
# Get container name
CONTAINER=$(docker ps --format '{{.Names}}' | grep paperless-ngx | head -1)

# Run with document ID
docker exec -e DOCUMENT_ID=123 $CONTAINER \
  bash -c "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && python3 post_consume_script.py"
```

### Method 3: Manual Debugpy Attach

Start the script manually and attach VS Code debugger.

**Step 1: Start script in container**
```bash
CONTAINER=$(docker ps --format '{{.Names}}' | grep paperless-ngx | head -1)
docker exec -e PNGX_POSTPROCESSOR_DEBUG=true -e DOCUMENT_ID=123 $CONTAINER \
  bash -c "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && python3 post_consume_script.py"
```

**Step 2: Attach debugger**
- The script will print: `⏳ Waiting for debugger to attach...`
- In VS Code, select **"Debug post_consume_script.py (Docker)"** and press F5
- The debugger will connect automatically

### Method 4: Python Debugger (pdb)

Add breakpoints directly in code for simple debugging.

**Add to your code:**
```python
import pdb; pdb.set_trace()
```

**Run:**
```bash
docker exec -e DOCUMENT_ID=123 $CONTAINER \
  bash -c "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && python3 post_consume_script.py"
```

**pdb commands:**
- `n` (next line)
- `s` (step into)
- `c` (continue)
- `l` (list code)
- `p variable` (print variable)
- `q` (quit)

## AI Model Recommendations

### Recommended Model: ministral-3

The **ministral-3** model is highly recommended for this project because it excels at both:

1. **Vision tasks**: Can analyze document images and extract information from visual content
2. **Suggestions**: Provides high-quality suggestions for document metadata, titles, and other fields

**Why ministral-3:**
- Excellent performance on document analysis tasks
- Good balance between speed and accuracy
- Supports multimodal input (text + images)
- Reliable output formatting
- Well-suited for structured data extraction

**Configuration:**
Set the model in your ruleset YAML files:
```yaml
ai_usage: OLLAMA
ollama_model: ministral-3
```

**Environment Variable:**
Ensure `OLLAMA_HOST` is set in your environment:
```bash
export OLLAMA_HOST=http://your-ollama-server:11434
```

## Troubleshooting

### Port 5678 Already in Use

**Error:** `RuntimeError: Can't listen for client connections: [Errno 98] Address already in use`

**Solution:**
- Stop any running debug sessions
- Kill any lingering Python processes in the container:
  ```bash
  docker exec $CONTAINER pkill -f 'post_consume_script.py'
  ```
- Restart the debug session

### Container Not Found

**Error:** Container name doesn't match

**Solution:**
1. Find the correct container name:
   ```bash
   docker ps --format '{{.Names}}' | grep paperless
   ```
2. Update `.vscode/tasks.json` with the correct container name, or
3. The auto-detection in `run_in_container.py` should handle most cases

### Debugger Doesn't Attach

**Symptoms:** Script runs but breakpoints don't hit

**Solutions:**
1. Verify `PNGX_POSTPROCESSOR_DEBUG=true` is set
2. Check that port 5678 is exposed in `docker-compose.yaml`:
   ```yaml
   ports:
     - "5678:5678"
   ```
3. Ensure debugpy is installed:
   ```bash
   docker exec $CONTAINER bash -c "cd /usr/src/paperless-ngx-postprocessor && source venv/bin/activate && pip list | grep debugpy"
   ```
4. Check the path mappings in `launch.json` match your setup

### Logs Not Appearing in Terminal

**Symptoms:** `self._logger.info()` calls don't show output

**Solutions:**
1. Check the logger level in your configuration
2. Ensure logging is configured:
   ```python
   logging.basicConfig(format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s")
   logger.setLevel(logging.INFO)  # or logging.DEBUG
   ```
3. Logs may be going to a file instead of stdout - check container logs:
   ```bash
   docker logs $CONTAINER
   ```

### AI Response Parsing Issues

**Note:** The current implementation returns the raw AI response directly without JSON parsing. The system prompt instructs the model to return plain text without formatting.

If you need JSON parsing, you can modify `paperlessngx_postprocessor/ai.py`:
```python
response = chat(self._model, messages=messages)
raw_content = response['message']['content']
# Add JSON parsing if needed
jsonvalue = json.loads(raw_content)
return jsonvalue.get('info', raw_content)
```

## Additional Resources

### Viewing Logs

```bash
# Container logs
docker logs -f $CONTAINER

# Paperless logs (if mounted)
docker exec $CONTAINER tail -f /usr/src/paperless/log/paperless.log
```

### Testing AI Configuration

The `selfCheck()` method in the `AI` class tests the Ollama connection:
```python
ai = AI("ministral-3", logger)
if ai.selfCheck():
    print("AI configured correctly")
else:
    print("AI configuration error")
```

### Environment Variables

Key environment variables:
- `DOCUMENT_ID`: Document to process (default: 1)
- `PNGX_POSTPROCESSOR_DEBUG`: Enable debugpy (set to "true")
- `OLLAMA_HOST`: Ollama server URL
- `PNGX_POSTPROCESSOR_POST_CONSUME_SCRIPT`: Optional post-processing script

## Summary

The debugging setup uses:
- **VS Code** for the debugging interface
- **debugpy** for remote debugging
- **Docker** for containerized execution
- **Tasks** for automation
- **Path mappings** for seamless local/remote code synchronization

The recommended AI model **ministral-3** provides excellent results for both vision tasks and metadata suggestions, making it ideal for document processing workflows.
