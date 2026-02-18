#!/bin/bash
set -e

echo "🚀 Setting up Spec Kit environment..."

# uv パッケージマネージャーのインストール
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# シェル起動時にも uv/uvx を見つけられるよう PATH を恒久化
if ! grep -q "\.local/bin" "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"' >> "$HOME/.bashrc"
fi
if ! grep -q "\.local/bin" "$HOME/.profile"; then
    echo 'export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"' >> "$HOME/.profile"
fi

# Specify CLI（GitHub Spec Kit）のインストール
echo "🔧 Installing Specify CLI..."
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git || {
    echo "⚠️  Specify CLI installation encountered an issue, but continuing..."
}

# Specify CLI 確認
if command -v specify &> /dev/null; then
    specify --help 2>&1 | head -1 || echo "✅ Specify CLI is installed"
fi

# uvx 確認（Serena MCP の起動に必要）
if command -v uvx &> /dev/null; then
    uvx --version || true
else
    echo "⚠️  uvx が見つかりません。再起動後に PATH を確認してください。"
fi

echo "✨ Ready for Spec-Driven Development!"
