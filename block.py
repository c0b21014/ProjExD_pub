import pygame as pg 
import sys

TITLE = "ブロック崩し"
BLOCK_NUM_XY = (5,10)
SCREEN_SIZE = (900,600)
BACKGROUND_IMAGE = 'fig/utyuu.jpg'
BALL_R = 20
BALL_COLOR = (255, 0, 0)
BALL_V0 = (0.0, 1.0)

""" BGM設定のクラス """ #[迫]
class Bgm:
    def __init__(self, fn):     # fn:BGMファイルのパス
        pg.mixer.music.load(fn) # 音楽ファイルの読み込み
        pg.mixer.music.play(1)  # 音楽の再生回数(1回)   


""" ウィンドウ作成のクラス """
class Screen:

    """初期化メソッド"""
    def __init__(self, fn, wh, title):
        # fn：背景画像のパス　wh：画面サイズ(タプル)　title：ウィンドウの名前
        pg.display.set_caption(title)           # ウィンドウの名前を設定
        self.surface = pg.display.set_mode(wh)  # 画面用suface
        self.rect = self.surface.get_rect()     # 画面用rect
        self.bg = pg.image.load(fn)             # 背景用surface
        self.width, self.height = wh            # 画面の横・縦の長さ

    """画面描画のメソッド"""
    def draw(self):
        self.surface.blit(self.bg, self.rect)  # 画面用surfaceに背景用surfaceを貼り付ける


""" 棒作成のクラス """
class Bar():
       #棒の左右移動用辞書[黒杉]
    key_delta = {pg.K_LEFT : [-1, 0],
                 pg.K_RIGHT: [+1, 0],
                }

    """ 初期化メソッド """
    def __init__(self, sc_w, sc_h):
        # screen：Screenクラスのオブジェクト
        self.surface = pg.Surface((200,20))     # 棒のsurfaceを作成
        self.surface.fill((0,0,200))            # 棒の色を指定
        self.rect = self.surface.get_rect()     # 棒のrectを指定
        self.rect.centerx = sc_w //2    # 棒の中心座標(x)を指定
        self.rect.centery = sc_h - 70  # 棒の中心座標(y)を指定

    """ 棒描画のメソッド """
    def draw(self, screen):
        # screen：Screenクラスのオブジェクト
        key_states = pg.key.get_pressed()             # keyの情報の辞書を作成(keyが押されているとき値がTrue)
        #辞書を利用した棒移動[黒杉]
        for key, delta in Bar.key_delta.items():
            if key_states[key] == True:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]
        screen.surface.blit(self.surface, self.rect)  # 画面用surfaceに棒のsurfaceを貼り付ける


"""" ブロック作成のクラス """
class Block:

    """初期化メソッド"""
    def __init__(self, xy, sc_w, sc_h):
        # xy：ブロックの数のタプル(横,縦)　sc_w：画面の横の長さ　sc_h：画面の縦の長さ
        self.nx, self.ny = xy                                   # 横、縦のブロック数
        self.list = [[1]*self.nx for _ in range(self.ny)]       # [[横1],[横2]...]の二次元リスト(1の時にブロックが存在)
        self.y = (sc_h/2 - 5*(self.ny+1)) // (self.ny+1)        # ブロック1個の縦の長さ(ブロック間の隙間5)
        self.x = (sc_w   - 5*(self.nx+1)) //  self.nx           # ブロック1個の横の長さ(ブロック間の隙間5)
        self.rect_list = [[0]*self.nx for _ in range(self.ny)]  # 各ブロックのrectの情報を保管するためのリスト

    """ ブロック描画のメソッド """
    def draw(self, screen):  
        # sc_surface:描画先のsurface 
        for ny in range(self.ny):           # 縦(0列目、1列目...)
            for nx in range(self.nx):       # 横(0行目、1行目...)
                if self.list[ny][nx] == 1:  # block.listをみて値が1だったら
                    block_surface = pg.Surface((self.x, self.y))       # ブロックのsurfaceを作成
                    block_surface.fill((100,100,100))                  # ブロックの色を指定
                    block_rect = block_surface.get_rect()              # ブロックのrectを作成
                    block_rect.left = nx * self.x + 5*(nx+1)           # rectの左の位置を指定
                    block_rect.top = (ny + 1) * self.y +5*(ny+1)       # rectの上の位置を指定
                    self.rect_list[ny][nx] = block_rect                # block.rect_listに作ったrectの位置情報を入れる
                    screen.surface.blit(block_surface, block_rect)     # 画面用surfaceにブロックsurfaceを貼り付ける


"""ボール作成のクラス"""
class Ball():

    """初期化メソッド"""
    def __init__(self, r, col, vxy, sc_w, sc_h):
        # r：ボールの半径　col：ボールの色　vxy：ボールの速さ(tupleで)　screen：Screenクラスのオブジェクト
        self.surface = pg.Surface((r*2,r*2))        # ボールのsurfaceの作成
        self.surface.set_colorkey((0,0,0))          # 黒色を透過する
        pg.draw.circle(self.surface, col, (r,r),r)  # ボールsurfaceに色col ,中心座標(r,r),半径rの円を描く
        self.rect = self.surface.get_rect()         # ボールのrectを作成
        self.rect.centerx = sc_w //2                # ボールのx方向の中心座標を初期値(画面中央)に設定
        self.rect.centery = sc_h  -100              # ボールのy方向の中心座標を初期値(画面下から100)に設定
        self.vx, self.vy = vxy                      # ボールの速さのx成分、ボールの速さのy成分

    """ボール描画のメソッド"""
    def draw(self, screen, bar, block):
        #screen：Screenクラスのオブジェクト bar：Barクラスのオブジェクト block：Blockクラスのオブジェクト
        self.rect.move_ip(self.vx, self.vy)           # ボールのrectをvx, vyだけ動かす
        x1, y1 = check_ball_screen(self, screen)      # 画面端での跳ね返りの判定
        x2, y2 = check_ball_bar(self, bar)            # 棒での跳ね返りの判定
        x3, y3 = check_ball_block(self, block)        # ブロックとの衝突・跳ね返りの判定
        self.vx *= x1 * x2 * x3                       # x方向の跳ね返り
        self.vy *= y1 * y2 * y3                       # y方向の跳ね返り
        screen.surface.blit(self.surface, self.rect)  # 画面用surfaceにボールsurfaceを貼り付ける


