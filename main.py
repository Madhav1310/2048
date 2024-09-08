import wx
import time
from game import GameField
from config.colors import color_map  

TIMER_DURATION = 120  # Total game time (in seconds)

class Multiplayer2048(wx.Frame):
    def __init__(self, *args, **kw):
        super(Multiplayer2048, self).__init__(*args, **kw)

        self.game1 = GameField(win=2048)  # Player 1 (WASD)
        self.game2 = GameField(win=2048)  # Player 2 (Arrow keys)
        self.moves1 = 0  # Moves for Player 1
        self.moves2 = 0  # Moves for Player 2
        self.start_time = time.time()  # Start time of the game
        self.timer_duration = TIMER_DURATION  # Countdown timer in seconds
        self.game_over = False  # Track if the game is over

        self.InitUI()

        self.panel.SetFocus()

        self.Centre()
        self.Show()

    def InitUI(self):
        self.SetTitle("2048 Multiplayer")
        self.SetSize((800, 500))  

        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)  
        self.panel.SetFocus()  

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)

    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        size = self.panel.GetSize()
        w, h = size.x // 8, size.y // 5  

        # Timer at the top
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(self.timer_duration - elapsed_time, 0)
        minutes, seconds = divmod(remaining_time, 60)
        dc.SetTextForeground(wx.RED)  
        timer_str = f"Time remaining: {minutes:02}:{seconds:02}"
        dc.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.DrawText(timer_str, 350, 10)

        # Player 1's game (on the left)
        dc.SetTextForeground(wx.WHITE)  
        dc.DrawText(f"Player 1 - Score: {self.game1.score} - Moves: {self.moves1}", 10, 50)
        for r in range(4):
            for c in range(4):
                value = self.game1.field[r][c]
                color = self.get_tile_color(value)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(c * w, (r + 1) * h, w, h)

                if value:
                    dc.SetTextForeground(wx.BLACK)
                    dc.DrawText(str(value), (c * w) + w // 2 - 10, (r + 1) * h + h // 2 - 10)

        # Player 1 Controls 
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText("Controls: W (Up), A (Left), S (Down), D (Right)", 10, 70)

        # Player 2's game (on the right)
        dc.SetTextForeground(wx.WHITE)  
        dc.DrawText(f"Player 2 - Score: {self.game2.score} - Moves: {self.moves2}", 410, 50)
        for r in range(4):
            for c in range(4):
                value = self.game2.field[r][c]
                color = self.get_tile_color(value)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(400 + c * w, (r + 1) * h, w, h)

                if value:
                    dc.SetTextForeground(wx.BLACK)
                    dc.DrawText(str(value), 400 + (c * w) + w // 2 - 10, (r + 1) * h + h // 2 - 10)

        # Player 2 Controls 
        dc.SetTextForeground(wx.WHITE)
        dc.DrawText("Controls: Arrow Keys", 410, 70)

        # Separator between two games
        dc.SetPen(wx.Pen(wx.BLACK, 3))
        dc.DrawLine(400, 50, 400, 5000)  

    def get_tile_color(self, value):
        return color_map.get(value, wx.Colour(60, 58, 50))

    def OnKeyDown(self, event):
        if self.game_over:  
            return

        key_code = event.GetKeyCode()
        moved1, moved2 = False, False

        # Player 1 (WASD keys)
        if key_code == ord('A'):
            moved1 = self.game1.move('Left')
        elif key_code == ord('D'):
            moved1 = self.game1.move('Right')
        elif key_code == ord('W'):
            moved1 = self.game1.move('Up')
        elif key_code == ord('S'):
            moved1 = self.game1.move('Down')

        # Player 2 (Arrow keys)
        if key_code == wx.WXK_LEFT:
            moved2 = self.game2.move('Left')
        elif key_code == wx.WXK_RIGHT:
            moved2 = self.game2.move('Right')
        elif key_code == wx.WXK_UP:
            moved2 = self.game2.move('Up')
        elif key_code == wx.WXK_DOWN:
            moved2 = self.game2.move('Down')

        if moved1:
            self.moves1 += 1
            self.Refresh()

        if moved2:
            self.moves2 += 1
            self.Refresh()

        if self.game1.is_gameover() and self.game2.is_gameover():
            self.EndGame()

    def OnTimer(self, event):
        if not self.game_over:
            elapsed_time = int(time.time() - self.start_time)
            if elapsed_time >= self.timer_duration:
                self.EndGame()  
            else:
                self.Refresh()

    def EndGame(self):
        self.game_over = True
        self.timer.Stop()

        score1 = self.game1.score
        score2 = self.game2.score
        max_tile1 = max(max(row) for row in self.game1.field)
        max_tile2 = max(max(row) for row in self.game2.field)

        result_msg = (
            f"Player 1 - Score: {score1}, Highest Tile: {max_tile1}, Moves: {self.moves1}\n"
            f"Player 2 - Score: {score2}, Highest Tile: {max_tile2}, Moves: {self.moves2}\n"
        )

        # Determine the winner based on the highest tile
        if max_tile1 > max_tile2:
            result_msg += "Player 1 Wins!"
        elif max_tile2 > max_tile1:
            result_msg += "Player 2 Wins!"
        else:
            # In case of a tie, we can use the score or moves as a tiebreaker
            if score1 > score2:
                result_msg += "Player 1 Wins by Score!"
            elif score2 > score1:
                result_msg += "Player 2 Wins by Score!"
            else:
                result_msg += "It's a Tie!"

        wx.MessageBox(result_msg, "Game Over", wx.OK | wx.ICON_INFORMATION)

        self.Refresh()

if __name__ == '__main__':
    app = wx.App(False)
    frame = Multiplayer2048(None)
    app.MainLoop()