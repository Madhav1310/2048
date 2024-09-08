import wx
from game import GameField

class Game2048Frame(wx.Frame):
    def __init__(self, *args, **kw):
        super(Game2048Frame, self).__init__(*args, **kw)

        self.game = GameField(win=2048)
        self.InitUI()

        # Set focus on the window to capture key events
        self.panel.SetFocus()

        # Center and show the window
        self.Centre()
        self.Show()

    def InitUI(self):
        self.SetTitle("2048 Game")
        self.SetSize((400, 400))

        # Create a panel for drawing and binding events
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)  # Bind key events to the panel
        self.panel.SetFocus()  # Ensure the panel has focus for key events

    def OnPaint(self, event):
        # Painting the game board
        dc = wx.PaintDC(self.panel)
        size = self.panel.GetSize()
        w, h = size.x // 4, size.y // 4

        for r in range(4):
            for c in range(4):
                value = self.game.field[r][c]
                color = self.get_tile_color(value)
                dc.SetBrush(wx.Brush(color))
                dc.DrawRectangle(c * w, r * h, w, h)

                if value:
                    # Draw the tile value in the center of the rectangle
                    dc.SetTextForeground(wx.BLACK)
                    dc.DrawText(str(value), (c * w) + w // 2 - 10, (r * h) + h // 2 - 10)

    def get_tile_color(self, value):
        # Map tile values to colors
        color_map = {
            0: wx.Colour(205, 193, 180),
            2: wx.Colour(238, 228, 218),
            4: wx.Colour(237, 224, 200),
            8: wx.Colour(242, 177, 121),
            16: wx.Colour(245, 149, 99),
            32: wx.Colour(246, 124, 95),
            64: wx.Colour(246, 94, 59),
            128: wx.Colour(237, 207, 114),
            256: wx.Colour(237, 204, 97),
            512: wx.Colour(237, 200, 80),
            1024: wx.Colour(237, 197, 63),
            2048: wx.Colour(237, 194, 46),
        }
        return color_map.get(value, wx.Colour(60, 58, 50))

    def OnKeyDown(self, event):
        # Handle key events for arrow keys
        key_code = event.GetKeyCode()

        # Map arrow keys to the game's move directions
        if key_code == wx.WXK_LEFT:
            moved = self.game.move('Left')
        elif key_code == wx.WXK_RIGHT:
            moved = self.game.move('Right')
        elif key_code == wx.WXK_UP:
            moved = self.game.move('Up')
        elif key_code == wx.WXK_DOWN:
            moved = self.game.move('Down')
        else:
            moved = False

        # If a valid move occurred, refresh the screen to update the game board
        if moved:
            self.Refresh()

        # Check if the game is over or if the player has won
        if self.game.is_win():
            wx.MessageBox("You Win!", "2048", wx.OK | wx.ICON_INFORMATION)
        elif self.game.is_gameover():
            wx.MessageBox("Game Over", "2048", wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    frame = Game2048Frame(None)
    app.MainLoop()