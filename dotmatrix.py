from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle,Line
#--------------------------------------------------------------------------------------
# ドットマトリックス描画用ウィジット
#--------------------------------------------------------------------------------------
class DotMatrix(Widget):
    # 変数の初期化
    dot_d = 0                       # ドットマスの大きさ
    dot_w = 0                       # ドットの幅
    dot_h = 0                       # ドットの高さ
    line_color = Color(.3,.3,.3)    # マスの色
    dote= [[0 *32 ] for _ in range(32)]      # ドットデータ配列（キャンバスの座標に併せて左下が開始位置）
    # 初期処理
    def __init__(self, **kwargs):
        super(DotMatrix, self).__init__(**kwargs)
    # マトリックスのサイズをセット
    def set_size(self,w,h):
        self.dot_w = w
        self.dot_h = h
        self.dot_d=min([int(self.width/self.dot_w),int(self.height/self.dot_h)]) # キャンバスのサイズからマス1個の大きさを求める
        self.display()      # 画面更新
    # ドットデータの初期化 
    def clear(self):
        self.dote= [[0]* 32 for _ in range(32)]     # ドットデータ格納用
        self.display()      # 画面更新
    # ドットデータを表示
    def display(self):
        self.canvas.clear()                         # キャンバスを初期化
        # ドットデータ配列のデータを表示
        # キャンバスの座標は、左下が起点となります。
        for i in range(self.dot_w):
            for j in range(self.dot_h):
                if(self.dote[j][i] == 0):
                    self.canvas.add(Color(0,0,0))   #黒
                else:
                    self.canvas.add(Color(1,1,1))   #白
                self.canvas.add(Rectangle(pos=(self.x+i*self.dot_d,self.y+j*self.dot_d),size=(self.dot_d,self.dot_d)))
        # マスの線を描画
        self.canvas.add(self.line_color)            #グレー  
        self.canvas.add(Line(rectangle=(self.x,self.y,self.dot_d*self.dot_w,self.dot_d*self.dot_h)))
        for i in range(self.dot_w):
            self.canvas.add(Line(points=[self.x+i*self.dot_d,self.y,self.x+i*self.dot_d,self.y+self.dot_h*self.dot_d],width=1))
        for i in range(self.dot_h):
            self.canvas.add(Line(points=[self.x,self.y+i*self.dot_d,self.x+self.dot_w*self.dot_d,self.y+i*self.dot_d],width=1))
    # 線を描く（始点と終点で線を描く）
    def draw(self,pos_s,color):
        # キャンバス内であれば、描く
        if((pos_s[1] > self.y)*(pos_s[1] < self.y + self.dot_d*self.dot_h)*(pos_s[0] > self.x)*(pos_s[0] < self.x + self.dot_d*self.dot_w)):
            x=int((pos_s[0]-self.x)/self.dot_d)
            y=int((pos_s[1]-self.y)/self.dot_d)
            if(color == 0):
                self.canvas.add(Color(0,0,0)) #黒
                self.dote[y][x]=0
            else:
                self.canvas.add(Color(1,1,1)) #白
                self.dote[y][x]=1
            self.canvas.add(Rectangle(pos=(x*self.dot_d+self.x,y*self.dot_d+self.y),size=(self.dot_d,self.dot_d)))
            self.canvas.add(self.line_color) #グレー       
            self.canvas.add(Line(rectangle=(x*self.dot_d+self.x,y*self.dot_d+self.y,self.dot_d,self.dot_d)))
    # ドットデータ配列を取得(32x32 bit)
    def get_dotedata(self):
        return self.dote
    # ドットデータ配列を設定(32x32 bit)
    def set_dotedata(self,buf):
        self.dote = buf
    # ドットデータを取得（16進数)
    def get_dotedata_hex(self):
        buf=""
        # ビットデータから16進数データへ
        # ドットデータの開始位置を左上に変換して作成
        for i in range(self.dot_h):
            sline=0
            # 8x16サイズの場合
            if (self.dot_w == 8):
                for j in range(self.dot_w):
                    sline = sline << 1
                    sline += self.dote[self.dot_h-i-1][j]                
                buf += "0x" + format(sline,'02X') 
            # 16x16サイズの場合
            if (self.dot_w == 16):
                for j in range(self.dot_w):
                    sline = sline << 1
                    sline += self.dote[self.dot_h-i-1][j]                
                buf += "0x" + format(sline,'04X')
            # 32x32サイズの場合
            if (self.dot_w == 32):
                for j in range(16):
                    sline = sline << 1
                    sline += self.dote[self.dot_h-i-1][j]                
                buf += "0x" + format(sline,'04X') + "," 
                sline=0
                for j in range(16,32):
                    sline = sline << 1
                    sline += self.dote[self.dot_h-i-1][j]                
                buf += "0x" + format(sline,'04X') 
            if(i != self.dot_h-1):
                buf += ","
        return buf
    # ドットデータを設定（16進数)
    def set_dotedata_hex(self,buf):
        byte_num=0
        sline=0
        buf_array=buf.replace('\n','').split(',')
        buf_cnt=len(buf_array)  # 個数を取得
        self.clear()
        # 16進数データから、ビットデータへ
        # 8x16,16x16サイズの場合
        if(buf_cnt == 16):
            byte_num=(len(buf_array[0])==4)*8+(len(buf_array[0])==6)*16
            for i in range(buf_cnt):
                for j in range(byte_num):
                    sline = int(buf_array[i],16) >> j & 0x1
                    self.dote[buf_cnt-i-1][byte_num-j-1]=sline
            return True
        # 32x32サイズの場合
        elif(buf_cnt == 64):
            for i in range(64):
                for j in range(16):
                    sline = int(buf_array[i],16) >> j & 0x1
                    self.dote[31-int(i/2)][15+16*(i%2==1)-j]=sline
            return True
        else:
            # データの個数が16or64出ない場合、取り込まない
            return False
    # ドットデータを反転する
    def invert_colors(self):
        for i in range(32):
            for j in range(32):
                self.dote[i][j]=not(self.dote[i][j]) 
        self.display()      # 画面更新
