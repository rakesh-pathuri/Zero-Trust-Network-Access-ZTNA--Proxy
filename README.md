# Zero-Trust Cryptographic Identity Proxy (ZTNA)

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green)](https://flask.palletsprojects.com/)
[![Security](https://img.shields.io/badge/Security-Zero%20Trust-red)](https://www.ncsc.gov.uk/collection/zero-trust-architecture)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Development Context:** This project was engineered as a portfolio piece for my Cybersecurity Master's application. It demonstrates a practical implementation of Zero-Trust Network Access (ZTNA) principles, cryptographic token signing, and identity-aware proxying in Python.

## 📖 Overview

In traditional network security, anything inside the corporate firewall is implicitly trusted (the "castle-and-moat" model). If an attacker breaches the perimeter, they gain access to everything. 

This project implements a **Zero-Trust Architecture (ZTA)**. It assumes the network is already compromised. Before any request is allowed to reach the hidden internal application, it must pass through the **Identity Proxy**. The proxy cryptographically validates the user's identity via a JSON Web Token (JWT) on every single request.

## ✨ Core Architecture

The repository contains three microservices:

1. **Identity Provider (`auth_server.py`)**: 
   - Acts as the authentication gateway.
   - Verifies credentials and mints a cryptographically signed JWT (using the `HS256` algorithm) with a strict 15-minute expiration time (`TTL`).
2. **Zero-Trust Proxy (`ztna_proxy.py`)**: 
   - Sits at the network edge. It intercepts all incoming web traffic.
   - Extracts the `Authorization: Bearer` token, verifies the cryptographic signature, checks the expiration claims, and logs the user identity for auditing.
   - If valid, it acts as a reverse proxy, seamlessly forwarding the traffic to the protected internal app. If invalid, it drops the connection with a 401 Unauthorized.
3. **Internal Application (`dummy_internal_app.py`)**: 
   - A hidden, isolated backend resource that simulates classified data. It is bound strictly to `127.0.0.1` and is completely inaccessible from the outside internet.

## 🛠️ Technical Stack

- **Network Routing**: Python `Flask`, `requests`
- **Cryptography & Identity**: `PyJWT`, `cryptography`
- **Security Posture**: Stateless Token Validation, Secrets Injection (`python-dotenv`)

## 🚀 How to Run Locally

### Prerequisites
Make sure you have `Python 3.11+` and `git` installed.

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rakesh-pathuri/ZeroTrust_Proxy.git
   cd ZeroTrust_Proxy
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   Create a `.env` file in the root directory and define your cryptographic secret:
   ```env
   JWT_SECRET_KEY="your_super_secret_key"
   INTERNAL_APP_URL="http://127.0.0.1:8000"
   ```

### Execution

You must run all three services simultaneously (in three separate terminal windows):

1. **Start the Hidden Internal App:**
   ```bash
   python dummy_internal_app.py
   ```
2. **Start the Identity Provider:**
   ```bash
   python auth_server.py
   ```
3. **Start the Zero-Trust Proxy:**
   ```bash
   python ztna_proxy.py
   ```

### Testing the Zero-Trust Architecture

If you try to access the proxy `http://localhost:5000` directly in your browser, you will be blocked with a `401 Unauthorized` error because you lack a cryptographic identity token. 

To access it, you must first request a token from the Auth Server (`http://localhost:5001/login`), and then attach it as a `Bearer` token in the headers of your request to the proxy!

---

### Authorship
**Developed by:** Rakesh Pathuri
*Engineered to demonstrate modern identity-aware network security and applied cryptography paradigms.*
