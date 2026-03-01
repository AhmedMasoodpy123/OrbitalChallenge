# OrbitalChallenge: Build a simple Python API that calculates how many credits customers have used during the current billing period

This project implements a lightweight API that calculates credit usage for the current billing period. The API exposes with a single endpoint which returns usage information derived from message data and metadata.

# Running the API
1. Create a virtual env
python3/python -m venv venv
source venev/bin/activate
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Run the API
uvicorn app:app --reload

4. Access endpoint
curl http://127.0.0.1:8000/usage

5. Optional (Run Tests)
pytest

Note this work is done on a dev branch, upon testing and approval, there is an existing MR to merge to main.