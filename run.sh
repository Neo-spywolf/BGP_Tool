#!/bin/bash

# === Config ===
VENV_DIR="venv"
PYTHON_BIN="$VENV_DIR/bin/python3"
ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
MAIN_FILE="main.py"
BACKUP_FILE="${MAIN_FILE}.bak"

# === Helper: Check if venv is active ===
is_venv_active() {
    # Check if VIRTUAL_ENV env var is set and matches our venv dir
    [[ "$VIRTUAL_ENV" != "" ]] && [[ "$VIRTUAL_ENV" == *"$VENV_DIR"* ]]
}

# === Backup main.py if not backed up ===
backup_main() {
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "📂 Backing up $MAIN_FILE to $BACKUP_FILE"
        cp "$MAIN_FILE" "$BACKUP_FILE"
    else
        echo "⚠️ Backup $BACKUP_FILE already exists"
    fi
}

# === Apply temporary patches ===
patch_main() {
    echo "🛠️ Applying temporary patches to $MAIN_FILE..."

    # Change fetch window to 48 hours ago
    sed -i 's/last_fetch_timestamp = None/last_fetch_timestamp = int(time.time()) - 48 * 3600/' "$MAIN_FILE"

    # Fix deprecated datetime usage
    sed -i 's/datetime\.datetime\.utcfromtimestamp/datetime.datetime.fromtimestamp/g' "$MAIN_FILE"

    # Insert "from datetime import UTC" if missing
    if ! grep -q "from datetime import UTC" "$MAIN_FILE"; then
        sed -i '1i\\nfrom datetime import UTC' "$MAIN_FILE"
    fi
}

# === Restore original main.py ===
restore_main() {
    echo -e "\n♻️ Restoring original $MAIN_FILE..."
    if [ -f "$BACKUP_FILE" ]; then
        mv -f "$BACKUP_FILE" "$MAIN_FILE"
        echo "✅ Restored $MAIN_FILE"
    else
        echo "❌ Backup not found! $MAIN_FILE not restored."
    fi
}

# === Cleanup on exit ===
cleanup() {
    restore_main
    exit
}

# Trap exit signals to restore main.py
trap cleanup INT TERM EXIT

# Activate venv if not already active
if is_venv_active; then
    echo "✅ Virtual environment already active."
else
    if [ -f "$ACTIVATE_SCRIPT" ]; then
        echo "👉 Activating virtual environment..."
        # shellcheck disable=SC1090
        source "$ACTIVATE_SCRIPT"
    else
        echo "❌ Virtual environment activation script not found: $ACTIVATE_SCRIPT"
        echo "Please create a virtual environment first with:"
        echo "  python3 -m venv $VENV_DIR"
        exit 1
    fi
fi

# Backup and patch main.py
backup_main
patch_main

# Run your BGP anomaly detector
echo "🚀 Running BGP Anomaly Detector..."
$PYTHON_BIN "$MAIN_FILE"

# Cleanup and restore on normal exit
cleanup
