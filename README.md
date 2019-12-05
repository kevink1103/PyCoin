# PyCoin

## Mini Project for EE4017 Internet Finance

To develop a “Bitcoin” application using Python.

1. Each group consists of 5 students
2. Each group to demo in week 12
3. Each group submits a report in week 12
4. Requirements: Compulsory features (passing marks) and optional features (additional marks)
5. Marks based on:
    1. Features implemented
    2. Code complexity; and
    3. The quality of the written report

## Compulsory Features

- [x] Able to generate a new wallet
- [x] Able to perform transactions
- [x] Able to generate coins reward
- [x] Able to generate new blocks using proof-of work consensus protocol
- [x] Able to broadcast new blocks to the rests of connected peers
- [x] Able to connect peers and sync the whole blockchain

## Optional Features

- [ ] Able to reject malformed blocks
- [ ] Able to check the balance before confirming a transaction
- [ ] Able to give interest to coins holder
- [ ] Able to charge transaction fee from the sender of the transaction
- [ ] Able to demonstrate partial validation using merkle tree
- [ ] Developed a lightweight node that store block header (First criteria
must be fulfilled)
- [ ] Able to change difficulty when the hash power of the network change
- [ ] Develop an App on any mobile platform to perform mobile payment using the cryptocurrency network

## Requirements

- Python 3
- Requests
- PyCrypto
- PyPrnt
- Flask
- Coverage

```bash
# If you have both Python 2 and 3,
pip3 install -r requirements.txt
# If you only have Python 3,
pip install -r requirements.txt
```

## Start

```bash
python3 Server.py
```

## Unit Test

```bash
python3 -m unittest
```

### Test with Coverage

```bash
bash test.sh
```
