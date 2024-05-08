import streamlit as st
import requests
from datetime import datetime, timedelta

# API Key para acessar a API de futebol
api_key = "9c6b8d27f7mshee5304e7c078b51p1ac484jsn8f51006e77bd" 
headers = {"X-RapidAPI-Key": api_key}

# Dicionário com os nomes e IDs das principais ligas europeias
PRINCIPAIS_LIGAS = {
    "Premier League (Inglaterra)": 39,
    "La Liga (Espanha)": 140,
    "Serie A (Itália)": 135,
    "Bundesliga (Alemanha)": 78,
    "Ligue 1 (França)": 61,
}

def get_fixtures(league_id, season, next_n_days=None):
    """
    Obtém os jogos de uma liga e temporada específicas.

    Args:
        league_id: O ID da liga.
        season: O ano da temporada.
        next_n_days: (Opcional) Número de dias à frente para buscar jogos.

    Returns:
        Uma lista de dicionários, onde cada dicionário representa um jogo.
    """
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={league_id}&season={season}"
    if next_n_days:
        today = datetime.today().date()
        end_date = today + timedelta(days=int(next_n_days))  # Calcula a data final
        url += f"&from={today}&to={end_date}"  # Adiciona filtro de data à URL

    response = requests.get(url, headers=headers)  # Faz a requisição à API
    return response.json()["response"]  # Retorna a lista de jogos

def get_teams(league_id):
    """
    Obtém a lista de times de uma liga específica.

    Args:
        league_id: O ID da liga.

    Returns:
        Uma lista de dicionários, onde cada dicionário representa um time.
    """
    url = f"https://api-football-v1.p.rapidapi.com/v3/teams?league={league_id}&season={datetime.now().year}"
    response = requests.get(url, headers=headers)
    return response.json()["response"]

def get_standings(league_id, season):
    """
    Obtém a classificação de uma liga e temporada específicas.

    Args:
        league_id: O ID da liga.
        season: O ano da temporada.

    Returns:
        Um dicionário contendo informações sobre a classificação da liga.
    """
    url = f"https://api-football-v1.p.rapidapi.com/v3/standings?league={league_id}&season={season}"
    response = requests.get(url, headers=headers)
    return response.json()["response"]

def main():
    st.title("Futebol Europeu - Principais Ligas")
    current_season = datetime.now().year  # Obtém o ano atual

    # Cria abas para cada liga usando seus nomes como rótulos
    tabs = st.tabs(list(PRINCIPAIS_LIGAS.keys()))

    # Itera sobre as ligas e cria o conteúdo de cada aba
    for i, (liga_nome, liga_id) in enumerate(PRINCIPAIS_LIGAS.items()):
        with tabs[i]:  # Define o contexto para a aba atual
            st.header(liga_nome)  # Exibe o nome da liga como cabeçalho

            # Seleção da Temporada
            season = st.selectbox("Selecione a Temporada", range(current_season, 2021, -1))

            # Obtém os jogos da liga e temporada selecionadas
            fixtures = get_fixtures(liga_id, season)

            # Itera sobre os jogos e exibe as informações
            for fixture in fixtures:
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                date = fixture["fixture"]["date"]
                score = fixture["goals"]
                status = fixture["fixture"]["status"]["long"]

                # Cria 4 colunas para organizar os dados do jogo
                cols = st.columns(4)
                cols[0].write(f"**{home_team} vs {away_team}**")  # Nomes dos times
                cols[1].write(f"Data: {date}")  # Data do jogo
                if score:  # Exibe o placar se estiver disponível
                    cols[2].write(f"Placar: {score['home']} - {score['away']}") 
                cols[3].write(f"Status: {status}")  # Status do jogo (ex: "Finalizado")

            # ... (implementação das abas "Times" e "Estatísticas" seguindo o mesmo padrão)

if __name__ == "__main__":
    main()
