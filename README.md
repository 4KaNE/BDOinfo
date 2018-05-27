# BDOinfo
黒い砂漠のボスpopを通知するBot  
ボス湧き時間固定後用
### 使用方法  
* [Discord.py](https://github.com/Rapptz/discord.py)をインストール  
`pip install discord`  

* Botの作成  
https://discordapp.com/developers/applications/me  
1 新しいアプリを選択  
2 アプリケーション名を入力してアプリを作成  
3 Botユーザーを作成  
4 Bot欄のトークンをメモして変更を保存  
5 Generate OAuth2 URLをクリック  
6 botにチェックが入っているのを確認してURLをCOPYして開く  
7 Botを自分のサーバーに招待

* 設定の書き換え  
1 メモしておいたBotのトークンをconfig.iniのBOT_TOKENに上書き  
2 Discordの設定→テーマ→開発者モードにチェックを入れる  
3 通知を送るテキストチャンネルを右クリック→IDをコピー  
4 3でコピーしたチャンネルIDをconfig.iniのCHANNELに上書き  
5 COMAND_PREFIXとDEL_TIMEの変更はお好みで

* 権限の設定  
Discordのサーバー設定→役職→Botが属する役職に以下の権限を付与    
・テキストチャンネルの閲覧・ボイスチャンネルの一覧表示  
・メッセージを送信  
・メッセージの管理  
・埋め込みリンク  
・リアクションの追加

* 起動  
bot.pyをダブルクリックで起動、ウインドウを閉じると終了  
!helpでhelpの表示、!infoでボス時間の表示  
起動中はBotステータスに次のボスの名前と湧き時間を表示

### 動作環境
Python 3.5  
Discord.py 0.6.12
