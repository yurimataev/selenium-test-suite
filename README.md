Install pipenv:

    pip install pipenv

Install dependencies:

    pipenv install

Install Chrome:

    yum install chromium

Or (for the latest):

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && yum install ./google-chrome-stable_current_*.rpm

Install chrome driver:

    pipenv run python setup.py

Run tests with:

    pipenv run python -m unittest
