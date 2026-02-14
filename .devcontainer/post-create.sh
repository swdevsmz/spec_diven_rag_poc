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

# GitHub CLI 認証初期化（オプション）
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found, skipping re-auth"
else
    echo "⚠️  GitHub CLI not found in PATH"
fi

# Specify CLI 確認
echo "✅ Environment setup complete!"
if command -v specify &> /dev/null; then
    echo "📋 Spec Kit version:"
    specify --version || true
fi

echo "✨ Ready for Spec-Driven Development!"
