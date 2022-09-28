if find venv
then
    sleep 1
else
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt