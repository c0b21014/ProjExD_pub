## 第6回
### ゲーム開発演習
#### Pygameでゲーム開発
-  ゲーム概要：
    - ルール
        - ボールが画面の下端まで行くとゲームオーバー
        - 全てのブロックを消すことが出来たらゲームクリア
        - ボールがブロックに当たるとブロックが消える
        - ボールは壁・棒・ブロックに当たった時、跳ね返る
    - game/block.pyを実行すると、900×600のウィンドウに背景・棒・ブロック・ボールが描画され、ブロック崩しゲームで遊ぶことができる。
    - ゲームが始まるとボールは斜め上に打ち上げられ、ブロックや壁に当たると下の方に進むようになる。画面の下端に行かないように棒で弾き返し、ボールをブロックに当て、ブロックを消していく。
-  操作方法：「←」「→」を入力すると棒が左右に動く
-  プログラムの説明
    >迫
    - Bgmクラス : BGM作成のクラス  
    >飯村
    - Screenクラス：ウィンドウ作成のクラス
         - インスタンス変数
             - screen : 画面surface
             - rect : 画面rect
             - bg : 背景画像surface
             - width : 画面の幅
             - height : 画面の高さ
         - インスタンスメソッド
             - draw() : 画面描画のメソッド(blitをしている)
    - Barクラス：棒作成のクラス
         - インスタンス変数
             - surface : 棒surface
             - rect : 棒rect
                 - rect.centerx : 棒の中心座標(x)
                 - rect.centery : 棒の中心座標(y)
         - インスタンスメソッド
             - draw() : 棒描画のメソッド(blitをしている)
    - Blockクラス：ブロック作成のクラス
         - インスタンス変数
             - nx : 横のブロック数
             - ny : 縦のブロック数
             - list : ブロックの有無を0, 1で記録するリスト
             - x : ブロック1個の幅
             - y : ブロック1個の高さ
             - rect_list : 各ブロックのrectを記録するリスト
         - インスタンスメソッド
             - draw() : ブロック描画のメソッド
                 - Block.listをみて値が１の時にblock_surfaceを作成し、色を付け、rectを取得し、rectの位置を定め、Block.rect_listにrectの情報を入れ、blitする
    - Ballクラス：ボール作成のクラス
         - インスタンス変数
             - surface : ボールsurface
             - rect : ボールrect
                 - rect.centerx : ボールの中心座標(x)
                 - rect.centery : ボールの中心座標(y)
             - vx : ボールの速さのx成分
             - vy : ボールの速さのy成分
         - インスタンスメソッド
             - draw() : ボール描画のメソッド
                 - rectの位置をBall.vx , Ball.vy 分だけ動かし、画面端・棒・ブロックの跳ね返りの判定を行い(check_bound()関数・check_ball_bar()関数・collition()関数を用いて判定)、跳ね返りのためにBall.vx , Ball.vyを更新して、blitする
     - check_bound()関数 : ボールと壁の衝突判定の関数
     左右の壁にぶつかった場合返り値は(-1,1)、上下の壁にぶつかった場合は(1,-1)。(-1の時に進行方向が逆転する)
     - check_ball_bar()関数 : ボールと棒の衝突判定の関数
     衝突時返り値(1,-1)でy方向の進行方向のみ逆転する。
     - collition()関数 : ボールとブロックの衝突判定の関数
     ボールとすべてのブロックについて衝突判定を行う。もし衝突しているなら、衝突しているブロックに対応するインデックス番号のBlock.listの値を0にすることで、以降描画されないようにする。また、同じく対応するインデックス番号のBlock.rect_listの値を0にすることで、存在しないブロックに対する衝突判定が起こらないようにする。
         - 判定に.colliderect()を使用しているため、もしrect型の値が残っているとブロックが存在しないのに衝突判定が行われ、何もない空間でボールの跳ね返りが発生してしまう。
     - main()関数 : 
         - Screenクラス、Barクラス、Blockクラス、Ballクラスからインスタンス(screen、bar、block、ball)を作成。while文の中でそれぞれ.draw()メソッドを実行し、pg.display.update()することで画面を更新していく
         - ウィンドウの「✕」ボタンが押された場合にはプログラムを終了
         - ボールが画面下に達したらゲームオーバーの文字を表示
         - ブロックがすべて消えたらゲームクリアの文字を表示
-  改善点：
     - ボールの挙動に変化をつけたい(例えば重力をつけたり、ブロックに当たった時に作用反作用の力が加わったりなど)
     - バグがあるので治したい(ボールを突き刺すように棒を移動すると、ボールが棒の上を転がり、棒の端まで行くと斜め上か斜め下に進み出す)
     - ボールの挙動をプレイヤーが調整できるようになったら、クリア時間を測定したい
     - 簡単にブロック数が変更できるようになっているので、第2ステージなどを作りたい
-  参考サイト：
     - pygame ― Pygameドキュメント 日本語訳 
     http://westplain.sakuraweb.com/translate/pygame/
     - Python3 2次元リストの合計(行・列・全要素)を求める
     https://knuth256.com/2021/05/06/python3-%E3%80%802%E6%AC%A1%E5%85%83%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E5%90%88%E8%A8%88%E8%A1%8C%E3%83%BB%E5%88%97%E3%83%BB%E5%85%A8%E8%A6%81%E7%B4%A0%E3%82%92%E6%B1%82%E3%82%81%E3%82%8B%EF%BC%81/
     - Python, enumerateの使い方: リストの要素とインデックスを取得
     https://note.nkmk.me/python-enumerate-start/