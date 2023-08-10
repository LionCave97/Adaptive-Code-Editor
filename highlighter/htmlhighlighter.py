from PySide6 import QtCore, QtGui, QtWidgets

class HTMLHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(HTMLHighlighter, self).__init__(parent)

        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setForeground(QtGui.QColor("blue"))
        keyword_format.setFontWeight(QtGui.QFont.Bold)

        tag_format = QtGui.QTextCharFormat()
        tag_format.setForeground(QtGui.QColor("purple"))

        attribute_format = QtGui.QTextCharFormat()
        attribute_format.setForeground(QtGui.QColor("red"))

        value_format = QtGui.QTextCharFormat()
        value_format.setForeground(QtGui.QColor("green"))

        self.highlighting_rules = [
            (QtCore.QRegularExpression("<[a-zA-Z0-9_]+"), tag_format),  # HTML tags
            (QtCore.QRegularExpression("[a-zA-Z0-9_]+(?=\\=)"), attribute_format),  # HTML attributes
            (QtCore.QRegularExpression("\"[^\"]*\"|'[^']*'"), value_format),  # Attribute values
            (QtCore.QRegularExpression("\\b(?:class|id|name)\\b"), keyword_format),  # Reserved keywords
        ]

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QtCore.QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    text_editor = QtWidgets.QPlainTextEdit()
    highlighter = HTMLHighlighter(text_editor.document())

    text_editor.show()
    sys.exit(app.exec())
