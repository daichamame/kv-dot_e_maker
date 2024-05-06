#--------------------------------------------------------------------------------------------------
# タイトル：ドット絵つくる
# 内容：
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import sys
from kivy.clock import Clock
import dotmatrix

#--------------------------------------------------------------------------------------
# プログラムの終了ダイアログ
#--------------------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------------------
# マトリックス初期化ダイアログ
#--------------------------------------------------------------------------------------
class OkCancelDialog(Popup):
     pass
#--------------------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------------------
class MameWidget(Widget):
    select_color = 7            # 選択色
    # 初期処理
    def __init__(self, **kwargs):
        # ウィンドウサイズの指定
        Window.size=(640,480)
        Window.bind(size = self.on_resize)
        super(MameWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.init_callback,1)           # 初回実行
    # 起動時の初回だけ実行
    def init_callback(self,dt):
        self.clear_canvas(0)
        self.set_matrix_size(16,16)
    # タッチした時の処理
    def on_touch_down(self, touch):
        if super(MameWidget, self).on_touch_down(touch):
             return True
        self.ids.id_main_mx.draw(touch.pos,self.select_color)
        touch.grab(self)
        # メッセージ初期化
        self.ids.id_msg.text=""
        return True
    # タッチしたまま移動した時の処理
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.ids.id_main_mx.draw(touch.pos,self.select_color)
            return True
        return super(MameWidget, self).on_touch_move(touch)
    # タッチした状態から離れた時の処理
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.points =touch.pos  # 次の始点に設定
            # プレビューに反映
            self.ids.id_prev_mx.set_dotedata(self.ids.id_main_mx.get_dotedata())
            self.ids.id_prev_mx.display()
            self.ids.id_data.text=self.ids.id_main_mx.get_dotedata_hex()
            return True
        return super(MameWidget, self).on_touch_up(touch)
    # キャンバス初期化
    def clear_canvas(self,value):
        self.ids.id_data.text = ""
        self.ids.id_main_mx.clear()
        self.ids.id_prev_mx.clear()
        self.set_message("ドットマトリックスを初期化しました")
    # キャンバスサイズ変更(8x16,16x16,32x32)
    def set_matrix_size(self,w,h):
        self.ids.id_main_mx.set_size(w,h)
        self.ids.id_prev_mx.set_size(w,h)
        self.ids.id_data.text=self.ids.id_main_mx.get_dotedata_hex()
        self.set_message("マトリックスのサイズを設定しました")
    # 描画色セット
    def set_color(self,color_no):
        self.select_color=color_no  # 0 黒、7 白
        self.set_message("ペンの色を設定しました")
    # サイズ変更
    def on_resize(self,width,height):
        Window.size=(640,480)   # サイズ固定
    # クリップボードにコピー
    def copy_data(self):
        Clipboard.copy(self.ids.id_data.text)
        self.set_message("クリップボードにコピーしました")
    # 16進数データをドットデータの配列に設定
    def set_data(self):
        ret=self.ids.id_main_mx.set_dotedata_hex(self.ids.id_data.text)
        if(ret == False):
            self.set_message("データのフォーマットが少し違うようです")
        else:
            self.ids.id_main_mx.display()
        self.ids.id_prev_mx.set_dotedata(self.ids.id_main_mx.get_dotedata())
        self.ids.id_prev_mx.display()
        self.ids.id_data.text=self.ids.id_main_mx.get_dotedata_hex()
        self.set_message("取り込んでみました")
    # 反転する
    def invert_colors(self):
        self.ids.id_main_mx.invert_colors()
        self.ids.id_prev_mx.set_dotedata(self.ids.id_main_mx.get_dotedata())
        self.ids.id_prev_mx.display()
        self.ids.id_data.text=self.ids.id_main_mx.get_dotedata_hex()
        self.set_message("反転しました")
    # メッセージを表示
    def set_message(self,buf):
        self.ids.id_msg.text=buf
        Clock.schedule_once(self.clear_message,1) # 1秒後にメッセージを消す
    # メッセージを消す
    def clear_message(self,dt):
        self.ids.id_msg.text=""
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
    # キャンバス初期化の確認
    def confirm_clear_canvas(self):
        popup_confirm = OkCancelDialog()
        # OKボタンを押したら、キャンバス初期化を実行する設定
        popup_confirm.ids.id_ok.bind(on_press=self.clear_canvas)   
        popup_confirm.open()
# アプリの定義
class MameWidgetApp(App):
    def __init__(self, **kwargs):
        super(MameWidgetApp,self).__init__(**kwargs)
        self.title="ドット絵つくる"              # ウィンドウタイトル名
# メインの定義
if __name__ == '__main__':
    MameWidgetApp().run()                   # クラスを指定

Builder.load_file('mamewidget.kv')          # kvファイル名
