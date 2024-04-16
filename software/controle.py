from PyQt5 import uic, QtWidgets
import mysql.connector

conexao = mysql.connector.connect(
    host = 'localhost', #127.0.0.1
    user = 'root',
    password = '',
    database = 'cadastro_membros'
)
numero_id = 0 #varivel global

def excluir():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM membros')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco [remover][0]
    cursor.execute('DELETE FROM membros WHERE id=' +str(valor_id))

    conexao.commit()


def editar(): #alterar dados no banco de dados
    global numero_id
    dados = lista.tableWidget.currentRow() #linha ativa
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM membros') #pesquisar por id
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco [dados][0]
    cursor.execute('SELECT* FROM membros WHERE id=' + str(valor_id))
    leitura_banco = cursor.fetchall()

    editar.show()
    numero_id = valor_id

#alterar valores na tela editar
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarNome.setText(str(leitura_banco[0][1]))
    editar.txtAlterarTelefone.setText(str(leitura_banco[0][2]))
    editar.txtAlterarNascimento.setText(str(leitura_banco[0][3]))
    editar.txtAlterarRua.setText(str(leitura_banco[0][4]))
    editar.txtAlterarBairro.setText(str(leitura_banco[0][5]))
    editar.txtAlterarCidade.setText(str(leitura_banco[0][6]))
    editar.txtAlterarMembro.setText(str(leitura_banco[0][7]))
    editar.txtAlterarDataBatizmo.setText(str(leitura_banco[0][8]))
    editar.txtAlterarIgrejaBatizmo.setText(str(leitura_banco[0][9]))
    editar.txtAlterarEncontro.setText(str(leitura_banco[0][10]))
    editar.txtAlterarNave.setText(str(leitura_banco[0][11]))
    editar.txtAlterarVoluntariado.setText(str(leitura_banco[0][12]))

def salvar_dados():
    global numero_id

    id = editar.txtAlterarId.text()
    nome = editar.txtAlterarNome.text()
    telefone = editar.txtAlterarTelefone.text()
    nascimento = editar.txtAlterarNascimento.text()
    rua = editar.txtAlterarRua.text()
    bairro = editar.txtAlterarBairro.text()
    cidade = editar.txtAlterarCidade.text()
    membro = editar.txtAlterarMembro.text()
    data_batizmo = editar.txtAlterarDataBatizmo.text()
    igreja_batizmo = editar.txtAlterarIgrejaBatizmo.text()
    encontro = editar.txtAlterarEncontro.text()
    nave = editar.txtAlterarNave.text()
    voluntariado = editar.txtAlterarVoluntariado.text()

    cursor = conexao.cursor()
    cursor.execute("UPDATE membros SET id='{}', nome='{}', telefone='{}', data_nascimento='{}', rua='{}', bairro='{}', cidade='{}', membro_desde='{}', data_batizmo='{}', igreja_batizmo='{}', encontro='{}', nave='{}', voluntariado='{}' WHERE id={}".format(id, nome, telefone, nascimento, rua, bairro, cidade, membro, data_batizmo, igreja_batizmo, encontro, nave, voluntariado, numero_id))

    editar.close()
    lista.close()
    formulario.show()

    conexao.commit()


def lista():
    lista.show()
    cursor = conexao.cursor()
    comando_SQL = 'SELECT* FROM membros'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leitura_banco))
    lista.tableWidget.setColumnCount(13)

    for linha in range(0, len(leitura_banco)):
        for coluna in range(0, 13):
            lista.tableWidget.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(leitura_banco[linha][coluna])))


def inserir():
    nome = formulario.txtNome.text()
    telefone = formulario.txtTelefone.text()
    data_nascimento = formulario.txtDataNascimento.text()
    rua = formulario.txtRua.text()
    bairro = formulario.txtBairro.text()
    cidade = formulario.txtCidade.text()
    membro_desde = formulario.txtDataMembro.text()
    data_batizmo = formulario.txtDataBatizmo.text()
    igreja_batizmo = formulario.txtIgrejaBatizmo.text()
    encontro = formulario.txtEncontro.text()
    nave = formulario.txtNave.text()
    voluntariado = formulario.txtVoluntariado.text()

    cursor = conexao.cursor()
    comando_SQL = 'INSERT INTO membros (nome,telefone,data_nascimento,rua,bairro,cidade,membro_desde,data_batizmo,igreja_batizmo,encontro,nave,voluntariado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    dados = (str(nome),str(telefone),str(data_nascimento),str(rua),str(bairro),str(cidade),str(membro_desde),str(data_batizmo),str(igreja_batizmo),str(encontro),str(nave),str(voluntariado))
    cursor.execute(comando_SQL, dados)
    conexao.commit()

    formulario.txtNome.setText('')
    formulario.txtTelefone.setText('')
    formulario.txtDataNascimento.setText('')
    formulario.txtRua.setText('')
    formulario.txtBairro.setText('')
    formulario.txtCidade.setText('')
    formulario.txtDataMembro.setText('')
    formulario.txtDataBatizmo.setText('')
    formulario.txtIgrejaBatizmo.setText('')
    formulario.txtEncontro.setText('')
    formulario.txtNave.setText('')
    formulario.txtVoluntariado.setText('')

#botões de ação
app = QtWidgets.QApplication([])
formulario = uic.loadUi('formulario.ui')
formulario.btnCadastrar.clicked.connect(inserir)
formulario.btnPesquisar.clicked.connect(lista)
lista = uic.loadUi('listas.ui')
lista.btnAlterar.clicked.connect(editar)
editar = uic.loadUi('editar.ui')
editar.btnConfirmar.clicked.connect(salvar_dados)
lista.btnApagar.clicked.connect(excluir)

formulario.show()
app.exec()