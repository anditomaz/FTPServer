from flask import Flask, render_template, request, session, redirect, url_for, send_file
from ftplib import FTP

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ftp_host = request.form['ftp_host']
        ftp_port = int(request.form['ftp_port'])
        ftp_user = request.form['ftp_user']
        ftp_password = request.form['ftp_password']

        ftp = FTP()
        try:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(user=ftp_user, passwd=ftp_password)
            session['logged_in'] = True
            session['ftp_host'] = ftp_host
            session['ftp_port'] = ftp_port
            session['ftp_user'] = ftp_user
            session['ftp_password'] = ftp_password
            return redirect(url_for('lista_arquivos'))
        except Exception as e:
            error_message = str(e)
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

@app.route('/lista_arquivos')
def lista_arquivos():
    if 'logged_in' in session:
        try:
            ftp = FTP()
            ftp.connect(session['ftp_host'], session['ftp_port'])
            ftp.login(user=session['ftp_user'], passwd=session['ftp_password'])
            files = ftp.nlst()
            return render_template('arquivos.html', files=files)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    return redirect(url_for('index'))

@app.route('/baixar_arquivos/<nome_arquivo>')
def baixar_arquivos(nome_arquivo):
    if 'logged_in' in session:
        try:
            ftp_host = session['ftp_host']
            ftp_port = session['ftp_port']
            ftp_user = session['ftp_user']
            ftp_password = session['ftp_password']

            ftp = FTP()
            ftp.connect(ftp_host, ftp_port)
            ftp.login(user=ftp_user, passwd=ftp_password)

            arquivo = '/' + nome_arquivo
            link = url_for('download', arquivo=arquivo)
            return f'<a href="{link}">Baixar {nome_arquivo}</a>'
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    return redirect(url_for('index'))

@app.route('/download/<arquivo>')
def download(arquivo):
    if 'logged_in' in session:
        try:
            ftp_host = session['ftp_host']
            ftp_port = session['ftp_port']
            ftp_user = session['ftp_user']
            ftp_password = session['ftp_password']

            ftp = FTP()
            ftp.connect(ftp_host, ftp_port)
            ftp.login(user=ftp_user, passwd=ftp_password)

            ftp.retrbinary('RETR ' + arquivo, open(arquivo, 'wb').write)
            return send_file(arquivo, as_attachment=True)
        except Exception as e:
            error_message = str(e)
            return render_template('error.html', error_message=error_message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
