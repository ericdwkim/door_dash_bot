### Door Dash Bot - Delivery Orders Scraping
**Using Conda:**

1. Open a command-line interface (such as Anaconda Prompt or Terminal).
2. Navigate to the directory where your `requirements.txt` file is located:
   ```bash
   cd path/to/directory
   ```
3. Create a new conda environment (optional but recommended for isolation):
   ```bash
   conda create --name myenv
   ```
4. Activate the conda environment:
   ```bash
   conda activate myenv
   ```
5. Install the packages from `requirements.txt`:
   ```bash
   conda install --file requirements.txt
   ```
   
**Using venv (Python's built-in virtual environment module):**

1. Open a command-line interface (such as Terminal or Command Prompt).
2. Navigate to the directory where your `requirements.txt` file is located:
   ```bash
   cd path/to/directory
   ```
3. Create a new virtual environment. Feel free to replace `myenv` with the desired name for your environment.
   ```bash
   python -m venv myenv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```
5. Install the packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   
Feel free to replace `myenv` with the desired name for your environment.

6. Set the following environmental variables on local machine:
   ```
   DEV_LOGIN_EMAIL
   DEV_LOGIN_PASSWORD
   DD_MERCHANT_LOGIN_URL = "https://identity.doordash.com/auth?client_id={client_id}"
   ```
   
7. Run the script:

   ```
   python -m src.app.main
   ```