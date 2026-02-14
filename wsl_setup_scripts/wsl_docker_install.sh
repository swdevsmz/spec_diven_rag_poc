# 1. システム更新と必須ツールの導入
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl gnupg sudo

# 2. Docker公式スクリプトでインストール
curl -fsSL https://get.docker.com | sh

# 3. ユーザーをdockerグループに追加
sudo usermod -aG docker $USER

# 4. 【重要】dockerdの起動をパスワードなしで許可する設定を追加
# これにより .bashrc からの自動起動がパスワード入力なしで成功するようになります
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/dockerd" | sudo tee /etc/sudoers.d/docker-vcode

# 5. WSL起動時にDockerを自動で立ち上げる設定 (.bashrc)
# 既存の設定と重複しないようチェックしてから追記します
if ! grep -q "dockerd" ~/.bashrc; then
cat << 'EOF' >> ~/.bashrc

# Docker Daemon Auto-start
if [ -z "$(pgrep dockerd)" ]; then
    sudo dockerd > /dev/null 2>&1 &
    sleep 2
fi
EOF
fi

# 6. wsl.conf の設定
sudo tee /etc/wsl.conf <<EOF
[boot]
systemd=false
[user]
default=$USER
EOF

# 7. 不要なキャッシュを削除してディスクを節約
sudo apt-get autoremove -y && sudo apt-get clean

echo "修正セットアップが完了しました！"
echo "一度 'exit' で抜けて、PowerShellで 'wsl --shutdown' を実行してください。"