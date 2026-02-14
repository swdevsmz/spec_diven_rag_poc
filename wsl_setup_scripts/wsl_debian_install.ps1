# 1. Debianのインストール
Write-Host "Debianをインストールしています..." -ForegroundColor Cyan
wsl --install -d Debian

# 2. ディスク容量の自動返却（Sparse VHD）設定を有効化
# これにより、Linux側でファイルを消すとWindows側のディスクサイズも自動で縮小されます
Write-Host "ディスク自動圧縮設定（Sparse VHD）を適用しています..." -ForegroundColor Cyan
wsl --manage Debian --set-sparse true

# 3. 起動して初期設定を促す
Write-Host "完了しました。Debianを起動します。ユーザー名とパスワードを設定してください。" -ForegroundColor Green
wsl -d Debian