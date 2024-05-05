# League of Legends Summoner Data Collector

This Python script collects data about League of Legends summoners and stores it in a SQLite database. It gathers summoners from specified ranks and divisions and saves their summoner ID, rank, division, and win rate.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/league-summoner-data-collector.git
    ```

2. Navigate to the project directory:

    ```bash
    cd league-summoner-data-collector
    ```

3. Install the required dependencies using pip and the provided `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Update the `config.py` file with your Riot API token. You can obtain a token from the [Riot Developer Portal](https://developer.riotgames.com/).

```python
# Replace 'YOUR_RIOT_API_TOKEN' with your actual Riot API token
API_TOKEN = 'YOUR_RIOT_API_TOKEN'
DATABASE_NAME = "LeagueSummonerData"  # Customize the database name if needed
DATABASE_PATH = "/"  # Customize the database path if needed
```

## Usage

1. Ensure your Riot API token is correctly set in `config.py`.
2. Run the script:

    ```bash
    python main.py
    ```

3. The script will start collecting summoner data based on the specified ranks and divisions and store it in the SQLite database.

## Contributing

Contributions to optimize algorithms, improve documentation, or add new features are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
