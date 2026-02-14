#!/bin/bash
set -e

echo "🚀 Setting up Spec Kit environment..."

# uv パッケージマネージャーのインストール
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Specify CLI（GitHub Spec Kit）のインストール
echo "🔧 Installing Specify CLI..."
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git || {
    echo "⚠️  Specify CLI installation encountered an issue, but continuing..."
}

# Specify CLI 確認
if command -v specify &> /dev/null; then
    specify --help 2>&1 | head -1 || echo "✅ Specify CLI is installed"
fi

echo "✨ Ready for Spec-Driven Development!"
