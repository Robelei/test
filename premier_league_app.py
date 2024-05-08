import streamlit as st
import requests
from datetime import datetime, timedelta

# API Key
api_key = "9c6b8d27f7mshee5304e7c078b51p1ac484jsn8f51006e77bd" 
headers = {"X-RapidAPI-Key": api_key}

# Principais Ligas Europeias
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
        end_date = today + timedelta(days=int(next_n_days))  # Conversão para inteiro
        url += f"&from={today}&to={end_date}"
    response = requests.get(url, headers=headers)
    return response.json()["response"]

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
    current_season = datetime.now().year

    # Seleção da Liga e Ano
    with st.sidebar:
        liga_selecionada = st.selectbox("Selecione a Liga", list(PRINCIPAIS_LIGAS.keys()))
        liga_id = PRINCIPAIS_LIGAS[liga_selecionada]
        season = st.selectbox("Selecione a Temporada", range(current_season, 2021, -1))

    tab1, tab2, tab3 = st.tabs(["Jogos", "Times", "Estatísticas"])

    with tab1:
        fixtures = get_fixtures(league_id, season)

        for fixture in fixtures:
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            date = fixture["fixture"]["date"]
            score = fixture["goals"]
            status = fixture["fixture"]["status"]["long"]

            st.write(f"**{home_team} vs {away_team}**")
            st.write(f"Data: {date}")
            if score:
                st.write(f"Placar: {score['home']} - {score['away']}")
            st.write(f"Status: {status}")
            st.write("---")

    with tab2:
        next_n_days = st.slider("Próximos dias:", min_value=1, max_value=30, value=7)
        fixtures = get_fixtures(league_id, current_season, next_n_days)

        # Ordena os jogos do mais recente para o mais antigo
        fixtures = sorted(fixtures, key=lambda fixture: datetime.fromisoformat(fixture["fixture"]["date"]), reverse=True)

        for fixture in fixtures:
            home_team = fixture["teams"]["home"]["name"]
            away_team = fixture["teams"]["away"]["name"]
            date = fixture["fixture"]["date"]
            score = fixture["goals"]
            status = fixture["fixture"]["status"]["long"]

            st.write(f"**{home_team} vs {away_team}**")
            st.write(f"Data: {date}")
            if score:
                st.write(f"Placar: {score['home']} - {score['away']}")
            st.write(f"Status: {status}")
            st.write("---")

    with tab3:
        standings = get_standings(league_id, current_season)[0]['league']['standings'][0]  
        
        st.write("## Classificação")
        for team in standings:
            st.write(f"**{team['rank']}º - {team['team']['name']}** ({team['points']} pts)") 

if __name__ == "__main__":
    main()
