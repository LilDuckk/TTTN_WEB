#cài flask
pip install flask

#thiết lập môi trường 
$env:FLASK_ENV = "development"
$env:FLASK_APP = "main.py"

#cài các depen
pip install --user -r requirements.txt

#tạo đb
flask create_db

#chạy
python main.py 


#Với Codespace

#cài đặt pyenv để thay đổi phiên bản python 
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
source ~/.bashrc  # hoặc source ~/.zshrc nếu dùng zsh

#cài đặt python 3.10.2
pyenv install 3.10.2
pyenv global 3.10.2
python --version

#thiết lập môi trường 
export FLASK_ENV=development
export FLASK_APP=main.py

#cài các depen
pip install --user -r requirements.txt

#tạo db
flask create_db

#chạy
python main.py 

#Hoặc

flask run --host=0.0.0.0 --port=5000
