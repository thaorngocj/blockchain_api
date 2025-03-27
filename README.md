# Simple Blockchain
This is a basic blockchain implementation using Python and Flask.

## Installation
1. Clone the repository:
   ```
   git clone
   ```
2. Navigate into the project directory:
   ```
   cd simple-blockchain
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Project
Start the blockchain server:
```python
python node.py
```

## API Endpoints
- **Mine a Block**: `GET /mine`
- **Get the Blockchain**: `GET /chain`
- **Add a Transaction**: `POST /transaction`

## Example Transaction Request
```json
{
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 50
}
```