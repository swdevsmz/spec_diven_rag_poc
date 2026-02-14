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

# GitHub CLI 認証初期化（オプション）および gh-copilot インストール
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found"

    # gh-copilot (official gh extension) をインストール（未インストール時のみ）
    if gh extension list | grep -q 'github/gh-copilot'; then
        echo "✅ gh-copilot extension already installed"
    else
        echo "🔧 Installing gh-copilot extension..."
        gh extension install github/gh-copilot || echo "⚠️ gh-copilot install failed (run 'gh auth login' inside the container if required)"
    fi
else
    echo "⚠️  GitHub CLI not found in PATH"
fi

# Specify CLI 確認
# Node / npm 確認
if command -v node &> /dev/null; then
  echo "✅ node $(node -v) / npm $(npm -v)"
else
  echo "⚠️ node / npm not found (DevContainer の再ビルドが必要です)"
fi

echo "✅ Environment setup complete!"
if command -v specify &> /dev/null; then
    echo "📋 Spec Kit version:"
    specify --help 2>&1 | head -1 || echo "✅ Specify CLI is installed"
fi

echo "✨ Ready for Spec-Driven Development!"