"""ボールと壁の衝突判定関数"""
def check_ball_screen(ball, screen): 
    # screen：Screenクラスのオブジェクト　ball：Ballクラスのオブジェクト
    x, y = (1, 1)                                       # 初期値 運動方向の反転無し
    if ball.rect.left < screen.rect.left or\
         screen.rect.right  < ball.rect.right : x = -1  # ボールが画面の左外 or 右外のとき x方向の反射
    if ball.rect.top  < screen.rect.top or\
         screen.rect.bottom < ball.rect.bottom: y = -1  # ボールが画面の上 or 下のとき y方向の反射
    reflection = (x, y)
    return reflection                                   # 反射の有無を返す


"""ボールと棒の衝突判定関数"""
def check_ball_bar(ball, bar):
    reflection = (1, 1)                              # 初期値 運動方向の反転無し
    if ball.rect.bottom < bar.rect.centery and\
         ball.rect.colliderect(bar.rect) == True:    # ボールがバーより低い and 衝突していたら
        reflection = (1,-1)                          # 運動方向の変更はy方向のみ
        if bar.rect.centerx < ball.rect.centerx < bar.rect.right:
            ball.vx += 1
        if bar.rect.left < ball.rect.centerx < bar.rect.centerx:
            ball.vx -= 1
    return reflection                                # 反射の有無を返す


""" ボールとブロックの当たり判定関数"""
def check_ball_block(ball, block):
    # ball：Ballクラスのオブジェクト　block：Blockクラスのオブジェクト            
    reflection = (1,1) # 初期値 運動方向の反転無し
    for y, x_block_rect_list in enumerate(block.rect_list):
        for x, block_rect in enumerate(x_block_rect_list):
            # ｙ：index番号(1次元)
            # x ：index番号(2次元)
            # block.rect_list 　= [ [rect(01),rect(02),…], [rect(11),rect(12),…], … ]
            # x_block_rect_list =   [rect(y1),rect(y2),…]
            # block_rect      　=    rect(yx)
            try :
                # block_rectが「0」の場合がありrect型ではないため、その時にTypeErrorが発生する
                if ball.rect.colliderect(block_rect) == True :  # ボールとあるブロックが衝突していたら
                    block.list[y][x] = 0                        # そのブロックに対応するblock.listの値を0に変更
                    block.rect_list[y][x] = 0                   # そのブロックのrectの情報をblock.rect_listから消す
                    reflection = (-1,-1)                        # 運動方向を反転させる
                pass
            except TypeError : pass
    return reflection                                           #反射の有無を返す


""" メインプログラム """
def main():
    # BGM設定 [迫]
    bgm = Bgm("music/旧支配者のキャロル_loop.mp3")                              
    #スクリーン・ブロック・棒・ボールを作成
    screen = Screen(BACKGROUND_IMAGE, SCREEN_SIZE, TITLE)
    bar = Bar(screen.width, screen.height)
    block = Block(BLOCK_NUM_XY, screen.width, screen.height)
    ball = Ball(BALL_R, BALL_COLOR, BALL_V0 ,screen.width, screen.height)

    # 繰り返し実行
    while True:
        #スクリーン・ブロック・棒・ボールの更新準備
        screen.draw()
        bar.draw(screen)
        block.draw(screen)
        ball.draw(screen, bar, block)
        pg.display.update() #画面を更新

        # '✕'が押されたらmain()関数から抜けプログラム終了
        for event in pg.event.get():
            if event.type == pg.QUIT : return

        # ゲームオーバー
        if ball.rect.bottom >= screen.rect.bottom:                             #ボールが画面下に到達したら
            font = pg.font.Font(None, 100)                                     # フォントの設定
            text = font.render("GAME OVER", True, (255,255,255))               # 文字のsurfaceの作成(文字列、色指定)
            screen.surface.blit(text, [screen.width//2-200,screen.height//2-30])  # 画面用surfaceに文字のsurfaceを貼り付ける
            pg.display.update()                                                # 画面の更新
            pg.time.wait(1000)                                                 # GAME OVERの表示時間の確保
            return                                                             # main()関数を抜ける

        # ゲームクリア
        if sum(sum(i) for i in block.list) == 0:                               # block.listの要素がすべて0になっていたら
            font = pg.font.Font(None, 100)                                      # フォントの設定
            text = font.render("GAME CLEAR", True, (255,255,255))              # 文字のsurfaceの作成(文字列、色指定)
            screen.draw()                                                      # 最後のsurfaceの更新を反映
            block.draw(screen.surface)
            bar.draw(screen)
            ball.draw(screen, bar, block)
            screen.surface.blit(text, [screen.width//2-230,screen.height//2-30])  # 画面用surfaceに文字のsurfaceを貼り付ける
            pg.display.update()                                                # 画面の更新
            pg.time.wait(1000)                                                 # GAME OVERの表示時間の確保
            return                                                             # main()関数を抜ける
        

if __name__ == "__main__":
    pg.init()   #pygameモジュールを初期化
    main()      #main()関数を実行
    pg.quit()   #pygameモジュールの初期化を解除
    sys.exit()  #プログラムを終了する
