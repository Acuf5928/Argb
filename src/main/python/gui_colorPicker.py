import PyQt5.QtWidgets as QtWidgets


class App(QtWidgets.QColorDialog):

    def __init__(self, ctx, mode):
        super().__init__()

        self.ctx = ctx
        self.mode = mode

        self.setOptions(QtWidgets.QColorDialog.DontUseNativeDialog | QtWidgets.QColorDialog.NoButtons)

        self.currentColorChanged.connect(self.onChangedColor)

    def onChangedColor(self, color):
        if color.isValid():
            color = list(color.getRgb())

            if color[0] < 10:
                color[0] = "00" + str(color[0])
            elif color[0] < 100:
                color[0] = "0" + str(color[0])

            if color[1] < 10:
                color[1] = "00" + str(color[1])
            elif color[1] < 100:
                color[1] = "0" + str(color[1])

            if color[2] < 10:
                color[2] = "00" + str(color[2])
            elif color[2] < 100:
                color[2] = "0" + str(color[2])

            color = self.mode + str(color[0]) + str(color[1]) + str(color[2])

            self.ctx.setEffect(color)
            self.ctx.serial().write(color)

    # Prevent program exit when click on X button
    def closeEvent(self, event):
        self.hide()
        event.ignore()
