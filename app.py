import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QHBoxLayout, QAction, QFileDialog, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import urllib.parse

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
        self.setWindowIcon(QIcon('Icon.png'))

    def onTextChanged(self):
        md_text = self.editor.toPlainText()
        md_text_limpio = self.limpiarMarkdown(md_text)
        self.updatePreview(md_text_limpio)

    def updatePreview(self, md_text):
        # Codificar el texto Markdown para uso en una URI
        md_text_encoded = urllib.parse.quote(md_text)

        # Actualizar la vista previa con el Markdown renderizado
        html_content = f"""
            <html>
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/github.min.css">
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>
                <script>hljs.highlightAll();</script>
                <style>
                    body {{
                        background-color: #282C34;
                        color: #ABB2BF;
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
                        margin: 0;
                        padding: 0;
                    }}
                    #preview {{
                        padding: 20px;
                    }}
                    img {{
                    max-width: 100%;
                    height: auto;
                    object-fit: contain;
                    }}
                    a {{
                    color: #0366d6;
                    text-decoration: none;
                    transition: color 0.2s;
                    }}

                    a:hover {{
                    color: #0550ae;
                    }}
                    .box {{
                    border: 1px solid #30363d;
                    padding: 8px;
                    margin-bottom: 16px;
                    border-radius: 6px;
                    }}
                    img, table, pre {{
                    class: 'box';
                    }}


                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/2.0.3/marked.min.js"></script>
            </head>
            <body>
                <div id="preview"></div>
                <script>
                    document.getElementById('preview').innerHTML =
                        marked(decodeURIComponent('{md_text_encoded}'));
                    document.querySelectorAll('pre code').forEach((block) => {{
                        hljs.highlightBlock(block);
                    }});
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
