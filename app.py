import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QHBoxLayout, QAction, QFileDialog, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MarkdownPreviewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Markdown Live Preview')
        self.setGeometry(100, 100, 1200, 600)

        # Caja de texto para el editor de Markdown (columna izquierda)
        self.editor = QTextEdit(self)
        self.editor.textChanged.connect(self.onTextChanged)
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #282C34;
                color: #ABB2BF;
            }
        """)

        # Vista previa de Markdown (columna derecha)
        self.preview = QWebEngineView(self)
        self.preview.setStyleSheet("""
            QWebEngineView {
                background-color: #282C34;
                color: #ABB2BF;
            }
        """)

        # Crear una acción para abrir archivo
        open_action = QAction("Abrir archivo", self)
        open_action.triggered.connect(self.openFile)

        # Crear un menú y agregar la acción
        self.menuBar().addMenu("Archivo").addAction(open_action)

        # Diseño horizontal para organizar los elementos
        layout = QHBoxLayout()
        layout.addWidget(self.editor, 1)
        layout.addWidget(self.preview, 1)

        # Widget central para contener el layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Cargar el archivo HTML que renderiza el Markdown
        self.preview.setHtml(open("markdown_preview.html").read(), baseUrl=QUrl.fromLocalFile("."))

    def onTextChanged(self):
        md_text = self.editor.toPlainText()
        md_text_limpio = self.limpiarMarkdown(md_text)
        self.updatePreview(md_text_limpio)

    def updatePreview(self, md_text):
        # Actualizar la vista previa con el Markdown renderizado
        html_content = f"""
            <html>
            <head>
                <style>
                    body {{
                        background-color: #282C34;
                        color: #ABB2BF;
                        margin: 0;
                        padding: 0;
                    }}
                    #preview {{
                        padding: 20px;
                    }}
                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/2.0.3/marked.min.js"></script>
            </head>
            <body>
                <div id="preview"></div>
                <script>
                    document.getElementById('preview').innerHTML = marked(`{md_text}`);
                </script>
            </body>
            </html>
        """
        self.preview.setHtml(html_content, baseUrl=QUrl.fromLocalFile("."))

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo Markdown", "", "Archivos Markdown (*.md)")
        if file_path:
            with open(file_path, "r", encoding='utf-8') as file:
                markdown_text = file.read()
                self.editor.setPlainText(markdown_text)
                self.onTextChanged()

    def limpiarMarkdown(self, md_text):
        # Eliminar espacios en blanco al principio y al final de cada línea
        lineas_limpias = [linea.rstrip() for linea in md_text.splitlines()]
        # Unir las líneas limpias
        md_text_limpio = '\n'.join(lineas_limpias)
        return md_text_limpio

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MarkdownPreviewer()
    ex.show()
    sys.exit(app.exec_())
